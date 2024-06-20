from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from logging import basicConfig, INFO


class Settings(BaseSettings):

    stac_url: str = "http://localhost:8082"
    env: str = "dev"

    model_config = SettingsConfigDict(env_file=".env")

    def configure_logging(self):
        basicConfig(
            level=INFO,
            filename="app/logs/app.log",
            format="%(asctime)s.%(msecs)03d %(levelname)s - %(name)s - %(module)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )


@lru_cache
def get_settings():
    return Settings()
