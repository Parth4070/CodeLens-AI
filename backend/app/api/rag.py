from fastapi import APIRouter

from app.models.ask import AskRequest
from app.models.rag import RAGResponse
from app.services.rag.rag_service import RAGService

router = APIRouter(prefix="/rag", tags=["rag"])

_rag_service: RAGService | None = None


def get_rag_service() -> RAGService:
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service


@router.post("/ask", response_model=RAGResponse)
async def ask(request: AskRequest):
    service = get_rag_service()
    return service.ask(repo_id=request.repo_id, question=request.question, top_k=request.top_k)

