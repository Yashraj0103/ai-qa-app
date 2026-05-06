# 🤖 AI Document & Multimedia Q&A App

A full-stack web application that allows users to upload PDF documents, audio, and video files and interact with an AI-powered chatbot to ask questions based on the uploaded content.

## 🚀 Live Demo
> Record your walkthrough and paste the YouTube/Drive link here

## ✨ Features
- 📄 Upload PDF documents and extract text
- 🎵 Upload audio/video files with automatic transcription
- 🤖 AI-powered chatbot using LangChain + Groq (LLaMA 3.3)
- 🔍 Semantic search using FAISS vector store
- ⏱️ Timestamp extraction for audio/video content
- ▶️ Play button to jump to relevant timestamps
- 📝 Automatic content summarization
- 🔐 JWT-based user authentication
- 💾 MongoDB for document storage

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python + FastAPI |
| LLM | LangChain + Groq (LLaMA 3.3) |
| Transcription | Deepgram Nova-2 |
| Vector Search | FAISS |
| Database | MongoDB Atlas |
| Frontend | React + Vite |
| Auth | JWT |
| Containerization | Docker + Docker Compose |
| CI/CD | GitHub Actions |

## 📋 Prerequisites
- Python 3.11+
- Node.js 20+
- Docker Desktop
- API Keys: Groq, Deepgram, MongoDB Atlas

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/Yashraj0103/ai-qa-app.git
cd ai-qa-app
```

### 2. Set up environment variables
Create `backend/.env`:
```env
GROQ_API_KEY=your-groq-key
DEEPGRAM_API_KEY=your-deepgram-key
MONGODB_URL=your-mongodb-url
SECRET_KEY=your-secret-key
```

### 3. Run with Docker (Recommended)
```bash
docker compose up --build
```
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 4. Run without Docker

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 🧪 Testing
```bash
cd backend
pytest tests/ -v --cov=. --cov-report=term-missing
```
Current coverage: **96%**

## 📡 API Documentation
Visit http://localhost:8000/docs for interactive Swagger UI.

| Method | Endpoint | Description |
|---|---|---|
| POST | /upload/pdf | Upload a PDF file |
| POST | /upload/audio | Upload audio/video file |
| GET | /upload/documents | List all documents |
| POST | /chat/ask | Ask a question |
| GET | /chat/summary/{id} | Get document summary |
| POST | /auth/register | Register user |
| POST | /auth/login | Login user |

## 🔄 CI/CD
GitHub Actions automatically runs tests on every push to main branch.

## 📁 Project Structure
```
ai-qa-app/
├── backend/
│   ├── main.py
│   ├── routers/
│   │   ├── upload.py
│   │   ├── chat.py
│   │   └── auth.py
│   ├── services/
│   │   ├── pdf_service.py
│   │   ├── audio_service.py
│   │   ├── vector_service.py
│   │   └── llm_service.py
│   ├── models/
│   │   └── database.py
│   ├── tests/
│   │   ├── test_upload.py
│   │   └── test_chat.py
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   └── api/
│   └── Dockerfile
├── docker-compose.yml
└── .github/
    └── workflows/
        └── ci.yml
```