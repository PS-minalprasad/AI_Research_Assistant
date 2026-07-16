"""
RAG Pipeline
"""

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

        docs = self.retriever.search(question)

        context = "\n\n".join(
            doc.page_content
            for doc in docs
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

        return {
            "answer": response.content,
            "sources": [
                {
                    "source": doc.metadata.get("source", "Unknown"),
                    "page": doc.metadata.get("page", "N/A")
                }
                for doc in docs
            ],
            "response_time": round(end_time - start_time, 2)
        }