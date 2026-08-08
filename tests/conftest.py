"""
Pytest Fixtures Configuration.
Provides Async HTTP Client fixture and auto-initialized test database.
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from backend.main import app
from backend.database.init_db import init_db, seed_data


@pytest_asyncio.fixture(autouse=True)
async def setup_test_db():
    """Auto-initializes and seeds test database before each test run."""
    await init_db()
    await seed_data()


@pytest_asyncio.fixture
async def async_client():
    """Provides an asynchronous HTTP client for testing FastAPI routes."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
