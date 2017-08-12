from Repository import Repository
from Scraper import Scraper
import requests
from bs4 import BeautifulSoup

class RawDataWorker:

    def write_raw_users(self, urls):
        data = []
        scraper = Scraper()

        for url in urls:
            soup = BeautifulSoup(requests.get(url).text, 'html.parser')
            data.append(scraper.extract_user(soup))

        repo = Repository()
        repo.write_raw_users(data)

