from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class APISettings(BaseSettings):
    debug_status: bool = True
    debug_exception: bool = True
    disable_superuser_dependency: bool = False
    include_admin_route: bool = True

    title: str = 'Online-BookStore'
    description: str = 'Description'
    version: str = '1.0'
    doc_url: str = '/swagger'
    redoc_url: str = '/redoc'


class Settings(BaseSettings):
    DEBUG: str
    CLIENT_ORIGIN: str
    ES_HOST: str
    ELASTICSEARCH_URL: str
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = 'app/.env'


settings = Settings()


@lru_cache()
def get_api_settings() -> APISettings:
    return APISettings()
