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
