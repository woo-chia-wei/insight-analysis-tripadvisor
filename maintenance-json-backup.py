from repositories.Repository import Repository
from bson import json_util
import json 

repo = Repository()
# json.dump(json_util.dumps(repo.read_raw_reviews_singapore_zoo_families()), open("raw_data_backups/raw_reviews_singapore_zoo_families.json", "w"))
json.dump(json_util.dumps(repo.read_raw_reviews_singapore_zoo_couples()), open("raw_data_backups/raw_reviews_singapore_zoo_couples.json", "w"))
# json.dump(json_util.dumps(repo.read_raw_reviews_singapore_zoo_solo()), open("raw_data_backups/raw_reviews_singapore_zoo_solo.json", "w"))
# json.dump(json_util.dumps(repo.read_raw_reviews_singapore_zoo_business()), open("raw_data_backups/raw_reviews_singapore_zoo_business.json", "w"))
# json.dump(json_util.dumps(repo.read_raw_reviews_singapore_zoo_friends()), open("raw_data_backups/raw_reviews_singapore_zoo_friends.json", "w"))

# json.dump(json_util.dumps(repo.read_raw_reviews_river_safari()), open("raw_data_backups/raw_reviews_river_safari.json", "w"))
# json.dump(json_util.dumps(repo.read_raw_reviews_night_safari()), open("raw_data_backups/raw_reviews_night_safari.json", "w"))