"""
Password Reset Audit Log Database ORM Model.
"""

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from backend.models.user import User


class PasswordResetLog(Base, TimestampMixin):
    """Password Reset Security Audit Log Model."""
    __tablename__ = "password_reset_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    employee_id: Mapped[str] = mapped_column(String(50), ForeignKey("users.employee_id"), nullable=False, index=True)
    reset_token: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="Requested")
    reset_ip: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, default="127.0.0.1")
    requested_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="password_resets")
