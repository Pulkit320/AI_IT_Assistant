"""
ElevenLabs Webhook Pydantic Validation Schemas.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel


class ElevenLabsWebhookRequest(BaseModel):
    agent_id: Optional[str] = "agent_default"
    conversation_id: Optional[str] = "conv_sample"
    tool_name: str
    parameters: Dict[str, Any]


class ElevenLabsWebhookResponse(BaseModel):
    status: str
    tool_name: str
    response: str
