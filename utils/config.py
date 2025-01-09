import os
from pymongo import MongoClient
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = MongoClient(MONGO_URI)
db = client["chatbot_db"]
collection = db["vectors"]

model = SentenceTransformer("all-MiniLM-L6-v2")
