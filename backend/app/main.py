from fastapi import FastAPI
from app.api.router import router
from app.config.settings import settings
from app.utils.logger import logger
from dotenv import load_dotenv

load_dotenv()

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


if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)