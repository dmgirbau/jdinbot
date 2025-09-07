# src/jdinbot/api/v1/endpoints/health.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from jdinbot.db.session import get_db
from jdinbot.core.config import settings

router = APIRouter()

@router.get(
    "/health",
    summary="Health check endpoint",
    description="Returns the health status of the API and database connectivity.",
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
async def health_check(db: AsyncSession = Depends(get_db)) -> dict:
    """Check the health of the API and database connection."""
    health_status = {"status": "healthy", "api": "ok"}

    if settings.ENV != "development":
        # In production, verify database connection
        try:
            await db.execute("SELECT 1")
            health_status["database"] = "ok"
        except Exception as e:
            health_status["status"] = "unhealthy"
            health_status["database"] = f"error: {str(e)}"

    return health_status