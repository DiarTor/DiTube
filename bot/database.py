from pymongo import MongoClient
#Enter Your Database Config Here / You Can Use Another Databases As Well
client = MongoClient("")
db = client['']
users_collection = db['']
