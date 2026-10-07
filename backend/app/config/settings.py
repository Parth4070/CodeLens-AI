from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
_ENV_FILES = (".env", str(_BACKEND_DIR / ".env"))


class Settings(BaseSettings):

    APP_NAME: str = "CodeLens AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    LLM_PROVIDER: str = "ollama"
    LLM_MODEL: str = "llama3.2"

    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str | None = None

    GROQ_API_KEY: str | None = None
    RERANKER_MODEL: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"

    model_config = SettingsConfigDict(
        env_file=_ENV_FILES,
        extra="ignore"
    )


settings = Settings()   