# Quickstart Setup Guide: AI Voice IT Helpdesk Agent

Follow this step-by-step guide to clone, configure, and run the **AI Voice IT Helpdesk Agent** locally on your computer in under 5 minutes.

---

## Prerequisites
- **Python**: Python 3.10, 3.11, or 3.12 installed.
- **Git**: Installed.
- **Terminal / Shell**: Bash, Zsh, or PowerShell.

---

## Step 1: Clone Repository & Create Virtual Environment

```bash
# Clone the repository
git clone https://github.com/your-username/AI-Voice-IT-Agent.git
cd AI-Voice-IT-Agent

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux / macOS:
source venv/bin/activate
# On Windows PowerShell:
# .\venv\Scripts\Activate.ps1
```

---

## Step 2: Install Python Dependencies

```bash
# Upgrade pip and install required dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Step 3: Configure Environment Variables

Copy `.env.example` to create your local `.env` file:

```bash
cp .env.example .env
```

By default, `.env` is configured for **100% Free Local Execution**:
- `DATABASE_URL="sqlite+aiosqlite:///./helpdesk.db"`
- `USE_MOCK_LLM=True`
- `ELEVENLABS_WEBHOOK_SECRET="sample-webhook-secret-key"`

---

## Step 4: Initialize Database & Seed Test Employees

Run the database initialization script to create tables and seed mock employees (`EMP-1001`, `EMP-1002`, `EMP-1003`):

```bash
python3 -m backend.database.init_db
```

Output:
```
{"timestamp": "...", "level": "INFO", "message": "Database tables initialized successfully."}
{"timestamp": "...", "level": "INFO", "message": "Mock database seeded with 3 users and 1 sample ticket."}
```

---

## Step 5: Start the FastAPI Server

Launch the Uvicorn web server:

```bash
uvicorn backend.main:app --reload --port 8000
```

Open your browser and navigate to:
- **Interactive OpenAPI Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Health Diagnostic Check**: [http://127.0.0.1:8000/api/v1/health](http://127.0.0.1:8000/api/v1/health)

---

## Step 6: Test Voice Webhooks via Interactive CLI Simulator

Open a second terminal window (leaving the server running) and run:

```bash
python3 playbooks/voice_cli_simulator.py
```

Select options `1-5` to test Password Resets, Software Requests, Ticket Status Checks, and Escalations in real time!

---

## Step 7: Run Automated Tests

To verify all 15 implementation phases, run Pytest:

```bash
pytest -v
```
