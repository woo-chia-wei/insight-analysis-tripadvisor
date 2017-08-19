from repositories.Repository import Repository
from workers.StopWatch import stop_watch
from dateutil.parser import parse
from datetime import date
import re as regex

class ProcessDataWorker:

    def __init__(self):
        self.repo = Repository()
    
    def __merge_all_attractions(self):
        all_data = []
        all_data += self.repo.read_raw_reviews_singapore_zoo()
        all_data += self.repo.read_raw_reviews_river_safari()
        all_data += self.repo.read_raw_reviews_night_safari()
        self.repo.write_raw_reviews_all_attractions(all_data)
        print("Merging is done, the final output table is 'raw_reviews'")

    def __data_cleansing_raw_reviews(self):
        reviews = self.repo.read_raw_reviews()
        for review in reviews:
            review['uid'] = regex.compile('UID_(.*)-SRC').search(review['uid']).group(1) if review['uid'] != '' else ''
            review['review_header'] = review['review_header'].replace("\n", " ").replace(",", "").replace("  ", " ")
            review['review_body'] = review['review_body'].replace("\n", " ").replace(",", "").replace("  ", " ")
            if review['user_name'] == "A TripAdvisor Member":
                review['username'] = "0"
            else:
                review['username'] = review['user_name']
            review.pop('user_name')
            month = regex.compile('\d+\s+(\S+)\s+\d+').search(review['review_date']).group(1)
            if month in ['January','February','March']:
                review['review_quarter'] = "1"
            elif month in ['April','May','June']:
                review['review_quarter'] = "2"
            elif month in ['July','August','September']:
                review['review_quarter'] = "3"
            else:
                review['review_quarter'] = "4"
        print("Data processing is done for raw reviews, data is then copied to collection 'processed_reviews'.")
        self.repo.write_processed_reviews(reviews)

    def __data_cleansing_raw_users(self):

        users = self.repo.read_raw_users()
        for user in users:

            # Get 'age_since_year' and 'age_since_month' from 'age_since'
            # Remove 'age_since'
            age_since = user['age_since'].lower().replace("since", "").strip()
            if age_since == "this week" or age_since == "this month":
                month = date.today().strftime("%B")
                year = date.today().year
                age_since = month + " " + str(year)
            age_since_date = parse(age_since)
            user['age_since_year'] = age_since_date.year
            user['age_since_month'] = age_since_date.month
            user.pop('age_since')

            # Get 'gender' from 'short_desc'
            # Remove 'short_desc'
            short_desc = user['short_desc'].lower()
            if 'female' in short_desc:
                gender = "female"
            elif 'male' in short_desc:
                gender = 'male'
            else:
                gender = ''
            user['gender'] = gender
            user.pop('short_desc')

            # Get 'country' from 'hometown'
            # Remove 'hometown' 
            countries = ['afghanistan', 'albania', 'algeria', 'andorra', 'angola', 'antigua and barbuda', 'argentina',
                         'armenia', 'aruba', 'australia', 'austria', 'azerbaijan', 'bahamas, the', 'bahrain',
                         'bangladesh', 'barbados', 'belarus', 'belgium', 'belize', 'benin', 'bhutan', 'bolivia',
                         'bosnia and herzegovina', 'botswana', 'brazil', 'brunei', 'bulgaria', 'burkina faso', 'burma',
                         'burundi', 'cabo verde', 'cambodia', 'cameroon', 'canada', 'central african republic', 'chad',
                         'chile', 'china', 'colombia', 'comoros', 'congo, democratic republic of the congo',
                         'republic of the costa rica', 'croatia', 'cuba', 'curacao', 'cyprus', 'czechia', 'denmark',
                         'djibouti', 'dominica', 'dominican republic', 'east timor (see timor-leste)', 'ecuador',
                         'egypt', 'el salvador', 'equatorial guinea', 'eritrea', 'estonia', 'ethiopia', 'fiji',
                         'finland', 'france', 'gabon', 'gambia, the', 'georgia', 'germany', 'ghana', 'greece',
                         'grenada', 'guatemala', 'guinea', 'guinea-bissau', 'guyana', 'haiti', 'holy see', 'honduras',
                         'hungary', 'iceland', 'india', 'indonesia', 'iran', 'iraq', 'ireland', 'israel', 'italy',
                         'jamaica', 'japan', 'jordan', 'kazakhstan', 'kenya', 'kiribati', 'korea, north',
                         'korea, south', 'kosovo', 'kuwait', 'kyrgyzstan', 'laos', 'latvia', 'lebanon', 'lesotho',
                         'liberia', 'libya', 'liechtenstein', 'lithuania', 'luxembourg', 'macedonia', 'madagascar',
                         'malawi', 'malaysia', 'maldives', 'mali', 'malta', 'marshall islands', 'mauritania',
                         'mauritius', 'mexico', 'micronesia', 'moldova', 'monaco', 'mongolia', 'montenegro', 'morocco',
                         'mozambique', 'namibia', 'nauru', 'nepal', 'netherlands', 'new zealand', 'nicaragua', 'niger',
                         'nigeria', 'north korea', 'norway', 'oman', 'pakistan', 'palau', 'palestinian territories',
                         'panama', 'papua new guinea', 'paraguay', 'peru', 'philippines', 'poland', 'portugal', 'qatar',
                         'romania', 'russia', 'rwanda', 'saint kitts and nevis', 'saint lucia',
                         'saint vincent and the grenadines', 'samoa', 'san marino', 'sao tome and principe',
                         'saudi arabia', 'senegal', 'serbia', 'seychelles', 'sierra leone', 'singapore', 'sint maarten',
                         'slovakia', 'slovenia', 'solomon islands', 'somalia', 'south africa', 'south korea',
                         'south sudan', 'spain', 'sri lanka', 'sudan', 'suriname', 'swaziland', 'sweden', 'switzerland',
                         'syria', 'tajikistan', 'tanzania', 'thailand', 'timor-leste', 'togo', 'tonga',
                         'trinidad and tobago', 'tunisia', 'turkey', 'turkmenistan', 'tuvalu', 'uganda', 'ukraine',
                         'united arab emirates', 'united kingdom', 'uruguay', 'uzbekistan', 'vanuatu', 'venezuela',
                         'vietnam', 'yemen', 'zambia', 'zimbabwe']
            if regex.search("\,", user['hometown']):
                user_country = regex.compile('(.*)\,(.*)').search(user['hometown']).group(2).strip().lower()
            else:
                user_country = user['hometown'].strip().lower()
            user['country'] = user_country if user_country in countries else "nil"
            user.pop('hometown')

            # travel style transformation
            ts_list = ['travel_style_60plus_traveller', 'travel_style_art_architecture_lover', 'travel_style_backpacker',
             'travel_style_beach_goer', 'travel_style_eco_tourist', 'travel_style_family_holiday_maker',
             'travel_style_foodie', 'travel_style_history_buff', 'travel_style_like_a_local',
             'travel_style_luxury_traveller', 'travel_style_nature_lover', 'travel_style_nightlife_seeker',
             'travel_style_peace_quiet_seeker', 'travel_style_shopping_fanatic', 'travel_style_thrifty_traveller',
             'travel_style_thrill_seeker', 'travel_style_trendsetter', 'travel_style_urban_explorer',
             'travel_style_vegetarian']
            for ts in ts_list:
                user[ts] = 0
            travel_styles = ['60+ Traveller', 'Art and Architecture Lover', 'Backpacker', 'Beach Goer', 'Eco-tourist',
                             'Family Holiday Maker', 'Foodie', 'History Buff', 'Like a Local', 'Luxury Traveller',
                             'Nature Lover', 'Nightlife Seeker', 'Peace and Quiet Seeker', 'Shopping Fanatic',
                             'Thrifty Traveller', 'Thrill Seeker', 'Trendsetter', 'Urban Explorer', 'Vegetarian']
            if user['travel_style'] != []:
                for ts in user['travel_style']:
                    if ts in travel_styles:
                        p = travel_styles.index(ts)
                        user[ts_list[p]] = 1
            user.pop('travel_style')
            #
            if regex.search('\d+',user['visited_cities']):
                user['visited_cities'] = regex.compile('(\d+)\s+.*').search(user['visited_cities']).group(1)
            if regex.search('\d+',user['helpful_votes']):
                user['helpful_votes'] = regex.compile('(\d+)\s+.*').search(user['helpful_votes']).group(1)
            if regex.search('\d+',user['passport_badge']):
                user['passport_badge'] = regex.compile('(\d+)\s+.*').search(user['passport_badge']).group(1)
            #

        print("Data processing is done for raw users, data is then copied to collection 'processed_users'.")
        self.repo.write_processed_users(users)

    @stop_watch
    def merge_all_attractions(self):
        self.__merge_all_attractions()

    @stop_watch
    def process_raw_reviews(self):
        self.__data_cleansing_raw_reviews()

    @stop_watch
    def process_user_reviews(self):
        self.__data_cleansing_raw_users()
    
