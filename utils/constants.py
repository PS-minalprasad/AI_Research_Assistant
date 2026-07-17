"""
Application Constants
"""

APP_NAME = "AI Research Assistant"

VERSION = "1.0.0"

UPLOAD_FOLDER = "uploads"

DATA_FOLDER = "data"

VECTORSTORE_FOLDER = "vectorstore"

LOG_FOLDER = "logs"

SUPPORTED_EXTENSIONS = [".pdf"]

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

WELCOME_MESSAGE = """
👋 Welcome to AI Research Assistant!

Upload one or more PDF documents and ask questions.
The assistant will answer using Retrieval-Augmented Generation (RAG).
"""

NO_DOCUMENT_MESSAGE = (
    "Please upload at least one PDF."
)

NOT_FOUND_MESSAGE = (
    "I could not find this information in the uploaded documents."
)