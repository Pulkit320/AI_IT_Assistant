"""
Unit & Integration Tests for Authentication & Employee Verification.
"""

import pytest
from backend.database.init_db import init_db, seed_data


@pytest.mark.asyncio
async def test_employee_login(async_client):
    """Test valid employee login returns JWT token."""
    await init_db()
    await seed_data()

    response = await async_client.post(
        "/api/v1/auth/login",
        json={"employee_id": "EMP-1001", "password": "Password123!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["employee_id"] == "EMP-1001"
    assert data["full_name"] == "Sarah Jenkins"


@pytest.mark.asyncio
async def test_employee_login_invalid(async_client):
    """Test invalid credentials return 401 Unauthorized."""
    response = await async_client.post(
        "/api/v1/auth/login",
        json={"employee_id": "EMP-1001", "password": "WrongPassword"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_voice_verify_employee(async_client):
    """Test voice employee verification endpoint."""
    response = await async_client.post(
        "/api/v1/auth/verify-employee",
        json={"employee_id": "EMP-1001", "security_answer": "Austin"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["verified"] is True
    assert data["full_name"] == "Sarah Jenkins"
