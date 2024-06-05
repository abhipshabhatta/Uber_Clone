from bson import ObjectId
from app.mongodb_client import MongoDBClient

class RideModel:
    def __init__(self, db_client: MongoDBClient):
        self.db = db_client.get_database()
        self.collection = self.db['rides']

    def create_ride(self, ride_data):
        result = self.collection.insert_one(ride_data)
        return str(result.inserted_id)

    def get_requested_rides(self):
        return list(self.collection.find({"status": "requested"}))

    def get_ride_by_id(self, ride_id):
        return self.collection.find_one({"_id": ObjectId(ride_id)})

    def update_ride_status(self, ride_id, status):
        self.collection.update_one({"_id": ObjectId(ride_id)}, {"$set": {"status": status}})
