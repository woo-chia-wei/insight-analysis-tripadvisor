from repositories.Repository import Repository
from workers.Scraper import Scraper
from workers.StopWatch import StopWatch

class RawDataWorker:

    def __init__(self):
        self.scraper = Scraper()
        self.repo = Repository()

    def write_raw_reviews(self, attractions):
        # Start stopwatch
        sw = StopWatch("write_raw_reviews")
        sw.start()

        data = []
        for attraction in attractions:
            data += self.scraper.extract_reviews(attraction['name'], attraction['url'])
        if(len(data) != 0):
            self.repo.write_raw_reviews(data)
            print(str(len(data)) + " data is being imported.")
        else:
            print("No data is being imported. There might be error during the web scraping.")

        # Stop stopwatch
        sw.stop()
            
    def write_raw_users(self, urls):
        data = []
        for url in urls:
            data.append(self.scraper.extract_user(url))
        self.repo.write_raw_users(data)