from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):

    APP_NAME: str
    VERSION: str

    DEBUG: bool

    API_PREFIX: str

    HOST: str

    PORT: int

    SECRET_KEY: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int

    MAX_UPLOAD_SIZE: int

    ALLOWED_EXTENSIONS: str

    LOG_LEVEL: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():

    return Settings()


settings = get_settings()