"""
Local Zero-Cost CLI Voice Agent Simulator.
Allows students to test ElevenLabs Playbook webhooks interactively in terminal without paid minutes.
"""

import sys
import httpx


def run_cli_simulator():
    """Runs interactive voice simulation CLI in terminal."""
    base_url = "http://127.0.0.1:8000/api/v1/elevenlabs/webhook"
    secret = "sample-webhook-secret-key"

    print("=" * 60)
    print(" AI VOICE IT HELPDESK - ZERO-COST CLI SIMULATOR")
    print(" Simulates ElevenLabs Playbook Webhooks locally.")
    print("=" * 60)
    print("Available Commands:")
    print(" 1. Password Reset (employee_id=EMP-1001, security_answer=Austin)")
    print(" 2. Request Software (employee_id=EMP-1001, software_name=VS Code)")
    print(" 3. Check Ticket Status (ticket_number=IT-8091)")
    print(" 4. Create IT Ticket (employee_id=EMP-1001, subject=VPN issues)")
    print(" 5. Escalate to Human (employee_id=EMP-1001, reason=Frustrated)")
    print(" 6. Exit")
    print("-" * 60)

    with httpx.Client(timeout=10.0) as client:
        while True:
            choice = input("\nSelect simulation action (1-6): ").strip()
            if choice == "6" or choice.lower() == "exit":
                print("Exiting Voice Agent Simulator. Goodbye!")
                break

            payload = None
            if choice == "1":
                payload = {
                    "tool_name": "password_reset",
                    "parameters": {"employee_id": "EMP-1001", "security_answer": "Austin"},
                }
            elif choice == "2":
                sw = input("Enter software name [default: VS Code]: ").strip() or "VS Code"
                payload = {
                    "tool_name": "request_access",
                    "parameters": {"employee_id": "EMP-1001", "software_name": sw},
                }
            elif choice == "3":
                t_num = input("Enter ticket number [default: IT-8091]: ").strip() or "IT-8091"
                payload = {
                    "tool_name": "check_ticket",
                    "parameters": {"ticket_number": t_num},
                }
            elif choice == "4":
                sub = input("Enter ticket subject [default: Wi-Fi Disconnecting]: ").strip() or "Wi-Fi Disconnecting"
                payload = {
                    "tool_name": "create_ticket",
                    "parameters": {
                        "employee_id": "EMP-1001",
                        "subject": sub,
                        "description": "Voice caller reported wifi drops.",
                    },
                }
            elif choice == "5":
                payload = {
                    "tool_name": "escalate_issue",
                    "parameters": {"employee_id": "EMP-1001", "reason": "Repeated network outages."},
                }
            else:
                print("Invalid choice, please select 1-6.")
                continue

            try:
                headers = {"X-ElevenLabs-Secret": secret}
                print(f"\n[Sending Webhook Payload to {base_url}]...")
                response = client.post(base_url, json=payload, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    print("\n[ELEVENLABS TTS SPOKEN RESPONSE]:")
                    print(f" -> \"{data.get('response')}\"")
                else:
                    print(f"Error {response.status_code}: {response.text}")
            except Exception as e:
                print(f"Connection Error: Is the FastAPI server running on http://127.0.0.1:8000? Details: {e}")


if __name__ == "__main__":
    run_cli_simulator()
