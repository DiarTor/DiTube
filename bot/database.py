from pymongo import MongoClient
from urllib.parse import quote_plus

# Replace these with your MongoDB server information
username = "root"
password = "bplko0o0@@##"
server_ip = "185.110.191.92"
port = 27017  # MongoDB default port

# Escape the username and password using quote_plus
escaped_username = quote_plus(username)
escaped_password = quote_plus(password)

# Create the MongoDB URI with escaped credentials
mongo_uri = f"mongodb://{escaped_username}:{escaped_password}@{server_ip}:{port}/"

# Create a MongoClient with the URI
client = MongoClient(mongo_uri)

# Access a specific database
db = client["mitube"]

# Access a specific collection
users_collection = db["users"]