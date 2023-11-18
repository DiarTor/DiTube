from pymongo import MongoClient

client = MongoClient("mongodb://admin:f6hDyEUr7rY3!ZFsYnwl@188.40.16.3:31419/admin")
db = client['ditube']
users_collection = db['users']
giftcodes_collection = db['giftcodes']