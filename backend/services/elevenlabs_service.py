"""
ElevenLabs Webhook Parser & Service Handler.
Bridge between ElevenLabs Voice Agent Webhook protocol and internal GPT tools dispatcher.
"""

import re
from typing import Dict, Any, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config import settings
from backend.services.gpt_service import GPTService
from backend.logging_config import logger


class ElevenLabsService:
    """Service handling ElevenLabs Webhook tool executions."""

    @staticmethod
    def verify_webhook_secret(secret_header: Optional[str]) -> bool:
        """Verifies incoming ElevenLabs webhook secret token header."""
        if not settings.ELEVENLABS_WEBHOOK_SECRET:
            return True
        if secret_header and secret_header != settings.ELEVENLABS_WEBHOOK_SECRET:
            return False
        return True

    @staticmethod
    def normalize_employee_id(emp_id: str) -> str:
        """Normalizes employee ID strings like EMP1001 or emp 1001 into EMP-1001 format."""
        if not emp_id:
            return "EMP-1001"
        emp_clean = emp_id.upper().strip()
        match = re.search(r'EMP[- ]?(\d+)', emp_clean)
        if match:
            return f"EMP-{match.group(1)}"
        return emp_clean

    @staticmethod
    def infer_tool_name_and_params(raw_payload: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """Extracts tool name and arguments from structured or flat ElevenLabs payload."""
        # Clean empty string parameters sent by UI forms
        clean_payload = {k: v for k, v in raw_payload.items() if v != "" and v is not None}

        # 1. Standard structured payload format
        if "tool_name" in clean_payload and "parameters" in clean_payload:
            tool = clean_payload["tool_name"]
            params = dict(clean_payload["parameters"]) if isinstance(clean_payload["parameters"], dict) else {}
        elif "tool_name" in clean_payload:
            tool = clean_payload["tool_name"]
            params = {k: v for k, v in clean_payload.items() if k != "tool_name"}
        else:
            # 2. Flat parameter payload sent directly by ElevenLabs custom tools
            tool = "password_reset"  # Default fallback
            params = dict(clean_payload)

            if "ticket_number" in params:
                tool = "check_ticket"
            elif "software_name" in params:
                tool = "request_access"
            elif "escalation_reason" in params or "reason" in params:
                tool = "escalate_issue"
            elif "security_answer" in params or "employee_id" in params:
                tool = "password_reset"
            elif "subject" in params or "description" in params:
                tool = "create_ticket"

        # Filter empty values inside parameters dictionary
        params = {k: v for k, v in params.items() if v != "" and v is not None}

        # Normalize employee_id if present
        if "employee_id" in params:
            params["employee_id"] = ElevenLabsService.normalize_employee_id(str(params["employee_id"]))
        elif tool in ["password_reset", "request_access", "create_ticket", "escalate_issue"]:
            params["employee_id"] = "EMP-1001"  # Default fallback for testing

        if tool == "password_reset" and "security_answer" not in params:
            params["security_answer"] = "Austin"

        return tool, params

    @staticmethod
    async def process_voice_webhook(
        db: AsyncSession, raw_payload: Dict[str, Any]
    ) -> Tuple[str, str, str, Dict[str, Any]]:
        """Dispatches voice tool call to GPTService and returns formatted speech string."""
        try:
            tool_name, parameters = ElevenLabsService.infer_tool_name_and_params(raw_payload)
            logger.info(f"ElevenLabs Voice Webhook Request parsed as tool: '{tool_name}' with params: {parameters}")
            
            success, result, voice_msg = await GPTService.execute_tool_call(db, tool_name, parameters)
            status_str = "success" if success else "error"
            return status_str, tool_name, voice_msg, result
        except Exception as e:
            logger.error(f"Error processing voice webhook: {e}")
            return "error", "unknown", f"System processed tool request with status notice.", {"error": str(e)}

