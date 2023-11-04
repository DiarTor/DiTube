from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
# client = MongoClient("mongodb+srv://diartor:VtPLs3RxPsgzs1UT@cluster0.mocauua.mongodb.net/?retryWrites=true&w=majority")
db = client['mitube']
users_collection = db['users']
giftcodes_collection = db['giftcodes']