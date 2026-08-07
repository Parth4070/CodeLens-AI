from fastapi import FastAPI
from app.api.router import router
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

app.include_router(router)