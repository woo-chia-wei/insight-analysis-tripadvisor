from repositories.Repository import Repository
from workers.StopWatch import StopWatch
from dateutil.parser import parse
from datetime import date
import re as regex

class ProcessDataWorker:

    def __init__(self):
        self.repo = Repository()

    def __monitor_process(self, process, process_name):
        # Start stopwatch
        sw = StopWatch(process_name)
        sw.start()

        # Run process
        process()

        # Stop stopwatch
        sw.stop()

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
            # Convert 'age_since' to 'age_since_year' and 'age_since_month'
            age_since = user['age_since'].lower().replace("since", "").strip()
            if age_since == "this week" or age_since == "this month":
                month = date.today().strftime("%B")
                year = date.today().year
                age_since = month + " " + str(year)
            age_since_date = parse(age_since)
            user['age_since_year'] = age_since_date.year
            user['age_since_month'] = age_since_date.month
            user.pop('age_since')

            # Get gender
            
        print("Data processing is done for raw users, data is then copied to collection 'processed_users'.")
        self.repo.write_processed_users(users)

    def merge_all_attractions(self):
        self.__monitor_process(self.__merge_all_attractions, "Merge all individual attractions to final raw reviews table.")

    def process_raw_reviews(self):
        self.__monitor_process(self.__data_cleansing_raw_reviews, "Process raw reviews and then copy to collection 'processed_reviews'.")

    def process_user_reviews(self):
        self.__monitor_process(self.__data_cleansing_raw_users, "Process user reviews and then copy to collection 'processed_users'.")
    
