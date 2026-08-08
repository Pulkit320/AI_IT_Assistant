"""
User & Authentication Pydantic Validation Schemas.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class LoginRequest(BaseModel):
    employee_id: str
    password: str


class EmployeeVerifyRequest(BaseModel):
    employee_id: str
    security_answer: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    employee_id: str
    full_name: str


class UserRead(BaseModel):
    id: int
    employee_id: str
    full_name: str
    email: EmailStr
    department: str
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class EmployeeVerifyResponse(BaseModel):
    verified: bool
    employee_id: str
    full_name: str
    department: str
    message: str
