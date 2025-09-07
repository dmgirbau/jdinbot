# src/jdinbot/main.py
# Entry point for the FastAPI application
# Integrates database initialization with structured logging

from fastapi import FastAPI
import asyncio


from jdinbot.db.engine import init_db_engine
from jdinbot.core.logging import get_logger
from jdinbot.api.v1 import routers
from jdinbot.core.config import settings

logger = get_logger(__name__)

jdinbot = FastAPI(
    title="JDINBot API",
    description="API for JDINBot, a high-performance Telegram bot.",
    version="0.1.0",
)

jdinbot.include_router(routers.router)

def main():
    import uvicorn
    uvicorn.run(
        jdinbot,
        host="0.0.0.0",
        port=8000,
        reload=settings.ENV == "development",
        workers=4 if settings.ENV == "production" else 1,
    )

@jdinbot.on_event("startup")
async def startup_event():
    """Initialize application dependencies on startup."""
    try:
        # Initialize database engine
        engine = await init_db_engine()
        logger.info("Application startup completed", component="fastapi")
        # Store engine in app state or dependency system if needed
        jdinbot.state.db_engine = engine
    except Exception as e:
        logger.error(
            "Application startup failed",
            component="fastapi",
            error=str(e),
            exc_info=True,
        )
        raise

@jdinbot.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    if hasattr(jdinbot.state, "db_engine"):
        await jdinbot.state.db_engine.dispose()
        logger.info("Database engine disposed", component="fastapi")

# Example route to verify API
@jdinbot.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    main()

"""
**Key Points**:
- Initializes the database engine during the FastAPI `startup` event using `init_db_engine`.
- Logs successful startup and any failures with `structlog`, including the component (`fastapi`) for context.
- Stores the engine in `jdinbot.state.db_engine` for use by other parts of the application (e.g., `src/jdinbot/db/session.py`).
- Cleans up the engine on shutdown to prevent resource leaks.
- Uses `async` to align with your async-first architecture (e.g., `SQLAlchemy[asyncio]`, `asyncpg`).
"""