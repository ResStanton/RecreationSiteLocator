import database

db =  database.Database(database.CONNECTION_STRING, "USFS_recreation_opportunities", "locations")

all_location = db.collection.find()

for location in all_location:
    if location["geometry"]["coordinates"][1] < 0:
        switched_coords = [location["geometry"]["coordinates"][1], location["geometry"]["coordinates"][0]]
        print(db.collection.update_one({"_id": location["_id"]}, {"$set": {"geometry.coordinates": switched_coords}}))