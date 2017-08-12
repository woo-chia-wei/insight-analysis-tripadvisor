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

urls = ["https://www.tripadvisor.com.sg/Attraction_Review-g294265-d324542-Reviews-Singapore_Zoo-Singapore.html"]
worker = RawDataWorker()
worker.write_raw_reviews(urls)

repo = Repository()
pp.pprint(repo.read_raw_reviews())