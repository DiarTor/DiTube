from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['ditube']
users_collection = db['users']
giftcodes_collection = db['giftcodes']