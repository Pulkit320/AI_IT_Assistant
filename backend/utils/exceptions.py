"""
Custom Helpdesk Domain Exception Hierarchy.
"""

from typing import Optional


class BaseHelpdeskException(Exception):
    """Base exception for Helpdesk Domain errors."""
    def __init__(self, message: str, status_code: int = 400, voice_fallback: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.voice_fallback = voice_fallback or message


class InvalidEmployeeError(BaseHelpdeskException):
    """Raised when an employee ID or credential check fails."""
    def __init__(self, employee_id: str):
        msg = f"No active employee record found for ID {employee_id}."
        voice = f"I could not locate an employee registered under ID {employee_id}. Please check the ID."
        super().__init__(message=msg, status_code=404, voice_fallback=voice)


class TicketNotFoundError(BaseHelpdeskException):
    """Raised when a ticket lookup fails."""
    def __init__(self, ticket_number: str):
        msg = f"Ticket {ticket_number} not found."
        voice = f"I could not find an IT ticket under number {ticket_number}."
        super().__init__(message=msg, status_code=404, voice_fallback=voice)


class SoftwareAccessError(BaseHelpdeskException):
    """Raised when software entitlement rules fail."""
    def __init__(self, message: str):
        super().__init__(message=message, status_code=400)


class LLMProviderError(BaseHelpdeskException):
    """Raised when an LLM service failure occurs."""
    def __init__(self, message: str):
        voice = "I am experiencing temporary technical difficulties processing your request with our AI system."
        super().__init__(message=message, status_code=503, voice_fallback=voice)
