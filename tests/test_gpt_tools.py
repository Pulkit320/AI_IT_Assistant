"""
Unit & Integration Tests for GPT-5 Tool Execution Layer.
"""

import pytest


@pytest.mark.asyncio
async def test_execute_create_ticket_tool(async_client):
    """Test executing create_ticket tool via GPT router."""
    payload = {
        "tool_name": "create_ticket",
        "arguments": {
            "employee_id": "EMP-1001",
            "subject": "Monitor Flickering",
            "description": "External monitor flickers on HDMI connection.",
            "category": "Hardware",
        },
    }
    response = await async_client.post("/api/v1/gpt/execute-tool", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["result"]["ticket_number"].startswith("IT-")
    assert "logged a new IT ticket" in data["voice_response"]


@pytest.mark.asyncio
async def test_execute_password_reset_tool(async_client):
    """Test executing password_reset tool via GPT router."""
    payload = {
        "tool_name": "password_reset",
        "arguments": {
            "employee_id": "EMP-1001",
            "security_answer": "Austin",
        },
    }
    response = await async_client.post("/api/v1/gpt/execute-tool", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "dispatched to sarah.jenkins@company.com" in data["voice_response"]


@pytest.mark.asyncio
async def test_execute_check_ticket_tool(async_client):
    """Test executing check_ticket tool via GPT router."""
    payload = {
        "tool_name": "check_ticket",
        "arguments": {
            "ticket_number": "IT-8091",
        },
    }
    response = await async_client.post("/api/v1/gpt/execute-tool", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "Ticket I T - 8 0 9 1" in data["voice_response"]
