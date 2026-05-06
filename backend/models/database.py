import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

client = MongoClient(os.getenv("MONGODB_URL"))
db = client["aiqa"]

documents_collection = db["documents"]
chats_collection = db["chats"]

def save_document(doc_id: str, filename: str, doc_type: str, summary: str, content: str):
    documents_collection.insert_one({
        "_id": doc_id,
        "filename": filename,
        "type": doc_type,
        "summary": summary,
        "content": content,
        "created_at": datetime.utcnow()
    })

def get_all_documents():
    return list(documents_collection.find({}, {"content": 0}))

def save_chat(doc_id: str, question: str, answer: str):
    chats_collection.insert_one({
        "doc_id": doc_id,
        "question": question,
        "answer": answer,
        "created_at": datetime.utcnow()
    })