# Deployment Guide: AI Voice IT Helpdesk Agent

This guide covers deploying the **AI Voice IT Helpdesk Agent** to production cloud platforms using **Supabase** (PostgreSQL) and **Render** (FastAPI Web Service).

---

## Architecture Overview

```
                        +---------------------------------+
                        |  ElevenLabs Playbook Cloud Agent|
                        +---------------------------------+
                                         |
                            (HTTPS Webhook Call)
                                         v
+--------------------------------------------------------------------------------+
| Render Web Service (FastAPI Server)                                            |
| Environment: PRODUCTION                                                        |
| Command: uvicorn backend.main:app --host 0.0.0.0 --port $PORT --workers 4     |
+--------------------------------------------------------------------------------+
                                         |
                             (Async PostgreSQL Driver)
                                         v
                        +---------------------------------+
                        |  Supabase PostgreSQL Cloud DB   |
                        +---------------------------------+
```

---

## Part 1: Provision Supabase Cloud Database (Free)

1. Create a free account at [Supabase.com](https://supabase.com).
2. Click **New Project** -> Name it `ai-voice-helpdesk`.
3. Set a strong database password.
4. Once provisioned, navigate to **Project Settings** -> **Database**.
5. Copy your Connection String under **URI** (Transaction Pooler):
   ```
   postgresql://postgres.xxx:password@aws-0-region.pooler.supabase.com:6543/postgres
   ```
6. Convert the prefix to SQLAlchemy Async format:
   ```
   postgresql+asyncpg://postgres.xxx:password@aws-0-region.pooler.supabase.com:6543/postgres
   ```

---

postgresql+asyncpg://postgres:[bJLr0&u20c@Pulkit]@db.gvlouhdsekerwehnlfin.supabase.co:5432/postgres
## Part 2: Deploy Backend to Render (Free)

1. Push your repository to GitHub.
2. Create a free account at [Render.com](https://render.com).
3. Click **New +** -> **Web Service** -> Connect your GitHub Repository.
4. Configure settings:
   - **Name**: `ai-voice-it-agent`
   - **Environment**: `Python 3`
   - **Region**: Select closest region to your location.
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT --workers 2`
5. Environment Variables:
   - `ENVIRONMENT` = `production`
   - `DEBUG` = `False`
   - `DATABASE_URL` = `<Your Supabase postgresql+asyncpg URL>`
   - `SECRET_KEY` = `<Generate random 64-char hex key>`
   - `ELEVENLABS_WEBHOOK_SECRET` = `<Your Secret Token>`
6. Click **Deploy Web Service**.

---

## Part 3: Configure ElevenLabs Playbook Agent

1. Log into your [ElevenLabs Dashboard](https://elevenlabs.io).
2. Navigate to **Conversational AI** -> **Agents** -> **Create New Agent**.
3. Import `playbooks/elevenlabs_agent_config.json`.
4. Set Webhook URL to your live Render endpoint:
   `https://ai-voice-it-agent.onrender.com/api/v1/elevenlabs/webhook`
5. Add custom header: `X-ElevenLabs-Secret: <Your Secret Token>`
6. Test your live agent via ElevenLabs web call widget or phone number binding!
