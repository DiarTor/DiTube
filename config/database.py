from pymongo import MongoClient

# client = MongoClient("mongodb://admin:kR35fSXHkSh$IbiiqO3j@188.40.16.3:30454/admin")
client = MongoClient("mongodb://localhost:27017/")
db = client['ditube']
users_collection = db['users']
giftcodes_collection = db['giftcodes']