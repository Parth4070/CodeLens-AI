from fastapi import APIRouter
from app.utils.logger import logger
from app.api.health import router as health_router
from app.api.github import router as github_router
from app.api.rag import router as rag_router

router = APIRouter()

router.include_router(health_router)
router.include_router(github_router)
router.include_router(rag_router)