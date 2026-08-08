# AI Voice IT Helpdesk Agent

A production-inspired, progressive educational repository that teaches how to build an enterprise **Voice AI IT Support System** from scratch using **FastAPI, Python, PostgreSQL/Supabase, GPT-5 Function Calling, and ElevenLabs Playbooks**.

> [!TIP]
> **100% Free-Tier & Zero-Cost Buildability**: This entire repository is executable and testable without entering a credit card or buying API tokens. It includes a local zero-cost **Mock LLM Provider Engine**, an interactive **CLI Voice Agent Simulator**, and local **SQLite Async** support!

---

## Technical Stack

- **Core Backend**: Python 3.10+ & FastAPI
- **ASGI Web Server**: Uvicorn
- **Database & ORM**: PostgreSQL / Supabase with SQLAlchemy 2.0 Async & Asyncpg (with SQLite local fallback)
- **AI Tool Execution**: GPT-5 / GPT-4o Function Calling (with Mock LLM Engine)
- **Voice Agent Protocol**: ElevenLabs Conversational AI Playbook Webhooks
- **Authentication**: JWT Tokens (Python JOSE) & Password Hashing (Bcrypt)
- **Data Validation**: Pydantic v2 & Pydantic Settings
- **Testing**: Pytest & HTTPX Async

---

## Capabilities & Workflows

1. **Employee Identity Verification**: Voice-optimized security answer validation against enterprise directory.
2. **Identity-Verified Password Reset**: Out-of-band credential reset link dispatch and audit logging into `password_reset_logs`.
3. **Software Access Request Engine**: Rule engine auto-approving standard tools (VS Code, Slack) and routing privileged tools (Docker, GitHub, Jira) to manager queues.
4. **Ticket Management (CRUD)**: Create, view, update, delete, search, and list IT tickets.
5. **Speech-Optimized Ticket Status**: Formats complex ticket records into natural spoken text for ElevenLabs Text-to-Speech (TTS).
6. **Intelligent Human Escalation**: Heuristic sentiment score calculation, urgency priority assignment, and Tier-2 human agent handoff.

---

## 15-Phase Progressive Learning Curriculum

Every phase includes dedicated beginner-friendly documentation explaining technical concepts, folder structures, file walkthroughs, data flow diagrams, code line-by-line breakdowns, and what was learned:

- [Phase 1: Project Initialization & FastAPI Foundation](docs/Phase-01.md)
- [Phase 2: Database Design & Relational Modeling](docs/Phase-02.md)
- [Phase 3: Employee Verification & JWT Authentication](docs/Phase-03.md)
- [Phase 4: RESTful Ticket Management APIs (CRUD)](docs/Phase-04.md)
- [Phase 5: Identity-Verified Password Reset Workflow](docs/Phase-05.md)
- [Phase 6: Software Access Workflow & Approval Engine](docs/Phase-06.md)
- [Phase 7: Ticket Status Lookup & Voice Response Formatting](docs/Phase-07.md)
- [Phase 8: GPT-5 Function Calling & LLM Abstraction Layer](docs/Phase-08.md)
- [Phase 9: ElevenLabs Playbooks & Webhooks Integration](docs/Phase-09.md)
- [Phase 10: Conversation Design & System Playbooks](docs/Phase-10.md)
- [Phase 11: Intelligent Human Escalation System](docs/Phase-11.md)
- [Phase 12: Enterprise Structured Logging & Monitoring](docs/Phase-12.md)
- [Phase 13: Error Handling & Graceful Degradation](docs/Phase-13.md)
- [Phase 14: Comprehensive Automated Testing Suite](docs/Phase-14.md)
- [Phase 15: Deployment, Free-Tier & Production Operations](docs/Phase-15.md)

---

## Quickstart Installation

```bash
# 1. Clone repository
git clone https://github.com/your-username/AI-Voice-IT-Agent.git
cd AI-Voice-IT-Agent

# 2. Set up Python virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment configuration
cp .env.example .env

# 5. Initialize database & seed test employees
python3 -m backend.database.init_db

# 6. Launch FastAPI server
uvicorn backend.main.app --reload --port 8000
```

Access Swagger OpenAPI documentation at: `http://127.0.0.1:8000/docs`

---

## Testing Voice Webhooks (Zero-Cost CLI Simulator)

In a separate terminal window, run the local voice agent simulator:

```bash
python3 playbooks/voice_cli_simulator.py
```

---

## Running the Automated Test Suite

Run all 26 unit, integration, and voice webhook tests:

```bash
pytest -v
```

---

## Documentation & Diagram Index

- [GitHub Push & Repository Guide](docs/GitHub-Push-Guide.md)
- [Cost & Free-Tier Guide](docs/Cost-and-Free-Tier-Guide.md)
- [Quickstart Setup Guide](docs/Setup-Guide.md)
- [Cloud Deployment Guide](docs/Deployment-Guide.md)
- [Troubleshooting & Debugging Guide](docs/Troubleshooting-Guide.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
- [System Architecture Diagram](diagrams/architecture.mermaid)
- [Database ER Diagram](diagrams/er_diagram.mermaid)
- [Voice Request Sequence Diagram](diagrams/sequence_diagram.mermaid)
- [Voice Interaction Flowchart](diagrams/voice_interaction_flow.mermaid)

---

## License & Attribution
Designed for educational purposes as an enterprise-grade Voice AI reference implementation. Distributed under the [MIT License](LICENSE).

