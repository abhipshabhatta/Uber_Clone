from .mongodb_client import MongoDBClient

class PriceModel:
    def __init__(self, db_client: MongoDBClient):
        self.db = db_client.get_database()
        self.collection = self.db['prices']

    def calculate_price(self, start_location, end_location):
        distance = self._calculate_distance(start_location, end_location)
        base_fare = 2.50
        cost_per_mile = 1.75
        total_price = base_fare + (distance * cost_per_mile)
        return round(total_price, 2)

    def _calculate_distance(self, start_location, end_location):
        return abs(len(start_location) - len(end_location))
