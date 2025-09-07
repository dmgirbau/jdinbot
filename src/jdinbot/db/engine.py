# src/jdinbot/db/engine.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.exc import OperationalError
from jdinbot.core.config import settings  # Assuming settings contains DB config
from jdinbot.core.logging import get_logger

logger = get_logger(__name__)

async def init_db_engine() -> AsyncEngine:
    """Initialize the async SQLAlchemy engine with error logging."""
    db_url = (
        f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
        f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    )
    try:
        engine = create_async_engine(db_url, echo=False, future=True)
        # Test connection
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        logger.info(
            "Database connection established",
            db_host=settings.POSTGRES_HOST,
            db_port=settings.POSTGRES_PORT,
            db_name=settings.POSTGRES_DB,
        )
        return engine
    except OperationalError as e:
        logger.error(
            "Failed to connect to database",
            db_host=settings.POSTGRES_HOST,
            db_port=settings.POSTGRES_PORT,
            db_name=settings.POSTGRES_DB,
            error=str(e),
            exc_info=True,
        )
        raise
    except Exception as e:
        logger.error(
            "Unexpected error during database initialization",
            db_host=settings.POSTGRES_HOST,
            db_port=settings.POSTGRES_PORT,
            db_name=settings.POSTGRES_DB,
            error=str(e),
            exc_info=True,
        )
        raise

"""
**Key Points**:
- Uses `get_logger` from `src/jdinbot/core/logging.py` to create a logger for the module.
- Logs successful connections with `logger.info`, including context like `db_host`, `db_port`, and `db_name`.
- Catches `OperationalError` (common for database connectivity issues, e.g., wrong credentials or unreachable host) and logs it with `logger.error`, including the error message and stack trace (`exc_info=True`).
- Catches unexpected errors for robustness, logging them with context.
- Assumes `settings` from `src/jdinbot/core/config.py` provides database configuration (e.g., `POSTGRES_USER`, `POSTGRES_PASSWORD`, etc.) via `pydantic-settings`.
- Tests the connection with a simple `SELECT 1` query to ensure the database is ready.
"""