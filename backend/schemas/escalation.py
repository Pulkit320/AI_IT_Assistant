"""
Escalation Pydantic Validation Schemas.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class EscalationRequest(BaseModel):
    employee_id: str
    reason: str
    ticket_id: Optional[int] = None
    agent_notes: Optional[str] = None


class EscalationRead(BaseModel):
    id: int
    ticket_id: Optional[int]
    employee_id: str
    reason: str
    priority: str
    sentiment_score: float
    agent_notes: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EscalationResponse(BaseModel):
    success: bool
    escalation_id: int
    employee_id: str
    priority: str
    sentiment_score: float
    voice_message: str


class EscalationListResponse(BaseModel):
    total: int
    escalations: List[EscalationRead]
