from functools import lru_cache
from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict

from .routers import metrics


class Settings(BaseSettings):
    stac_url: str = "http://localhost:8080"
    env: str = "dev"

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
app = FastAPI(
    title="BioTableroSearch",
    description="Get metrics by predefined or custom (polygon) areas.",
    summary="Metrics for BioTablero Search module",
    version="0.1.0",
    contact={
        "name": "Equipo BioTablero",
        "url": "http://biotablero.humboldt.org.co/",
        "email": "biotablero@humboldt.org.co",
    },
    docs_url=None if settings.env.lower() == "prod" else "/docs",
)


app.include_router(metrics.router)
# TODO: disable swagger on production: https://fastapi.tiangolo.com/tutorial/metadata/#docs-urls
