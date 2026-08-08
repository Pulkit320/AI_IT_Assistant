# Phase 8: GPT-5 Function Calling & LLM Abstraction Layer

## Phase Goal
The goal of Phase 8 is to implement **GPT-5 Function Calling and LLM Tool Execution** for the **AI Voice IT Helpdesk Agent**. While Large Language Models (LLMs) excel at natural language understanding and conversation, they cannot directly read or modify external databases.

In this phase, we construct an LLM Abstraction Layer, define standardized JSON schemas for 5 tool capabilities (`create_ticket`, `password_reset`, `request_access`, `check_ticket`, `escalate_issue`), build a tool execution dispatcher, and implement a zero-cost Mock LLM provider engine.

---

## Concepts Introduced

### 1. Function Calling / Tool Calling
**Function Calling** is a technique where an LLM is provided with structured JSON schemas describing available backend functions. When a user asks a question requiring an action (e.g. "Can you reset my password for employee EMP-1001?"), the LLM chooses NOT to generate plain text, but instead outputs a structured JSON tool call payload specifying function name and arguments:

```json
{
  "tool_name": "password_reset",
  "arguments": {
    "employee_id": "EMP-1001",
    "security_answer": "Austin"
  }
}
```

### 2. Why LLMs Never Access Databases Directly
Security and safety rules dictate that an AI model must **NEVER** possess direct database access or execute raw SQL queries. If an LLM had direct SQL access, prompt injection attacks could trick the model into dropping tables or exfiltrating employee passwords.
Instead, the LLM acts as an intelligent router: it requests backend tools, and our FastAPI server validates parameters, enforces authorization rules, and executes controlled SQL queries safely.

### 3. LLM Abstraction Layer & Zero-Cost Mock Engine
To ensure students can build, test, and run 100% of this project without purchasing OpenAI API credits, our architecture includes a dual-mode LLM service (`backend/services/gpt_service.py`):
- If `USE_MOCK_LLM=True` (default), the server uses a deterministic intent classifier to select tools locally for **$0.00**.
- If `USE_MOCK_LLM=False` and `OPENAI_API_KEY` is provided, it calls OpenAI's GPT-5 / GPT-4o function calling API.

---

## Free-Tier Notes

- **Zero API Expenses**: The built-in Mock LLM Engine parses intent, extracts parameters, and dispatches tool functions locally without spending any money on LLM API tokens.

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
│   ├── Phase-06.md
│   ├── Phase-07.md
│   └── Phase-08.md            # This documentation file
├── backend/
│   ├── api/
│   │   └── v1/
│   │       └── gpt_tools.py   # Tool execution REST endpoint
│   ├── schemas/
│   │   └── gpt_tools.py       # Tool request & response Pydantic models
│   └── services/
│       └── gpt_service.py     # LLM tool dispatcher & Mock engine
├── playbooks/
│   └── tool_definitions.json  # Standardized OpenAI JSON schemas
└── tests/
    └── test_gpt_tools.py      # LLM tool execution unit tests
```

---

## Tool Definitions Schema (`playbooks/tool_definitions.json`)

```json
[
  {
    "name": "create_ticket",
    "description": "Creates an IT support ticket for an employee.",
    "parameters": {
      "type": "object",
      "properties": {
        "employee_id": {"type": "string"},
        "subject": {"type": "string"},
        "description": {"type": "string"},
        "category": {"type": "string"}
      },
      "required": ["employee_id", "subject", "description"]
    }
  },
  {
    "name": "password_reset",
    "description": "Requests an identity-verified password reset for an employee.",
    "parameters": {
      "type": "object",
      "properties": {
        "employee_id": {"type": "string"},
        "security_answer": {"type": "string"}
      },
      "required": ["employee_id"]
    }
  }
]
```

---

## Data Flow Diagram

```
User Voice Request: "I need Docker Desktop for microservices development"
      |
      v
GPT-5 / Mock LLM Engine
      |
      | Selects tool: request_access({"employee_id": "EMP-1001", "software_name": "Docker"})
      v
POST /api/v1/gpt/execute-tool Payload
      |
      v
GPT Tools Controller (gpt_tools.py)
      |
      | Dispatches to GPTService.execute_tool()
      v
Executes SoftwareService.request_software_access() -> Saves to DB
      |
      v
Returns Tool Execution Result -> LLM synthesizes natural voice response
```

---

## What Was Learned & What Is Next

### Summary of What Was Learned:
- How LLM Function Calling acts as a secure bridge between AI models and backend APIs.
- How to design standardized tool JSON schemas.
- How to build a mock LLM provider engine to eliminate development costs.

### What Will Be Implemented Next:
In **Phase 9**, we will integrate **ElevenLabs Playbooks & Webhooks**. We will build the ElevenLabs agent webhook handler, signature verifier, and an interactive CLI voice simulator.
