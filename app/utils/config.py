from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import logging
from logging import INFO, StreamHandler
from tortoise import Tortoise
from app.models.seed_area_types import seed_area_types
import sys


class Settings(BaseSettings):

    stac_url: str = "http://localhost:8080"
    env: str = "dev"
    cors_origin: str = ""
    db_user: str = ""
    db_password: str = ""
    db_host: str = "localhost"
    db_port: int = 5433
    db_name: str = ""

    tortoise_models: List[str] = [
        "app.models.models",
        "aerich.models",
    ]

    @property
    def db_url(self) -> str:
        return f"postgres://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    model_config = SettingsConfigDict(env_file=".env")

    def configure_logging(self):
        logger = logging.getLogger()
        logger.setLevel(INFO)

        # Formato de log
        formatter = logging.Formatter(
            "%(asctime)s.%(msecs)03d %(levelname)s - %(name)s - %(module)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        file_handler = logging.FileHandler("logs/app.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stream_handler = StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
settings.configure_logging()

TORTOISE_ORM = {
    "connections": {
        "default": get_settings().db_url,
    },
    "apps": {
        "models": {
            "models": get_settings().tortoise_models,
            "default_connection": "default",
        },
    },
}


async def init_tortoise():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)
    await seed_area_types()
