# 🤖 AI Research Assistant (RAG + MCP Prototype)

An AI-powered research assistant that lets you upload PDF documents, ask questions about them, and get answers grounded in those documents using Retrieval-Augmented Generation (RAG). Includes a basic MCP (Model Context Protocol) prototype exploring standardized AI tool communication.

---

## 📌 Project Overview

LLMs can generate incorrect information when they lack access to domain-specific knowledge. This project addresses that with RAG: relevant chunks from user-provided PDFs are retrieved and given to the LLM as context before it answers.

**Workflow**

1. User uploads a PDF (or PDFs are placed in the `data/` folder).
2. The document is loaded and its text extracted.
3. Text is split into overlapping chunks.
4. Each chunk is embedded (Ollama `nomic-embed-text`).
5. Embeddings are stored in a local FAISS vector index.
6. A user question is embedded the same way.
7. FAISS returns the most relevant chunks.
8. Those chunks are inserted into the prompt as context.
9. The LLM (Ollama `llama3.2:3b`) generates a grounded answer, with sources and page numbers.

---

## ✨ Features

**Document processing** — upload PDFs, extract text, chunk it, build a searchable index.

**Semantic search** — embed chunks and queries, retrieve the most relevant context via FAISS similarity search.

**Grounded Q&A** — answers are generated only from retrieved context, with source file + page shown alongside each answer, and the assistant declines to answer when no relevant evidence is found.

**MCP prototype** — `mcp_tool.py` exposes a small FastMCP server (`list_documents`, `document_count`, `system_info`, `current_time`) as a standalone learning exercise. It is **not yet wired into the RAG pipeline** — the assistant doesn't call it as an MCP client. Full client/tool integration is a planned next step, not a current feature.

---

## 🏗️ Architecture

```
Streamlit UI (app.py)
        │  HTTP
        ▼
FastAPI backend (api.py)
        │
        ▼
RAGPipeline (rag.py)
   ├── RetrievalService → FAISS vectorstore/
   └── LLMService → Ollama (llama3.2:3b)

ingest.py → builds/updates vectorstore/ from data/*.pdf
```

The UI and the backend are **two separate processes** that must both be running — see step 8 below. This is the step that was missing from earlier versions of this README and caused the app to show "Backend Offline."

---

## 📁 Project Structure

```
AI_Research_Assistant/
├── app.py               # Streamlit UI
├── api.py                # FastAPI backend (chat, upload, health, documents)
├── rag.py                 # RAG pipeline (retrieval + generation)
├── ingest.py               # Builds/updates the FAISS index from PDFs
├── config.py                # Model, chunking, and path configuration
├── prompts.py                 # System prompt
├── mcp_server.py                # Plain utility class used by /documents
├── mcp_tool.py                    # Standalone FastMCP prototype server
├── services/
│   ├── embedding_service.py         # Ollama embeddings
│   ├── llm_service.py                # Ollama chat model
│   └── retrieval_service.py           # FAISS load + similarity search
├── utils/
│   ├── constants.py                     # App-wide constants/messages
│   ├── helper.py                         # Filesystem helpers
│   ├── validator.py                       # PDF upload validation
│   └── logger.py                           # Logging setup
├── data/                    # PDFs live here (created automatically)
├── vectorstore/               # FAISS index (created automatically, gitignored)
├── logs/                         # App logs (created automatically)
├── requirements.txt
└── .env.example
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/PS-minalprasad/AI_Research_Assistant
cd AI_Research_Assistant
```

### 2. Create a virtual environment

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / Mac**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> If you're uploading PDFs through the UI, make sure `python-multipart` is included in `requirements.txt` — FastAPI needs it to accept file uploads. Add it if it's missing: `pip install python-multipart`.

### 4. Install Ollama

Download and install from [https://ollama.com](https://ollama.com).

### 5. Pull the required models

```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

### 6. Start Ollama

```bash
ollama serve
```

Leave this running in its own terminal.

### 7. Configure environment variables (optional)

```bash
cp .env.example .env
```

Defaults work out of the box; edit `.env` only if you want a different model, chunk size, or relevance threshold.

### 8. Start the backend and frontend (two separate terminals)

**Terminal A — FastAPI backend** (activate the venv here too):
```bash
uvicorn api:app --reload --port 8000
```
Wait until you see `Application startup complete`. Visit `http://127.0.0.1:8000/health` — it should return `{"status": "healthy", ...}`.

**Terminal B — Streamlit UI**:
```bash
streamlit run app.py
```
This opens the chat UI in your browser and talks to the backend from Terminal A. If it shows "🔴 Backend Offline," Terminal A isn't running yet.

### 9. Add your first documents

Either:
- **Upload through the UI** — use the sidebar's "Upload & Process" button (this saves the PDF to `data/` and rebuilds the index automatically), or
- **Pre-seed the `data/` folder** and build the index manually before starting the backend:
  ```bash
  python ingest.py
  ```

Once at least one PDF is indexed, ask questions in the chat box. Answers include the source file and page number they were drawn from; if nothing relevant is found in your documents, the assistant will say so instead of guessing.

---

## 🔌 MCP Status

This project currently ships an MCP prototype (`mcp_tool.py`) as a separate exploration, run independently of the RAG app if you want to try it:

```bash
python mcp_tool.py
```

It is not called by `api.py` or `rag.py`. The `/documents` endpoint instead uses a plain helper class (`mcp_server.py`, despite its name) — this is a naming leftover from the prototype phase, not an active MCP integration.

---







