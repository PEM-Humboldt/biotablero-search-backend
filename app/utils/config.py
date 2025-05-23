from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import logging
from logging import INFO, StreamHandler
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
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "bt-search"
    s3_bucket_name: str = "bt-search"
    s3_endpoint_url: str = "http://localhost:9000"
    storage_driver: str = "s3"
    connect_timeout: int = 5
    read_timeout: int = 10
    retry_max_attempts: int = 1
    retry_mode: str = "standard"

    @property
    def retry_config(self) -> dict:
        return {
            "max_attempts": self.retry_max_attempts,
            "mode": self.retry_mode,
        }

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
        formatter = logging.Formatter(
            "%(asctime)s.%(msecs)03d %(levelname)s - %(request_id)s - %(name)s - %(module)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        request_filter = RequestIdFilter()
        logger.addFilter(request_filter)

        file_handler = logging.FileHandler("logs/app.log")
        file_handler.setFormatter(formatter)
        file_handler.addFilter(request_filter)
        logger.addHandler(file_handler)

        stream_handler = StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        stream_handler.addFilter(request_filter)
        logger.addHandler(stream_handler)


class RequestIdFilter(logging.Filter):
    """
    Custom logging filter to ensure each log record contains a 'request_id'.
    If 'request_id' is not present, it sets it to "N/A".
    """

    def filter(self, record):
        if not hasattr(record, "request_id"):
            record.request_id = "N/A"
        return True


@lru_cache
def get_settings():
    return Settings()


TORTOISE_ORM = {
    "connections": {
        "default": get_settings().db_url,
    },
    "apps": {
        "bt_search_bk": {
            "models": get_settings().tortoise_models,
            "default_connection": "default",
        },
    },
}
