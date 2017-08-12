from workers.RawDataWorker import RawDataWorker

# Following codes should not be executed in a row

def extract_raw_reviews_all_attractions():
    raw_data_worker = RawDataWorker()
    raw_data_worker.write_raw_reviews([
        {
            "name": "Singapore Zoo",
            "url": "https://www.tripadvisor.com.sg/Attraction_Review-g294265-d324542-Reviews-Singapore_Zoo-Singapore.html"
        },
        {
            "name": "River Safari",
            "url": "https://www.tripadvisor.com.sg/Attraction_Review-g294265-d4089881-Reviews-River_Safari-Singapore.html"
        },
        {
            "name": "Night Safari",
            "url": "https://www.tripadvisor.com.sg/Attraction_Review-g294265-d324761-Reviews-Night_Safari-Singapore.html"
        }
    ])

extract_raw_reviews_all_attractions()

