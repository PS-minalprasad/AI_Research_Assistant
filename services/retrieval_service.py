"""
Retrieval Service
Loads FAISS vector database and performs similarity search.
"""

import os

from langchain_community.vectorstores import FAISS

from config import (
    VECTOR_DB,
    TOP_K,
)

from services.embedding_service import EmbeddingService


class RetrievalService:

    def __init__(self):

        embeddings = EmbeddingService().get_embeddings()

        # Check whether the FAISS index exists
        if not os.path.exists(VECTOR_DB):
            # Application can start without vectorstore.
            # User needs to run ingest.py before performing search.
            self.db = None
            return

        # Vectorstore is generated locally through ingest.py
        # and loaded only from a trusted local source.
        self.db = FAISS.load_local(
            VECTOR_DB,
            embeddings,
            allow_dangerous_deserialization=True
        )

    def search(self, question):

        # Handle missing vector database gracefully
        if self.db is None:
            return []

        # Retrieve documents with relevance scores
        results = self.db.similarity_search_with_relevance_scores(
            question,
            k=TOP_K
        )

        # Keep only relevant documents
        RELEVANCE_THRESHOLD = 0.70

        filtered_docs = [
            doc
            for doc, score in results
            if score >= RELEVANCE_THRESHOLD
        ]

        return filtered_docs
