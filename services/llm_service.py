"""
LLM Service
Loads Ollama model.
"""

from langchain_ollama import ChatOllama

from config import LLM_MODEL


class LLMService:

    def __init__(self):

        self.llm = ChatOllama(
            model=LLM_MODEL,
            temperature=0,
            num_predict=512
        )

    def generate(self, prompt):

        return self.llm.invoke(prompt)