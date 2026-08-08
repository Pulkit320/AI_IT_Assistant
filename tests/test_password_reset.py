"""
Unit & Integration Tests for Password Reset Workflow.
"""

import pytest


@pytest.mark.asyncio
async def test_password_reset_success(async_client):
    """Test successful password reset for verified employee."""
    payload = {
        "employee_id": "EMP-1001",
        "security_answer": "Austin",
    }
    response = await async_client.post("/api/v1/password-reset", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["employee_id"] == "EMP-1001"
    assert data["reset_token"].startswith("RESET-")
    assert "dispatched to sarah.jenkins@company.com" in data["voice_message"]


@pytest.mark.asyncio
async def test_password_reset_invalid_employee(async_client):
    """Test password reset fails for invalid employee ID."""
    payload = {
        "employee_id": "EMP-9999",
        "security_answer": "Invalid",
    }
    response = await async_client.post("/api/v1/password-reset", json=payload)
    assert response.status_code == 400
