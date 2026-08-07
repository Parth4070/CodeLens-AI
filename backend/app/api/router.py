from fastapi import APIRouter
from app.utils.logger import logger
from app.api.health import router as health_router

router = APIRouter()

router.include_router(health_router)