"""
Embedding Service
Creates embeddings using Ollama.
"""

from langchain_ollama import OllamaEmbeddings

from config import EMBEDDING_MODEL


class EmbeddingService:

    def __init__(self):

        self.embeddings = OllamaEmbeddings(
            model=EMBEDDING_MODEL
        )

    def get_embeddings(self):

        return self.embeddings