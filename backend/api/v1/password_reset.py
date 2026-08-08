"""
Password Reset Router Endpoint.
"""

from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.session import get_db
from backend.models.password_reset_log import PasswordResetLog
from backend.schemas.password_reset import PasswordResetRequest, PasswordResetResponse

router = APIRouter()


@router.post(
    "/password-reset",
    response_model=PasswordResetResponse,
    summary="Request Password Reset",
    description="Verifies employee identity, generates a temporary reset token, and logs the security request.",
)
async def request_password_reset(
    payload: PasswordResetRequest, db: AsyncSession = Depends(get_db)
):
    """Processes password reset request."""
    from backend.services.password_reset_service import PasswordResetService
    success, message, token, full_name = await PasswordResetService.request_password_reset(
        db, payload.employee_id, payload.security_answer
    )

    if not success or not token or not full_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )

    return PasswordResetResponse(
        success=True,
        employee_id=payload.employee_id,
        full_name=full_name,
        reset_token=token,
        status="Requested",
        voice_message=message,
    )


@router.get(
    "/password-reset/logs",
    summary="List Password Reset Audit Logs",
    description="Retrieves all password reset audit logs stored in the database.",
)
async def list_password_reset_logs(db: AsyncSession = Depends(get_db)):
    """Lists all password reset audit logs."""
    result = await db.execute(select(PasswordResetLog).order_by(PasswordResetLog.created_at.desc()))
    logs = result.scalars().all()
    return [
        {
            "id": log.id,
            "employee_id": log.employee_id,
            "reset_token": log.reset_token,
            "status": log.status,
            "requested_at": str(log.requested_at),
        }
        for log in logs
    ]
