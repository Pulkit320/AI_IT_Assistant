"""
Software Access Pydantic Validation Schemas.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class SoftwareAccessRequest(BaseModel):
    employee_id: str
    software_name: str
    justification: str = "Standard work entitlement"


class SoftwareAccessRead(BaseModel):
    id: int
    employee_id: str
    software_name: str
    justification: str
    approval_status: str
    approved_by: Optional[str]
    requested_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SoftwareAccessResponse(BaseModel):
    success: bool
    request_id: int
    employee_id: str
    software_name: str
    approval_status: str
    voice_message: str


class SoftwareAccessListResponse(BaseModel):
    total: int
    requests: List[SoftwareAccessRead]
