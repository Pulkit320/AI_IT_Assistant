"""
Main v1 API Router Aggregator.
Consolidates modular endpoint routers under /api/v1 prefix.
"""

from fastapi import APIRouter
from backend.api.v1 import (
    health,
    auth,
    tickets,
    password_reset,
    software_access,
    gpt_tools,
    elevenlabs,
    escalation,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health & Diagnostics"])
api_router.include_router(auth.router, tags=["Authentication & Verification"])
api_router.include_router(tickets.router, tags=["Ticket Management"])
api_router.include_router(password_reset.router, tags=["Password Reset Workflow"])
api_router.include_router(software_access.router, tags=["Software Access Workflow"])
api_router.include_router(gpt_tools.router, tags=["GPT-5 Tool Calling"])
api_router.include_router(elevenlabs.router, tags=["ElevenLabs Playbooks Webhooks"])
api_router.include_router(escalation.router, tags=["Human Escalation System"])
