from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from os import getenv

class Authenticate:
      def __init__ (self):
          self.uri = getenv("API_KEY_MongoDb")
          # Create a new client and connect to the server
          self.client = MongoClient(self.uri, server_api=ServerApi('1'))
          # Send a ping to confirm a successful connection
          try:
              self.client.admin.command('ping')
              print("successfully connected to MongoDB!")
          except Exception as e:
              print(e)

      def varify_api_key(self, api_key: str) -> bool:
        db = self.client["ApiKey"]
        collection = db["token"]

        result = collection.find_one({"token": api_key})
        return result is not None
      