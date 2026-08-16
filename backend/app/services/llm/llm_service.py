# pyrefly: ignore [missing-import]
from langchain_ollama import ChatOllama

class LLMService:
    def __init__(self, model_name:str = "llama3.2"):
        self.llm = ChatOllama(model=model_name, temperature=0)
    
    def generate(self, prompt: str) -> str:
        response  = self.llm.invoke(prompt)

        return response.content