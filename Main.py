from workers.RawDataWorker import RawDataWorker

raw_data_worker = RawDataWorker()
actions = {
    "1": {"name": "Get raw reviews from Singapore Zoo", "execute": "raw_data_worker.extract_raw_reviews_singapore_zoo()"},
    "2": {"name": "Get raw reviews from River Safari", "execute": "raw_data_worker.extract_raw_reviews_river_safari()"},
    "3": {"name": "Get raw reviews from Night Safari", "execute": "raw_data_worker.extract_raw_reviews_night_safari()"},
    "4": {"name": "Get raw user profiles from all attractions", "execute": "raw_data_worker.extract_raw_users_all_attractions()"}
}

print("####################################")
print("## WildLife Reserves Web Scraping ##")
print("####################################")
for action_key, action_item in actions.items():
    print(action_key + ". " + action_item['name'])

choice = input("Please enter your choice.")

if choice not in actions:
    print("'" + choice + "' is invalid choice.")
else:
    eval(actions[choice]['execute'])

