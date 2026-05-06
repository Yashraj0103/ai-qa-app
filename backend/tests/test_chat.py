from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_ask_question_missing_doc():
    response = client.post("/chat/ask", json={
        "doc_id": "nonexistent-id",
        "question": "What is this about?"
    })
    assert response.status_code == 404

def test_get_summary_missing_doc():
    response = client.get("/chat/summary/nonexistent-id")
    assert response.status_code == 404

def test_register_user():
    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "token" in response.json()

def test_login_user():
    client.post("/auth/register", json={
        "username": "loginuser",
        "password": "pass123"
    })
    response = client.post("/auth/login", json={
        "username": "loginuser",
        "password": "pass123"
    })
    assert response.status_code == 200
    assert "token" in response.json()

def test_login_wrong_password():
    response = client.post("/auth/login", json={
        "username": "loginuser",
        "password": "wrongpass"
    })
    assert response.status_code == 401