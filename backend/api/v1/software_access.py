"""
Software Access Request Router Endpoints.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.session import get_db
from backend.schemas.software_request import (
    SoftwareAccessRequest,
    SoftwareAccessResponse,
    SoftwareAccessListResponse,
)
from backend.services.software_service import SoftwareService

router = APIRouter()


@router.post(
    "/software-access/request",
    response_model=SoftwareAccessResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Request Software Access",
    description="Submits a software access request and evaluates auto-approval policies.",
)
async def request_software_access(
    payload: SoftwareAccessRequest, db: AsyncSession = Depends(get_db)
):
    """Processes software entitlement request."""
    success, message, req = await SoftwareService.request_software_access(db, payload)
    if not success or not req:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )

    return SoftwareAccessResponse(
        success=True,
        request_id=req.id,
        employee_id=req.employee_id,
        software_name=req.software_name,
        approval_status=req.approval_status,
        voice_message=message,
    )


@router.get(
    "/software-access/requests",
    response_model=SoftwareAccessListResponse,
    summary="List Software Requests",
    description="Lists all submitted software requests.",
)
async def list_software_requests(
    employee_id: Optional[str] = Query(None, description="Filter by Employee ID"),
    db: AsyncSession = Depends(get_db),
):
    """Returns list of software access requests."""
    requests = await SoftwareService.list_software_requests(db, employee_id=employee_id)
    return SoftwareAccessListResponse(total=len(requests), requests=requests)
