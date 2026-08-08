"""
Health Check Diagnostic Endpoint.
Provides API status verification and infrastructure diagnostics.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from backend.config import settings

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    project: str
    version: str
    environment: str


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="System Health Diagnostic",
    description="Returns current operational status of the AI Voice IT Helpdesk Agent backend.",
)
async def check_health() -> HealthResponse:
    """Returns JSON payload confirming operational readiness."""
    return HealthResponse(
        status="healthy",
        project=settings.PROJECT_NAME,
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
    )
