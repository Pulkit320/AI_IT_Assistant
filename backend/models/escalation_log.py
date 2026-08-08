"""
Tier-2 Escalation Audit Log Database ORM Model.
"""

from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Text, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from backend.models.user import User
    from backend.models.ticket import Ticket


class EscalationLog(Base, TimestampMixin):
    """Tier-2 Human Escalation Audit Log Model."""
    __tablename__ = "escalation_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ticket_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tickets.id"), nullable=True)
    employee_id: Mapped[str] = mapped_column(String(50), ForeignKey("users.employee_id"), nullable=False, index=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="High")
    sentiment_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)
    agent_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="escalations")
    ticket: Mapped[Optional["Ticket"]] = relationship("Ticket", back_populates="escalation")
