# AI-Interview-Assistant--RAG
Perfect.
You now need a **professional, production-level README** — something that makes recruiters immediately understand:

* Architecture
* RAG flow
* Deployment
* DevOps setup
* Monitoring
* CI/CD
* Testing
* Docker

Below is a complete, clean, recruiter-ready README you can copy.

---

# 📄 README.md

---

# 🤖 AI Interview Assistant (RAG-based System)

A Retrieval-Augmented Generation (RAG) chatbot built with:

* **FastAPI** (Backend API)
* **FAISS** (Vector Database)
* **Google Gemini API** (LLM + Embeddings)
* **LangChain LCEL** (Retrieval pipeline)
* **Streamlit** (Frontend)
* **Docker** (Containerization)
* **GitHub Actions** (CI/CD)
* **Render** (Cloud Deployment)
* **Prometheus Metrics** (Monitoring)

---

# 🏗 Architecture Overview

## 🔹 High-Level Flow

```
User → Streamlit Frontend → FastAPI Backend → FAISS Retrieval → Gemini LLM → Response
```

---

## 🔹 Detailed Architecture

```
                    ┌──────────────────┐
                    │  Streamlit UI     │
                    │ (Frontend Layer)  │
                    └─────────┬────────┘
                              │ REST API
                              ▼
                    ┌──────────────────┐
                    │   FastAPI RAG    │
                    │     Backend      │
                    ├──────────────────┤
                    │  /chat endpoint  │
                    │  /health         │
                    │  Rate Limiting   │
                    │  Prometheus      │
                    └─────────┬────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  FAISS Index     │
                    │  Vector Store    │
                    └─────────┬────────┘
                              │ Top 4 docs
                              ▼
                    ┌──────────────────┐
                    │ Gemini LLM       │
                    │ (Context-aware)  │
                    └──────────────────┘
```

---

# 🧠 RAG Workflow

1. User submits question
2. Backend retrieves top **4 similar document chunks** using FAISS
3. Retrieved context is injected into prompt
4. Gemini LLM generates grounded response
5. Response + source filenames returned

---

# 🛠 Tech Stack

### Backend

* FastAPI
* LangChain (LCEL)
* FAISS
* Google Gemini API
* SlowAPI (rate limiting)
* Prometheus FastAPI Instrumentator

### Frontend

* Streamlit
* Requests

### DevOps

* Docker
* GitHub Actions CI
* Render Deployment

---

# 📁 Project Structure

```
AI-Interview-Assistant--RAG/
│
├── backend/
│   ├── main.py
│   ├── rag_pipeline.py
│   ├── vector_store.py
│   ├── faiss_index/
│   └── __init__.py
│
├── tests/
│   ├── test_api.py
│
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│
├── Dockerfile
├── pytest.ini
├── requirements.txt
└── README.md
```

---

# 🚀 Running Locally

## 1️⃣ Clone Repo

```bash
git clone <repo-url>
cd AI-Interview-Assistant--RAG
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\activate   # Windows
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Set Environment Variables

Create `.env`:

```
GOOGLE_API_KEY=your_api_key_here
```

---

## 5️⃣ Create FAISS Index

```bash
python backend/vector_store.py
```

---

## 6️⃣ Run Backend

```bash
uvicorn backend.main:app --reload
```

Visit:

```
http://localhost:8000/docs
```

---

## 7️⃣ Run Frontend

```bash
cd frontend
streamlit run app.py
```

Visit:

```
http://localhost:8501
```

---

# 🐳 Docker Deployment

## Build Image

```bash
docker build -t rag-backend .
```

## Run Container

```bash
docker run -p 8000:8000 \
  -e GOOGLE_API_KEY=your_api_key \
  rag-backend
```

---

# ☁ Deployment on Render

## Deploy Backend

1. Push repo to GitHub
2. Login to Render
3. Create **New Web Service**
4. Connect GitHub repo
5. Environment: **Docker**
6. Add environment variable:
https://ai-interview-assistant-rag.onrender.com
```
GOOGLE_API_KEY=your_key
```

7. Deploy

---

## Deploy Frontend

Deployed on streamlit cloud
https://nazzzzzz096-ai-interview-assistant--rag-frontendapp-zklnq7.streamlit.app/

# 🔒 API Endpoints

## GET /health

Returns service health

```json
{
  "status": "healthy"
}
```

---

## POST /chat

Request:

```json
{
  "question": "What is supervised learning?"
}
```

Response:

```json
{
  "answer": "Supervised learning is...",
  "sources": ["machine_learning.pdf"]
}
```

---

# 🧪 Testing

Run:

```bash
pytest
```

CI uses `TEST_MODE=true` to disable real API calls.

---

# 🛡 Rate Limiting

```
10 requests per minute per IP
```

---

# 📊 Monitoring

Prometheus metrics exposed at:

```
/metrics
```

Tracks:

* Total RAG requests
* Latency
* Error rate

---

# ⚡ CI/CD Pipeline

GitHub Actions pipeline includes:

* Dependency install
* Black formatting check
* Ruff lint check
* Pytest test suite
* TEST_MODE isolation

---

# 🎯 Key Engineering Highlights

* Uses LCEL chain composition
* Avoids hardcoded API keys
* Proper test isolation
* Dockerized backend
* Cloud-ready configuration
* Rate limiting
* Observability with Prometheus
* Modular architecture
* Clean package structure

---

# 🔮 Future Improvements

* Redis caching for embeddings
* Authentication layer
* Async RAG execution
* Streaming responses
* Conversation memory
* Multi-model support
* Horizontal scaling

---

# 👩‍💻 Author

Built as a production-ready RAG system to demonstrate:

* Retrieval-based LLM architecture
* Vector database integration
* Cloud deployment
* CI/CD practices
* Modern backend engineering

---

# ⭐ Why This Project Stands Out

This is not just an LLM wrapper.

It demonstrates:

* True RAG implementation
* Production architecture
* Cloud deployment
* Testable backend
* Observability
* Rate limiting
* Docker expertise

---

---



