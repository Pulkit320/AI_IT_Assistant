# Phase 2: Database Design & Relational Modeling

## Phase Goal
The goal of Phase 2 is to design a normalized, production-grade relational database schema for the **AI Voice IT Helpdesk Agent**. Every voice interaction that triggers an action—such as checking ticket status, logging a password reset request, or requesting software access—must interact with a structured database.

In this phase, we implement our database ORM (Object-Relational Mapping) layer using **SQLAlchemy 2.0 Async** and design 5 core tables: `users`, `tickets`, `password_reset_logs`, `software_requests`, and `escalation_logs`.

---

## Concepts Introduced

### 1. Relational Database & PostgreSQL / Supabase
A **Relational Database Management System (RDBMS)** stores data in tables consisting of rows and columns. Relationships between entities are enforced using **Foreign Keys**. **Supabase** is an open-source Firebase alternative built on top of enterprise PostgreSQL.

### 2. Primary Keys & Foreign Keys
- **Primary Key (PK)**: A unique identifier for every record in a table (e.g. `user_id` or `ticket_id`).
- **Foreign Key (FK)**: A column in one table that references the Primary Key of another table (e.g. `employee_id` in `tickets` pointing to `users.employee_id`). Foreign keys enforce **Referential Integrity**.

### 3. Database Normalization (1NF, 2NF, 3NF)
Normalization is the process of structuring relational database columns to reduce data redundancy and eliminate anomalies:
- **First Normal Form (1NF)**: Every cell contains single, atomic values.
- **Second Normal Form (2NF)**: All non-key columns depend on the entire primary key.
- **Third Normal Form (3NF)**: Non-key columns depend ONLY on the primary key (no transitive dependencies).

### 4. SQLAlchemy 2.0 Async ORM
An **ORM (Object-Relational Mapper)** allows developers to interact with database tables using Python classes instead of writing raw SQL strings. Using SQLAlchemy's `async` session engine, database queries do not block the web server thread.

---

## Free-Tier Notes

- **Zero-Cost Flexibility**: The database engine is configured using a generic URL in `.env`:
  - For local development: `sqlite+aiosqlite:///./helpdesk.db` ($0.00 cost, zero setup required).
  - For Supabase / PostgreSQL free tier: `postgresql+asyncpg://user:pass@ep-xxx.supabase.co:5432/postgres` (Free tier provides 500MB storage).

---

## Database ER Diagram

```mermaid
erDiagram
    USERS ||--o{ TICKETS : "creates"
    USERS ||--o{ PASSWORD_RESET_LOGS : "requests"
    USERS ||--o{ SOFTWARE_REQUESTS : "requests"
    USERS ||--o{ ESCALATION_LOGS : "involved_in"
    TICKETS ||--o| ESCALATION_LOGS : "escalates_to"

    USERS {
        int id PK
        string employee_id UK
        string full_name
        string email UK
        string password_hash
        string department
        string role
        string security_answer
        datetime created_at
    }

    TICKETS {
        int id PK
        string ticket_number UK
        string employee_id FK
        string category
        string priority
        string status
        string subject
        string description
        string voice_summary
        datetime created_at
    }

    PASSWORD_RESET_LOGS {
        int id PK
        string employee_id FK
        string reset_token
        string status
        datetime requested_at
        datetime completed_at
    }

    SOFTWARE_REQUESTS {
        int id PK
        string employee_id FK
        string software_name
        string justification
        string approval_status
        datetime requested_at
    }

    ESCALATION_LOGS {
        int id PK
        int ticket_id FK
        string employee_id FK
        string reason
        string priority
        float sentiment_score
        datetime escalated_at
    }
```

---

## Folder Walkthrough

```
AI-Voice-IT-Agent/
├── docs/
│   ├── Phase-01.md
│   └── Phase-02.md            # This documentation file
├── backend/
│   ├── database/              # Database connections & session management
│   │   ├── connection.py      # Async SQLAlchemy engine & sessionmaker
│   │   ├── session.py         # FastAPI dependency injection for DB sessions
│   │   └── init_db.py         # Table creation & mock data seeder script
│   └── models/                # SQLAlchemy ORM model definitions
│       ├── base.py            # Declarative base & common timestamp mixin
│       ├── user.py            # User/Employee model
│       ├── ticket.py          # IT Ticket model
│       ├── password_reset_log.py # Password reset audit log model
│       ├── software_request.py   # Software request entitlement model
│       └── escalation_log.py  # Tier-2 Human escalation audit model
└── tests/
    └── test_database.py       # Database schema & seeder tests
```

---

## File & Code Walkthrough

### 1. `backend/models/base.py`
Provides `Base` and `TimestampMixin` so that all models automatically track `created_at` and `updated_at` timestamps in UTC.

### 2. `backend/database/connection.py`
Creates the asynchronous engine (`create_async_engine`) and session factory (`async_sessionmaker`).

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from backend.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
```

### 3. `backend/database/session.py`
FastAPI dependency generator yielding isolated DB sessions per HTTP request:

```python
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

---

## Data Flow Diagram

```
FastAPI Route Handler
      |
      | Depends(get_db)
      v
AsyncSession context created
      |
      | ORM Query (e.g. select(User).where(User.employee_id == 'EMP-1001'))
      v
SQLAlchemy Engine -> Driver (asyncpg or aiosqlite) -> Database Engine
      |
      | Returns database row
      v
Python Model Instance -> Conversion to Pydantic DTO Schema -> HTTP JSON
```

---

## What Was Learned & What Is Next

### Summary of What Was Learned:
- How to design 3NF normalized tables for enterprise IT systems.
- How to model one-to-many relationships in SQLAlchemy 2.0.
- How to use async database engines in Python to ensure non-blocking I/O.

### What Will Be Implemented Next:
In **Phase 3**, we will build the **Authentication & Mock Employee Directory** system. We will create employee verification services, login endpoints, password hashing utilities, and JWT (JSON Web Token) authentication dependencies.
