from fastapi import APIRouter

from app.models.ask import AskRequest
from app.models.rag import RAGResponse
from app.services.rag.rag_service import RAGService

router  = APIRouter(prefix="/rag", tags=["rag"])

rag_service = RAGService()

@router.post("/ask", response_model=RAGResponse)
async def ask(request: AskRequest):
    return rag_service.ask(request.question, request.top_k)
