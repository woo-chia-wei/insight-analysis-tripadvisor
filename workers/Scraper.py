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

    def extract_user(self, uid, index, total):

        def get_travel_style(soup):
            travel_style_list = []
            travel_style = soup.find_all('div', {'class': 'tagBubble unclickable'})
            for ts in travel_style:
                travel_style_list.append(ts.get_text().strip())
            return travel_style_list

        def get_member_overlay(uid):
            soup = self.get_soup("https://www.tripadvisor.com.sg/MemberOverlay?uid=" + uid)

            selector_visited_cities = soup.select_one(".memberOverlay .countsReviewEnhancementsItem .globe-world")
            selector_helpful_votes = soup.select_one(".memberOverlay .countsReviewEnhancementsItem .thumbs-up-fill")
            selector_reviews_counts = soup.select(".memberOverlay .rowCountReviewEnhancements.rowCellReviewEnhancements")

            visited_cities = selector_visited_cities.parent.select("span")[1].text if selector_visited_cities else ""
            helpful_votes = selector_helpful_votes.parent.select("span")[1].text if selector_helpful_votes else ""
            if selector_reviews_counts:
                review_1x = int(selector_reviews_counts[4].text.replace(',', ''))
                review_2x = int(selector_reviews_counts[3].text.replace(',', ''))
                review_3x = int(selector_reviews_counts[2].text.replace(',', ''))
                review_4x = int(selector_reviews_counts[1].text.replace(',', ''))
                review_5x = int(selector_reviews_counts[0].text.replace(',', ''))
            else:
                review_1x = review_2x = review_3x = review_4x = review_5x = 0

            url = soup.select_one('.memberOverlay a')['href']
            return (visited_cities,
                    helpful_votes,
                    review_1x,
                    review_2x,
                    review_3x,
                    review_4x,
                    review_5x,
                    "https://www.tripadvisor.com.sg" + url)

        (visited_cities, helpful_votes, review_1x, review_2x, review_3x, review_4x, review_5x, url) = get_member_overlay(uid)
        soup = self.get_soup(url)

        print("Extracting profile (" + str(index + 1) + "/" + str(total) + ") from " + url)

        username = soup.find('span', {'class': 'nameText'}).get_text().strip()
        hometown = soup.find('div', {'class': 'hometown'}).get_text().strip()
        age_since = soup.select_one('.ageSince .since').get_text().strip()
        short_desc = soup.select('.ageSince p')[1].get_text().strip() if len(soup.select('.ageSince p')) >= 2 else ""
        no_reviews = int(soup.find('a', {'name': 'reviews'}).get_text().replace('Reviews', '').replace('Review', ''))
        travel_style = get_travel_style(soup)
        selector_user_contribution = soup.find('div',{'class':'level tripcollectiveinfo'})
        user_contribution = int(selector_user_contribution.find('span').get_text()) if selector_user_contribution else ""
        
        return {
            "username": username,
            "hometown": hometown,
            "age_since": age_since,
            "short_desc": short_desc,
            "no_reviews": no_reviews, 
            "travel_style": travel_style,
            "user_contribution": user_contribution,
            "visited_cities": visited_cities,
            "helpful_votes": helpful_votes,
            "review_1x": review_1x,
            "review_2x": review_2x,
            "review_3x": review_3x,
            "review_4x": review_4x,
            "review_5x": review_5x,
        }

    def extract_reviews(self, attraction, url, traveller_type):

        def get_rating(rating_class):
            for i in [1,2,3,4,5]:
                if(('bubble_' + str(i) + '0') in rating_class):
                    return i

        data = []

        try:
            driver = webdriver.Chrome("drivers/chromedriver.exe")
            print("Opening url " + url)
            driver.get(url)

            # Reopen page and check traveller type filter
            driver.find_element_by_css_selector('#taplc_location_review_filter_controls_0_filterSegment_' + traveller_type).click()
            sleep(3)
            
            # Start extracting

            while True:
                reviews = driver.find_elements_by_css_selector('div.review-container')
                current_page = driver.find_elements_by_css_selector(".pageNum.current")[0].get_attribute("data-page-number")
                last_page = driver.find_elements_by_css_selector(".pageNum.last")[0].get_attribute("data-page-number")
                print("Working on '" + attraction + " 'with '" + traveller_type + "' type at page " + current_page + " out of " + last_page + "...")

                # Click on more links to expand the review description
                while True:
                    more_links = driver.find_elements_by_css_selector('div.review-container .partial_entry span.taLnk.ulBlueLinks')
                    if len(more_links) == 0: break
                    for link in more_links:
                        sleep(0.8)
                        try:
                            link.click()
                        except:
                            pass

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
                
                # Try click on next button, error raised if next button is not found
                try:
                    driver.find_element_by_css_selector('#taplc_location_reviews_list_0 .nav.next.taLnk').click()
                    no_more_pages = False
                except:
                    no_more_pages = True 

                if(no_more_pages): break
                sleep(1.5)

        except Exception as err:
            print("Error: " + err)
        finally:
            driver.quit()
            print(str(len(data)) + " data is extracted...")
            return data