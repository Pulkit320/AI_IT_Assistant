# Phase 7: Ticket Status Lookup & Voice Response Formatting

## Phase Goal
The goal of Phase 7 is to implement **Voice-Optimized Ticket Status Search** for the **AI Voice IT Helpdesk Agent**. When employees call an IT helpdesk to inquire about an existing issue, they expect a quick, natural status update rather than a dump of complex database JSON objects.

In this phase, we add voice status lookup controllers that transform raw database ticket records into short, conversational speech strings designed specifically for ElevenLabs Text-to-Speech (TTS) synthesis.

---

## Concepts Introduced

### 1. Designing API Responses for Speech Synthesis (TTS)
Standard REST APIs return raw ISO timestamps (`2026-08-07T16:30:00Z`), technical IDs, and unformatted arrays. Speech synthesis engines pronounce raw ISO timestamps awkwardly (e.g. "twenty-twenty-six dash zero-eight...").
To create a human-like voice experience, our backend formats status output as natural speech:
- *Raw DB Status*: `status: "Pending Manager Approval", updated_at: "2026-08-07T14:00:00Z"`
- *Voice-Ready Output*: `"Your ticket IT 8091 for Docker access is currently Pending Manager Approval. It was last updated 2 hours ago."`

### 2. Phonetic Spacing for Identifiers
Voice agents often slur ticket numbers like `IT-8091` ("eye-tee-eighty-ninety-one"). In speech strings, we insert spaces between digits (`I T 8 0 9 1`) or pronounce numbers clearly so ElevenLabs TTS speaks each digit distinctly.

---

## Free-Tier Notes

- **Zero-Latency Formatting**: Text transformation takes place directly in Python. No external voice generation calls are required for endpoint testing.

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
│   └── Phase-07.md            # This documentation file
├── backend/
│   ├── api/
│   │   └── v1/
│   │       └── tickets.py     # Voice status lookup endpoints
│   └── services/
│       └── ticket_service.py  # Voice response formatter logic
└── tests/
    └── test_tickets.py        # Updated tests for voice status formatting
```

---

## File & Code Walkthrough

### 1. `backend/services/ticket_service.py`
Adds `get_voice_status_summary()` to translate ticket records into natural speech responses.

```python
@staticmethod
def format_voice_summary(ticket: Ticket) -> str:
    formatted_num = " ".join(ticket.ticket_number) # "I T - 8 0 9 1"
    return (
        f"Ticket {formatted_num} regarding {ticket.subject} is currently {ticket.status}. "
        f"Priority is set to {ticket.priority}."
    )
```

---

## Data Flow Diagram

```
User / Voice Agent
      |
      | GET /api/v1/tickets/IT-8091/voice-status
      v
Tickets Controller (tickets.py)
      |
      | Calls TicketService.get_voice_ticket_status()
      v
Ticket Service -> Queries Ticket IT-8091 -> Runs format_voice_summary()
      |
      | Returns {"ticket_number": "IT-8091", "voice_response": "Ticket I T - 8 0 9 1..."}
      v
ElevenLabs TTS -> Converts text stream -> Spoken voice audio
```

---

## What Was Learned & What Is Next

### Summary of What Was Learned:
- The importance of formatting API outputs specifically for voice synthesis.
- How to convert raw database fields into conversational natural language.

### What Will Be Implemented Next:
In **Phase 8**, we will build the **GPT-5 Function Calling & LLM Abstraction Layer**. We will define OpenAI tool schemas (`create_ticket`, `password_reset`, `request_access`, `check_ticket`, `escalate_issue`) and create a zero-cost Mock LLM provider.
