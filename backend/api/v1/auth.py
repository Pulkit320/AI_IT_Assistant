"""
Authentication & Verification Router Endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.session import get_db
from backend.schemas.user import (
    LoginRequest,
    TokenResponse,
    EmployeeVerifyRequest,
    EmployeeVerifyResponse,
)
from backend.services.auth_service import AuthService
from backend.utils.security import create_access_token

router = APIRouter()


@router.post(
    "/auth/login",
    response_model=TokenResponse,
    summary="Employee Login & Token Generation",
    description="Authenticates employee credentials and issues a signed JWT bearer access token.",
)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Authenticates employee and returns access token."""
    user = await AuthService.authenticate_employee(db, payload.employee_id, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Employee ID or password",
        )

    token = create_access_token(subject=user.employee_id)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        employee_id=user.employee_id,
        full_name=user.full_name,
    )


@router.post(
    "/auth/verify-employee",
    response_model=EmployeeVerifyResponse,
    summary="Voice Agent Employee Verification",
    description="Fast identity verification endpoint designed for real-time voice interaction.",
)
async def verify_employee(
    payload: EmployeeVerifyRequest, db: AsyncSession = Depends(get_db)
):
    """Verifies employee identity for voice agent calls."""
    is_valid, user, message = await AuthService.verify_employee_voice_identity(
        db, payload.employee_id, payload.security_answer
    )

    if not is_valid or not user:
        return EmployeeVerifyResponse(
            verified=False,
            employee_id=payload.employee_id,
            full_name="Unknown",
            department="Unknown",
            message=message,
        )

    return EmployeeVerifyResponse(
        verified=True,
        employee_id=user.employee_id,
        full_name=user.full_name,
        department=user.department,
        message=message,
    )
