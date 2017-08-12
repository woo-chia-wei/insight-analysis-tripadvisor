from repositories.Repository import Repository
from workers.Scraper import Scraper

class RawDataWorker:

    def __init__(self):
        self.scraper = Scraper()

    def write_raw_reviews(self, url):
        self.scraper.extract_reviews(url)

    def write_raw_users(self, urls):
        data = []

        for url in urls:
            data.append(self.scraper.extract_user(url))

        repo = Repository()
        repo.write_raw_users(data)