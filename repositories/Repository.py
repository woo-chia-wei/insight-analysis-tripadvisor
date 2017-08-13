from pymongo import MongoClient

class Repository:

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['tripadvisor']
    
    def __write(self, collection_name, data):
        collection = self.db[collection_name]
        collection.delete_many({})
        is_array = isinstance(data, list)
        if(is_array):
            collection.insert_many(data)
        else:
            collection.insert_one(data)
            
    def __read(self, collection_name, query, projection):
        collection = self.db[collection_name]
        return list(collection.find(query, projection))
    
    # Writers
    
    def write_raw_reviews_all_attractions(self, data):
        self.__write('raw_reviews', data)

    def write_raw_reviews_singapore_zoo(self, data):
        self.__write('raw_reviews_singapore_zoo', data)

    def write_raw_reviews_river_safari(self, data):
        self.__write('raw_reviews_river_safari', data)

    def write_raw_reviews_night_safari(self, data):
        self.__write('raw_reviews_night_safari', data)

    def write_raw_users(self, data):
        self.__write('raw_users', data)
        
    def write_processed_reviews(self, data):
        self.__write('processed_reviews', data) 
    
    def write_processed_users(self, data):
        self.__write('processed_users', data)  
    
    def write_analysis(self, data):
        self.__write('analysis', data)
        
    # Readers
    
    def read_raw_reviews(self, query={}, projection=None):
        return self.__read('raw_reviews', query, projection)

    def read_raw_reviews_singapore_zoo(self, query={}, projection=None):
        return self.__read('raw_reviews_singapore_zoo', query, projection)

    def read_raw_reviews_river_safari(self, query={}, projection=None):
        return self.__read('raw_reviews_river_safari', query, projection)

    def read_raw_reviews_night_safari(self, query={}, projection=None):
        return self.__read('raw_reviews_night_safari', query, projection)

    def read_raw_users(self, query={}, projection=None):
        return self.__read('raw_users', query, projection)
        
    def read_processed_reviews(self, query={}, projection=None):
        return self.__read('processed_reviews', query, projection)
    
    def read_processed_users(self, query={}, projection=None):
        return self.__read('processed_users', query, projection)
    
    def read_analysis(self, query={}, projection=None):
        return self.__read('analysis', query, projection)

    # Data Patching

    def write_raw_reviews_singapore_zoo_families(self, data):
        self.__write('raw_reviews_singapore_zoo_families', data)

    def write_raw_reviews_singapore_zoo_couples(self, data):
        self.__write('raw_reviews_singapore_zoo_couples', data)

    def write_raw_reviews_singapore_zoo_solo(self, data):
        self.__write('raw_reviews_singapore_zoo_solo', data)

    def write_raw_reviews_singapore_zoo_business(self, data):
        self.__write('raw_reviews_singapore_zoo_business', data)

    def write_raw_reviews_singapore_zoo_friends(self, data):
        self.__write('raw_reviews_singapore_zoo_friends', data)

    def merge_raw_reviews_singapore_zoo_all_traveller_types(self, data):
        data = []
        data += self.__read('raw_reviews_singapore_zoo_families', {}, None)
        data += self.__read('raw_reviews_singapore_zoo_couples', {}, None)
        data += self.__read('raw_reviews_singapore_zoo_solo', {}, None)
        data += self.__read('raw_reviews_singapore_zoo_business', {}, None)
        data += self.__read('raw_reviews_singapore_zoo_friends', {}, None)
        self.write_raw_reviews_singapore_zoo(data)

    def read_raw_reviews_singapore_zoo_families(self, query={}, projection=None):
        return self.__read('raw_reviews_singapore_zoo_families', query, projection)

    def read_raw_reviews_singapore_zoo_couples(self, query={}, projection=None):
        return self.__read('raw_reviews_singapore_zoo_couples', query, projection)

    def read_raw_reviews_singapore_zoo_solo(self, query={}, projection=None):
        return self.__read('raw_reviews_singapore_zoo_solo', query, projection)

    def read_raw_reviews_singapore_zoo_business(self, query={}, projection=None):
        return self.__read('raw_reviews_singapore_zoo_business', query, projection)

    def read_raw_reviews_singapore_zoo_friends(self, query={}, projection=None):
        return self.__read('raw_reviews_singapore_zoo_friends', query, projection)
