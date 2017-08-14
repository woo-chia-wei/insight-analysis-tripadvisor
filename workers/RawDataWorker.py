from repositories.Repository import Repository
from workers.Scraper import Scraper
from workers.StopWatch import stop_watch
import re as regex
import json
import pprint as pp

class RawDataWorker:

    def __init__(self):
        self.scraper = Scraper()
        self.repo = Repository() 

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
        errors = []
        uids = read_user_id_from_raw_reviews()
        total = len(uids)
        for index, uid in enumerate(uids):
            result, err = self.scraper.extract_user(uid, index, total)
            if err:
                errors.append(err)
                print(err)
            else:
                data.append(result)

        if(len(data) != 0):
            self.repo.write_raw_users(data)
            print(str(len(data)) + " data is being imported to mongodb db 'raw_users'.")

            if len(errors) > 0:
                print("Error logs are shown below: ")
                pp.pprint(errors)

        else:
            print("No data is being imported. There might be error during the web scraping.")

    @stop_watch
    def extract_raw_users_all_attractions(self):
        self.__write_raw_users()

    @stop_watch
    def extract_raw_reviews_singapore_zoo(self):
        self.__write_raw_reviews_singapore_zoo()

    @stop_watch
    def extract_raw_reviews_river_safari(self):
        self.__write_raw_reviews_river_safari()

    @stop_watch
    def extract_raw_reviews_night_safari(self):
        self.__write_raw_reviews_night_safari()