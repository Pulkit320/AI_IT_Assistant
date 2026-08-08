"""
End-to-End Integration & Multi-Step Voice Conversation Scenario Tests.
"""

import pytest
from backend.config import settings


@pytest.mark.asyncio
async def test_end_to_end_voice_caller_journey(async_client):
    """Simulates a complete caller journey: verify employee -> reset password -> request software -> check status -> escalate."""
    headers = {"X-ElevenLabs-Secret": settings.ELEVENLABS_WEBHOOK_SECRET}

    # Step 1: Verify employee
    v_res = await async_client.post(
        "/api/v1/auth/verify-employee",
        json={"employee_id": "EMP-1001", "security_answer": "Austin"},
    )
    assert v_res.status_code == 200
    assert v_res.json()["verified"] is True

    # Step 2: Voice Password Reset Webhook
    pr_res = await async_client.post(
        "/api/v1/elevenlabs/webhook",
        json={
            "tool_name": "password_reset",
            "parameters": {"employee_id": "EMP-1001", "security_answer": "Austin"},
        },
        headers=headers,
    )
    assert pr_res.status_code == 200
    assert "dispatched to sarah.jenkins@company.com" in pr_res.json()["response"]

    # Step 3: Voice Software Request Webhook (VS Code)
    sw_res = await async_client.post(
        "/api/v1/elevenlabs/webhook",
        json={
            "tool_name": "request_access",
            "parameters": {"employee_id": "EMP-1001", "software_name": "VS Code"},
        },
        headers=headers,
    )
    assert sw_res.status_code == 200
    assert "automatically approved" in sw_res.json()["response"]

    # Step 4: Voice Ticket Status Lookup Webhook
    tk_res = await async_client.post(
        "/api/v1/elevenlabs/webhook",
        json={
            "tool_name": "check_ticket",
            "parameters": {"ticket_number": "IT-8091"},
        },
        headers=headers,
    )
    assert tk_res.status_code == 200
    assert "Ticket I T - 8 0 9 1" in tk_res.json()["response"]

    # Step 5: Voice Human Escalation Webhook
    esc_res = await async_client.post(
        "/api/v1/elevenlabs/webhook",
        json={
            "tool_name": "escalate_issue",
            "parameters": {"employee_id": "EMP-1001", "reason": "Network down for entire department"},
        },
        headers=headers,
    )
    assert esc_res.status_code == 200
    assert "escalated your case" in esc_res.json()["response"]
