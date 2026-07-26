from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from pathlib import Path
import shutil
import os

from rag import RAGPipeline
from mcp_server import MCPServer
import ingest

from config import DATA_FOLDER
from utils.constants import MAX_FILE_SIZE
from utils.validator import validate_pdf


app = FastAPI(
    title="AI Research Assistant API",
    version="1.0.0",
    description="Production Ready RAG API"
)


# Global RAG instance
rag = None


def load_rag():
    """
    Initialize RAG pipeline safely.
    Application can start even without vectorstore.
    """

    global rag

    try:
        rag = RAGPipeline()

    except Exception as e:
        print(f"RAG initialization skipped: {e}")
        rag = None



# Initialize RAG safely
load_rag()



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
        "status": "healthy",
        "rag_available": rag is not None
    }



@app.get("/documents")
def documents():

    return {
        "documents": MCPServer.list_documents()
    }



@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):

    global rag


    # Sanitize filename first — needed before any check or save
    filename = Path(file.filename).name

    if not filename:

        raise HTTPException(
            status_code=400,
            detail="Invalid filename."
        )


    try:

        os.makedirs(
            DATA_FOLDER,
            exist_ok=True
        )


        file_path = os.path.join(
            DATA_FOLDER,
            filename
        )


        # Save uploaded PDF
        with open(file_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )


        # Single source of truth for validation: extension + size,
        # checked together via the shared validator (not duplicated here).
        is_valid, message = validate_pdf(
            filename,
            os.path.getsize(file_path)
        )

        if not is_valid:

            os.remove(file_path)

            raise HTTPException(
                status_code=400,
                detail=message
            )


        # Create/update FAISS vector database
        ingest.main()


        # Reload RAG pipeline
        load_rag()


        return {
            "message": "PDF uploaded and indexed successfully.",
            "filename": filename
        }


    except HTTPException:
        raise


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )



@app.post("/chat")
def chat(request: ChatRequest):


    if rag is None:

        raise HTTPException(
            status_code=503,
            detail=(
                "Knowledge base is not ready. "
                "Please upload documents or run ingestion first."
            )
        )


    try:

        return rag.ask(
            request.question
        )


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Chat failed: {str(e)}"
        )
