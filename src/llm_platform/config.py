"""Settings for the local stack. Defaults match docker-compose.yml; override with env vars."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="LLMP_", env_file=".env", extra="ignore")

    database_url: str = "postgresql://llm:llm@localhost:5433/llm_platform"
    langfuse_host: str = "http://localhost:3000"


def load_settings() -> Settings:
    return Settings()
