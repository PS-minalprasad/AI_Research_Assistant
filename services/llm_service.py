"""
LLM Service

Loads the Ollama language model used for answer generation.
"""

from langchain_ollama import ChatOllama

from config import LLM_MODEL


class LLMService:

    def __init__(self):

        self.llm = ChatOllama(
            model=LLM_MODEL,
            temperature=0.0,      # Deterministic answers
            num_predict=768,      # Allow longer answers
            top_p=0.9,
            repeat_penalty=1.1
        )

    def generate(self, prompt):

        return self.llm.invoke(prompt)
