from repositories.Repository import Repository
from workers.StopWatch import StopWatch
import re as regex
import json

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

    def merge_all_attractions(self):
        self.__monitor_process(self.__merge_all_attractions, "Merge all individual attractions to final raw table")
