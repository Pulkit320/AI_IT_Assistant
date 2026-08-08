# Phase 5: Password Reset Workflow

## Phase Goal
The goal of Phase 5 is to implement an **Identity-Verified Password Reset Workflow** for the **AI Voice IT Helpdesk Agent**. Password resets represent over 30% of IT helpdesk call volume in enterprise organizations. Automating password resets via voice saves significant support overhead while maintaining strict security controls.

In this phase, we build a password reset engine that verifies employee security identity, logs an audit entry into `password_reset_logs`, generates a secure temporary reset token, and formats a voice-optimized response.

---

## Concepts Introduced

### 1. Why Password Resets Are Mocked in Voice AI
In modern enterprise security architecture:
- An automated voice AI agent **NEVER** speaks a user's new raw password out loud over the telephone or browser voice channel.
- Speaking credentials aloud poses severe eavesdropping and recording risks.
- Instead, the voice agent verifies identity, triggers an out-of-band reset workflow (e.g. sending a secure one-time magic link or PIN to the employee's registered corporate email/SMS), and confirms execution in natural language.

### 2. Out-of-Band Security & Verification
**Out-of-Band (OOB) authentication** uses two separate channels to complete a transaction. The caller interacts via the **Voice Channel** (Phone call), but the credential reset token is delivered via an independent **Email / Mobile Channel**.

### 3. Security Audit Logging
Every password reset request must create a permanent immutable record in `password_reset_logs` recording the requesting `employee_id`, `reset_token`, timestamp, and execution status (`Requested` or `Completed`).

---

## Free-Tier Notes

- **Zero Third-Party SMS/Email Fees**: To preserve 100% free local execution for students, email dispatch is simulated via logger outputs and mock token generators. No Twilio or SendGrid account is required.

---

## Folder Walkthrough

```
AI-Voice-IT-Agent/
├── docs/
│   ├── Phase-01.md
│   ├── Phase-02.md
│   ├── Phase-03.md
│   ├── Phase-04.md
│   └── Phase-05.md            # This documentation file
├── backend/
│   ├── api/
│   │   └── v1/
│   │       └── password_reset.py # Password reset endpoint
│   ├── schemas/
│   │   └── password_reset.py  # Pydantic password reset schemas
│   └── services/
│       └── password_reset_service.py # Reset validation & audit logging logic
└── tests/
    └── test_password_reset.py # Password reset unit tests
```

---

## File & Code Walkthrough

### 1. `backend/schemas/password_reset.py`
Defines `PasswordResetRequest` and `PasswordResetResponse`.

```python
class PasswordResetRequest(BaseModel):
    employee_id: str
    security_answer: Optional[str] = None

class PasswordResetResponse(BaseModel):
    success: bool
    employee_id: str
    full_name: str
    reset_token: str
    voice_message: str
```

### 2. `backend/services/password_reset_service.py`
Validates employee existence, checks security answers, inserts a row into `PasswordResetLog`, and formats speech text.

---

## Data Flow Diagram

```
Employee / Voice Agent
      |
      | POST /api/v1/password-reset {"employee_id": "EMP-1001", "security_answer": "Austin"}
      v
Password Reset Controller (password_reset.py)
      |
      | Calls PasswordResetService.process_password_reset()
      v
Password Reset Service -> Verifies identity -> Inserts record into PasswordResetLog table
      |
      | Generates mock token (e.g. RESET-948271)
      v
Returns Voice Response -> "Password reset link sent to sarah.jenkins@company.com"
```

---

## What Was Learned & What Is Next

### Summary of What Was Learned:
- Why credentials should never be spoken over voice channels.
- How out-of-band verification maintains enterprise compliance.
- How to record security audit logs in relational databases.

### What Will Be Implemented Next:
In **Phase 6**, we will implement the **Software Access Workflow**. We will create endpoints supporting requests for software like VS Code, Docker, Slack, GitHub, and Jira with an automated approval rules engine.
