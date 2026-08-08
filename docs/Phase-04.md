# Phase 4: Ticket Management APIs (CRUD)

## Phase Goal
The goal of Phase 4 is to build the core **IT Ticket Management System** for the **AI Voice IT Helpdesk Agent**. Every enterprise IT helpdesk operates on tickets that record employee issues, track SLA (Service Level Agreement) progress, and record resolutions.

In this phase, we implement full **CRUD** (Create, Read, Update, Delete) endpoints with search and filtering capabilities.

---

## Concepts Introduced

### 1. CRUD Pattern
**CRUD** stands for the four basic operations of persistent storage:
- **C**reate: Inserting a new record (e.g. creating a new IT ticket).
- **R**ead: Querying existing records (e.g. retrieving ticket details or listing all tickets for an employee).
- **U**pdate: Modifying existing fields (e.g. changing ticket status to "In Progress" or "Resolved").
- **D**elete: Removing a record or marking it as soft-deleted.

### 2. HTTP Method Semantics & Status Codes
REST APIs map CRUD operations directly to standard HTTP verbs and status codes:
- `POST /api/v1/tickets`: Create a ticket -> Returns `201 Created`.
- `GET /api/v1/tickets/{ticket_number}`: Fetch ticket details -> Returns `200 OK` (or `404 Not Found`).
- `GET /api/v1/tickets?employee_id=EMP-1001&status=Open`: Filter tickets -> Returns `200 OK`.
- `PATCH /api/v1/tickets/{ticket_number}`: Partially update a ticket -> Returns `200 OK`.
- `DELETE /api/v1/tickets/{ticket_number}`: Delete a ticket -> Returns `200 OK` or `204 No Content`.

### 3. Path Parameters vs Query Parameters
- **Path Parameters**: Used to identify a specific resource uniquely (e.g. `/tickets/IT-8091`).
- **Query Parameters**: Used to filter, sort, or paginate collections (e.g. `/tickets?category=Software&limit=10`).

---

## Free-Tier Notes

- **Zero API Costs**: All ticket management logic runs against your local database or free Supabase instance without external API fees.

---

## Folder Walkthrough

```
AI-Voice-IT-Agent/
├── docs/
│   ├── Phase-01.md
│   ├── Phase-02.md
│   ├── Phase-03.md
│   └── Phase-04.md            # This documentation file
├── backend/
│   ├── api/
│   │   └── v1/
│   │       └── tickets.py     # Ticket CRUD REST endpoints
│   ├── schemas/
│   │   └── ticket.py          # Pydantic request & response DTO schemas
│   └── services/
│       └── ticket_service.py  # Ticket business logic & database queries
└── tests/
    └── test_tickets.py        # Automated CRUD unit & integration tests
```

---

## File & Code Walkthrough

### 1. `backend/schemas/ticket.py`
Defines input models (`TicketCreate`, `TicketUpdate`) and output response model (`TicketRead`).

```python
class TicketCreate(BaseModel):
    employee_id: str
    subject: str
    description: str
    category: str = "General IT"
    priority: str = "Medium"
```

### 2. `backend/services/ticket_service.py`
Contains async functions to:
- Generate unique ticket numbers (e.g. `IT-8492`).
- Query tickets by employee ID, ticket number, or keyword.
- Update ticket status and voice summaries.

### 3. `backend/api/v1/tickets.py`
Provides FastAPI endpoints enforcing validation and returning formatted HTTP responses.

---

## Data Flow Diagram

```
User / Voice Agent
      |
      | POST /api/v1/tickets {"employee_id": "EMP-1001", "subject": "VPN Disconnecting"}
      v
Tickets Controller (tickets.py)
      |
      | Calls TicketService.create_ticket()
      v
Ticket Service -> Generates IT-XXXX number -> Saves to database
      |
      | Returns Ticket ORM instance
      v
Pydantic Serializer -> Formats TicketRead schema -> Returns HTTP 201 JSON
```

---

## What Was Learned & What Is Next

### Summary of What Was Learned:
- How to design RESTful endpoints adhering to HTTP standards.
- How to write SQLAlchemy async query filters with multiple optional conditions.
- How to separate route controllers from database service methods.

### What Will Be Implemented Next:
In **Phase 5**, we will implement the **Identity-Verified Password Reset Workflow**. We will create reset endpoints, audit logs, and voice-optimized credential confirmation responses.
