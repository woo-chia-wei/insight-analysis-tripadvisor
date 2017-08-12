from repositories.Repository import Repository
from workers.Scraper import Scraper
from workers.StopWatch import StopWatch
import re as regex

class RawDataWorker:

    def __init__(self):
        self.scraper = Scraper()
        self.repo = Repository()

    def __monitor_action(self, process, process_name):
        # Start stopwatch
        sw = StopWatch(process_name)
        sw.start()

        # Run process
        process()

        # Stop stopwatch
        sw.stop()  

    def __write_raw_reviews(self):
        data = []
        traveller_types = [
            "Families",
            "Couples",
            "Solo",
            "Business",
            "Friends"
        ]
        attractions = [
            {
                "name": "Singapore Zoo",
                "url": "https://www.tripadvisor.com.sg/Attraction_Review-g294265-d324542-Reviews-Singapore_Zoo-Singapore.html"
            },
            {
                "name": "River Safari",
                "url": "https://www.tripadvisor.com.sg/Attraction_Review-g294265-d4089881-Reviews-River_Safari-Singapore.html"
            },
            {
                "name": "Night Safari",
                "url": "https://www.tripadvisor.com.sg/Attraction_Review-g294265-d324761-Reviews-Night_Safari-Singapore.html"
            }
        ]

        for attraction in attractions:
            for traveller_type in traveller_types:
                # if(traveller_type != "Business"): continue
                if(attraction['name'] != 'Night Safari'): continue

                data += self.scraper.extract_reviews(attraction['name'], attraction['url'], traveller_type)

        if(len(data) != 0):
            self.repo.write_raw_reviews(data)
            print(str(len(data)) + " data is being imported to mongodb db 'raw_reviews'.")
        else:
            print("No data is being imported. There might be error during the web scraping.")
            
    def __write_raw_users(self):

        def read_user_id_from_raw_reviews():
            repo = Repository()
            records = repo.read_raw_reviews({ 'uid': { '$ne': ''} }, {"uid": 1})
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

    def extract_raw_reviews_all_attractions(self):
        self.__monitor_action(self.__write_raw_reviews, "Write Raw Reviews")

    def extract_raw_users_all_attractions(self):
        self.__monitor_action(self.__write_raw_users, "Write Raw Users")