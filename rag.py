

import time

from services.retrieval_service import RetrievalService
from services.llm_service import LLMService
from prompts import SYSTEM_PROMPT


class RAGPipeline:

    def __init__(self):
        self.retriever = RetrievalService()
        self.llm = LLMService()

    def ask(self, question):

        start_time = time.time()

        # Retrieve relevant documents
        docs = self.retriever.search(question)

        # If nothing relevant is retrieved, don't call the LLM
        if not docs:
            return {
                "answer": "I couldn't find enough relevant information in the uploaded documents to answer your question.",
                "sources": [],
                "response_time": round(time.time() - start_time, 2)
            }

        context = "\n\n".join(
            doc.page_content for doc in docs
        )

        prompt = f"""
{SYSTEM_PROMPT}

Context:
{context}

Question:
{question}

Answer:
"""

        response = self.llm.generate(prompt)

        end_time = time.time()

        # Remove duplicate sources
        unique_sources = []

        for doc in docs:
            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", "N/A")

            source_data = {
                "source": source,
                "page": page
            }

            if source_data not in unique_sources:
                unique_sources.append(source_data)

        return {
            "answer": response.content,
            "sources": unique_sources,
            "response_time": round(end_time - start_time, 2)
        }
