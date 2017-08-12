from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pprint as pp

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

    def extract_reviews(self, url):
        try:
            driver = webdriver.Chrome("drivers/chromedriver.exe")
            driver.get(url)
            pp.pprint(driver.find_element_by_css_selector('h1 a').text)
            pp.pprint([element.text for element in driver.find_elements_by_css_selector('.tag-item a.tag')])
        except Exception:
            pp.pprint(Exception)
        finally:
            driver.quit()

    def extract_reviews_bk(url):





        bs = get_soup(url)
        uid,reviewid,user_name,location=[],[],[],[]
        rating_score,rating_date,via,review_header,review_content = [],[],[],[],[]
        for container in bs.select('div.review-container'):
            if container.select_one('div.memberOverlayLink'):
                uid_src = container.select_one('div.memberOverlayLink')['id']
                uid_tmp = re.compile('UID_(.*)-SRC').search(uid_src).group(1)
            else:
                uid_tmp = ""
            reviewid_tmp = container['data-reviewid'] if container['data-reviewid'] else ""
            user_name_tmp = container.select_one('div.username.mo').text.strip() \
                if container.select_one('div.username.mo') else ""
            location_tmp = container.select_one('div.location').text.strip().\
                replace("\n"," ").replace(",","").replace("  "," ") \
                if container.select_one('div.location') else ""
            #if uid_tmp:
            #   user_profile_url_tmp = get_user_profile_url(uid_tmp)
            #else:
            #   user_profile_url_tmp = ""
            #user_profile_url_tmp = "https://www.tripadvisor.com.sg/members/" + user_name_tmp \
            #    if user_name_tmp != "A TripAdvisor Member" else ""
            rating_score_tmp = re.compile('bubble_(\d)0').\
                search(container.select_one('div.rating.reviewItemInline').span['class'][1]).group(1)
            rating_date_tmp = container.select_one('span.ratingDate.relativeDate')['title']
            #via = container.select_one('div.rating.reviewItemInline').a['class'] if container.select_one('div.rating.reviewItemInline').a else ""
            if container.select_one('div.rating.reviewItemInline').a:
                via_tmp = container.select_one('div.rating.reviewItemInline').a['class']
                via_tmp = re.compile('via(\w+)').search(str(via_tmp)).group(1)
            else:
                via_tmp = "Website"
            review_header_tmp = container.select_one('span.noQuotes').text.strip()
            review_content_tmp = container.select_one('p.partial_entry').text.strip().\
                replace("\n"," ").replace(",","").replace("  "," ")
            #
            uid.append(uid_tmp)
            reviewid.append(reviewid_tmp)
            user_name.append(user_name_tmp)
            location.append(location_tmp)
            #user_profile_url.append(user_profile_url_tmp)
            rating_score.append(rating_score_tmp)
            rating_date.append(rating_date_tmp)
            via.append(via_tmp)
            review_header.append(review_header_tmp)
            review_content.append(review_content_tmp)
        return(uid,reviewid,user_name,location,
            rating_score,rating_date,via,review_header,review_content)