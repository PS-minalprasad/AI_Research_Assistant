from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from rag import RAGPipeline
from mcp_server import MCPServer

app = FastAPI(
    title="AI Research Assistant API",
    version="1.0.0",
    description="Production Ready RAG API"
)

rag = RAGPipeline()


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "AI Research Assistant API Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/documents")
def documents():
    return {
        "documents": MCPServer.list_documents()
    }


@app.post("/chat")
def chat(request: ChatRequest):

    try:
        result = rag.ask(request.question)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )