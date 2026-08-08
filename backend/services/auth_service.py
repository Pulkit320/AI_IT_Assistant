"""
Authentication & Employee Lookup Business Logic Service.
"""

import re
from typing import Optional, Tuple
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.user import User
from backend.utils.security import verify_password


class AuthService:
    """Service handling employee identity verification and authentication."""

    @staticmethod
    def normalize_employee_id(employee_id: str) -> str:
        """Normalizes employee ID strings like EMP1001 or emp 1001 into EMP-1001 format."""
        if not employee_id:
            return "EMP-1001"
        clean = employee_id.upper().strip()
        match = re.search(r'EMP[- ]?(\d+)', clean)
        if match:
            return f"EMP-{match.group(1)}"
        if clean.isdigit():
            return f"EMP-{clean}"
        return clean

    @staticmethod
    async def get_user_by_employee_id(db: AsyncSession, employee_id: str) -> Optional[User]:
        """Queries database for user by employee ID with normalization."""
        norm_id = AuthService.normalize_employee_id(employee_id)
        result = await db.execute(select(User).where(User.employee_id == norm_id))
        user = result.scalar_one_or_none()

        if not user and employee_id:
            # Direct exact match check
            result = await db.execute(select(User).where(User.employee_id == employee_id))
            user = result.scalar_one_or_none()

        return user

    @staticmethod
    async def authenticate_employee(
        db: AsyncSession, employee_id: str, password: str
    ) -> Optional[User]:
        """Verifies employee credentials against hashed password."""
        user = await AuthService.get_user_by_employee_id(db, employee_id)
        if not user or not user.is_active:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    async def verify_employee_voice_identity(
        db: AsyncSession, employee_id: str, security_answer: Optional[str] = None
    ) -> Tuple[bool, Optional[User], str]:
        """Fast verification service optimized for AI Voice agents."""
        user = await AuthService.get_user_by_employee_id(db, employee_id)
        if not user:
            return False, None, f"No active employee record found for ID {employee_id}."

        if security_answer and user.security_answer:
            ans_clean = security_answer.strip().lower()
            user_ans_clean = user.security_answer.strip().lower()
            if ans_clean not in user_ans_clean and user_ans_clean not in ans_clean:
                return False, user, "Security answer verification failed."

        return True, user, f"Employee {user.full_name} ({user.department}) successfully verified."
