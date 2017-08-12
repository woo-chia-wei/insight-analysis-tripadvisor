import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import datetime
import json

#
class AttOverview(object):
    '''
    attraction overview contaions following properties:
        name: A string representing attraction name
        location:
        tel:
        overall_rating:
        review_count:
        review_5x:
        review_4x:
        review_3x:
        review_2x:
        review_1x:
        review_highlights:
    '''
    def __init__(self,name,loc,tel,overall_rating,review_count,
                 review_5x,review_4x,review_3x,
                 review_2x,review_1x,
                 review_highlights):
        self.name = name
        self.loc = loc
        self.tel = tel
        self.overall_rating = overall_rating
        self.review_count = review_count
        self.review_5x = review_5x
        self.review_4x = review_4x
        self.review_3x = review_3x
        self.review_2x = review_2x
        self.review_1x = review_1x
        self.review_highlights = review_highlights
    def print_overview(self):
        print('{0:25s} : {1:s}'.format("Attraction",self.name))
        print('{0:25s} : {1:s}'.format("Location", self.loc))
        print('{0:25s} : {1:s}'.format("Tel", self.tel))
        print('{0:25s} : {1:s} / 5.0'.format("Overall Rating", self.overall_rating))
        print('{0:25s} : {1:d}'.format("Review Count", self.review_count))
        print('{0:25s} : {1:f}'.format("Excellent", self.review_5x))
        print('{0:25s} : {1:f}'.format("Very Good", self.review_4x))
        print('{0:25s} : {1:f}'.format("Average", self.review_3x))
        print('{0:25s} : {1:f}'.format("Poor", self.review_2x))
        print('{0:25s} : {1:f}'.format("Terrible", self.review_1x))
        print('{0:25s} : {1:}'.format("Travellers Talk About", self.review_highlights))
        return 1
#
def get_soup(url):
    requests.adapters.DEFAULT_RETRIES = 5
    requests.session().keep_alive = False
    try:
        html = requests.get(url)
        return BeautifulSoup(html.content, 'html.parser')
    except requests.exceptions.MissingSchema as err:
        print(err)
#
def get_page_numbers(url):
    bs = get_soup(url)
    for container in bs.select_one('div.pageNumbers').select('span'): pass
    return int(container['data-page-number'])
#
def get_user_profile_url(uid):
    url_member_overlay = "https://www.tripadvisor.com.sg/MemberOverlay?Mode=owa&uid=" + uid
    member = get_soup(url_member_overlay).select_one('a')['href'].strip()
    user_profile_url = "https://www.tripadvisor.com.sg" + member
    return user_profile_url
#
def parse_attraction_overview(url):
    '''
    param:
        url
    return:
        attraction_name, attraction_location, telephone number
        overall_rating, review_count,
        review_distributions: percentage of excellent,very_good,average,poor,terrible,
        review_highlights: travellers talk about most?
    '''
    bs = get_soup(url)
    # name
    name = bs.select_one('h1.heading_title').text.strip()
    # location
    street = bs.select_one('span.street-address').text.strip()
    locality = bs.select_one('span.locality').text.strip()
    country = bs.select_one('span.country-name').text.strip()
    loc= street + locality + country
    # telephone number
    tel = bs.select_one('div.detail_section.phone').text.strip()
    # overall rating
    overall_rating = bs.select_one('span.overallRating').text.strip()
    # review count
    review_count_s = bs.select_one('a.seeAllReviews').text.strip()
    pat_1 = re.compile('(\d*.\d*)')
    review_count = pat_1.search(review_count_s).group()
    if "," in review_count:
        review_count = review_count.replace(",","")
    # review distribution
    review_dis = bs.select_one('ul.ratings_chart').text.strip()
    pat_2 = re.compile('Excellent(\d*)%Very\s+good(\d*)%Average(\d*)%Poor(\d*)%Terrible(\d*)%')
    (review_5x, review_4x, review_3x, review_2x, review_1x) = pat_2.search(review_dis).groups()
    # review highlights
    review_highlights = []
    for s in bs.select('div.reviewKeyword'):
        keyword = s.select_one('a').text.strip()
        keyword_count = s.select_one('span.keywordCount').text.strip()
        review_highlights.append((keyword + keyword_count).encode('ascii','ignore').decode('ascii'))

    return(name,loc,tel,overall_rating,int(review_count),
           int(review_5x)/100.0, int(review_4x)/100.0, int(review_3x)/100.0,
           int(review_2x)/100.0, int(review_1x)/100.0,
           review_highlights)
#
def parse_review_details(url):
    '''
    param:
        url
    return:
        uid,
        reviewid, user_name, location,
        rating_score, rating_data, via,
        review_header, review_content,
    '''
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

