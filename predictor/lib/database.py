import os

from pymongo import MongoClient

print("Creating MongoDB client...")
mongodb_client = MongoClient(os.getenv("MONGO_URI"))
db = mongodb_client[os.getenv("MONGO_DB")]
print("MongoDB client created!")
