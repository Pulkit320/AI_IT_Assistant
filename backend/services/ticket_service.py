"""
Ticket Business Logic & Query Service.
"""

import random
from typing import Optional, List
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.ticket import Ticket
from backend.models.user import User
from backend.schemas.ticket import TicketCreate, TicketUpdate


class TicketService:
    """Service providing ticket CRUD operations and search logic."""

    @staticmethod
    def generate_ticket_number() -> str:
        """Generates a unique random ticket identifier (e.g., IT-8492)."""
        num = random.randint(1000, 9999)
        return f"IT-{num}"

    @staticmethod
    async def create_ticket(db: AsyncSession, payload: TicketCreate) -> Ticket:
        """Creates a new IT ticket entity."""
        ticket_number = TicketService.generate_ticket_number()
        
        # Verify ticket number uniqueness
        existing = await db.execute(select(Ticket).where(Ticket.ticket_number == ticket_number))
        while existing.scalar_one_or_none() is not None:
            ticket_number = TicketService.generate_ticket_number()
            existing = await db.execute(select(Ticket).where(Ticket.ticket_number == ticket_number))

        voice_summary = payload.voice_summary or (
            f"Ticket {ticket_number} created for {payload.subject}. Priority: {payload.priority}."
        )

        ticket = Ticket(
            ticket_number=ticket_number,
            employee_id=payload.employee_id,
            subject=payload.subject,
            description=payload.description,
            category=payload.category,
            priority=payload.priority,
            status="Open",
            voice_summary=voice_summary,
        )
        db.add(ticket)
        await db.commit()
        await db.refresh(ticket)
        return ticket

    @staticmethod
    async def get_ticket_by_number(db: AsyncSession, ticket_number: str) -> Optional[Ticket]:
        """Queries ticket by ticket number."""
        result = await db.execute(select(Ticket).where(Ticket.ticket_number == ticket_number.upper()))
        return result.scalar_one_or_none()

    @staticmethod
    async def list_tickets(
        db: AsyncSession,
        employee_id: Optional[str] = None,
        status: Optional[str] = None,
        category: Optional[str] = None,
        query: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> tuple[List[Ticket], int]:
        """Lists tickets with optional filters and keyword search."""
        stmt = select(Ticket)
        count_stmt = select(func.count(Ticket.id))

        filters = []
        if employee_id:
            filters.append(Ticket.employee_id == employee_id)
        if status:
            filters.append(Ticket.status == status)
        if category:
            filters.append(Ticket.category == category)
        if query:
            keyword = f"%{query}%"
            filters.append(
                or_(
                    Ticket.ticket_number.ilike(keyword),
                    Ticket.subject.ilike(keyword),
                    Ticket.description.ilike(keyword),
                )
            )

        if filters:
            stmt = stmt.where(*filters)
            count_stmt = count_stmt.where(*filters)

        stmt = stmt.order_by(Ticket.id.desc()).offset(skip).limit(limit)

        tickets_result = await db.execute(stmt)
        tickets = list(tickets_result.scalars().all())

        count_result = await db.execute(count_stmt)
        total = count_result.scalar_one() or 0

        return tickets, total

    @staticmethod
    async def update_ticket(
        db: AsyncSession, ticket_number: str, payload: TicketUpdate
    ) -> Optional[Ticket]:
        """Updates ticket fields."""
        ticket = await TicketService.get_ticket_by_number(db, ticket_number)
        if not ticket:
            return None

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(ticket, key, value)

        await db.commit()
        await db.refresh(ticket)
        return ticket

    @staticmethod
    async def delete_ticket(db: AsyncSession, ticket_number: str) -> bool:
        """Deletes a ticket entity."""
        ticket = await TicketService.get_ticket_by_number(db, ticket_number)
        if not ticket:
            return False

        await db.delete(ticket)
        await db.commit()
        return True

    @staticmethod
    async def get_voice_ticket_status(db: AsyncSession, ticket_number: str) -> tuple[bool, str]:
        """Formats ticket details into a concise, speech-optimized string for voice AI agents."""
        ticket = await TicketService.get_ticket_by_number(db, ticket_number)
        if not ticket:
            return False, f"I could not locate any IT ticket registered under ticket number {ticket_number}."

        spoken_num = " ".join(ticket.ticket_number)
        speech_text = (
            f"Ticket {spoken_num} regarding '{ticket.subject}' is currently {ticket.status}. "
            f"The category is {ticket.category} with a priority level of {ticket.priority}."
        )
        return True, speech_text

