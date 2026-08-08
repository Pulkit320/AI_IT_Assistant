"""
GPT-5 LLM Service & Tool Dispatcher Layer.
Includes zero-cost Mock LLM engine and OpenAI API integration capability.
"""

from typing import Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config import settings
from backend.services.ticket_service import TicketService
from backend.services.password_reset_service import PasswordResetService
from backend.services.software_service import SoftwareService
from backend.schemas.ticket import TicketCreate
from backend.schemas.software_request import SoftwareAccessRequest
from backend.logging_config import logger


class GPTService:
    """Service executing tool calls dispatched by GPT-5 or Mock LLM engine."""

    @staticmethod
    async def execute_tool_call(
        db: AsyncSession, tool_name: str, arguments: Dict[str, Any]
    ) -> Tuple[bool, Dict[str, Any], str]:
        """Dispatches tool call payload to backend service and returns result dict & voice response."""
        logger.info(f"Executing LLM Tool Call '{tool_name}' with args: {arguments}")

        if tool_name == "create_ticket":
            payload = TicketCreate(
                employee_id=arguments.get("employee_id", "EMP-1001"),
                subject=arguments.get("subject", "General Support"),
                description=arguments.get("description", "No details provided."),
                category=arguments.get("category", "General IT"),
                priority=arguments.get("priority", "Medium"),
            )
            ticket = await TicketService.create_ticket(db, payload)
            result = {"ticket_number": ticket.ticket_number, "status": ticket.status}
            voice_msg = (
                f"I have logged a new IT ticket under number {ticket.ticket_number} for {ticket.subject}."
            )
            return True, result, voice_msg

        elif tool_name == "password_reset":
            employee_id = arguments.get("employee_id", "")
            security_answer = arguments.get("security_answer")
            success, msg, token, name = await PasswordResetService.request_password_reset(
                db, employee_id, security_answer
            )
            return success, {"employee_id": employee_id, "token": token}, msg

        elif tool_name == "request_access":
            payload = SoftwareAccessRequest(
                employee_id=arguments.get("employee_id", "EMP-1001"),
                software_name=arguments.get("software_name", "VS Code"),
                justification=arguments.get("justification", "Required for work"),
            )
            success, msg, req = await SoftwareService.request_software_access(db, payload)
            res = {"request_id": req.id if req else None, "status": req.approval_status if req else "Failed"}
            return success, res, msg

        elif tool_name == "check_ticket":
            t_num = arguments.get("ticket_number", "")
            success, msg = await TicketService.get_voice_ticket_status(db, t_num)
            return success, {"ticket_number": t_num}, msg

        elif tool_name == "escalate_issue":
            # Deferred to escalation service in Phase 11
            from backend.services.escalation_service import EscalationService
            emp_id = arguments.get("employee_id", "EMP-1001")
            reason = arguments.get("reason", "Employee requested tier 2 human agent.")
            t_id = arguments.get("ticket_id")
            success, msg, log = await EscalationService.create_escalation(db, emp_id, reason, t_id)
            return success, {"escalation_id": log.id if log else None}, msg

        else:
            return False, {}, f"Unknown tool execution requested: {tool_name}"
