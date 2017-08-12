# from TripAdvisorProfile import extract_profile
# from Repository import Repository

# import requests
# from bs4 import BeautifulSoup

# links = [
#     "https://www.tripadvisor.com.sg/members/WendyK225",
#     "https://www.tripadvisor.com.sg/members/192manun",
#     "https://www.tripadvisor.com.sg/members/neila953"
# ]

# data = []

# for link in links:
#     response = requests.get(link)
#     html = response.text
#     soup = BeautifulSoup(html, 'html.parser')
#     data.append(extract_profile(soup))
#     print("Done: " + link)

# repo = Repository()
# repo.write_raw_users(data)

import requests
from bs4 import BeautifulSoup
from RawDataWorker import RawDataWorker

links = [
    "https://www.tripadvisor.com.sg/members/WendyK225",
    "https://www.tripadvisor.com.sg/members/192manun",
    "https://www.tripadvisor.com.sg/members/neila953"
]


soups = []

for link in links:
    soup = BeautifulSoup(requests.get(link).text, 'html.parser')
    soups.append(soup)
    print("Created soup for " + link)

worker = RawDataWorker()
worker.write_raw_users(soups)
print("Done")
