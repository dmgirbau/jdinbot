from datetime import datetime
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from jdinbot.db.models.user import User

@pytest.mark.asyncio
async def test_user_model(session: AsyncSession) -> None:
    # Create a user instance
    user = User(
        telegram_id=123456789,
        username="testuser",
        first_name="Test",
        last_name="User",
        balance=100
    )

    # Add and commit to the database
    session.add(user)
    await session.commit()

    # Refresh to ensure data was saved
    await session.refresh(user)

    # Verify attributes
    assert user.id is not None
    assert user.telegram_id == 123456789
    assert user.username == "testuser"
    assert user.first_name == "Test"
    assert user.last_name == "User"
    assert user.balance == 100
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)
    assert str(user) == "<User(telegram_id=123456789, username=testuser)>"

    # Test updating a field
    user.balance = 200
    session.add(user)
    await session.commit()
    await session.refresh(user)
    assert user.balance == 200
    assert user.updated_at >= user.created_at