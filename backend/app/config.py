import os
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    LLM_PROVIDER: str = "groq"
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = "openai/gpt-oss-120b"
    LLM_TEMPERATURE: float = 0.1
    DATABASE_URL: str = "sqlite:///./adaptive_loop.db"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: str = "http://localhost:3000"
    FALLBACK_TO_MOCK: bool = False

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    class Config:
        env_file = (os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"), ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
