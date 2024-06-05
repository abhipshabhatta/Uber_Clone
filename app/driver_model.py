from bson import ObjectId
from app.mongodb_client import MongoDBClient

class DriverModel:
    def __init__(self, db_client: MongoDBClient):
        self.db = db_client.get_database()
        self.collection = self.db['drivers']

    def create_driver(self, driver_data):
        result = self.collection.insert_one(driver_data)
        return str(result.inserted_id)

    def get_driver_by_email(self, email):
        return self.collection.find_one({"email": email})

    def get_driver(self, driver_id):
        return self.collection.find_one({"_id": ObjectId(driver_id)})

    def update_driver(self, driver_id, driver_data):
        self.collection.update_one({"_id": ObjectId(driver_id)}, {"$set": driver_data})
