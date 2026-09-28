from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "CodeLens AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    LLM_PROVIDER: str = "ollama"
    LLM_MODEL: str = "llama3.2"

    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str | None = None

    GROQ_API_KEY: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="forbid"
    )


settings = Settings()   