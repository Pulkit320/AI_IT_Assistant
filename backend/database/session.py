"""
FastAPI Database Session Dependency Generator.
Provides an isolated async session for route handlers with auto-close logic.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.connection import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency yielding an async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
