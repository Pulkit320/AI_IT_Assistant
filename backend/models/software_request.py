"""
Software Entitlement Request Database ORM Model.
"""

from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from backend.models.user import User


class SoftwareRequest(Base, TimestampMixin):
    """Software Access Request Entity Model."""
    __tablename__ = "software_requests"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    employee_id: Mapped[str] = mapped_column(String(50), ForeignKey("users.employee_id"), nullable=False, index=True)
    software_name: Mapped[str] = mapped_column(String(100), nullable=False)
    justification: Mapped[str] = mapped_column(Text, nullable=False)
    approval_status: Mapped[str] = mapped_column(String(30), nullable=False, default="Pending Manager Approval")
    approved_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="software_requests")
