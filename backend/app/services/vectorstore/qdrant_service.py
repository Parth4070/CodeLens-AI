from qdrant_client.conversions.common_types import PointStruct
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import os
from dotenv import load_dotenv
from app.config.settings import settings

load_dotenv()

# pyrefly: ignore [missing-import]
from langchain_core.documents import Document

class QdrantService:
    def __init__(self, collection_name: str = 'codelens'):
        self.collection_name = collection_name
        qdrant_url = os.getenv("QDRANT_URL") or settings.QDRANT_URL
        qdrant_api_key = os.getenv("QDRANT_API_KEY") or settings.QDRANT_API_KEY
        self.client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key or None,
        )
    
    def create_collection(self, vector_size: int):
        collections = self.client.get_collections()
        existing_collections = [collection.name for collection in collections.collections]

        if self.collection_name not in existing_collections:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config={
                    "content": VectorParams(
                        size=vector_size,
                        distance=Distance.COSINE,
                    )
                },
            )

        self._ensure_payload_indices()

    def _ensure_payload_indices(self):
        try:
            from qdrant_client.models import PayloadSchemaType
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="repo_id",
                field_schema=PayloadSchemaType.KEYWORD,
            )
        except Exception:
            pass
    
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