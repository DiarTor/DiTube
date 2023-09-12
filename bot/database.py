#Edit this file with your database settings (please remember to do refactor all codes referenced to the database).
import os

from pymongo import MongoClient

client = MongoClient(os.environ.get("MONGODB_URI", "mongodb://localhost:27017/"))
db = client['mitube']
users_collection = db['users']
