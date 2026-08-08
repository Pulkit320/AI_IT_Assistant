# Phase 3: Authentication & Mock Employee Directory

## Phase Goal
The goal of Phase 3 is to establish an **Employee Verification and Authentication System** for the **AI Voice IT Helpdesk Agent**. In any enterprise IT application, before an automated voice agent can perform high-privilege actions (like resetting a password or modifying system access), it must verify the caller's identity against the enterprise Employee Directory.

In this phase, we implement identity verification services, password hashing with Bcrypt, JWT (JSON Web Token) generation, and authentication dependencies to protect API endpoints.

---

## Concepts Introduced

### 1. Authentication (AuthN) vs Authorization (AuthZ)
- **Authentication (Who are you?)**: Verifying that users are who they claim to be (e.g. checking Employee ID and Password or Security Question).
- **Authorization (What are you allowed to do?)**: Verifying that an authenticated user has permission to perform a specific action (e.g. an standard Employee cannot access Administrator settings).

### 2. Session-Based vs Token-Based Authentication
- **Session-Based Auth**: The server creates a session record in a database/Redis and returns a session ID cookie to the client. Every request requires a database lookup to validate the session ID.
- **Token-Based Auth (JWT)**: The server signs a self-contained cryptographic payload (JSON Web Token) and returns it to the client. The server can validate the token on subsequent requests **statelessly** without querying the database every time.

### 3. JSON Web Token (JWT) Anatomy
A JWT string consists of three parts separated by dots (`.`): `Header.Payload.Signature`
1. **Header**: Specifies the hashing algorithm (e.g., HS256) and token type (`JWT`).
2. **Payload**: Contains claims such as user ID, employee ID, expiration timestamp (`exp`), and role.
3. **Signature**: Cryptographic signature calculated by hashing `Header + Payload` with the server's secret key (`SECRET_KEY`). If a malicious user tampers with the payload, the signature verification fails instantly.

---

## Free-Tier Notes

- **Stateless & Local**: JWT token generation and Bcrypt password hashing take place entirely in memory. No external identity providers (like Auth0 or Okta) are required, preserving **100% free local execution**.

---

## Folder Walkthrough

```
AI-Voice-IT-Agent/
├── docs/
│   ├── Phase-01.md
│   ├── Phase-02.md
│   └── Phase-03.md            # This documentation file
├── backend/
│   ├── api/
│   │   └── v1/
│   │       └── auth.py        # Login & employee verification endpoint
│   ├── schemas/
│   │   └── user.py            # Pydantic schemas for authentication
│   ├── services/
│   │   └── auth_service.py    # Employee verification & credential check logic
│   └── utils/
│       └── security.py        # Bcrypt hashing & JWT encode/decode helpers
└── tests/
    └── test_auth.py           # Unit & integration tests for Auth & JWT
```

---

## File & Code Walkthrough

### 1. `backend/utils/security.py`
Contains helper functions for hashing passwords using `passlib[bcrypt]` and generating/decoding JWT access tokens using `python-jose`:

```python
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=60))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
```

### 2. `backend/services/auth_service.py`
Provides logic to:
- Authenticate employee credentials against database users.
- Verify security questions for voice-based out-of-band verification.

### 3. `backend/api/v1/auth.py`
Exposes the POST `/api/v1/auth/login` endpoint and the POST `/api/v1/auth/verify-employee` endpoint designed for quick voice verification.

---

## Data Flow Diagram

```
Employee / Voice Agent
      |
      | POST /api/v1/auth/login (employee_id, password)
      v
FastAPI Auth Controller (auth.py)
      |
      | Calls AuthService.authenticate_employee()
      v
Auth Service -> Queries User table -> Verifies Bcrypt hash
      |
      | Returns user entity
      v
Security Helper -> Encodes JWT Token -> Returns {"access_token": "ey...", "token_type": "bearer"}
```

---

## What Was Learned & What Is Next

### Summary of What Was Learned:
- The difference between Session and Token authentication.
- How JWT signatures prevent token tampering.
- How to write FastAPI dependency injection functions to extract and validate bearer tokens from incoming requests.

### What Will Be Implemented Next:
In **Phase 4**, we will implement **Ticket Management APIs (CRUD)**. We will build endpoints to create, view, search, update, and delete IT support tickets.
