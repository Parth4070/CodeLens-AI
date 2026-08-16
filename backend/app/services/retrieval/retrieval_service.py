from app.services.embeddings.huggingface_embedding import HuggingFaceEmbeddingsService
from app.services.vectorstore.qdrant_service import QdrantService
from app.models.retrieval import RetrievedChunk

class RetrievalService:
    def __init__(self):
        self.embedding_service = HuggingFaceEmbeddingsService()
        self.qdrant_service = QdrantService()

    def search(self, query: str, limit: int = 5) -> list[RetrievedChunk]:
        query_vector = self.embedding_service.embed_query(query)

        results = self.qdrant_service.client.query_points(
            collection_name=self.qdrant_service.collection_name,
            query=query_vector,
            using="content",
            limit=limit,
            with_payload=True,
        ).points

        retrieved_chunks = []
        
        for result in results:
            payload = result.payload

            retrieved_chunk = RetrievedChunk(
                content=payload["content"],
                file_path=payload["file_path"],
                chunk_type=payload["chunk_type"],
                class_name=payload.get("class_name"),
                function_name=payload.get("function_name"),
                start_line=payload.get("start_line"),
                end_line=payload.get("end_line"),
                score=result.score,
            )

            retrieved_chunks.append(retrieved_chunk)
        
        return retrieved_chunks