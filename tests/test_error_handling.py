"""
Unit & Integration Tests for Exception Handling & RFC 7807 Errors.
"""

import pytest
from backend.utils.exceptions import InvalidEmployeeError, TicketNotFoundError


@pytest.mark.asyncio
async def test_custom_exception_response(async_client):
    """Test invalid employee raises RFC 7807 error format."""
    response = await async_client.post(
        "/api/v1/auth/login",
        json={"employee_id": "EMP-9999", "password": "WrongPassword"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_ticket_not_found_voice_status(async_client):
    """Test non-existent ticket status lookup returns clear message."""
    response = await async_client.get("/api/v1/tickets/IT-999999/voice-status")
    assert response.status_code == 200
    data = response.json()
    assert data["found"] is False
    assert "could not locate" in data["voice_response"]
