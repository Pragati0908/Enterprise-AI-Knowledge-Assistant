from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Application
    APP_NAME: str = "Enterprise AI Knowledge Assistant"
    VERSION: str = "1.0.0"

    # Debug / API
    DEBUG: bool = False
    API_PREFIX: str = "/api"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Authentication
    # This is only a safe fallback for local/CI testing.
    # Production should provide SECRET_KEY through an environment variable.
    SECRET_KEY: str = "ci-development-secret-key-change-in-production"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Upload configuration
    MAX_UPLOAD_SIZE: int = 10485760

    ALLOWED_EXTENSIONS: str = "pdf,docx,pptx,xlsx"

    # Logging
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
