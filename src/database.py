import pymongo
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

    """Return a list of all the data in the database collection"""
    def query_all(self) -> list:
        return self.collection.find().to_list()
    
    """Return a one location based of of its geospacial location"""
    def query_latitude_longitude(self, latitude: float, longitude: float):
        return self.collection.find_one({"geometry.coordinates": [longitude, latitude]})
    
    def get_unique_location_types(self):
        return self.collection.distinct("properties.MARKERACTIVITYGROUP")
    
    def query_by_name(self, name: str):
        return list(self.collection.find({"properties.RECAREANAME": {"$regex":f"{name}*", "$options": "i"}}))
   
    # This query checks if 'activity_type' exists in the ACTIVITY array
    def query_by_activity_type(self, activity_type: str) -> list:
	    return list(self.collection.find({"properties.MARKERACTIVITYGROUP": activity_type}))
    
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

        # Simulate dropdown selection
    selected_activity = "Hiking"  # Change this to test other activities or leave empty

   
    # query for all locations
    print("Querying all locations")
    start_time = time.time()
    location_types = database.query_by_name("yellow")
    print(f"Operation took: {time.time()-start_time} Seconds")

    # print the name of each location
    print("printing all points")
    start_time = time.time()
    for location_type in location_types:
        print(location_type["properties"]["RECAREANAME"])
    print(f"Operation took: {time.time()-start_time} Seconds")
