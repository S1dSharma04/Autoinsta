"""
src/app/infrastructure/db/base.py

The declarative base every ORM model inherits from, and the async
engine/session factory the whole app shares.
"""
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings


class Base(DeclarativeBase):
    """Every ORM model (User, Workflow, ...) inherits from this."""
    pass


settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    pool_size=5,
    max_overflow=10,
    echo=(settings.environment == "development"),
)

async_session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    """
    FastAPI dependency. Yields one session per request, always closed
    via try/finally even if the request raises.
    """
    async with async_session_factory() as session:
        yield session