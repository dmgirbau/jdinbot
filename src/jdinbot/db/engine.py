from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from jdinbot.core.config import settings


DATABASE_URL = (
f"postgresql+asyncpg://jdin:jdin@postgres:5432/jdin"
) # TODO: build dynamically from settings


engine = create_async_engine(DATABASE_URL, echo=False, future=True)


AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncSession:
async with AsyncSessionLocal() as session:
yield session