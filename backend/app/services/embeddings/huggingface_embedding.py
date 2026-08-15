# pyrefly: ignore [missing-import]
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

from app.services.embeddings.base_embedding import BaseEmbeddingService

class HuggingFaceEmbeddingsService(BaseEmbeddingService):
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        self.embedding_model = HuggingFaceEmbeddings(model_name= model_name)

    def embed_docs(self, docs: list[Document]) -> list[list[float]]:
        texts = [document.page_content for document in docs]
        return self.embedding_model.embed_documents(texts)

    def embed_query(self, query: str) -> list[float]:
        return self.embedding_model.embed_query(query)