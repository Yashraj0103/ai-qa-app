import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

MONGODB_URL = os.getenv("MONGODB_URL")

try:
    client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client["aiqa"]
    documents_collection = db["documents"]
    chats_collection = db["chats"]
    print("MongoDB connected successfully")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    client = None
    db = None
    documents_collection = None
    chats_collection = None

def save_document(doc_id: str, filename: str, doc_type: str, summary: str, content: str):
    if documents_collection is None:
        print("MongoDB not available, skipping save")
        return
    documents_collection.insert_one({
        "_id": doc_id,
        "filename": filename,
        "type": doc_type,
        "summary": summary,
        "content": content,
        "created_at": datetime.utcnow()
    })

def get_all_documents():
    if documents_collection is None:
        return []
    return list(documents_collection.find({}, {"content": 0}))

def save_chat(doc_id: str, question: str, answer: str):
    if chats_collection is None:
        print("MongoDB not available, skipping save")
        return
    chats_collection.insert_one({
        "doc_id": doc_id,
        "question": question,
        "answer": answer,
        "created_at": datetime.utcnow()
    })