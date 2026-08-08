"""
Intelligent Human Escalation & Sentiment Analysis Service.
"""

from typing import Optional, List, Tuple
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.escalation_log import EscalationLog
from backend.models.ticket import Ticket
from backend.services.auth_service import AuthService
from backend.logging_config import logger


class EscalationService:
    """Service managing human handoffs, sentiment evaluation, and priority calculation."""

    @staticmethod
    def calculate_sentiment_and_priority(reason: str) -> Tuple[float, str]:
        """Calculates a heuristic sentiment score and assigns priority based on keywords."""
        reason_lower = reason.lower()
        high_risk_keywords = ["outage", "down", "broken", "emergency", "urgent", "frustrated", "manager"]
        
        score = 0.5  # Neutral default
        hits = sum(1 for kw in high_risk_keywords if kw in reason_lower)
        
        if hits >= 2 or "outage" in reason_lower:
            return 0.15, "Critical"
        elif hits == 1 or "urgent" in reason_lower:
            return 0.3, "High"
        return score, "Medium"

    @staticmethod
    async def create_escalation(
        db: AsyncSession,
        employee_id: str,
        reason: str,
        ticket_id: Optional[int] = None,
        agent_notes: Optional[str] = None,
    ) -> Tuple[bool, str, Optional[EscalationLog]]:
        """Processes human escalation and logs audit record."""
        user = await AuthService.get_user_by_employee_id(db, employee_id)
        if not user:
            return False, f"Employee {employee_id} not found.", None

        sentiment_score, priority = EscalationService.calculate_sentiment_and_priority(reason)

        escalation_log = EscalationLog(
            ticket_id=ticket_id,
            employee_id=user.employee_id,
            reason=reason,
            priority=priority,
            sentiment_score=sentiment_score,
            agent_notes=agent_notes or f"Escalated from AI voice agent call for {user.full_name}.",
        )
        db.add(escalation_log)
        
        # If ticket ID exists, update ticket priority to High/Escalated
        if ticket_id:
            result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
            ticket = result.scalar_one_or_none()
            if ticket:
                ticket.status = "Escalated to Human"
                ticket.priority = priority

        await db.commit()
        await db.refresh(escalation_log)

        logger.info(
            f"Escalation Log #{escalation_log.id} created for {user.employee_id} [Priority: {priority}]."
        )

        voice_msg = (
            f"I have escalated your case to our Tier 2 senior IT support team with {priority} priority. "
            f"A specialist from {user.department} support will review your file immediately."
        )

        return True, voice_msg, escalation_log

    @staticmethod
    async def list_escalations(
        db: AsyncSession, employee_id: Optional[str] = None
    ) -> List[EscalationLog]:
        """Lists escalation logs."""
        stmt = select(EscalationLog)
        if employee_id:
            stmt = stmt.where(EscalationLog.employee_id == employee_id)
        stmt = stmt.order_by(EscalationLog.id.desc())

        result = await db.execute(stmt)
        return list(result.scalars().all())
