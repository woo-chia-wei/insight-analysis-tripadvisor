from workers.RawDataWorker import RawDataWorker
from workers.ProcessDataWorker import ProcessDataWorker

raw_data_worker = RawDataWorker()
process_data_worker = ProcessDataWorker()
actions = {
    "1": {"name": "Get raw reviews from Singapore Zoo.", "execute": "raw_data_worker.extract_raw_reviews_singapore_zoo()"},
    "2": {"name": "Get raw reviews from River Safari.", "execute": "raw_data_worker.extract_raw_reviews_river_safari()"},
    "3": {"name": "Get raw reviews from Night Safari.", "execute": "raw_data_worker.extract_raw_reviews_night_safari()"},
    "4": {"name": "Get raw user profiles from all attractions.", "execute": "raw_data_worker.extract_raw_users_all_attractions()"},
    "5": {"name": "Merge raw reviews from all attractions into single raw reviews.", "execute": "process_data_worker.merge_all_attractions()"},
    "6": {"name": "Process final raw reviews and copy to processed reviews.", "execute": "process_data_worker.process_raw_reviews()"},
    "7": {"name": "Process final raw users and copy to processed users.", "execute": "process_data_worker.process_user_reviews()"}
}

# Console Interface
# User can selection action to perform

print("####################################")
print("## WildLife Reserves Web Scraping ##")
print("####################################")
for action_key, action_item in actions.items():
    print(action_key + ". " + action_item['name'])

choice = input("Please enter your choice. ")

if choice not in actions:
    print("'" + choice + "' is invalid choice.")
else:
    print("====================================")
    eval(actions[choice]['execute'])

