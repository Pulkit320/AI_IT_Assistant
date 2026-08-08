"""
Configuration Management Module.
Loads environment variables safely using Pydantic Settings.
"""

from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Voice IT Helpdesk Agent"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./helpdesk.db"

    # Security / JWT Authentication
    SECRET_KEY: str = "super-secret-development-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # LLM Settings
    OPENAI_API_KEY: str = ""
    USE_MOCK_LLM: bool = True

    # ElevenLabs Webhook Settings
    ELEVENLABS_API_KEY: str = ""
    ELEVENLABS_AGENT_ID: str = ""
    ELEVENLABS_WEBHOOK_SECRET: str = "sample-webhook-secret-key"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
