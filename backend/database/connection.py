"""
Database Connection & Engine Factory.
Provides asynchronous engine creation for SQLite / PostgreSQL.
"""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from backend.config import settings

# Clean database URL (stripping trailing newlines or whitespace)
db_url = settings.DATABASE_URL.strip()

connect_args = {}
if "postgresql" in db_url:
    connect_args = {
        "statement_cache_size": 0,
        "prepared_statement_cache_size": 0,
    }

# Create Async Engine
engine = create_async_engine(
    db_url,
    echo=settings.DEBUG,
    future=True,
    connect_args=connect_args,
)



# Async Session Factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)
