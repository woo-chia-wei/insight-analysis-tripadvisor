from workers.RawDataWorker import RawDataWorker
from workers.ProcessDataWorker import ProcessDataWorker
from workers.DataAnalysisWorker import DataAnalysisWorker

raw_data_worker = RawDataWorker()
process_data_worker = ProcessDataWorker()
data_analysis_worker = DataAnalysisWorker()
actions = {
    "1": {"name": "Get raw reviews from Singapore Zoo.", "execute": "raw_data_worker.extract_raw_reviews_singapore_zoo()"},
    "2": {"name": "Get raw reviews from River Safari.", "execute": "raw_data_worker.extract_raw_reviews_river_safari()"},
    "3": {"name": "Get raw reviews from Night Safari.", "execute": "raw_data_worker.extract_raw_reviews_night_safari()"},
    "4": {"name": "Get raw user profiles from all attractions.", "execute": "raw_data_worker.extract_raw_users_all_attractions()"},
    "5": {"name": "Merge raw reviews from all attractions into single raw reviews.", "execute": "process_data_worker.merge_all_attractions()"},
    "6": {"name": "Process final raw reviews and copy to processed reviews.", "execute": "process_data_worker.process_raw_reviews()"},
    "7": {"name": "Process final raw users and copy to processed users.", "execute": "process_data_worker.process_user_reviews()"},
    "8": {"name": "Run sentiment analysis and topic modelling.", "execute": "data_analysis_worker.run_analysis()"},
    "Q": {"name": "Exit program.", "execute":"print('Exited program.')"}
}

def print_action(choice):
    print(choice + ". " + actions[choice]['name'])

# Console Line Interface
print()
print("##############################################")
print("#       WildLife Reserves Web Scraping       #")
print("##############################################")
print()
print("Raw Data Extraction")
print("------------------------------------")
print_action("1")
print_action("2")
print_action("3")
print_action("4")
print()
print("Data Pre-processing")
print("------------------------------------")
print_action("5")
print_action("6")
print_action("7")
print()
print("Perform text analytics")
print("------------------------------------")
print_action("8")
print()
print_action("Q")
print()
choice = input("Please enter your choice. ").upper()

if choice not in actions:
    print("'" + choice + "' is invalid choice.")
else:
    print()
    eval(actions[choice]['execute'])

