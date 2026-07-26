"""
config.py

Application configuration.
Loads environment variables from .env.s
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==========================================================
# Models
# ==========================================================

LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2:3b")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

# ==========================================================
# RAG Settings
# ==========================================================

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 700))

CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 150))

TOP_K = int(os.getenv("TOP_K", 8))

# Minimum similarity score for retrieved chunks
RELEVANCE_THRESHOLD = float(os.getenv("RELEVANCE_THRESHOLD", 0.50))

# ==========================================================
# Project Paths
# ==========================================================

DATA_FOLDER = "data"

UPLOAD_FOLDER = "uploads"

VECTOR_DB = "vectorstore"

LOG_FOLDER = "logs"
