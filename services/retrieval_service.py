"""
Retrieval Service
Loads FAISS and performs similarity search.
"""

from langchain_community.vectorstores import FAISS

from config import (
    VECTOR_DB,
    TOP_K,
)

from services.embedding_service import EmbeddingService


class RetrievalService:

    def __init__(self):

        embeddings = EmbeddingService().get_embeddings()

        self.db = FAISS.load_local(
            VECTOR_DB,
            embeddings,
            allow_dangerous_deserialization=True
        )

    def search(self, question):

        return self.db.similarity_search(
            question,
            k=TOP_K
        )