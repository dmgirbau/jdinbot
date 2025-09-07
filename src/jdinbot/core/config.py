# src/jdinbot/core/config.py
# Configuration management using pydantic-settings
# Loads settings from environment variables and a .env file
# Matches variables defined in docker-compose.yml and .env.example
# Ensure to include database configuration variables
# Requires pydantic-settings as per pyproject.toml

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ENV: str = "development"
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    TELEGRAM_TOKEN: str
    WEBHOOK_SECRET_PATH: str
    ADMIN_CHAT_ID: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
ENV = settings.ENV

"""
**Key Points**:
- Uses `pydantic-settings` to load environment variables from `.env`, matching your `docker-compose.yml` and `.env.example`.
- Defines all required variables, including `POSTGRES_*` for database connectivity.
- Exports `ENV` for use in `logging.py` to toggle between JSON and console output.
"""