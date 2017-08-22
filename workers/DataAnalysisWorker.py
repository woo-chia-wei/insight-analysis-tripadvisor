from repositories.Repository import Repository
from workers.StopWatch import stop_watch
from gensim.summarization import keywords
from gensim import corpora,models
from nltk.stem import WordNetLemmatizer
from rake_nltk import Rake
from operator import itemgetter
from bson import json_util
from datetime import date
import re as regex
import nltk
import string
import json
import requests

class DataAnalysisWorker:
    def __init__(self):
        self.repo = Repository()

    def __perform_sentiment_analysis(self, zoo_reviews_raw):
        sentiment_results = []
        for reviews in zoo_reviews_raw:
            review_rating = int(reviews.split(',')[4])
            sentiment = 'neutral'
            if review_rating < 3 and review_rating > 0:
                sentiment = 'neg'
            elif review_rating >3:
                sentiment = 'pos'
            elif review_rating == 0:
                text_value = reviews.split(',')[7]
                response = requests.post("http://text-processing.com/api/sentiment/", data={"text": text_value})
                json_obj = json.loads(response.text)
                sentiment = json_obj["label"]

            sentiment_results.append(reviews + ','+sentiment)
        return sentiment_results

    def __create_interim_dataset(self, zoo_reviews_raw):
		#'uid,review_id,user_name,traveller_type,rating,review_date,review_header,review_body,attraction,review_quarter'
        interim_data=[]
        for reviews in zoo_reviews_raw:
            uid=reviews["uid"]
            rid=reviews["review_id"]
            username=reviews["username"]
            traveller_type=reviews["traveller_type"]
            rating=reviews["rating"]
            review_date=reviews["review_date"]
            review_header = reviews["review_header"].replace(',','')
            review_content=reviews["review_body"].replace('\n','').replace(',','')
            attraction = reviews["attraction"]
            review_quarter = reviews["review_quarter"]
            interim_data.append(str(uid)+','+str(rid)+','+username+','+traveller_type+','+str(rating)+','+review_date+','+review_header+','+review_content+','+attraction+','+review_quarter)
        return interim_data

    def __write_analysis_2_db(self, json_val):
        rr = Repository()
        rr.write_analysis_reviews(json_val)

    def __retrieve_processed_reviews(self, attraction_value):
        rr = Repository()
        review_list = rr.read_processed_reviews(query={"attraction":attraction_value})
        review_json_list = []
        for rrr in review_list:
            jsonv = json.dumps(rrr, sort_keys=True, indent=4, default=json_util.default)
            jsont = json.loads(jsonv)
            review_json_list.append(jsont)
        return review_json_list

    def __do_preprocess(self, reviews_data, stopword_list):
        doc_list = []
        wnl = nltk.WordNetLemmatizer()
        for text_data in reviews_data:
            text_data_arr = text_data.split(',')
            text = text_data_arr[7].replace("\n","")
            post_clean = regex.sub(r'\d+', '', text)
            post_clean_word = nltk.regexp_tokenize(post_clean.lower(), pattern='\w+')
            lemma_list = [wnl.lemmatize(t) for t in post_clean_word]
            stop_wordless = [token for token in lemma_list if token not in stopword_list]
            if len(stop_wordless) > 0:
                doc_list.append(stop_wordless)
        return doc_list

    def __retrieve_topic_list(self, lda_model):
        topic_list = []
        for x1, x2 in lda_model:
            result_post_clean_word = nltk.regexp_tokenize(x2.lower(), pattern='\w+')
            result ='+'.join([w for w in result_post_clean_word if not w.isdigit()])
            print("\tTopic: " + result)
            topic_list.append(result)
        return topic_list

    def __create_analysis_json(self, raw_text):
        raw_text_arr = raw_text.split(',')
        #'UID,ReviewId,UserName,Location,Rating,Date,Via,ReviewHeader,ReviewContent,Sentiment,Topic,Concepts
        uid=raw_text_arr[0]
        rid=raw_text_arr[1]
        userName=raw_text_arr[2]
        traveller_type = raw_text_arr[3]
        rating = raw_text_arr[4]
        date= raw_text_arr[5]
        review_header = raw_text_arr[6]
        review_content=raw_text_arr[7]
        attraction=raw_text_arr[8]
        review_q = raw_text_arr[9]
        sentiment=raw_text_arr[10]
        topic=raw_text_arr[11]
        concepts=raw_text_arr[12]
        json_value = {"uid": uid,"review_id":rid,"userName":userName, "traveller_type":traveller_type,"rating":rating,"date":date,
        "rating":rating,"review_header":review_header,"review_content":review_content,"attraction":attraction,"review_quarter":review_q,"sentiment":sentiment,"topic":topic,"concepts":concepts}
        return json_value

    def __perform_final_analysis(self, trained_ldamodel, combine_results, stopword_list, dictionary, t_list):
        json_list = []

        for result_data in combine_results:
            #Preprocess
            result_data_arr = result_data.split(',')
            result_text = result_data_arr[7]
            result_post_clean = regex.sub(r'\d+', '', result_text)
            result_wnl = nltk.WordNetLemmatizer()
            result_post_clean_word = nltk.regexp_tokenize(result_post_clean.lower(), pattern='\w+')
            result_lemma_list2 = [result_wnl.lemmatize(t) for t in result_post_clean_word]
            stop_wordless2 = [token for token in result_lemma_list2 if token not in stopword_list]
            #Tag Topic to Document
            result_doc_topics = trained_ldamodel.get_document_topics(dictionary.doc2bow(stop_wordless2))
            #perform Keyword Extraction
            r = Rake()
            result_text_lemma = ' '.join(result_lemma_list2)
            result_text_no_punc = ' '.join(word.strip(string.punctuation) for word in result_text_lemma.split())
            r.extract_keywords_from_text(result_text_no_punc)
            keywords_list = r.get_ranked_phrases_with_scores()
            keyword_1 = 'nil'
            if len(keywords_list) > 0:
                keyword_1 = keywords_list[0][1].replace('.', '').replace('wa','').replace('would','')
                # print(doc_topics)
            result_data_max = max(result_doc_topics, key=itemgetter(1))

            json_value = self.__create_analysis_json(
                result_data.replace('\n', '') + ',' + t_list[result_data_max[0]].replace('\"', '') + ',' + keyword_1)
            json_list.append(json_value)
        return json_list

    @stop_watch
    def run_analysis(self):
        
        ############### Initialise Base Values ######################
        stopword_list = [line.strip() for line in open('config/stopwords_merged_processed.txt','r')]
        attraction_type_list = ['Singapore Zoo','Night Safari']
        #############################################################

        final_result = []

        for attraction_v in attraction_type_list:
            print("Processing " + attraction_v + "...")

            #Step 1 Retrieve Data from MongoDB, create Interim files
            print(attraction_v + ": Step 1 Retrieve Data from MongoDB, create Interim files")
            zoo_reviews = self.__create_interim_dataset(self.__retrieve_processed_reviews(attraction_v))

            #Step 2 Perform Sentiment Analysis
            zoo_reviews_sentiments = self.__perform_sentiment_analysis(zoo_reviews)
            print(attraction_v + ": Step 2 Perform Sentiment Analysis")

            #Step 3 PreProcess Reviews
            print(attraction_v + ": Step 3 PreProcess Reviews")
            corpus_processed = self.__do_preprocess(zoo_reviews, stopword_list)

            #Step 4 Create Topic Models
            print(attraction_v + ": Step 4 Create Topic Models")
            dictionary = corpora.Dictionary(corpus_processed)
            corpus = [dictionary.doc2bow(text_corpus) for text_corpus in corpus_processed]
            tfidf = models.TfidfModel(corpus)
            tf_list = []
            for corpus_data in corpus_processed:
                tf_list.append(tfidf[dictionary.doc2bow(corpus_data)])
            ldamodel = models.ldamodel.LdaModel(tf_list, num_topics=10, id2word = dictionary,passes=1)
            model_filename=''
            if attraction_v == 'Singapore Zoo':
                model_filename='zoo_mongo.model'
            else:
                model_filename='night_safari_mongo.model'
            lda_model_out = ldamodel.print_topics(num_topics=10, num_words=7)
            ldamodel.save(model_filename)
            t_list = self.__retrieve_topic_list(lda_model_out)

            #Step 5 perform Keyword Extraction + Map Topic to Review
            print(attraction_v + ": Step 5 perform Keyword Extraction + Map Topic to Review")
            final_result += self.__perform_final_analysis(ldamodel, zoo_reviews_sentiments, stopword_list, dictionary, t_list)
        
        # Write Text Analytics Results to MongoDB
        print("Write Text Analytics Results to MongoDB")
        self.__write_analysis_2_db(final_result)