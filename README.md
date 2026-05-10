# 🧠 Pragya — AI-Powered Learning Assistant

> **Pragya** (Sanskrit: *wisdom*) is a personalized AI learning assistant that lets students interact with their own study material — PDFs and YouTube lectures — through natural, conversational question answering.

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-orange)](https://langchain.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20DB-purple)](https://trychroma.com)
[![Gemini](https://img.shields.io/badge/Google-Gemini%20API-blue?logo=google)](https://ai.google.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 📌 Overview

Instead of manually scrubbing through long PDFs or rewinding lecture videos, Pragya lets you upload your study material and ask questions in plain language. It retrieves the most relevant content from your own sources and generates grounded, context-aware answers.

No hallucinations from generic web knowledge. Just answers from *your* material.

---

## 🎯 Why I Built This

As a student, I constantly juggled:
- 📄 PDFs and class notes
- 🎥 YouTube lecture videos
- 🔍 Search tabs for every concept

Finding a single concept across all these sources is slow and frustrating. Pragya unifies them into one AI-powered interface where you can upload your material, ask questions naturally, and get grounded answers — combining formal definitions from notes with intuitive explanations from lectures.

---

## ✨ Features (V1)

| Feature | Status |
|---|---|
| PDF Upload & Processing | ✅ |
| YouTube Transcript Ingestion | ✅ |
| Semantic Search via Vector Embeddings | ✅ |
| Context-Aware AI Answers | ✅ |
| Source-Aware Responses | ✅ |
| FastAPI Backend | ✅ |
| Responsive Chat-Style Frontend | ✅ |
| Real-Time Query Latency Tracking | ✅ |
| ChromaDB Vector Storage | ✅ |
| Google Gemini LLM Integration | ✅ |
| Dark-Themed Modern UI | ✅ |

---

## ⚡ Performance

One of the most significant milestones of this project was a **~94% reduction in query latency**:

| Version | LLM Provider | Query Latency |
|---|---|---|
| V0 (initial) | NVIDIA NIM | ~76 seconds |
| V1 (current) | Google Gemini | ~4.2–4.3 seconds |

**Same query. Same API structure. 18× faster.**

> **Why the switch?**
> NVIDIA NIM offered 40 requests/second throughput, but real-world latency was unacceptably high for a conversational interface. Migrating to the **Google Gemini API** brought latency down to ~4.2 seconds, making the experience feel genuinely interactive.
>
> ⚠️ **Current Gemini limitation:** The free tier is capped at **20 requests/day**. For heavier usage, upgrade to a paid Gemini API plan.

---

## 🛠️ Tech Stack

### Backend
- **Python** — Core language
- **FastAPI** — REST API server
- **LangChain** — RAG orchestration
- **ChromaDB** — Vector database for semantic storage
- **Google Gemini API** — LLM for answer generation
- **YouTube Transcript API** — Lecture ingestion

### Frontend
- **HTML / CSS / JavaScript** — Responsive, dark-themed chat UI

### AI / NLP
- Retrieval-Augmented Generation (RAG)
- Text Embeddings
- Semantic Search
- Chunking Pipelines

---

## 🏗️ Architecture

```
User Question
      │
      ▼
Frontend (HTML/CSS/JS)
      │
      ▼
FastAPI Backend
      │
      ▼
Embedding Search (ChromaDB)
      │
      ▼
Relevant Chunks Retrieved
      │
      ▼
Prompt Construction
      │
      ▼
Google Gemini LLM
      │
      ▼
Grounded Response Returned
```

---

## 📁 Project Structure

```
Pragya/
│
├── backend/
│   ├── chroma/                        # Vector database storage
│   ├── data/                          # Uploaded PDFs
│   │
│   ├── llm/
│   │   └── llm_client.py              # Gemini API integration
│   │
│   ├── rag/
│   │   ├── get_embedding_function.py  # Embedding model setup
│   │   ├── populatedb.py              # Chunk & embed pipeline
│   │   ├── query_data_llm.py          # RAG querying logic
│   │   └── youtube_loader.py          # YouTube transcript ingestion
│   │
│   ├── .env                           # Environment variables
│   ├── app.py                         # FastAPI server
│   ├── requirements.txt
│   └── youtube_links.txt
│
└── frontend/
    ├── index.html
    ├── script.js
    └── style.css
```

---

## ⚙️ How It Works

### 1. Upload Content
- Upload one or more **PDF files** (notes, textbooks, slides)
- Paste **YouTube lecture links**

### 2. Processing Pipeline

**PDFs:**
1. Extract text from document
2. Split into semantic chunks
3. Generate vector embeddings
4. Store in ChromaDB

**YouTube Videos:**
1. Fetch transcript via YouTube Transcript API
2. Chunk transcript by segment
3. Generate vector embeddings
4. Store with timestamps for traceability

### 3. Query & Answer
1. User question is embedded
2. ChromaDB performs semantic similarity search
3. Top-k relevant chunks are retrieved
4. Chunks + question are sent to Gemini as a structured prompt
5. Gemini generates a grounded, source-aware response

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- A [Google Gemini API key](https://ai.google.dev)

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd Pragya
```

### 2. Create & Activate Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file inside the `backend/` folder:
```env
API_KEY=YOUR_GEMINI_API_KEY
```

### 5. Run the Backend
```bash
cd backend
uvicorn app:app --reload
```

Backend will be available at: `http://localhost:8000`

### 6. Launch the Frontend

Open `frontend/index.html` in your browser, or use the **VSCode Live Server** extension for hot-reloading.

---

## 💡 Example Workflow

```
1. Upload: "operating_systems_notes.pdf"
2. Add YouTube link: https://youtube.com/watch?v=...
3. Ask:
   → "What is deadlock?"
   → "Explain paging with an intuition"
   → "What is the difference between a process and a thread?"

Pragya retrieves relevant chunks from your material
and generates grounded, context-aware answers.
```

---

## 📸 Screenshots

```markdown
![Uploading Docs](screenshot/processing.png)
![Processed Docs](screenshot/processed.png)
![Query Example](screenshot/askingquestion.png)
```

---

## 🧩 Challenges Faced

- Managing long-context prompts within API token limits
- Handling Gemini API daily quota constraints (20 requests/day on free tier)
- Optimizing retrieval quality — right chunk size, overlap, and top-k selection
- Structuring chunk metadata for source-aware responses
- Frontend-backend integration with async query handling
- Maintaining answer groundedness (no hallucinated content)
- Organizing ChromaDB vector storage across multiple ingestion sessions

---

## 🔮 Roadmap

### V2 — AI & Retrieval Upgrades
- [ ] Streaming responses (token-by-token output)
- [ ] Multi-LLM support (switch between Gemini, GPT-4, Claude, etc.)
- [ ] Smarter, adaptive chunking strategies
- [ ] Multimodal retrieval (images, graphs, tables from PDFs)
- [ ] Summarization pipeline per document

### V3 — Product Features
- [ ] Authentication system
- [ ] Per-user vector databases
- [ ] Persistent chat history
- [ ] Document management dashboard
- [ ] Support for PPT/PPTX, DOCX, Images, Scanned PDFs (OCR)

### Performance
- [ ] Faster retrieval with hybrid search (BM25 + semantic)
- [ ] Better indexing strategies
- [ ] Lower query latency (target: < 2s)

---

## 📚 Key Learnings

Building Pragya gave me hands-on experience with:

- Real-world RAG pipeline design
- Vector databases and embedding workflows
- Prompt engineering for grounded, source-faithful answers
- LLM API integration and quota management
- Frontend/backend communication with FastAPI
- Latency profiling and optimization
- Scalable architecture thinking for AI-native applications

---

## 👤 Author

**Kushagra Jain**

Built as a personal project to explore AI systems, retrieval-augmented generation, backend engineering, and intelligent educational tooling.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
