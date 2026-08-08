"""
ElevenLabs Conversational AI Webhook Router Endpoint.
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.session import get_db
from backend.services.elevenlabs_service import ElevenLabsService
from backend.logging_config import logger

router = APIRouter()


@router.post(
    "/elevenlabs/webhook",
    summary="ElevenLabs Voice Agent Webhook",
    description="Receives real-time voice tool call webhooks from ElevenLabs Conversational AI Playbooks.",
)
async def elevenlabs_webhook(
    payload: Dict[str, Any],
    x_elevenlabs_secret: Optional[str] = Header(None, alias="X-ElevenLabs-Secret"),
    db: AsyncSession = Depends(get_db),
):
    """Processes ElevenLabs voice agent webhooks gracefully."""
    logger.info(f"Incoming ElevenLabs Webhook Payload: {payload}")

    status_str, tool_name, speech_response, result = await ElevenLabsService.process_voice_webhook(
        db, payload
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "success",
            "tool_name": tool_name,
            "response": speech_response,
            "message": speech_response,
            "text": speech_response,
            "result": result,
        },
    )
