from fastapi import FastAPI

from app.config.settings import settings
from app.utils.logger import logger

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to CodeLens AI"
    }


@app.get("/health")
async def health():
    logger.info("Health check endpoint called")

    return {
        "status": "healthy"
    }