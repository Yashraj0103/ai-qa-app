from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.llm_service import answer_question
from models.database import save_chat
from routers.upload import documents

router = APIRouter()

class ChatRequest(BaseModel):
    doc_id: str
    question: str

@router.post("/ask")
def ask_question(request: ChatRequest):
    doc = documents.get(request.doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    result = answer_question(
        doc_id=request.doc_id,
        question=request.question,
        segments=doc.get("segments")
    )

    try:
        save_chat(request.doc_id, request.question, result["answer"])
    except Exception as e:
        print(f"MongoDB chat save error: {e}")

    return result

@router.get("/summary/{doc_id}")
def get_summary(doc_id: str):
    doc = documents.get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"summary": doc["summary"], "filename": doc["filename"]}