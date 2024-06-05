from .mongodb_client import MongoDBClient
from bson.objectid import ObjectId

class UserModel:
    def __init__(self, db_client: MongoDBClient):
        self.db = db_client.get_database()
        self.collection = self.db['users']

    def create_user(self, user_data):
        result = self.collection.insert_one(user_data)
        return result.inserted_id

    def get_user_by_email(self, email):
        return self.collection.find_one({"email": email})

    def get_user_by_id(self, user_id):
        return self.collection.find_one({"_id": ObjectId(user_id)})
