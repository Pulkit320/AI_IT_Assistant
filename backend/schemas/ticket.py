"""
Ticket Pydantic Validation Schemas.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class TicketCreate(BaseModel):
    employee_id: str
    subject: str
    description: str
    category: str = "General IT"
    priority: str = "Medium"
    voice_summary: Optional[str] = None


class TicketUpdate(BaseModel):
    subject: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    voice_summary: Optional[str] = None


class TicketRead(BaseModel):
    id: int
    ticket_number: str
    employee_id: str
    category: str
    priority: str
    status: str
    subject: str
    description: str
    voice_summary: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TicketListResponse(BaseModel):
    total: int
    tickets: List[TicketRead]
