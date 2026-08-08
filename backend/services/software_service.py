"""
Software Access Entitlement Business Logic & Rule Engine.
"""

from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.software_request import SoftwareRequest
from backend.services.auth_service import AuthService
from backend.schemas.software_request import SoftwareAccessRequest
from backend.logging_config import logger

AUTO_APPROVED_SOFTWARE = {"vs code", "vscode", "visual studio code", "slack", "zoom"}


class SoftwareService:
    """Service managing software access entitlement workflows and approval rules."""

    @staticmethod
    def evaluate_approval_rule(software_name: str) -> tuple[str, Optional[str]]:
        """Evaluates software request policy rules."""
        name_clean = software_name.strip().lower()
        if name_clean in AUTO_APPROVED_SOFTWARE:
            return "Approved", "System Auto-Approval Engine"
        return "Pending Manager Approval", None

    @staticmethod
    async def request_software_access(
        db: AsyncSession, payload: SoftwareAccessRequest
    ) -> tuple[bool, str, Optional[SoftwareRequest]]:
        """Processes software access request using business rule engine."""
        user = await AuthService.get_user_by_employee_id(db, payload.employee_id)
        if not user:
            return False, f"Employee {payload.employee_id} not found.", None

        status_str, approved_by = SoftwareService.evaluate_approval_rule(payload.software_name)

        req = SoftwareRequest(
            employee_id=user.employee_id,
            software_name=payload.software_name,
            justification=payload.justification,
            approval_status=status_str,
            approved_by=approved_by,
        )
        db.add(req)
        await db.commit()
        await db.refresh(req)

        logger.info(
            f"Software request #{req.id} for '{payload.software_name}' by {user.employee_id}: {status_str}."
        )

        if status_str == "Approved":
            voice_msg = (
                f"Your request for {payload.software_name} has been automatically approved. "
                f"The license is now assigned to {user.full_name}."
            )
        else:
            voice_msg = (
                f"Your request for {payload.software_name} has been logged and routed to your "
                f"manager in the {user.department} department for review."
            )

        return True, voice_msg, req

    @staticmethod
    async def list_software_requests(
        db: AsyncSession, employee_id: Optional[str] = None
    ) -> List[SoftwareRequest]:
        """Lists software requests, optionally filtered by employee ID."""
        stmt = select(SoftwareRequest)
        if employee_id:
            stmt = stmt.where(SoftwareRequest.employee_id == employee_id)
        stmt = stmt.order_by(SoftwareRequest.id.desc())

        result = await db.execute(stmt)
        return list(result.scalars().all())
