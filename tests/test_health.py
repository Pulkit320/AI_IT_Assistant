"""
Unit tests for Health Check & Root Welcome endpoints.
"""

import pytest


@pytest.mark.asyncio
async def test_root_endpoint(async_client):
    """Verify root GET endpoint returns 200 OK and expected links."""
    response = await async_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["version"] == "1.0.0"


@pytest.mark.asyncio
async def test_health_endpoint(async_client):
    """Verify GET /api/v1/health returns status healthy."""
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["project"] == "AI Voice IT Helpdesk Agent"
