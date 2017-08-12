from workers.RawDataWorker import RawDataWorker
from repositories.Repository import Repository
import pprint as pp


# links = [
#     "https://www.tripadvisor.com.sg/members/WendyK225",
#     "https://www.tripadvisor.com.sg/members/192manun",
#     "https://www.tripadvisor.com.sg/members/neila953"
# ]

# worker = RawDataWorker()
# worker.write_raw_users(links)

# repo = Repository()
# pp.pprint(repo.read_raw_users())

url = "http://quotes.toscrape.com"
worker = RawDataWorker()
worker.write_raw_reviews(url)