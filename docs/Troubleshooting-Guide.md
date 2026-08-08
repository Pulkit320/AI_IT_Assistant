# Troubleshooting & Debugging Guide: AI Voice IT Helpdesk Agent

This guide addresses common issues, error codes, and resolution steps when building or running the **AI Voice IT Helpdesk Agent**.

---

## 1. Environment & Dependency Issues

### Problem: `ImportError: email-validator is not installed`
- **Cause**: Pydantic EmailStr validation requires the `email-validator` package.
- **Fix**: Run `./venv/bin/pip install email-validator==2.1.1`.

### Problem: `ValueError: password cannot be longer than 72 bytes` or `passlib bcrypt version error`
- **Cause**: In Python 3.12, `passlib` has a compatibility bug with `bcrypt>=4.1.0`.
- **Fix**: Pin `bcrypt==4.0.1` in `requirements.txt` (`./venv/bin/pip install bcrypt==4.0.1`).

---

## 2. Database Connection Issues

### Problem: `sqlite3.OperationalError: no such table: users`
- **Cause**: Database tables have not been created yet.
- **Fix**: Run the initialization script: `python3 -m backend.database.init_db`.

### Problem: `asyncpg.exceptions.InvalidPasswordError` when connecting to Supabase
- **Cause**: Incorrect database password or unescaped special characters in connection URL.
- **Fix**: Ensure your `DATABASE_URL` in `.env` uses `postgresql+asyncpg://` and special characters in passwords (like `#` or `@`) are URL-encoded.

---

## 3. ElevenLabs & Voice Webhook Issues

### Problem: `401 Unauthorized - Invalid or missing ElevenLabs webhook secret header`
- **Cause**: The incoming request is missing the `X-ElevenLabs-Secret` header or the value does not match `ELEVENLABS_WEBHOOK_SECRET` in `.env`.
- **Fix**: Verify header name is `X-ElevenLabs-Secret` and matches `.env`. For local CLI testing, use `playbooks/voice_cli_simulator.py`.

### Problem: High Voice Latency (> 2 seconds)
- **Cause**: Database queries or external LLM calls are taking too long.
- **Fix**: Enable `USE_MOCK_LLM=True` for sub-50ms tool executions, and ensure SQLite/PostgreSQL indexes are built on `employee_id` and `ticket_number`.

---

## 4. Log Inspection Commands

Inspect server logs in real time:

```bash
# View structured JSON server logs
tail -f helpdesk.log

# Extract error log entries using grep
grep '"level": "ERROR"' helpdesk.log
```
