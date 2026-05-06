from fastapi import APIRouter, UploadFile, File, HTTPException
from services.pdf_service import extract_text_from_pdf
from services.audio_service import transcribe_audio
from services.vector_service import VectorStore, vector_stores
from services.llm_service import summarize_content
from models.database import save_document, get_all_documents
import uuid

router = APIRouter()
documents = {}

@router.post("/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    file_bytes = await file.read()
    text = extract_text_from_pdf(file_bytes)

    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from PDF")

    doc_id = str(uuid.uuid4())
    store = VectorStore()
    store.build_index(text)
    vector_stores[doc_id] = store

    summary = summarize_content(text)

    documents[doc_id] = {
        "id": doc_id,
        "filename": file.filename,
        "type": "pdf",
        "text": text,
        "summary": summary,
        "segments": None
    }

    try:
        save_document(doc_id, file.filename, "pdf", summary, text)
    except Exception as e:
        print(f"MongoDB save error: {e}")

    return {
        "doc_id": doc_id,
        "filename": file.filename,
        "summary": summary,
        "char_count": len(text)
    }

@router.post("/audio")
async def upload_audio(file: UploadFile = File(...)):
    allowed = [".mp3", ".mp4", ".wav", ".m4a", ".webm"]
    if not any(file.filename.endswith(ext) for ext in allowed):
        raise HTTPException(status_code=400, detail=f"Allowed formats: {allowed}")

    file_bytes = await file.read()
    result = transcribe_audio(file_bytes, file.filename)

    doc_id = str(uuid.uuid4())
    store = VectorStore()
    store.build_index(result["full_text"])
    vector_stores[doc_id] = store

    summary = summarize_content(result["full_text"])

    documents[doc_id] = {
        "id": doc_id,
        "filename": file.filename,
        "type": "audio",
        "text": result["full_text"],
        "summary": summary,
        "segments": result["segments"]
    }

    try:
        save_document(doc_id, file.filename, "audio", summary, result["full_text"])
    except Exception as e:
        print(f"MongoDB save error: {e}")

    return {
        "doc_id": doc_id,
        "filename": file.filename,
        "summary": summary,
        "segments": result["segments"][:10],
        "total_segments": len(result["segments"])
    }

@router.get("/documents")
def list_documents():
    return [
        {
            "id": doc["id"],
            "filename": doc["filename"],
            "type": doc["type"],
            "summary": doc["summary"]
        }
        for doc in documents.values()
    ]