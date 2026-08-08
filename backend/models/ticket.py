"""
IT Ticket Database ORM Model.
"""

from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from backend.models.user import User
    from backend.models.escalation_log import EscalationLog


class Ticket(Base, TimestampMixin):
    """IT Support Ticket Entity Model."""
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ticket_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    employee_id: Mapped[str] = mapped_column(String(50), ForeignKey("users.employee_id"), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False, default="General IT")
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="Medium")
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="Open")
    subject: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    voice_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="tickets")
    escalation: Mapped[Optional["EscalationLog"]] = relationship("EscalationLog", back_populates="ticket", uselist=False)
