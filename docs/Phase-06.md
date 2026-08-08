# Phase 6: Software Access Workflow & Approval Engine

## Phase Goal
The goal of Phase 6 is to build a **Software Access Request & Entitlement System** for the **AI Voice IT Helpdesk Agent**. Software provisioning is another major responsibility of IT helpdesks. Employees frequently request software licenses, developer tools, and SaaS application access via telephone or chat.

In this phase, we implement a software request endpoint, a software entitlement database model, and an automated rule-based approval engine that auto-approves standard tools while routing privileged software to manager queues.

---

## Concepts Introduced

### 1. Rule-Based Business Engines
A **Rule Engine** evaluates incoming request metadata (software name, employee department, software license cost) against predefined business policies.
- **Auto-Approval Policy**: Standard tools (e.g. VS Code, Slack) carry zero licensing cost or security risk and are approved instantly by the voice agent.
- **Manager Approval Policy**: Restricted tools (e.g. Docker Pro, GitHub Enterprise, Jira Admin access) create a pending entitlement record requiring explicit approval from the employee's manager.

### 2. Supported Software Catalog
Our system defines a catalog of corporate software assets:
- `VS Code`: Standard IDE -> Auto-Approved
- `Slack`: Communication -> Auto-Approved
- `Docker Desktop`: Containerization -> Manager Approval Required
- `GitHub`: Source Control -> Manager Approval Required
- `Jira`: Project Tracking -> Manager Approval Required

---

## Free-Tier Notes

- **Zero License Server Costs**: Provisioning workflows interact with our internal relational database. External API calls to Okta, LDAP, or Active Directory are simulated, enabling **100% free execution**.

---

## Folder Walkthrough

```
AI-Voice-IT-Agent/
├── docs/
│   ├── Phase-01.md
│   ├── Phase-02.md
│   ├── Phase-03.md
│   ├── Phase-04.md
│   ├── Phase-05.md
│   └── Phase-06.md            # This documentation file
├── backend/
│   ├── api/
│   │   └── v1/
│   │       └── software_access.py # Software request & list endpoints
│   ├── schemas/
│   │   └── software_request.py# Pydantic software schemas
│   └── services/
│       └── software_service.py# Rule engine & database logic
└── tests/
    └── test_software_access.py# Software entitlement unit tests
```

---

## File & Code Walkthrough

### 1. `backend/schemas/software_request.py`
Defines `SoftwareAccessRequest` and `SoftwareAccessResponse`.

### 2. `backend/services/software_service.py`
Evaluates software entitlement policies:

```python
AUTO_APPROVED_SOFTWARE = {"vs code", "vscode", "slack", "zoom"}

def evaluate_approval(software_name: str) -> str:
    if software_name.lower().strip() in AUTO_APPROVED_SOFTWARE:
        return "Auto-Approved"
    return "Pending Manager Approval"
```

---

## Data Flow Diagram

```
Employee / Voice Agent
      |
      | POST /api/v1/software-access/request {"employee_id": "EMP-1001", "software_name": "VS Code"}
      v
Software Controller (software_access.py)
      |
      | Calls SoftwareService.process_software_request()
      v
Rule Engine -> Evaluates policy for "VS Code" -> "Auto-Approved"
      |
      | Saves entitlement to software_requests table
      v
Returns Voice Response -> "Access to VS Code has been approved immediately. License assigned."
```

---

## What Was Learned & What Is Next

### Summary of What Was Learned:
- How to implement business policy rule engines in Python backend services.
- How to manage entitlement lifecycles in relational databases.
- How to communicate entitlement status clearly to voice agents.

### What Will Be Implemented Next:
In **Phase 7**, we will implement **Voice-Optimized Ticket Status Search**. We will construct lookups that transform raw database rows into speech-ready status strings optimized for ElevenLabs text-to-speech synthesis.
