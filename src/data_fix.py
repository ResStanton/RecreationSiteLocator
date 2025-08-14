import database

db =  database.Database(database.CONNECTION_STRING, "USFS_recreation_opportunities", "locations")

all_location = db.collection.find({"properties.MARKERACTIVITYGROUP": None})

for location in all_location:
    print(db.collection.update_one({"_id": location["_id"]}, {"$set": {"properties.MARKERACTIVITYGROUP": "Uncategorized"}}))
