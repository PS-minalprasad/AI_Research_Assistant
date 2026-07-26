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

        # Retrieve relevant documents
        docs = self.retriever.search(question)

        # If no relevant documents are found
        if not docs:
            return {
                "answer": "I could not find this information in the uploaded documents.",
                "sources": [],
                "response_time": round(time.time() - start_time, 2)
            }

        # Build context while removing duplicate chunks
        context_parts = []
        seen_chunks = set()

        for doc in docs:
            content = doc.page_content.strip()

            if content not in seen_chunks:
                seen_chunks.add(content)
                context_parts.append(content)

        context = "\n\n".join(context_parts)

        # Build prompt
        prompt = f"""
{SYSTEM_PROMPT}

Retrieved Context:

{context}

Question:
{question}

Answer:
"""

        # Generate response
        response = self.llm.generate(prompt)

        end_time = time.time()

        # Collect unique sources
        unique_sources = []
        seen_sources = set()

        for doc in docs:

            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", 0)

            try:
                page = int(page) + 1
            except Exception:
                page = "N/A"

            source_key = (source, page)

            if source_key not in seen_sources:
                seen_sources.add(source_key)

                unique_sources.append({
                    "source": source,
                    "page": page
                })

        return {
            "answer": response.content.strip(),
            "sources": unique_sources,
            "response_time": round(end_time - start_time, 2)
        }

