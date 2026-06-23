from pymongo import MongoClient

try:
    client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=3000)

    client.server_info()

    print("✅ MongoDB Connected Successfully!")

except Exception as e:
    print("❌ Connection Failed")
    print(e)