import pymongo
from bson.objectid import ObjectId

USERNAME = 'PythonBacked'
PASSWORD = 'NJgAD1jRPc7j441F'

CONNECTION_STRING = f"mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.ykhbmhb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


class Database:
    def __init__(self, collection_string: str, database_name: str, collection_name: str):
        # Store the arguments as private attributes in the class
        # NOTE: Python does not have private attributes, so they designated by the leading _ 
        self._connection_string = collection_string
        self.database_name = database_name
        self._collection_name = collection_name

        # Configure the client, database, and collection
        self._client = pymongo.MongoClient(collection_string)
        self._database = self._client[database_name]

        # The collection is left public in case it needs to be accessed for more advanced queries then those built in
        self.collection = self._database[collection_name]

    def query_all(self) -> list:
        """Return a list of all the data in the database collection"""
        return self.collection.find().to_list()
    
    def query_id(self, location_id: str):
        """Get a location bases on its _id from the database"""
        return self.collection.find_one({"_id": ObjectId(location_id)})

    def get_unique_location_types(self):
        """Return a list of all unique location types"""
        return self.collection.distinct("properties.MARKERACTIVITYGROUP")
    
    def query_by_name(self, name: str):
        return list(self.collection.find({"properties.RECAREANAME": {"$regex":f"{name}*", "$options": "i"}}))
   
    # This query checks if 'activity_type' exists in the ACTIVITY array
    def query_by_activity_type(self, activity_type: str) -> list:
        return list(self.collection.find({"properties.MARKERACTIVITYGROUP": activity_type}))
    
    def query_name_and_activity_type(self, name: str, activity_type: str) -> list:
        """Return a list of locations that have the same given activity type and match the given search name"""
        return self.collection.find({
            "properties.MARKERACTIVITYGROUP": activity_type,
            "properties.RECAREANAME": {"$regex":f"{name}*", "$options": "i"}
            }).to_list()
    
       # This query search by using the coordinates for sites near that location - Session 9
    def query_near_location(self,longitude, latitude, max_distance=20000):
        return self.collection.find({'geometry': { 
                                        '$near': { 
                                        '$geometry': { 
                                            ' type': "Point", 
                                            'coordinates': [longitude, latitude] 
                                        }, 
                                        '$maxDistance': max_distance, 
                                        '$minDistance': 0 
                                        } 
                                    }} 
                                    ).to_list()
    
    def activity_type_and_query_near_location(self, longitude, latitude, activity_type, max_distance=20000):
        """Return a list of locations that have the same given activity type and are near the same location"""
        return self.collection.find({'geometry': { 
                                        '$near': { 
                                        '$geometry': { 
                                            ' type': "Point", 
                                            'coordinates': [longitude, latitude] 
                                        }, 
                                        '$maxDistance': max_distance, 
                                        '$minDistance': 0 
                                        } 
                                    }, 
                                    "properties.MARKERACTIVITYGROUP": activity_type })
 
    
    def close(self):
        self._client.close()
    

# Run the file for testing the database
if __name__ == "__main__":
    import time
    # NOTE: test code goes here

    # Create database connection
    print("opening the database")
    start_time = time.time()
    database = Database(CONNECTION_STRING, "USFS_recreation_opportunities", "locations")
    print(f"Operation took: {time.time()-start_time} Seconds")
   
    # query locations near coordinates 
    print("Querying Near locations")
    start_time = time.time()
    location_types = database.query_near_location(-106.4322, 38.7474)
    print(f"Operation took: {time.time()-start_time} Seconds")

    # print the name of each location
    print("printing all points")
    start_time = time.time()
    for location_type in location_types:
        print(location_type["properties"]["RECAREANAME"])
    print(f"Operation took: {time.time()-start_time} Seconds")
