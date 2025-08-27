from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
TELEGRAM_TOKEN: str = Field(..., description="Telegram bot token")
ENV: str = Field("development", description="Environment: development/production")
PUBLIC_BASE_URL: Optional[str] = None
WEBHOOK_SECRET_PATH: str = Field("telegram-webhook", description="Webhook secret path")
ADMIN_CHAT_ID: Optional[int] = None


class Config:
env_file = ".env"


settings = Settings()