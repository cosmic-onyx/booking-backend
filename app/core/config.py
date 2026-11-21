import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


PROJECT_ROOT_PATH = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL")

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT_PATH / '.env',
        extra='allow'
    )


settings = Settings()
