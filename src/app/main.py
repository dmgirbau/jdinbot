# app/main.py

# uvicorn app.main:app
# --host 0.0.0.0 --port 8000

"""
FastAPI + aiogram starter for JDINBot.
- Webhook when PUBLIC_BASE_URL is set, otherwise polling.
- Minimal handlers (/start, /help).
- Health endpoint and graceful startup/shutdown.

Why certain choices:
- Secret path for webhook reduces unsolicited hits without coupling to Telegram secret_token.
- Polling fallback keeps local dev simple.
- Single file for bootstrap; larger repos should move Settings/routers to modules.
"""
from __future__ import annotations

import asyncio
import logging
import os
from contextlib import asynccontextmanager
from typing import Optional
from enum import Enum

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, Update
from aiogram.client.default import DefaultBotProperties

# ----------------------------
# Settings
# ----------------------------
class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"

class Settings(BaseModel):
    telegram_token: str = Field(..., alias="TELEGRAM_TOKEN", description="Telegram Bot API Token")
    public_base_url: Optional[str] = Field(None, alias="PUBLIC_BASE_URL", description="Public URL for webhook")
    webhook_secret_path: str = Field("telegram-webhook", alias="WEBHOOK_SECRET_PATH", description="Secret path for webhook")
    admin_chat_id: Optional[int] = Field(None, alias="ADMIN_CHAT_ID", description="Admin's Telegram chat ID")
    env: Environment = Field(
        Environment.DEVELOPMENT,
        alias="ENV",
        description="Environment (development/production)"
    )

    @classmethod
    def load(cls) -> "Settings":
        try:
            return cls.model_validate({k: v for k, v in os.environ.items()})
        except ValidationError as e:
            raise RuntimeError(f"Invalid configuration: {e}")


settings = Settings.load()

# ----------------------------
# Logging
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger("jdinbot.main")

# ----------------------------
# aiogram wiring
# ----------------------------

bot = Bot(
    token=settings.telegram_token, 
    default=DefaultBotProperties(parse_mode="HTML")
)

dp = Dispatcher()
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "👋 Welcome to <b>JDINBot</b>\n\n"
        "Use /help to see available commands."
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        "Available commands:\n"
        "• /start — welcome\n"
        "• /help — this help"
    )


# Register router to dispatcher
dp.include_router(router)

# ----------------------------
# FastAPI app
# ----------------------------
class HealthOut(BaseModel):
    status: str
    mode: str
    webhook: bool


async def start_webhook(app: FastAPI) -> None:
    if not settings.public_base_url:
        return
    url = settings.public_base_url.rstrip("/") + f"/webhook/{settings.webhook_secret_path}"
    await bot.set_webhook(url=url)
    log.info("Webhook set: %s", url)


async def stop_webhook(app: FastAPI) -> None:
    if not settings.public_base_url:
        return
    await bot.delete_webhook(drop_pending_updates=True)
    log.info("Webhook deleted")


_polling_task: Optional[asyncio.Task] = None


async def start_polling(app: FastAPI) -> None:
    global _polling_task
    if settings.public_base_url:
        return

    async def _poll() -> None:
        log.info("Starting polling mode…")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

    _polling_task = asyncio.create_task(_poll())


async def stop_polling(app: FastAPI) -> None:
    global _polling_task
    if _polling_task and not _polling_task.done():
        _polling_task.cancel()
        try:
            await _polling_task
        except asyncio.CancelledError:
            pass
        log.info("Polling stopped")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    if settings.public_base_url:
        await start_webhook(app)
    else:
        await start_polling(app)
    yield
    # Shutdown
    if settings.public_base_url:
        await stop_webhook(app)
    else:
        await stop_polling(app)
    await bot.session.close()


app = FastAPI(title="JDINBot", version="0.1.0", lifespan=lifespan)


@app.get("/health", response_model=HealthOut)
async def health() -> HealthOut:
    return HealthOut(
        status="ok",
        mode="webhook" if settings.public_base_url else "polling",
        webhook=bool(settings.public_base_url),
    )


@app.post(f"/webhook/{{secret}}")
async def telegram_update(secret: str, request: Request):
    if not settings.public_base_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if secret != settings.webhook_secret_path:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid secret")

    data = await request.json()
    try:
        update = Update.model_validate(data)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    await dp.feed_update(bot, update)
    return JSONResponse({"ok": True})


# Optional root for sanity
@app.get("/")
async def root():
    return {"name": "JDINBot", "mode": "webhook" if settings.public_base_url else "polling"}


if __name__ == "__main__":
    import uvicorn

    # Dev convenience: `python -m app.main`
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENV", "development") == "development",
    )
