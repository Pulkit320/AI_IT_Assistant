"""
Password Reset Pydantic Validation Schemas.
"""

from typing import Optional
from pydantic import BaseModel


class PasswordResetRequest(BaseModel):
    employee_id: str
    security_answer: Optional[str] = None


class PasswordResetResponse(BaseModel):
    success: bool
    employee_id: str
    full_name: str
    reset_token: str
    status: str
    voice_message: str
