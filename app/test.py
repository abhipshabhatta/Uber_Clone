from pymongo import MongoClient
from urllib.parse import quote_plus

username = 'abhipshabhatta'
password = '@bheeps@123'

escaped_username = quote_plus(username)
escaped_password = quote_plus(password)
uri = f"mongodb+srv://{escaped_username}:{escaped_password}@uberclone.qqr6qbm.mongodb.net/uber_clone_db?retryWrites=true&w=majority"

try:
    client = MongoClient(uri)
    db = client['uber_clone_db']
    print("Connection successful")
except Exception as e:
    print(f"Error: {e}")
