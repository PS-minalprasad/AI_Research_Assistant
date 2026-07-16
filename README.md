# 🤖 AI Research Assistant using RAG + MCP Prototype

An intelligent AI-powered research assistant that allows users to upload documents, retrieve relevant information, and generate context-aware answers using Retrieval-Augmented Generation (RAG).

This project focuses on building a reliable document-based question-answering system using LLMs, embeddings, vector databases, and semantic search. It also includes a basic MCP (Model Context Protocol) prototype to explore how AI applications can communicate with external tools.

---

# 📌 Project Overview

Large Language Models (LLMs) are powerful but may generate incorrect information when they do not have access to domain-specific knowledge.

This project solves this problem using Retrieval-Augmented Generation (RAG).

The system retrieves relevant information from user-provided documents and provides this context to the LLM before generating an answer.

The workflow:

1. User uploads documents.
2. Documents are loaded and processed.
3. Text is divided into smaller chunks.
4. Embeddings are generated for each chunk.
5. Embeddings are stored in a vector database.
6. User queries are converted into embeddings.
7. Relevant document chunks are retrieved using similarity search.
8. Retrieved context is provided to the LLM.
9. The LLM generates a grounded response.

Additionally, the project explores MCP (Model Context Protocol) through a prototype implementation to understand standardized AI tool communication.

---

# ✨ Features

## 📄 Document Processing

- Upload and process PDF documents.
- Extract text from documents.
- Split large documents into smaller chunks.
- Create a searchable knowledge base.

---

## 🔎 Semantic Search

- Generate text embeddings.
- Store embeddings using a vector database.
- Perform similarity-based document retrieval.
- Retrieve the most relevant context for user queries.

---

## 🧠 AI Question Answering

- Generate answers based on retrieved document information.
- Reduce hallucination by grounding responses in source documents.
- Provide context-aware responses.

---

## 🔌 MCP Prototype Integration

The project includes a basic exploration of Model Context Protocol (MCP).

Current MCP implementation:

- Created MCP server structure.
- Studied MCP tool-based communication.
- Designed architecture for future MCP integration.

Future improvements:

- Complete MCP client-server communication.
- Connect MCP tools directly with the RAG pipeline.
- Add multiple AI tools through MCP.

---

# 🏗️ System Architecture

## Architecture Flow Explanation

1. User Interface
   - User interacts with the application through Streamlit.
   - User uploads documents and asks questions.

2. Document Processing Pipeline
   - Documents are loaded.
   - Text is extracted and divided into chunks.
   - Embeddings are generated.

3. Vector Database
   - Document embeddings are stored in FAISS.
   - User queries are matched using similarity search.

4. Retrieval-Augmented Generation (RAG)
   - Relevant document chunks are retrieved.
   - Retrieved context is sent to the LLM.

5. LLM Response Generation
   - The LLM generates a final answer based on retrieved information.

6. MCP Prototype
   - A basic MCP server structure is included.
   - It demonstrates how AI systems can expose tools for future integration.