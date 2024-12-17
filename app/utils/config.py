from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from logging import basicConfig, INFO
from tortoise import Tortoise


class Settings(BaseSettings):

    stac_url: str = "http://localhost:8080"
    env: str = "dev"
    cors_origin: str = ""
    db_user: str = ""
    db_password: str = ""
    db_host: str = ""
    db_port: int
    db_name: str = ""

    tortoise_models: List[str] = [
        "app.models.models",
        "aerich.models",
    ]  # Ajusta según la ruta de tus modelos

    @property
    def db_url(self) -> str:
        return f"postgres://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    model_config = SettingsConfigDict(env_file=".env")

    def configure_logging(self):
        basicConfig(
            level=INFO,
            filename="logs/app.log",
            format="%(asctime)s.%(msecs)03d %(levelname)s - %(request_id)s - %(name)s - %(module)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )


@lru_cache
def get_settings():
    return Settings()


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
    await Tortoise.generate_schemas()
