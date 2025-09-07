# tests/integration/test_api.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from jdinbot.main import jdinbot
from jdinbot.db.session import get_db
from jdinbot.core.config import settings

# Override settings for testing
settings.ENV = "development"

@pytest.mark.asyncio
async def test_health_endpoint():
    client = TestClient(jdinbot)
    
    # Mock database dependency for development mode (no DB check)
    async def mock_get_db():
        engine = create_async_engine("sqlite+aiosqlite:///:memory:")
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            yield session
    
    jdinbot.dependency_overrides[get_db] = mock_get_db
    
    response = client.get("/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "api": "ok"}
    
    # Clean up overrides
    jdinbot.dependency_overrides.clear()