import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import OperationalError

from jdinbot.db.session import get_db
from jdinbot.db.engine import init_db_engine
from jdinbot.core.config import settings


@pytest.mark.asyncio
async def test_database_connection():
    async with get_db() as session:
        assert isinstance(session, AsyncSession)
        result = await session.execute("SELECT 1")
        assert result.scalar() == 1
   
@pytest.mark.asyncio
async def test_database_connection_failure(monkeypatch):
    # Simulate wrong password
    monkeypatch.setattr(settings, "POSTGRES_PASSWORD", "wrong")
    with pytest.raises(OperationalError):
        await init_db_engine()