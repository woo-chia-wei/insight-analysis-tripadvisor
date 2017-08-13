# This file is to isolate the process of extracting raw reviews for singapore zoo

from workers.Scraper import Scraper
from repositories.Repository import Repository
from workers.StopWatch import stop_watch

class Patch():

    @stop_watch
    def run_patch(self):
        scraper = Scraper()
        repo = Repository()
        url = "https://www.tripadvisor.com.sg/Attraction_Review-g294265-d324542-Reviews-Singapore_Zoo-Singapore.html"

        # repo.write_raw_reviews_singapore_zoo_families(scraper.extract_reviews("Singapore Zoo", url, "Families"))
        # repo.write_raw_reviews_singapore_zoo_couples(scraper.extract_reviews("Singapore Zoo", url, "Couples"))
        # repo.write_raw_reviews_singapore_zoo_solo(scraper.extract_reviews("Singapore Zoo", url, "Solo")) # Done
        # repo.write_raw_reviews_singapore_zoo_business(scraper.extract_reviews("Singapore Zoo", url, "Business")) # Done
        # repo.write_raw_reviews_singapore_zoo_friends(scraper.extract_reviews("Singapore Zoo", url, "Friends"))

        # data = []
        # data += repo.read_raw_reviews_singapore_zoo_families()
        # data += repo.read_raw_reviews_singapore_zoo_couples()
        # data += repo.read_raw_reviews_singapore_zoo_solo()
        # data += repo.read_raw_reviews_singapore_zoo_business()
        # data += repo.read_raw_reviews_singapore_zoo_friends()
        # repo.write_raw_reviews_all_attractions(data)

Patch().run_patch()





