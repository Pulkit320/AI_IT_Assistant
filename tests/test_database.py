"""
Unit tests for database initialization, models, and mock data seeder.
"""

import pytest
from sqlalchemy import select
from backend.database.connection import engine, AsyncSessionLocal
from backend.database.init_db import init_db, seed_data
from backend.models import Base, User, Ticket


@pytest.mark.asyncio
async def test_database_init_and_seed():
    """Verify tables are created and seeded correctly."""
    await init_db()
    await seed_data()

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.employee_id == "EMP-1001"))
        user = result.scalar_one_or_none()
        assert user is not None
        assert user.full_name == "Sarah Jenkins"
        assert user.email == "sarah.jenkins@company.com"

        ticket_result = await session.execute(select(Ticket).where(Ticket.employee_id == "EMP-1001"))
        ticket = ticket_result.scalar_one_or_none()
        assert ticket is not None
        assert ticket.ticket_number == "IT-8091"
