"""
Unit & Integration Tests for Human Escalation System.
"""

import pytest


@pytest.mark.asyncio
async def test_escalation_creation(async_client):
    """Test creating an escalation log for critical outage."""
    payload = {
        "employee_id": "EMP-1001",
        "reason": "VPN outage for entire engineering team is urgent and down!",
    }
    response = await async_client.post("/api/v1/escalation/escalate", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["priority"] in ["High", "Critical"]
    assert "escalated your case" in data["voice_message"]


@pytest.mark.asyncio
async def test_list_escalations(async_client):
    """Test listing escalations after creating one."""
    # Create escalation first
    await async_client.post(
        "/api/v1/escalation/escalate",
        json={"employee_id": "EMP-1001", "reason": "System outage"},
    )

    response = await async_client.get("/api/v1/escalation/logs?employee_id=EMP-1001")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
