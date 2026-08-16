from qdrant_client.conversions.common_types import PointStruct
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# pyrefly: ignore [missing-import]
from langchain_core.documents import Document

class QdrantService:
    def __init__(self, collection_name: str = 'codelens'):
        self.collection_name = collection_name
        self.client = QdrantClient(url="http://localhost:6333")

    
    def create_collection(self, vector_size:int):
        collections = self.client.get_collections()

        existing_collections = [collection.name for collection in collections.collections]

        if self.collection_name in existing_collections:
            return
        
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config={
                "content": VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                )
            },
        )
    
    def add_docs(self, documents: list[Document], embeddings: list[list[float]]):
        if len(documents) != len(embeddings):
            raise ValueError("Number of documents must match numeber of embeddings.")\
        
        points = []

        for document, embedding in zip(documents, embeddings):
            point = PointStruct(
                id=document.metadata["chunk_id"],
                vector={
                    "content": embedding
                },
                payload={
                    "content": document.page_content,
                    **document.metadata,
    },
)
            points.append(point)

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )