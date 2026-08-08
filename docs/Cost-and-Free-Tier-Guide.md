# Cost & Free-Tier Guide: AI Voice IT Helpdesk Agent

> [!IMPORTANT]
> **Free-Tier Confirmation**: This entire project has been designed and engineered so that any student or developer can build, run, test, and understand the complete Voice AI system **using only free-tier services or built-in local open-source fallbacks**. No credit card is required.

---

## Service Cost Matrix

| Technology / Component | Selected Platform | Free Tier Quota / Features | Free Alternative / Fallback | Estimated Cost Exceeding Free Tier |
| :--- | :--- | :--- | :--- | :--- |
| **Backend Web Server** | FastAPI / Uvicorn | Unlimited local execution | Local Python Virtual Environment (`venv`) | $0.00 (Local) / ~$5/mo (Render) |
| **Relational Database** | PostgreSQL / Supabase | 500 MB database, unlimited queries | Local SQLite Async (`helpdesk.db`) | $0.00 (Local & Supabase Free) |
| **LLM Reasoning & Function Calling** | GPT-5 / OpenAI | OpenAI $5 free trial credits (when available) | Built-in zero-cost **Mock LLM Engine** (`USE_MOCK_LLM=True`) | $0.00 (Mock Engine) / Pay-per-token |
| **Voice Speech & Agent Webhooks** | ElevenLabs Playbooks | 10,000 free characters / month | Built-in zero-cost **CLI Voice Simulator** (`voice_cli_simulator.py`) | $0.00 (Simulator) / ~$5/mo |
| **Authentication & JWT** | Python JOSE / PassLib | Unlimited local stateless JWT tokens | Built-in Bcrypt & JWT algorithms | $0.00 |
| **Automated Testing Suite** | Pytest / HTTPX Async | Unlimited local test runs | Local Pytest execution | $0.00 |

---

## Free-Tier Limitations & Built-in Fallback Strategies

### 1. ElevenLabs Free-Tier Voice Minutes
- **Limitation**: ElevenLabs free tier provides 10,000 text-to-speech characters per month (~10-15 minutes of voice calling).
- **Fallback Solution**: Use the included **Local CLI Voice Agent Simulator** (`playbooks/voice_cli_simulator.py`). It sends identical HTTP JSON webhook payloads to your local FastAPI server and prints spoken agent text responses directly in your terminal. You can test infinite voice interactions without consuming ElevenLabs credits!

### 2. OpenAI / GPT-5 API Key Limitations
- **Limitation**: OpenAI requires a credit card once free trial grants expire.
- **Fallback Solution**: Set `USE_MOCK_LLM=True` in `.env`. The backend activates an intelligent intent parsing engine that dispatches tools (`create_ticket`, `password_reset`, `request_access`, `check_ticket`, `escalate_issue`) deterministically for **$0.00**.

### 3. PostgreSQL Cloud Database Limits
- **Limitation**: Supabase free databases pause after 1 week of inactivity.
- **Fallback Solution**: Use `DATABASE_URL="sqlite+aiosqlite:///./helpdesk.db"` in `.env`. SQLite runs locally on your hard drive with zero cloud configuration required.

---

## Recommended Self-Hosted Open-Source Alternatives

If you want to scale this application in production using 100% open-source software:
- **LLM Engine**: Replace OpenAI with Ollama or vLLM running `Llama-3.1-8B-Instruct`.
- **Speech-to-Text (STT)**: Replace ElevenLabs STT with OpenAI Whisper Local (`faster-whisper`).
- **Text-to-Speech (TTS)**: Replace ElevenLabs TTS with Coqui TTS or Piper TTS.
- **Database**: Run PostgreSQL locally via Docker (`docker run -p 5432:5432 postgres:16`).

---

## Confirmation Statement
We confirm that a college student with zero budget can clone this repository, follow the phase-by-phase documentation, run the automated test suite, and interact with the Voice AI Helpdesk Agent using only free-tier services or the documented open-source fallbacks.
