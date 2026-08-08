"""
Database Initializer & Mock Data Seeder Script.
Creates tables and seeds mock employees and tickets for local testing.
"""

import asyncio
from passlib.context import CryptContext
from sqlalchemy import select
from backend.database.connection import engine, AsyncSessionLocal
from backend.models import Base, User, Ticket, PasswordResetLog, SoftwareRequest, EscalationLog
from backend.logging_config import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def init_db(reset: bool = True):
    """Creates all database tables, optionally dropping existing ones first."""
    async with engine.begin() as conn:
        if reset:
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables initialized successfully.")



async def seed_data():
    """Seeds initial mock employees and tickets into database."""
    async with AsyncSessionLocal() as session:
        # Check if users already exist
        result = await session.execute(select(User))
        existing_users = result.scalars().all()
        if existing_users:
            logger.info("Mock database already seeded.")
            return

        # Seed Employees
        hashed_password = pwd_context.hash("Password123!")
        
        employees = [
            User(
                employee_id="EMP-1001",
                full_name="Sarah Jenkins",
                email="sarah.jenkins@company.com",
                password_hash=hashed_password,
                department="Engineering",
                role="Software Engineer",
                security_answer="Austin",
            ),
            User(
                employee_id="EMP-1002",
                full_name="Michael Chen",
                email="michael.chen@company.com",
                password_hash=hashed_password,
                department="Marketing",
                role="Marketing Specialist",
                security_answer="Seattle",
            ),
            User(
                employee_id="EMP-1003",
                full_name="Elena Rostova",
                email="elena.rostova@company.com",
                password_hash=hashed_password,
                department="Finance",
                role="Financial Analyst",
                security_answer="Chicago",
            ),
        ]
        session.add_all(employees)
        await session.commit()

        # Seed Sample IT Ticket
        ticket1 = Ticket(
            ticket_number="IT-8091",
            employee_id="EMP-1001",
            category="Software",
            priority="Medium",
            status="Pending Approval",
            subject="Docker Desktop License Entitlement",
            description="Employee requested Docker Desktop Pro for containerized local microservices development.",
            voice_summary="Ticket IT-8091 for Docker access is currently Pending Manager Approval.",
        )
        session.add(ticket1)
        await session.commit()

        logger.info("Mock database seeded with 3 users and 1 sample ticket.")


if __name__ == "__main__":
    asyncio.run(init_db())
    asyncio.run(seed_data())
