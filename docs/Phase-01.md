# Phase 1: Project Initialization & FastAPI Foundation

## Phase Goal
The goal of Phase 1 is to establish a solid, production-ready project foundation for the **AI Voice IT Helpdesk Agent**. Every enterprise AI application requires a robust backend server capable of executing secure actions—such as checking database states, resetting passwords, and issuing API calls—that artificial intelligence models (like GPT-5 or ElevenLabs voice agents) cannot execute directly.

In this phase, we initialize the project structure, configure Python dependency management, set up structured logging, implement environment variable management, and expose our first FastAPI HTTP endpoints (`/` and `/health`).

---

## Concepts Introduced

### 1. Web API & REST
A **Web API** (Application Programming Interface) allows two software systems to communicate over HTTP (HyperText Transfer Protocol). In our system, the voice agent sends HTTP requests to our backend API when it needs to look up an employee or create a ticket.

### 2. FastAPI & ASGI
**FastAPI** is a high-performance Python web framework for building APIs. It is built on top of **Starlette** (for web routing) and **Pydantic** (for data validation). FastAPI runs on an **ASGI** (Asynchronous Server Gateway Interface) web server called **Uvicorn**, which allows the server to process hundreds of concurrent requests efficiently using Python's `async` and `await` keywords.

### 3. Environment Variables & `.env`
Enterprise applications never hardcode passwords, API keys, or database URLs in source code. We use environment variables loaded from a `.env` file via `pydantic-settings`. This allows the exact same code to run in development, testing, and production environments with different configurations.

### 4. Structured JSON Logging
Rather than using basic `print()` statements, enterprise servers output structured JSON logs. Structured logs include timestamps, log levels (INFO, WARNING, ERROR), module names, and request IDs, making it easy for search tools like Datadog or CloudWatch to index and search application logs.

---

## Free-Tier Notes

- **Hosting & Local Execution**: FastAPI and Uvicorn run locally on your computer for **$0.00**.
- **No Paid Dependencies**: All packages used in this phase (`fastapi`, `uvicorn`, `pydantic-settings`, `pytest`) are open-source and free.

---

## Folder Walkthrough

```
AI-Voice-IT-Agent/
├── docs/
│   └── Phase-01.md            # This documentation file
├── backend/
│   ├── api/                   # API routes and controllers
│   │   ├── v1/                # Version 1 API endpoints
│   │   │   └── health.py      # Health check endpoint
│   │   └── router.py          # Main router linking all endpoint modules
│   ├── config.py              # Environment configuration loader
│   ├── logging_config.py      # Structured logger setup
│   └── main.py                # FastAPI application entrypoint
├── tests/                     # Automated test suite
│   ├── conftest.py            # Pytest test fixtures
│   └── test_health.py         # Health endpoint unit test
├── .env.example               # Example environment variable file
├── .gitignore                 # Files excluded from Git version control
├── requirements.txt           # Python dependency requirements
└── README.md                  # Project landing page
```

---

## File & Code Walkthrough

### 1. `backend/config.py`
Loads settings from environment variables with default fallbacks using Pydantic's `BaseSettings`.

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Voice IT Helpdesk Agent"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### 2. `backend/logging_config.py`
Sets up a custom JSON logger using Python's standard `logging` library. Every log entry outputs clean JSON:

```json
{"timestamp": "2026-08-07T22:00:00", "level": "INFO", "message": "FastAPI Application Started"}
```

### 3. `backend/main.py`
Initializes the `FastAPI` instance, configures CORS middleware, attaches global routers, and registers lifecycle startup/shutdown events.

### 4. `backend/api/v1/health.py`
Defines the GET `/api/v1/health` diagnostic endpoint. It returns a `200 OK` JSON response indicating that the server is operational:

```json
{
  "status": "healthy",
  "project": "AI Voice IT Helpdesk Agent",
  "version": "1.0.0",
  "environment": "development"
}
```

---

## Data Flow Diagram

```
User / Voice Agent
      |
      | HTTP GET /api/v1/health
      v
FastAPI App (main.py)
      |
      | Directs request to router.py
      v
Health Controller (health.py)
      |
      | Returns Pydantic schema dictionary
      v
HTTP 200 JSON Response -> {"status": "healthy", ...}
```

---

## What Was Learned & What Is Next

### Summary of What Was Learned:
- How to set up a clean Python project structure for backend APIs.
- How FastAPI processes HTTP requests asynchronously.
- How to use Pydantic for type-safe environment configuration.
- How to write structured logs and test endpoints using `pytest`.

### What Will Be Implemented Next:
In **Phase 2**, we will design and implement the **Relational Database Schema** using PostgreSQL and SQLAlchemy 2.0 Async ORM. We will build tables for Users, Tickets, Password Reset Logs, Software Requests, and Escalation Logs.
