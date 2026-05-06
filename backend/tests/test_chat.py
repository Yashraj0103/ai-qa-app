from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
import routers.upload as upload_router

client = TestClient(app)

def test_ask_question_not_found():
    response = client.post("/chat/ask", json={
        "doc_id": "nonexistent-id",
        "question": "What is this about?"
    })
    assert response.status_code == 404
    assert "Document not found" in response.json()["detail"]

def test_get_summary_not_found():
    response = client.get("/chat/summary/nonexistent-id")
    assert response.status_code == 404

def test_ask_question_success():
    upload_router.documents["test-doc-id"] = {
        "id": "test-doc-id",
        "filename": "test.pdf",
        "type": "pdf",
        "text": "This is test content",
        "summary": "Test summary",
        "segments": None
    }

    with patch("routers.chat.answer_question", return_value={
        "answer": "This is a test answer",
        "timestamp": None,
        "sources": ["Test content"]
    }), patch("routers.chat.save_chat", return_value=None):

        response = client.post("/chat/ask", json={
            "doc_id": "test-doc-id",
            "question": "What is this about?"
        })
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert data["answer"] == "This is a test answer"

def test_get_summary_success():
    upload_router.documents["test-doc-2"] = {
        "id": "test-doc-2",
        "filename": "sample.pdf",
        "type": "pdf",
        "text": "Sample content",
        "summary": "Sample summary",
        "segments": None
    }
    response = client.get("/chat/summary/test-doc-2")
    assert response.status_code == 200
    data = response.json()
    assert data["summary"] == "Sample summary"
    assert data["filename"] == "sample.pdf"

def test_register_user():
    response = client.post("/auth/register", json={
        "username": "testuser123",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "token" in response.json()

def test_register_duplicate_user():
    client.post("/auth/register", json={
        "username": "dupuser",
        "password": "pass123"
    })
    response = client.post("/auth/register", json={
        "username": "dupuser",
        "password": "pass123"
    })
    assert response.status_code == 400

def test_login_success():
    client.post("/auth/register", json={
        "username": "logintest",
        "password": "pass123"
    })
    response = client.post("/auth/login", json={
        "username": "logintest",
        "password": "pass123"
    })
    assert response.status_code == 200
    assert "token" in response.json()

def test_login_wrong_password():
    client.post("/auth/register", json={
        "username": "wrongpass",
        "password": "correct123"
    })
    response = client.post("/auth/login", json={
        "username": "wrongpass",
        "password": "wrongpass"
    })
    assert response.status_code == 401

def test_login_nonexistent_user():
    response = client.post("/auth/login", json={
        "username": "nobody",
        "password": "pass"
    })
    assert response.status_code == 401