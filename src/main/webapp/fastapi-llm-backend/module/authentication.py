from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import ssl

import certifi

class Authenticate:
    def __init__(self, uri):
        print(ssl.OPENSSL_VERSION)
        try:
            # Create MongoDB client with TLS
            self.client = MongoClient(
                uri, tls=True, 
                tlsCAFile=certifi.where(), 
                serverSelectionTimeoutMS=5000
            )
            
            # Test connection
            self.client.admin.command('ping')
            print("✅ Successfully connected to MongoDB Atlas")
        
        except ConnectionFailure as e:
            print(f"❌ Could not connect to MongoDB: {e}")
            self.client = None

    def verify_api_key(self, api_key):
        if not self.client:
            print("❌ No MongoDB connection.")
            return False
        
        db = self.client["ApiKey"]
        collection = db["keys"]  # Replace with your collection name
        
        result = collection.find_one({"key": api_key})
        
        if result:
            print("✅ API Key is valid.")
            return True
        else:
            print("❌ API Key is invalid.")
            return False

