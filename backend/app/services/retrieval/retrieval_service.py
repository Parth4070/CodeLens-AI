from app.services.embeddings.huggingface_embedding import HuggingFaceEmbeddingsService
from app.services.vectorstore.qdrant_service import QdrantService

class RetrievalService:
    def __init__(self):
        self.embedding_service = HuggingFaceEmbeddingsService()
        self.qdrant_service = QdrantService()

    def search(self, query: str, limit: int = 5):
        query_vector = self.embedding_service.embed_query(query)

        results = self.qdrant_service.client.query_points(
            collection_name=self.qdrant_service.collection_name,
            query=query_vector,
            using="content",
            limit=limit,
            with_payload=True,
        ).points
        
        return results