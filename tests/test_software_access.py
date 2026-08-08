"""
Unit & Integration Tests for Software Access Workflow.
"""

import pytest


@pytest.mark.asyncio
async def test_software_auto_approval(async_client):
    """Test standard software (VS Code) is auto-approved."""
    payload = {
        "employee_id": "EMP-1001",
        "software_name": "VS Code",
        "justification": "Python development work",
    }
    response = await async_client.post("/api/v1/software-access/request", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["approval_status"] == "Approved"
    assert "automatically approved" in data["voice_message"]


@pytest.mark.asyncio
async def test_software_manager_approval(async_client):
    """Test restricted software (Docker) requires manager approval."""
    payload = {
        "employee_id": "EMP-1001",
        "software_name": "Docker Desktop",
        "justification": "Container microservices",
    }
    response = await async_client.post("/api/v1/software-access/request", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["approval_status"] == "Pending Manager Approval"
    assert "routed to your manager" in data["voice_message"]
