import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "agricrop_super_secret_key_2026"
    )

    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb://localhost:27017"
    )

    DATABASE_NAME = os.getenv(
        "DATABASE_NAME",
        "agricrop"
    )

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

    REPORT_FOLDER = os.path.join(BASE_DIR, "reports")

    DISEASE_MODEL = os.path.join(BASE_DIR, "disease_model.h5")

    MOISTURE_MODEL = os.path.join(BASE_DIR, "moisture_model.pkl")