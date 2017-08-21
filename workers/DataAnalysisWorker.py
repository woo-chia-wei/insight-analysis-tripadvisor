from repositories.Repository import Repository
from workers.StopWatch import stop_watch
from datetime import date
import re as regex

class DataAnalysisWorker:

    def __init__(self):
        self.repo = Repository()
    
    def run_analysis(self):
        print("run_analysis")

    # @stop_watch
    # def merge_all_attractions(self):
    #     self.__merge_all_attractions()

    # @stop_watch
    # def process_raw_reviews(self):
    #     self.__data_cleansing_raw_reviews()

    # @stop_watch
    # def process_user_reviews(self):
    #     self.__data_cleansing_raw_users()
    
