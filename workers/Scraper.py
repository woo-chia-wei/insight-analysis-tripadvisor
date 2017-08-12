from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import requests

class Scraper:

    def get_soup(self, url):
        requests.adapters.DEFAULT_RETRIES = 5
        requests.session().keep_alive = False
        try:
            html = requests.get(url)
            return BeautifulSoup(html.content, 'html.parser')
        except requests.exceptions.MissingSchema as err:
            print(err)

    def extract_user(self, url):

        def get_travel_style(soup):
            travel_style_list = []
            travel_style = soup.find_all('div', {'class': 'tagBubble unclickable'})
            for ts in travel_style:
                travel_style_list.append(ts.get_text().strip())
            return travel_style_list

        soup = self.get_soup(url)

        username = soup.find('span', {'class': 'nameText'}).get_text().strip()
        hometown = soup.find('div', {'class': 'hometown'}).get_text().strip()
        age_since = soup.select_one('.ageSince .since').get_text().strip()
        short_desc = soup.select('.ageSince p')[1].get_text().strip()
        no_reviews = int(soup.find('a', {'name': 'reviews'}).get_text().replace('Reviews', ''))
        travel_style = get_travel_style(soup)
        user_contribution = int(soup.find('div',{'class':'level tripcollectiveinfo'}).find('span').get_text())
        
        return {
            "username": username,
            "hometown": hometown,
            "age_since": age_since,
            "short_desc": short_desc,
            "no_reviews": no_reviews, 
            "travel_style": travel_style,
            "user_contribution": user_contribution
        }

    def extract_reviews(self, attraction, url):

        def get_rating(rating_class):
            for i in [1,2,3,4,5]:
                if(('bubble_' + str(i) + '0') in rating_class):
                    return i

        data = []
        traveller_types = [
            "Families",
            "Couples",
            "Solo",
            "Business",
            "Friends"
        ]

        try:
            driver = webdriver.Chrome("drivers/chromedriver.exe")
            driver.get(url)

            for traveller_type in traveller_types:
                # Reopen page and check traveller type filter
                driver.find_element_by_css_selector('#taplc_location_review_filter_controls_0_filterSegment_' + traveller_type).click()

                # Waits for loading
                sleep(2)
                
                # Start extracting
                reviews = driver.find_elements_by_css_selector('div.review-container')
                for review in reviews:

                    selector_uid = review.find_elements_by_css_selector('div.memberOverlayLink')
                    selector_review_id = review
                    selector_user_name = review.find_element_by_css_selector('div.username.mo')

                    uid = selector_uid[0].get_attribute("id").strip() if selector_uid else ""
                    review_id = selector_review_id.get_attribute("data-reviewid")
                    user_name = selector_user_name.text.strip() if selector_user_name else ""
                    rating = get_rating(review.find_element_by_css_selector('.rating span').get_attribute('class'))
                    review_date = review.find_element_by_css_selector('span.ratingDate.relativeDate').get_attribute('title')
                    review_header = review.find_element_by_css_selector('span.noQuotes').text.strip()
                    review_body = review.find_element_by_css_selector('p.partial_entry').text.strip()
                    
                    current_page = driver.find_elements_by_css_selector(".pageNum.current")[0].get_attribute("data-page-number")

                    data.append({
                        "attraction": attraction,
                        "traveller_type": traveller_type,
                        "uid": uid,
                        "review_id": review_id,
                        "user_name": user_name,
                        "rating": rating,
                        "review_date": review_date,
                        "review_header": review_header,
                        "review_body": review_body
                    })
                
                print("Working on " + attraction + " with " + traveller_type + " type at page " + current_page + " ...")

                # Uncheck traveller type filter
                sleep(3)
                driver.find_element_by_css_selector('#taplc_location_review_filter_controls_0_filterSegment_' + traveller_type).click()
                sleep(3)

        except Exception as err:
            print("Error: " + err)
        finally:
            driver.quit()
            print(str(len(data)) + " data is extracted...")
            return data