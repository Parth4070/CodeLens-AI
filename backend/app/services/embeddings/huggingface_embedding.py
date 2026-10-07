from typing import Optional
# pyrefly: ignore [missing-import]
from langchain_core.documents import Document
from app.services.embeddings.base_embedding import BaseEmbeddingService

class HuggingFaceEmbeddingsService(BaseEmbeddingService):
    _shared_model = None

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        self.model_name = model_name

    @property
    def embedding_model(self):
        if HuggingFaceEmbeddingsService._shared_model is None:
            from fastembed import TextEmbedding
            HuggingFaceEmbeddingsService._shared_model = TextEmbedding(model_name=self.model_name)
        return HuggingFaceEmbeddingsService._shared_model

    def embed_docs(self, docs: list[Document]) -> list[list[float]]:
        texts = [document.page_content for document in docs]
        if not texts:
            return []
        embeddings = list(self.embedding_model.embed(texts))
        return [e.tolist() if hasattr(e, "tolist") else list(e) for e in embeddings]

    def embed_query(self, query: str) -> list[float]:
        embeddings = list(self.embedding_model.embed([query]))
        vector = embeddings[0]
        return vector.tolist() if hasattr(vector, "tolist") else list(vector)