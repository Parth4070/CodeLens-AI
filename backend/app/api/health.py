from fastapi import APIRouter
from app.utils.logger import logger

router = APIRouter()

@router.get("/health", tags = ["Health"])
async def health():
    logger.info("Health check endpoint called")
    
    return {
        "status": "healthy"
    }