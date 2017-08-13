from repositories.Repository import Repository
from workers.Scraper import Scraper
from workers.StopWatch import StopWatch
import re as regex
import json

class RawDataWorker:

    def __init__(self):
        self.scraper = Scraper()
        self.repo = Repository()

    def __monitor_process(self, process, process_name):
        # Start stopwatch
        sw = StopWatch(process_name)
        sw.start()

        # Run process
        process()

        # Stop stopwatch
        sw.stop()  

    def __write_raw_reviews_singapore_zoo(self):
        self.__write_raw_reviews("Singapore Zoo")

    def __write_raw_reviews_river_safari(self):
        self.__write_raw_reviews("River Safari")

    def __write_raw_reviews_night_safari(self):
        self.__write_raw_reviews("Night Safari")

    def __write_raw_reviews(self, attraction):
        data = []
        traveller_types = [
            "Families",
            "Couples",
            "Solo",
            "Business",
            "Friends"
        ]

        if attraction == "Singapore Zoo":
            url = "https://www.tripadvisor.com.sg/Attraction_Review-g294265-d324542-Reviews-Singapore_Zoo-Singapore.html"
        elif attraction == "River Safari":
            url = "https://www.tripadvisor.com.sg/Attraction_Review-g294265-d4089881-Reviews-River_Safari-Singapore.html"
        elif attraction == "Night Safari":
            url = "https://www.tripadvisor.com.sg/Attraction_Review-g294265-d324761-Reviews-Night_Safari-Singapore.html"
        else:
            print("Selected attraction is not supported in this system.")
            pass

        for traveller_type in traveller_types:
            data += self.scraper.extract_reviews(attraction, url, traveller_type)

        if(len(data) != 0):
            if attraction == "Singapore Zoo":
                self.repo.write_raw_reviews_singapore_zoo(data)
            elif attraction == "River Safari":
                self.repo.write_raw_reviews_river_safari(data)
            elif attraction == "Night Safari":
                self.repo.write_raw_reviews_night_safari(data)

            print(str(len(data)) + " data is being imported to mongodb db '" + attraction + "'.")
        else:
            with open('debug.json', 'w') as file:
                json.dump(data, file, sort_keys=True, indent=4)
            print("No data is being imported. There might be error during the web scraping.")
            print("Please refer to debug.json for the partial captured data.")
            
    def __write_raw_users(self):

        def read_user_id_from_raw_reviews():
            repo = Repository()
            records = []
            records += repo.read_raw_reviews_singapore_zoo({ 'uid': { '$ne': ''} }, {"uid": 1})
            records += repo.read_raw_reviews_river_safari({ 'uid': { '$ne': ''} }, {"uid": 1})
            records += repo.read_raw_reviews_night_safari({ 'uid': { '$ne': ''} }, {"uid": 1})
            uids = [ regex.compile('UID_(.*)-SRC').search(data['uid']).group(1) for data in records]
            uids_set = set(uids)
            return list(uids_set)
        
        data = []
        uids = read_user_id_from_raw_reviews()
        total = len(uids)
        for index, uid in enumerate(uids):
            data.append(self.scraper.extract_user(uid, index, total))

        if(len(data) != 0):
            self.repo.write_raw_users(data)
            print(str(len(data)) + " data is being imported to mongodb db 'raw_users'.")
        else:
            print("No data is being imported. There might be error during the web scraping.")

    def extract_raw_users_all_attractions(self):
        self.__monitor_process(self.__write_raw_users, "Write Raw Users")

    def extract_raw_reviews_singapore_zoo(self):
        self.__monitor_process(self.__write_raw_reviews_singapore_zoo, "Write Raw Reviews of Singapore Zoo")

    def extract_raw_reviews_river_safari(self):
        self.__monitor_process(self.__write_raw_reviews_river_safari, "Write Raw Reviews of River Safari")

    def extract_raw_reviews_night_safari(self):
        self.__monitor_process(self.__write_raw_reviews_night_safari, "Write Raw Reviews of Night Safari")