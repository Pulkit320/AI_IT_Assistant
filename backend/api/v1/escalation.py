"""
Human Escalation Router Endpoint.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.session import get_db
from backend.schemas.escalation import (
    EscalationRequest,
    EscalationResponse,
    EscalationListResponse,
)
from backend.services.escalation_service import EscalationService

router = APIRouter()


@router.post(
    "/escalation/escalate",
    response_model=EscalationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Escalate to Human Agent",
    description="Logs a Tier-2 human escalation, calculates sentiment score, and updates ticket status.",
)
async def escalate_issue(
    payload: EscalationRequest, db: AsyncSession = Depends(get_db)
):
    """Processes human escalation request."""
    success, message, log = await EscalationService.create_escalation(
        db, payload.employee_id, payload.reason, payload.ticket_id, payload.agent_notes
    )

    if not success or not log:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )

    return EscalationResponse(
        success=True,
        escalation_id=log.id,
        employee_id=log.employee_id,
        priority=log.priority,
        sentiment_score=log.sentiment_score,
        voice_message=message,
    )


@router.get(
    "/escalation/logs",
    response_model=EscalationListResponse,
    summary="List Escalation Logs",
    description="Lists all logged human escalations.",
)
async def list_escalations(
    employee_id: Optional[str] = Query(None, description="Filter by Employee ID"),
    db: AsyncSession = Depends(get_db),
):
    """Returns list of escalation log records."""
    logs = await EscalationService.list_escalations(db, employee_id=employee_id)
    return EscalationListResponse(total=len(logs), escalations=logs)
