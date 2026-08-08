"""
GPT Tool Execution Pydantic Validation Schemas.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel


class ToolCallRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]


class ToolCallResponse(BaseModel):
    success: bool
    tool_name: str
    result: Dict[str, Any]
    voice_response: str
