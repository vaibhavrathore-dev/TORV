from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["torv_v1"]

bikes_collection = db["bikes"]
cars_collection = db["cars"]
users_collection = db["users"]

client.admin.command("ping")
print("MongoDB connected successfully")