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
            self.db = None
            return

        # Load local FAISS vector database
        self.db = FAISS.load_local(
            VECTOR_DB,
            embeddings,
            allow_dangerous_deserialization=True
        )

    def search(self, question):

        # Handle missing vector database
        if self.db is None:
            return []

        # Retrieve top matching chunks
        results = self.db.similarity_search_with_relevance_scores(
            question,
            k=TOP_K
        )

        # Lower threshold to improve recall
        RELEVANCE_THRESHOLD = 0.50

        filtered_docs = []

        print("\nRetrieved Chunks:\n")

        for doc, score in results:

            print(
                f"Score: {score:.3f} | "
                f"Page: {doc.metadata.get('page', 'N/A')} | "
                f"Source: {doc.metadata.get('source', 'Unknown')}"
            )

            if score >= RELEVANCE_THRESHOLD:
                filtered_docs.append(doc)

        # Fallback: return top 3 documents if threshold filters everything
        if not filtered_docs:
            print("\nNo chunks met the threshold. Using top 3 retrieved chunks.\n")
            filtered_docs = [doc for doc, score in results[:3]]

        return filtered_docs
