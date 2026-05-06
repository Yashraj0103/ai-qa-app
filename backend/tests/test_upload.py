from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app
import routers.upload as upload_router

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "AI Q&A API is running"}

def test_list_documents_empty():
    response = client.get("/upload/documents")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_upload_invalid_pdf_extension():
    response = client.post(
        "/upload/pdf",
        files={"file": ("test.txt", b"hello world", "text/plain")}
    )
    assert response.status_code == 400
    assert "Only PDF files allowed" in response.json()["detail"]

def test_upload_invalid_audio_extension():
    response = client.post(
        "/upload/audio",
        files={"file": ("test.txt", b"hello", "text/plain")}
    )
    assert response.status_code == 400

def test_upload_empty_pdf():
    with patch("routers.upload.extract_text_from_pdf", return_value=""):
        response = client.post(
            "/upload/pdf",
            files={"file": ("test.pdf", b"fake pdf content", "application/pdf")}
        )
        assert response.status_code == 400
        assert "Could not extract text" in response.json()["detail"]

def test_upload_pdf_success():
    with patch("routers.upload.extract_text_from_pdf", return_value="This is test content about AI"), \
         patch("routers.upload.VectorStore") as MockStore, \
         patch("routers.upload.summarize_content", return_value="Test summary"), \
         patch("routers.upload.save_document", return_value=None):
        mock_store = MagicMock()
        MockStore.return_value = mock_store
        response = client.post(
            "/upload/pdf",
            files={"file": ("test.pdf", b"fake pdf content", "application/pdf")}
        )
        assert response.status_code == 200
        data = response.json()
        assert "doc_id" in data
        assert data["filename"] == "test.pdf"
        assert data["summary"] == "Test summary"

def test_upload_audio_success():
    with patch("routers.upload.transcribe_audio", return_value={
            "full_text": "This is a test transcription",
            "segments": [{"start": 0.0, "end": 5.0, "text": "This is a test"}]
         }), \
         patch("routers.upload.VectorStore") as MockStore, \
         patch("routers.upload.summarize_content", return_value="Audio summary"), \
         patch("routers.upload.save_document", return_value=None):
        mock_store = MagicMock()
        MockStore.return_value = mock_store
        response = client.post(
            "/upload/audio",
            files={"file": ("test.mp3", b"fake audio", "audio/mpeg")}
        )
        assert response.status_code == 200
        data = response.json()
        assert "doc_id" in data
        assert data["filename"] == "test.mp3"

def test_list_documents_with_data():
    upload_router.documents["list-test-id"] = {
        "id": "list-test-id",
        "filename": "listed.pdf",
        "type": "pdf",
        "text": "content",
        "summary": "summary",
        "segments": None
    }
    response = client.get("/upload/documents")
    assert response.status_code == 200
    ids = [d["id"] for d in response.json()]
    assert "list-test-id" in ids

# --- PDF Service Tests ---
def test_pdf_service_extract():
    from services.pdf_service import extract_text_from_pdf
    import io
    import PyPDF2
    from unittest.mock import patch, MagicMock

    mock_page = MagicMock()
    mock_page.extract_text.return_value = "Hello World"

    with patch("PyPDF2.PdfReader") as MockReader:
        MockReader.return_value.pages = [mock_page]
        result = extract_text_from_pdf(b"fake pdf bytes")
        assert "Hello World" in result

def test_pdf_service_empty_page():
    from services.pdf_service import extract_text_from_pdf
    from unittest.mock import patch, MagicMock

    mock_page = MagicMock()
    mock_page.extract_text.return_value = None

    with patch("PyPDF2.PdfReader") as MockReader:
        MockReader.return_value.pages = [mock_page]
        result = extract_text_from_pdf(b"fake pdf bytes")
        assert isinstance(result, str)

# --- Vector Service Tests ---
def test_chunk_text():
    from services.vector_service import chunk_text
    text = " ".join(["word"] * 600)
    chunks = chunk_text(text)
    assert len(chunks) > 1
    assert all(isinstance(c, str) for c in chunks)

def test_chunk_text_short():
    from services.vector_service import chunk_text
    text = "short text"
    chunks = chunk_text(text)
    assert len(chunks) == 1

def test_get_embedding():
    from services.vector_service import get_embedding
    emb = get_embedding("hello world test")
    assert len(emb) == 768
    assert isinstance(emb[0], float)

def test_vector_store_build_and_search():
    from services.vector_service import VectorStore
    store = VectorStore()
    store.build_index("The quick brown fox jumps over the lazy dog. " * 20)
    results = store.search("quick fox", top_k=2)
    assert isinstance(results, list)

def test_vector_store_empty_search():
    from services.vector_service import VectorStore
    store = VectorStore()
    results = store.search("anything")
    assert results == []

# --- LLM Service Tests ---
def test_summarize_content():
    from services.llm_service import summarize_content
    from unittest.mock import patch, MagicMock
    mock_response = MagicMock()
    mock_response.content = "• Point 1\n• Point 2\n• Point 3"
    with patch("services.llm_service.llm") as mock_llm:
        mock_llm.invoke.return_value = mock_response
        result = summarize_content("Some long text content here")
        assert isinstance(result, str)

def test_answer_question_no_store():
    from services.llm_service import answer_question
    from unittest.mock import patch, MagicMock
    mock_response = MagicMock()
    mock_response.content = "Test answer"
    with patch("services.llm_service.llm") as mock_llm:
        mock_llm.invoke.return_value = mock_response
        result = answer_question("nonexistent-doc", "What is this?")
        assert "answer" in result
        assert result["answer"] == "Test answer"

def test_answer_question_with_store():
    from services.llm_service import answer_question
    from services.vector_service import vector_stores, VectorStore
    from unittest.mock import patch, MagicMock

    store = VectorStore()
    store.build_index("This document is about artificial intelligence and machine learning.")
    vector_stores["test-llm-doc"] = store

    mock_response = MagicMock()
    mock_response.content = "It is about AI"
    with patch("services.llm_service.llm") as mock_llm:
        mock_llm.invoke.return_value = mock_response
        result = answer_question("test-llm-doc", "What is this about?")
        assert result["answer"] == "It is about AI"

def test_find_timestamp_none_segments():
    from services.llm_service import find_relevant_timestamp
    result = find_relevant_timestamp("question", [])
    assert result is None

def test_find_timestamp_with_segments():
    from services.llm_service import find_relevant_timestamp
    from unittest.mock import patch, MagicMock
    mock_response = MagicMock()
    mock_response.content = "5.0"
    with patch("services.llm_service.llm") as mock_llm:
        mock_llm.invoke.return_value = mock_response
        result = find_relevant_timestamp("what happened at 5 seconds?", [
            {"start": 5.0, "end": 10.0, "text": "something happened"}
        ])
        assert result == 5.0

def test_find_timestamp_invalid_response():
    from services.llm_service import find_relevant_timestamp
    from unittest.mock import patch, MagicMock
    mock_response = MagicMock()
    mock_response.content = "none"
    with patch("services.llm_service.llm") as mock_llm:
        mock_llm.invoke.return_value = mock_response
        result = find_relevant_timestamp("question", [
            {"start": 0.0, "end": 5.0, "text": "test"}
        ])
        assert result is None

# --- Audio Service Tests ---
def test_transcribe_audio_error_handling():
    from services.audio_service import transcribe_audio
    result = transcribe_audio(b"invalid audio bytes", "test.mp3")
    assert "full_text" in result
    assert "segments" in result

# --- Database Tests ---
def test_save_document():
    from models.database import save_document
    from unittest.mock import patch, MagicMock
    with patch("models.database.documents_collection") as mock_col:
        mock_col.insert_one.return_value = MagicMock()
        save_document("doc1", "file.pdf", "pdf", "summary", "content")
        mock_col.insert_one.assert_called_once()

def test_get_all_documents():
    from models.database import get_all_documents
    from unittest.mock import patch
    with patch("models.database.documents_collection") as mock_col:
        mock_col.find.return_value = [{"_id": "1", "filename": "test.pdf"}]
        result = get_all_documents()
        assert isinstance(result, list)

def test_save_chat():
    from models.database import save_chat
    from unittest.mock import patch, MagicMock
    with patch("models.database.chats_collection") as mock_col:
        mock_col.insert_one.return_value = MagicMock()
        save_chat("doc1", "question?", "answer!")
        mock_col.insert_one.assert_called_once()