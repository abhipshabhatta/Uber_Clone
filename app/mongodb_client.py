from pymongo import MongoClient
from urllib.parse import quote_plus

class MongoDBClient:
    def __init__(self, username, password, uri_template="mongodb+srv://{}:{}@uberclone.qqr6qbm.mongodb.net/uber_clone_db?retryWrites=true&w=majority"):
        escaped_username = quote_plus(username)
        escaped_password = quote_plus(password)
        uri = uri_template.format(escaped_username, escaped_password)
        self.client = MongoClient(uri)
        self.db = self.client['uber_clone_db']

    def get_database(self):
        return self.db

