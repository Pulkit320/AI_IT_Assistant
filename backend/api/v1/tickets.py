"""
Ticket Management REST Router Endpoints.
Provides CRUD operations for IT support tickets.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.session import get_db
from backend.schemas.ticket import TicketCreate, TicketUpdate, TicketRead, TicketListResponse
from backend.services.ticket_service import TicketService

router = APIRouter()


@router.post(
    "/tickets",
    response_model=TicketRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create New IT Ticket",
    description="Creates a new IT support ticket and returns ticket details.",
)
async def create_ticket(payload: TicketCreate, db: AsyncSession = Depends(get_db)):
    """Creates a new ticket entity."""
    return await TicketService.create_ticket(db, payload)


@router.get(
    "/tickets",
    response_model=TicketListResponse,
    summary="List & Filter IT Tickets",
    description="Lists tickets with optional filters by employee ID, status, category, or search query.",
)
async def list_tickets(
    employee_id: Optional[str] = Query(None, description="Filter by Employee ID"),
    status_param: Optional[str] = Query(None, alias="status", description="Filter by Ticket Status"),
    category: Optional[str] = Query(None, description="Filter by Category"),
    query: Optional[str] = Query(None, description="Search query in ticket number, subject, or description"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Returns paginated list of matching tickets."""
    tickets, total = await TicketService.list_tickets(
        db,
        employee_id=employee_id,
        status=status_param,
        category=category,
        query=query,
        skip=skip,
        limit=limit,
    )
    return TicketListResponse(total=total, tickets=tickets)


@router.get(
    "/tickets/{ticket_number}",
    response_model=TicketRead,
    summary="Get Ticket Details",
    description="Fetches detailed information for a specific ticket by ticket number.",
)
async def get_ticket(ticket_number: str, db: AsyncSession = Depends(get_db)):
    """Fetches ticket by ticket number."""
    ticket = await TicketService.get_ticket_by_number(db, ticket_number)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket {ticket_number} not found.",
        )
    return ticket


@router.get(
    "/tickets/{ticket_number}/voice-status",
    summary="Voice-Ready Ticket Status Lookup",
    description="Returns a speech-optimized natural text response for ElevenLabs TTS voice agents.",
)
async def get_voice_ticket_status(ticket_number: str, db: AsyncSession = Depends(get_db)):
    """Returns speech formatted ticket status payload."""
    found, speech_text = await TicketService.get_voice_ticket_status(db, ticket_number)
    return {
        "ticket_number": ticket_number,
        "found": found,
        "voice_response": speech_text,
    }


@router.patch(
    "/tickets/{ticket_number}",
    response_model=TicketRead,
    summary="Update Ticket",
    description="Modifies existing ticket status, subject, priority, or voice summary.",
)
async def update_ticket(
    ticket_number: str, payload: TicketUpdate, db: AsyncSession = Depends(get_db)
):
    """Updates ticket fields."""
    ticket = await TicketService.update_ticket(db, ticket_number, payload)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket {ticket_number} not found.",
        )
    return ticket


@router.delete(
    "/tickets/{ticket_number}",
    status_code=status.HTTP_200_OK,
    summary="Delete Ticket",
    description="Deletes an IT ticket by ticket number.",
)
async def delete_ticket(ticket_number: str, db: AsyncSession = Depends(get_db)):
    """Deletes a ticket entity."""
    success = await TicketService.delete_ticket(db, ticket_number)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket {ticket_number} not found.",
        )
    return {"message": f"Ticket {ticket_number} successfully deleted."}
