"""
Unit & Integration Tests for Ticket Management REST APIs (CRUD) & Voice Status.
"""

import pytest


@pytest.mark.asyncio
async def test_create_ticket(async_client):
    """Test creating a new IT ticket."""
    payload = {
        "employee_id": "EMP-1001",
        "subject": "VPN Connection Drops",
        "description": "VPN connection drops every 15 minutes on macOS Sonoma.",
        "category": "Network",
        "priority": "High",
    }
    response = await async_client.post("/api/v1/tickets", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["ticket_number"].startswith("IT-")
    assert data["subject"] == "VPN Connection Drops"
    assert data["status"] == "Open"


@pytest.mark.asyncio
async def test_list_and_search_tickets(async_client):
    """Test listing and filtering tickets."""
    response = await async_client.get("/api/v1/tickets?employee_id=EMP-1001")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert len(data["tickets"]) >= 1


@pytest.mark.asyncio
async def test_get_ticket_by_number(async_client):
    """Test retrieving ticket details by number."""
    response = await async_client.get("/api/v1/tickets/IT-8091")
    assert response.status_code == 200
    data = response.json()
    assert data["ticket_number"] == "IT-8091"
    assert data["employee_id"] == "EMP-1001"


@pytest.mark.asyncio
async def test_voice_ticket_status(async_client):
    """Test speech-formatted voice status lookup."""
    response = await async_client.get("/api/v1/tickets/IT-8091/voice-status")
    assert response.status_code == 200
    data = response.json()
    assert data["found"] is True
    assert "Ticket I T - 8 0 9 1" in data["voice_response"]


@pytest.mark.asyncio
async def test_update_ticket(async_client):
    """Test updating ticket status."""
    payload = {"status": "In Progress", "priority": "Urgent"}
    response = await async_client.patch("/api/v1/tickets/IT-8091", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "In Progress"
    assert data["priority"] == "Urgent"


@pytest.mark.asyncio
async def test_delete_ticket(async_client):
    """Test deleting a ticket after creating a temporary one."""
    create_res = await async_client.post(
        "/api/v1/tickets",
        json={
            "employee_id": "EMP-1001",
            "subject": "Temporary Ticket for Deletion",
            "description": "Will be deleted",
        },
    )
    t_num = create_res.json()["ticket_number"]

    response = await async_client.delete(f"/api/v1/tickets/{t_num}")
    assert response.status_code == 200

    # Confirm ticket no longer exists
    get_res = await async_client.get(f"/api/v1/tickets/{t_num}")
    assert get_res.status_code == 404
