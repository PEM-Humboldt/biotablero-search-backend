from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from logging import basicConfig, INFO

load_dotenv()


class Settings(BaseSettings):
    stac_url: str = "http://localhost:8080"
    env: str = "dev"
    secret_key: str = ""
    algorithm: str = ""
    access_token_expire_minutes: int = 30
    user_username: str = ""
    user_hashed_password: str = ""

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
