from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

try:
    # Connect to MongoDB
    client = MongoClient(
        "mongodb://localhost:27017/",
        serverSelectionTimeoutMS=5000
    )

    # Check connection
    client.admin.command("ping")

    print("=" * 60)
    print("✅ MongoDB Connected Successfully")
    print("=" * 60)

    # Database
    db = client["agricrop"]

    # Collections
    users_collection = db["users"]
    prediction_collection = db["predictions"]
    moisture_collection = db["moisture"]
    report_collection = db["reports"]

except ConnectionFailure as e:
    print("=" * 60)
    print("❌ MongoDB Connection Failed")
    print(e)
    print("=" * 60)
    raise