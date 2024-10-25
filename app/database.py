# app/database.py# app/database.py
import pymongo
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get MongoDB URI from environment variables
MONGODB_URI = os.getenv("MONGODB_URI")

# Establish MongoDB client
client = pymongo.MongoClient(MONGODB_URI)
db = client.get_database("certificate_db")  # Replace with your database name
