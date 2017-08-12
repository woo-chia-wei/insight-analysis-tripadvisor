# python files:
Main.py
TripAdvisorReview.py
TripAdvisorProfile.py
ReviewAnalysis.py

# output files:  
Tripadvisor_singapore_zoo_review_overview.json
Tripadvisor_singapore_zoo_review_details.csv
Tripadvisor_singapore_zoo_user_profile.json
Analysis_1_review_rating_number_yearly.csv

# install modules
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import datetime
import json

# How to run?
> python3 Main.py

# How to use repository class?

from Repository import *

repo = Repository()

# Write single document
single_data = {"name":"Bruce", "school": "accounting"}
repo.write_analysis(single_data)

# Write multiple documents
multiple_data = [
    {"name":"Peter", "course": "computer science"},
    {"name":"John", "course": "electrical engineering"},
    {"name": "Jane", "country": "hong kong", "age": 15}
]
repo.write_raw_users(multiple_data)

# Read data from collection
print("Analysis Collection consists: ")
print(repo.read_analysis())
print()
print("Raw Users Collection consists: ")
print(repo.read_raw_users())

