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
    
