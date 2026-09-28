import os

from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq


class LLMService:

    def __init__(self):

        provider = os.getenv(
            "LLM_PROVIDER",
            "ollama"
        )

        if provider == "groq":

            self.llm = ChatGroq(
                model=os.getenv(
                    "LLM_MODEL",
                    "openai/gpt-oss-20b"
                ),
                temperature=0,
                api_key=os.getenv("GROQ_API_KEY"),
            )

        else:

            self.llm = ChatOllama(
                model=os.getenv(
                    "LLM_MODEL",
                    "llama3.2"
                ),
                temperature=0,
            )

    def generate(self, prompt: str) -> str:

        response = self.llm.invoke(prompt)

        return response.content