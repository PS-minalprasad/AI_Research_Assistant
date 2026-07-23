import os
from dotenv import load_dotenv

load_dotenv()

# ==========================
# Models
# ==========================

LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2:3b")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

# ==========================
# Chunk Settings
# ==========================

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 800))

CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 150))

TOP_K = int(os.getenv("TOP_K", 5))

# ==========================
# Project Paths
# ==========================

DATA_FOLDER = "data"

UPLOAD_FOLDER = "uploads"

VECTOR_DB = "vectorstore"

LOG_FOLDER = "logs"
