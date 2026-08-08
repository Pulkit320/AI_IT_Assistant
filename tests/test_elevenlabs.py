"""
Unit & Integration Tests for ElevenLabs Playbook Webhooks.
"""

import pytest
from backend.config import settings


@pytest.mark.asyncio
async def test_elevenlabs_webhook_success(async_client):
    """Test valid ElevenLabs webhook tool execution."""
    headers = {"X-ElevenLabs-Secret": settings.ELEVENLABS_WEBHOOK_SECRET}
    payload = {
        "agent_id": "agent_test",
        "conversation_id": "conv_test",
        "tool_name": "request_access",
        "parameters": {
            "employee_id": "EMP-1001",
            "software_name": "VS Code",
        },
    }
    response = await async_client.post("/api/v1/elevenlabs/webhook", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "automatically approved" in data["response"]


@pytest.mark.asyncio
async def test_elevenlabs_webhook_flat_payload(async_client):
    """Test webhook handles flat parameter payload format gracefully."""
    payload = {
        "employee_id": "EMP-1001",
        "software_name": "Docker Desktop",
    }
    response = await async_client.post("/api/v1/elevenlabs/webhook", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "routed to your manager" in data["response"]
