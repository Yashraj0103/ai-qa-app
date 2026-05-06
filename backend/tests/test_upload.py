from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "AI Q&A API is running"}

def test_upload_invalid_extension():
    response = client.post(
        "/upload/pdf",
        files={"file": ("test.txt", b"hello world", "text/plain")}
    )
    assert response.status_code == 400

def test_list_documents_empty():
    response = client.get("/upload/documents")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_upload_audio_invalid():
    response = client.post(
        "/upload/audio",
        files={"file": ("test.txt", b"not audio", "text/plain")}
    )
    assert response.status_code == 400