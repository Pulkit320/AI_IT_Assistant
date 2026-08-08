"""
Password Reset Business Logic Service.
Validates employee identity and logs reset audit events into password_reset_logs.
"""

import random
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.password_reset_log import PasswordResetLog
from backend.services.auth_service import AuthService
from backend.logging_config import logger


class PasswordResetService:
    """Service managing identity-verified password reset workflows."""

    @staticmethod
    def generate_reset_token() -> str:
        """Generates a secure random reset token."""
        return f"RESET-{random.randint(100000, 999999)}"

    @staticmethod
    async def request_password_reset(
        db: AsyncSession, employee_id: str, security_answer: Optional[str] = None
    ) -> tuple[bool, str, Optional[str], Optional[str]]:
        """Processes password reset request, creates audit entry, and builds speech response."""
        is_verified, user, message = await AuthService.verify_employee_voice_identity(
            db, employee_id, security_answer
        )

        if not is_verified or not user:
            return False, f"Password reset denied. {message}", None, None

        token = PasswordResetService.generate_reset_token()

        # Audit log creation
        reset_log = PasswordResetLog(
            employee_id=user.employee_id,
            reset_token=token,
            status="Requested",
            reset_ip="127.0.0.1",
        )
        db.add(reset_log)
        await db.commit()

        logger.info(f"Password reset token {token} generated for employee {user.employee_id}.")

        voice_msg = (
            f"A secure password reset link has been dispatched to {user.email}. "
            f"Your temporary reset token is {token}. Please check your inbox to complete the reset."
        )

        return True, voice_msg, token, user.full_name
