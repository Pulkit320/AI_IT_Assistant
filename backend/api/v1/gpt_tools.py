"""
GPT-5 LLM Tool Execution Router Endpoint.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.session import get_db
from backend.schemas.gpt_tools import ToolCallRequest, ToolCallResponse
from backend.services.gpt_service import GPTService

router = APIRouter()


@router.post(
    "/gpt/execute-tool",
    response_model=ToolCallResponse,
    summary="Execute LLM Tool Call",
    description="Receives structured tool call JSON payloads from GPT-5 or voice agents and executes backend logic.",
)
async def execute_tool(payload: ToolCallRequest, db: AsyncSession = Depends(get_db)):
    """Executes backend tool functions on behalf of LLM model."""
    success, result, voice_msg = await GPTService.execute_tool_call(
        db, payload.tool_name, payload.arguments
    )

    if not success and payload.tool_name not in ["check_ticket", "password_reset"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=voice_msg,
        )

    return ToolCallResponse(
        success=success,
        tool_name=payload.tool_name,
        result=result,
        voice_response=voice_msg,
    )
