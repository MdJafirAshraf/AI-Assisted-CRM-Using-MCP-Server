from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App Info
    APP_NAME: str = "CRM Hub"
    ENVIRONMENT: str = Field(default="development", pattern="^(development|staging|production)$")

    # Security
    JWT_SECRET_KEY: str = Field(
        default="crm-hub-super-secret-key-change-me",
        description="Secret key for signing JWT tokens",
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Database
    DATABASE_URL: str = "sqlite:///./crm.db"

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # LLM
    GROQ_API_KEY: str = Field(default="", description="API key for GROQ LLM service")

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance.
    Prevents reloading env variables multiple times.
    """
    return Settings()