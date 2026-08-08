"""
Database Connection & Engine Factory.
Provides asynchronous engine creation for SQLite / PostgreSQL.
"""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from backend.config import settings

# Clean database URL (stripping trailing newlines or whitespace)
db_url = settings.DATABASE_URL.strip()

# Create Async Engine
engine = create_async_engine(
    db_url,
    echo=settings.DEBUG,
    future=True,
)


# Async Session Factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)
