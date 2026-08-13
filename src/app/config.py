"""
src/app/config.py

Single source of truth for all configuration. Every environment variable
this app reads is declared here, with a type. pydantic-settings reads
.env automatically, coerces types, and raises a clear validation error
at STARTUP if something required is missing or malformed — never buried
mid-request.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "development"
    log_level: str = "INFO"

    database_url: str
    redis_url: str
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30

    fernet_key: str

    meta_app_id: str = ""
    meta_app_secret: str = ""
    meta_webhook_verify_token: str = ""


@lru_cache
def get_settings() -> Settings:
    """
    Cached so .env is parsed and validated exactly once per process,
    not once per request. Every module that needs config calls this
    function rather than constructing Settings() directly.
    """
    return Settings()