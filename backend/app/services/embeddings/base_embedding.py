from abc import ABC, abstractmethod
# pyrefly: ignore [missing-import]
from langchain_core.documents import Document

class BaseEmbeddingService(ABC):
    @abstractmethod
    def embed_docs(self, docs: list[Document]) -> list[list[float]]:
        """
        Embed a list of documents into vector representations.
        """
        pass

    @abstractmethod
    def embed_query(self, query: str) -> list[float]:
        """
        Embed a query into a vector representation.
        """
        pass