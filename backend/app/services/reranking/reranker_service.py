# pyrefly: ignore [missing-import]
from sentence_transformers import CrossEncoder
from app.models.retrieval import RetrievedChunk

class RerankerService:
    def __init__(self, model_name: str = "BAAI/bge-reranker-base"):
        self.model = CrossEncoder(model_name)


    def rerank(self, query: str, retrieved_chunks: list[RetrievedChunk], top_k: int=5) -> list[RetrievedChunk]:
        if not retrieved_chunks:
            return []
        
        pairs = [(query, chunk.content) for chunk in retrieved_chunks]
        scores = self.model.predict(pairs)

        ranked_chunks = []

        for chunk, score in zip(retrieved_chunks, scores):
            chunk.rerank_score = float(score)
            ranked_chunks.append(chunk)
        
        ranked_chunks.sort(key=lambda chunk: chunk.rerank_score, reverse=True)
        
        return ranked_chunks[:top_k]

