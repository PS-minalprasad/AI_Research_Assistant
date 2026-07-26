# 🤖 AI Research Assistant

> **A Retrieval-Augmented Generation (RAG) based AI Research Assistant that enables users to upload PDF documents, perform semantic search, and receive grounded answers using locally hosted Large Language Models (LLMs) powered by Ollama.**

---

## 📌 Table of Contents

- Project Overview
- Features
- Tech Stack
- System Architecture
- RAG Pipeline
- Project Workflow
- Project Structure
- Installation
- Configuration
- Running the Project
- First-Time Setup (Ingesting Documents)
- API Endpoints
- Evaluation
- MCP Prototype
- Example Usage
- Troubleshooting
- Future Improvements
- License

---

# 📖 Project Overview

Large Language Models (LLMs) are powerful but often generate incorrect or hallucinated information when answering questions outside their training knowledge.

This project solves this problem using **Retrieval-Augmented Generation (RAG)**.

Instead of answering directly from the LLM, the assistant first searches uploaded PDF documents for relevant information using semantic search. The retrieved document chunks are then provided as context to the language model, allowing it to generate accurate and grounded responses.

The application is completely local and uses **Ollama**, **FAISS**, **LangChain**, **FastAPI**, and **Streamlit**.

---

# 🎯 Objectives

The project aims to:

- Build an end-to-end RAG application
- Support PDF document question answering
- Retrieve relevant context using vector similarity search
- Generate grounded responses with citations
- Demonstrate modular AI application architecture
- Explore Model Context Protocol (MCP) concepts

---

# ✨ Features

## Document Processing

- Upload PDF documents
- Extract document text
- Recursive chunking with overlap
- Automatic document indexing

---

## Semantic Search

- Generate embeddings using Ollama
- Store embeddings inside FAISS
- Retrieve relevant document chunks
- Similarity-based document search

---

## Grounded Question Answering

- Context-aware answers
- Source attribution
- Page number citations
- Refusal for unsupported questions
- Reduced hallucinations

---

## Modular Architecture

The application separates responsibilities into dedicated modules:

- API Layer
- Retrieval Layer
- Embedding Layer
- LLM Layer
- Utility Layer

making the project easier to maintain and extend.

---

## Local AI Inference

Runs completely locally using:

- Ollama
- llama3.2:3b
- nomic-embed-text

No paid API keys are required.

---

## MCP Prototype

The repository also contains a standalone FastMCP prototype demonstrating:

- list_documents
- document_count
- system_info
- current_time

This prototype is independent of the RAG pipeline and is included as a learning exercise for Model Context Protocol.

---

# 🛠 Tech Stack

| Category | Technology |
|------------|------------------------|
| Language | Python 3.12 |
| Frontend | Streamlit |
| Backend | FastAPI |
| Framework | LangChain |
| LLM | Ollama (llama3.2:3b) |
| Embeddings | nomic-embed-text |
| Vector Database | FAISS |
| PDF Processing | PyPDFLoader |
| Server | Uvicorn |
| Evaluation | Automated + human-judged evaluation suite |
| MCP | FastMCP Prototype |

---

# 🏗 System Architecture

```

User
│
▼
Streamlit UI
│
▼
FastAPI Backend
│
▼
RAG Pipeline
│
├──────── Retrieval Service
│ │
│ ▼
│ FAISS Vector Store
│
└──────── LLM Service
│
▼
Ollama
(llama3.2:3b)

```

---

# 🔄 RAG Pipeline

```

PDF Documents

↓

Text Extraction

↓

Recursive Chunking

↓

Generate Embeddings

↓

Store in FAISS

↓

User Question

↓

Question Embedding

↓

Semantic Search

↓

Relevant Context

↓

Prompt Construction

↓

LLM Response

↓

Answer with Sources

```

---

# ⚙️ Project Workflow

1. User uploads one or more PDF documents.
2. Text is extracted from the uploaded files.
3. Documents are split into overlapping chunks.
4. Each chunk is converted into vector embeddings.
5. Embeddings are stored inside a FAISS vector database.
6. User asks a question.
7. The question is embedded.
8. Similar chunks are retrieved from FAISS.
9. Retrieved context is injected into the prompt.
10. Ollama generates a grounded response.
11. The answer is displayed along with source document names and page numbers.

---

# 🚀 Why RAG?

Traditional LLMs answer only from pretrained knowledge.

RAG improves answer quality by retrieving relevant information from external documents before generation.

Benefits include:

- Reduced hallucination
- Better factual accuracy
- Explainable responses
- Source citations
- Domain-specific knowledge
- Local document understanding

---

# 📂 Project Structure

```text
AI_Research_Assistant/
│
├── api.py
├── app.py
├── rag.py
├── ingest.py
├── config.py
├── prompts.py
├── mcp_server.py
├── mcp_tool.py
│
├── services/
│ ├── embedding_service.py
│ ├── llm_service.py
│ └── retrieval_service.py
│
├── utils/
│ ├── constants.py
│ ├── helper.py
│ ├── logger.py
│ └── validator.py
│
├── evaluation/
│ ├── evaluate.py
│ ├── test_questions.json
│ ├── results.csv
│ ├── results.json
│ └── evaluation_matrix.md
│
├── data/
│
├── vectorstore/
│
├── logs/
│
├── requirements.txt
├── README.md
└── .env.example

```

> **Note:** `data/`, `vectorstore/`, and `logs/` are runtime folders. `data/` must contain at least one PDF before the app can answer questions — see **First-Time Setup** below. `vectorstore/` is generated automatically and is not committed to the repository.

---

# ⚙️ Installation & Setup

## Prerequisites

Before running the project, ensure the following software is installed:

| Software | Version |
|----------|---------|
| Python | 3.12+ |
| Git | Latest |
| Ollama | Latest |
| pip | Latest |

---

## 1. Clone the Repository

```bash
git clone https://github.com/PS-minalprasad/AI_Research_Assistant

cd AI_Research_Assistant
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Verify installation

```bash
pip list
```

---

## 4. Install Ollama

Download and install Ollama from

https://ollama.com/download

---

## 5. Download Required Models

```bash
ollama pull llama3.2:3b

ollama pull nomic-embed-text
```

These models are required for:

- Response Generation
- Embedding Generation

---

## 6. Start Ollama

```bash
ollama serve
```

Keep this terminal running throughout the execution.

---

# 🔧 Environment Configuration

Create a `.env` file from `.env.example`.

### Windows

```bash
copy .env.example .env
```

### Linux / macOS

```bash
cp .env.example .env
```

Example configuration:

```env
# ==========================================
# AI Research Assistant Configuration
# ==========================================

# API Configuration
API_URL=http://127.0.0.1:8000

# Ollama Models
LLM_MODEL=llama3.2:3b
EMBEDDING_MODEL=nomic-embed-text

# Document Chunking
CHUNK_SIZE=700
CHUNK_OVERLAP=150

# Retrieval Configuration
TOP_K=8
RELEVANCE_THRESHOLD=0.50
```

### Configuration Description

| Variable | Description |
|-----------|-------------|
| `API_URL` | Base URL of the FastAPI backend, used by the Streamlit frontend (`app.py`) |
| `LLM_MODEL` | Ollama model used for answer generation |
| `EMBEDDING_MODEL` | Model used to generate document embeddings |
| `CHUNK_SIZE` | Number of characters in each document chunk |
| `CHUNK_OVERLAP` | Overlap between consecutive chunks |
| `TOP_K` | Number of relevant chunks retrieved |
| `RELEVANCE_THRESHOLD` | Minimum similarity score for retrieved chunks |

---

# 📄 First-Time Setup (Ingesting Documents)

**This step is required before the assistant can answer any questions.** On a fresh clone, the `data/` and `vectorstore/` folders are empty — the app will start without crashing, but `/chat` will return a "knowledge base not ready" message until a document is indexed.

1. Copy at least one PDF into the `data/` folder.
2. Run the ingestion script:

```bash
python ingest.py
```

This will:

- Load all PDFs from `data/`
- Split text into overlapping chunks
- Generate embeddings
- Create the FAISS vector index inside `vectorstore/`

Only after this step (or after uploading a PDF through the UI, see **Adding Documents** below) will `/health` report `"rag_available": true` and `/chat` return real answers.

---

# 🚀 Running the Project

The application consists of two independent services:

- FastAPI Backend
- Streamlit Frontend

Both must be running simultaneously, in two separate terminals.

---

## Terminal 1 – Start Backend

Activate the virtual environment

**Windows**
```bash
venv\Scripts\activate
```

**Linux / macOS**
```bash
source venv/bin/activate
```

Run FastAPI

```bash
uvicorn api:app --reload
```

If the server starts successfully, visit:

```
http://127.0.0.1:8000/health
```

Expected Response (after ingestion has been run at least once)

```json
{
  "status": "healthy",
  "rag_available": true
}
```

If no documents have been ingested yet, `rag_available` will be `false` — this is expected and not an error; follow **First-Time Setup** above.

---

## Terminal 2 – Start Frontend

Activate the virtual environment (same as above, in a new terminal)

Run Streamlit

```bash
streamlit run app.py
```

The application will automatically open in your browser.

---

# 📄 Adding Documents

The project supports two methods for indexing PDFs.

## Method 1 – Upload Through the UI

Upload PDF files using the sidebar.

The application will automatically:

- Validate the uploaded PDF (type and size)
- Save it to the `data/` folder
- Regenerate embeddings for the full `data/` folder
- Update the FAISS vector database
- Reload the RAG pipeline so the new document is immediately queryable

---

## Method 2 – Manual Ingestion

Copy PDF files into:

```text
data/
```

Then execute:

```bash
python ingest.py
```

This will:

- Load all PDFs
- Split text into chunks
- Generate embeddings
- Create/update the FAISS vector index

> If you add or remove files in `data/` directly (outside the UI), re-run `python ingest.py` and restart the FastAPI backend so the pipeline picks up the refreshed index.

---

# 💬 Ask Questions

After documents have been indexed, enter a question into the chat interface.

Example:

```text
What is Retrieval-Augmented Generation?
```

The assistant will:

- Convert the question into embeddings
- Search the FAISS vector database
- Retrieve relevant document chunks
- Generate a grounded response
- Display supporting source document(s)
- Display page number(s)

If no relevant context is found, the assistant responds that it cannot answer based on the available documents instead of generating unsupported information.

---

# 📚 API Endpoints

| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/` | GET | API status |
| `/health` | GET | Health check — reports whether the knowledge base is ready |
| `/upload` | POST | Upload a PDF, validate it, and index it into the FAISS vector store |
| `/chat` | POST | Ask a question and receive a grounded answer with sources |
| `/documents` | GET | View indexed documents |

---

# 🔌 MCP Prototype

The repository includes a standalone **FastMCP prototype** for learning purposes.

Run it using:

```bash
python mcp_tool.py
```

Available prototype tools:

- `list_documents`
- `document_count`
- `system_info`
- `current_time`

**Note:** The MCP prototype is currently independent of the RAG pipeline and is not invoked by `api.py` or `rag.py`. The `MCPServer` class used by `/documents` in `api.py` is a plain helper class, unrelated to this FastMCP server.

---

# 📊 Evaluation

The project includes an evaluation workflow to verify the quality of retrieval, grounding, and response generation. Full methodology and grading criteria are documented in [`evaluation/EVALUATION.md`](evaluation/EVALUATION.md).

The evaluation reports three separate metrics rather than one combined "accuracy" score, so retrieval failures, grounding failures, and generation-quality failures can each be identified independently:

| Metric | How it's measured | What it tells you |
|----------|-------------|-------------|
| Retrieval hit-rate | Automatic — checks if the expected source document appears in retrieved chunks | Is the retriever finding the right evidence? |
| Refuse accuracy | Automatic — checks that out-of-scope and prompt-injection questions are correctly declined | Is the system staying grounded and resistant to instruction override? |
| Answer accuracy | Human-judged against `expected_answer` | Is the generated answer actually correct, regardless of wording? |

### Test Set

`evaluation/test_questions.json` contains answerable questions (direct, paraphrased, and cross-topic) plus deliberately unanswerable and prompt-injection questions, so abstention behavior is tested, not just normal Q&A.

### Running Evaluation

Make sure at least one document has been ingested (see **First-Time Setup**), then execute:

```bash
python evaluation/evaluate.py
```

You will be prompted `(y/n)` only for answerable questions, to judge answer quality. Refusal cases are checked automatically with no prompt.

Results are stored in:

```
evaluation/results.csv
evaluation/results.json
evaluation/evaluation_matrix.md
```

---

# 🧪 Example Usage

## Example 1

### Question

```
What is Retrieval-Augmented Generation?
```

### Response

```
Retrieval-Augmented Generation (RAG) combines information retrieval with a Large Language Model. Relevant document chunks are retrieved from a vector database and used as context before generating the final answer.
```

**Source**

```
research.pdf
Page 5
```

---

## Example 2

### Question

```
Explain embeddings.
```

### Response

```
Embeddings are dense numerical vector representations of text that capture semantic meaning. They enable similarity search within the vector database.
```

---

## Example 3

### Question

```
Who won the FIFA World Cup?
```

### Response

```
I could not find this information in the uploaded documents.
```

This demonstrates that the assistant avoids generating unsupported answers, including for questions with no relation to the ingested documents.

---

# 📷 Screenshots

You can include screenshots of the application here.

Suggested screenshots:

- Home Screen
- Upload PDF
- Chat Interface
- Generated Answer
- Source Citation
- API Documentation
- Evaluation Results

Example:

```
docs/
├── home.png
├── upload.png
├── answer.png
├── evaluation.png
```

---

# 📈 Performance

The system provides:

- Semantic document retrieval
- Local LLM inference
- Fast similarity search using FAISS
- Context-aware response generation
- Source citation for improved transparency

Performance depends on:

- Number of indexed documents
- Chunk size
- Retrieved context (TOP_K)
- Hardware specifications
- Selected Ollama model

---

# ⚠️ Limitations

Current limitations include:

- Supports PDF documents only
- Uses local FAISS vector storage
- Single-user application
- Local deployment only
- Requires Ollama installation
- MCP prototype is not integrated with the RAG pipeline
- Evaluation was performed against a single ingested document; multi-document retrieval accuracy has not been separately validated

---

# 🚀 Future Improvements

Planned enhancements include:

- Hybrid Search (Keyword + Semantic Search)
- Cross-Encoder Re-ranking
- Multi-document conversations
- Streaming responses
- Chat history memory
- Authentication and user management
- Cloud deployment
- Docker support
- PostgreSQL or ChromaDB integration
- Full Model Context Protocol (MCP) client integration
- AI Agent support
- Multi-modal document understanding
- Code-enforced abstention (removing the retrieval fallback so refusal does not depend solely on prompt instructions)

---

# 🛠 Troubleshooting

## Backend Offline

Ensure the FastAPI server is running.

```bash
uvicorn api:app --reload
```

---

## Ollama Not Running

Start Ollama before launching the application.

```bash
ollama serve
```

---

## Models Not Found

Download the required models.

```bash
ollama pull llama3.2:3b

ollama pull nomic-embed-text
```

---

## Vector Store Missing / `rag_available: false`

This is expected on a fresh clone. Add a PDF to `data/` and generate the FAISS vector database:

```bash
python ingest.py
```

Then restart the FastAPI backend.

---

## `/upload` fails immediately

Ensure `python-multipart` is installed — it is required by FastAPI for file uploads and is listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## No Answers Returned

Possible reasons:

- No documents uploaded or ingested yet (`rag_available: false`)
- FAISS index not created
- Low retrieval relevance for the question asked
- Ollama service not running

---

## Dependency Errors

Install project dependencies again.

```bash
pip install -r requirements.txt
```

---

# 🤝 Contributing

Contributions are welcome.

Steps:

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push to your branch.
5. Open a Pull Request.

---

# 📜 License

This project is developed for educational purposes as part of the **Level 1 AI Foundation Program**.

---

# 👩‍💻 Author

**Minal Prasad**

B.Tech Computer Science Engineering (Artificial Intelligence)

AI Research Assistant – Retrieval-Augmented Generation (RAG) Project

---

# ⭐ Acknowledgements

This project was developed using the following open-source technologies:

- Python
- FastAPI
- Streamlit
- LangChain
- Ollama
- FAISS
- FastMCP

Special thanks to the AI open-source community for providing the tools and frameworks used in this project.

---

# 📬 Contact

For questions, suggestions, or collaboration, please open an issue in the GitHub repository.

---

## 🎯 Project Status

**Current Status:** ✅ Completed (Level 1 RAG Project)

### Implemented

- PDF document ingestion
- Semantic search
- FAISS vector database
- Ollama integration
- FastAPI backend (starts safely with no pre-existing index)
- Streamlit frontend
- Grounded question answering
- Source attribution
- `/upload` endpoint with shared validation logic
- Automated + human-judged evaluation workflow
- Prompt-injection resistant system prompt
- Standalone MCP prototype

### Planned

- Full MCP client integration
- AI Agents
- Hybrid Retrieval
- Docker deployment
- Cloud deployment
- Authentication
- Advanced evaluation metrics
- Code-enforced abstention (removing the retrieval score fallback)








