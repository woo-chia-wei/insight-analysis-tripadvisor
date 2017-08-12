import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import datetime
import json
from TripAdvisorReview import *
from RawDataWorker import RawDataWorker

url = "https://www.tripadvisor.com.sg/Attraction_Review-g294265-d324542-Reviews-Singapore_Zoo-Singapore.html"


#------------------------------------------#
# Review Details
#------------------------------------------#
page_num = get_page_numbers(url)
base_url = "https://www.tripadvisor.com.sg/Attraction_Review-g294265-d324542-Reviews"
location_url = "-Singapore_Zoo-Singapore.html"
uid_s,reviewid_s,user_name_s,location_s=[],[],[],[]
rating_score_s,rating_date_s,via_s=[],[],[]
review_header_s,review_content_s = [],[]

for i in range(page_num):
    if i%20 == 0:
        print("%s, processing %d / %d" % (str(datetime.datetime.now()),i,page_num))
    if i == 0:
        page = ""
    else:
        page = "-or" + str(i*10)
    url = base_url + page + location_url
    #print(url)
    review_details = parse_review_details(url)
    for j in range(len(review_details[0][:])):
        uid_s.append(review_details[0][j])
        reviewid_s.append(review_details[1][j])
        user_name_s.append(review_details[2][j])
        location_s.append(review_details[3][j])
        rating_score_s.append(review_details[4][j])
        rating_date_s.append(review_details[5][j])
        via_s.append(review_details[6][j])
        review_header_s.append(review_details[7][j])
        review_content_s.append(review_details[8][j])

# convert to data-frame and export
file_output = "Tripadvisor_singapore_zoo_review_details.csv"
df = pd.DataFrame({'UID':uid_s,'ReviewId':reviewid_s,'UserName':user_name_s,
                   'Location':location_s,
                   'Rating':rating_score_s,'Date':rating_date_s,'Via':via_s,
                   'ReviewHeader':review_header_s,
                   'ReviewContent':review_content_s})
df['Date'] = pd.to_datetime(df['Date'])
df.to_csv(file_output,index=False,sep=',',
          columns=['UID','ReviewId','UserName','Location',
                   'Rating','Date',
                   'Via','ReviewHeader','ReviewContent'])
#
print("-"*50+"\nReview Details\n"+"-"*50)
print("Check file: "+file_output+"\n")
#
#------------------------------------------#
# User Profile
#------------------------------------------#
worker = RawDataWorker()
# worker.write_raw_users(urls)





# total = len(uid_s)
# file_output2 = "Tripadvisor_singapore_zoo_user_profile.json"
# f=open(file_output2,"w")
# f.close()
# f=open(file_output2,'a')
# for i,uid in enumerate(uid_s):
#     if i%20 == 0:
#         print("%s, processing %d / %d" % (str(datetime.datetime.now()),i,total))
#     if uid:
#         #print(uid)
#         user_profile_url = get_user_profile_url(uid)
#         f.write(extract_profile(get_soup(user_profile_url)) + "\n")
# print("-" * 50 + "\nUser Profile\n" + "-" * 50)
# print("Check file: " + file_output2 + "\n")
# End.
