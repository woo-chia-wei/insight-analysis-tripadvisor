import requests
from bs4 import BeautifulSoup
import json

#result = requests.get("https://www.tripadvisor.com.sg/members/Dragonbaby12")

def retrieve_username(profile_page_soup):
    name = profile_page_soup.find('span', {'class': 'nameText'})
    return name.get_text()

def retrieve_travel_style(profile_page_soup):
    travel_style_list = []
    travel_style = profile_page_soup.find_all('div', {'class': 'tagBubble unclickable'})
    for ts in travel_style:
        #print('Travel Style:'+ts.get_text())
        travel_style_list.append(ts.get_text())
    return travel_style_list

def retrieve_user_review(profile_page_soup):
    review_location = profile_page_soup.find_all('li', {'class': 'cs-review'})
    counter = 0
    for location in review_location:
        counter = counter + 1
        review_location = location.find('div', {'class': 'cs-review-location'})
        review_rating = location.find('div', {'class': 'cs-review-rating'}).find('span')
        print(review_location.get_text())
        print(review_rating['class'][1].replace('bubble_', ''))
    print(counter)

def retrieve_hometown(profile_page_soup):
    return profile_page_soup.find('div', {'class': 'hometown'}).get_text()

def create_profile_json(profile_page_soup):
    #json_file = open(json_file_name,'w')
    username=retrieve_username(profile_page_soup)
    travel_style =retrieve_travel_style(profile_page_soup)
    no_reviews_raw = profile_page_soup.find('a', {'name': 'reviews'}).get_text()
    no_reviews = no_reviews_raw.replace('Reviews', '')
    level_contribution= profile_page_soup.find('div',{'class':'level tripcollectiveinfo'}).find('span').get_text()\
        if profile_page_soup.find('div',{'class':'level tripcollectiveinfo'}) else ""
    hometown = retrieve_hometown(profile_page_soup)
    json_value = {"username": username,"hometown":hometown,"no_reviews":no_reviews, "travel_style":travel_style,
    "user_contribution":level_contribution}
    return json.dumps(json_value,indent=4)
    #json_file.write(json.dumps(json_value))

#content = result.content
#soup = BeautifulSoup(content,"html.parser")
#
#create_profile_json(soup)


