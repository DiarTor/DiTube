from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
# client = MongoClient("mongodb://admin:vnICel577xTiHAR!jXoa@188.40.16.3:30454/admin")
db = client['ditube']
users_collection = db['users']
giftcodes_collection = db['giftcodes']
factors_collection = db['factors']
subscriptions_collection = db['subscriptions']
