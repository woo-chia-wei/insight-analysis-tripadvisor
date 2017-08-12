import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import datetime
import json

def get_soup(url):
    requests.adapters.DEFAULT_RETRIES = 5
    requests.session().keep_alive = False
    try:
        html = requests.get(url)
        return BeautifulSoup(html.content, 'html.parser')
    except requests.exceptions.MissingSchema as err:
        print(err)

def get_page_numbers(url):
    bs = get_soup(url)
    for container in bs.select_one('div.pageNumbers').select('span'): pass
    return int(container['data-page-number'])

def get_user_profile_url(uid):
    url_member_overlay = "https://www.tripadvisor.com.sg/MemberOverlay?Mode=owa&uid=" + uid
    member = get_soup(url_member_overlay).select_one('a')['href'].strip()
    user_profile_url = "https://www.tripadvisor.com.sg" + member
    return user_profile_url

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

