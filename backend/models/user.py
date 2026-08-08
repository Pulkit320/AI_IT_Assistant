"""
User / Employee Database ORM Model.
"""

from typing import List, TYPE_CHECKING
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from backend.models.ticket import Ticket
    from backend.models.password_reset_log import PasswordResetLog
    from backend.models.software_request import SoftwareRequest
    from backend.models.escalation_log import EscalationLog


class User(Base, TimestampMixin):
    """User / Employee Entity Model."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    employee_id: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    department: Mapped[str] = mapped_column(String(100), nullable=False, default="Engineering")
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="Employee")
    security_answer: Mapped[str] = mapped_column(String(255), nullable=False, default="Austin")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    tickets: Mapped[List["Ticket"]] = relationship("Ticket", back_populates="user", cascade="all, delete-orphan")
    password_resets: Mapped[List["PasswordResetLog"]] = relationship("PasswordResetLog", back_populates="user")
    software_requests: Mapped[List["SoftwareRequest"]] = relationship("SoftwareRequest", back_populates="user")
    escalations: Mapped[List["EscalationLog"]] = relationship("EscalationLog", back_populates="user")
