# Phase 9: ElevenLabs Playbooks & Webhook Integration

## Phase Goal
The goal of Phase 9 is to integrate **ElevenLabs Playbooks and Conversational AI Webhooks** into the **AI Voice IT Helpdesk Agent**. ElevenLabs Playbooks provide real-time speech synthesis (TTS), speech recognition (STT), and voice agent conversation state orchestration.

In this phase, we build an ElevenLabs webhook server endpoint (`/api/v1/elevenlabs/webhook`), implement HMAC signature/secret token verification, create ElevenLabs JSON response formatters, export an importable playbook configuration file, and provide a zero-cost local CLI voice agent simulator.

---

## Concepts Introduced

### 1. Voice Agent Architecture Pipeline
A real-time Voice AI system consists of three chained sub-systems:
```
Caller Voice Stream -> Speech-to-Text (STT) -> LLM / Playbook Decision -> Text-to-Speech (TTS) -> Spoken Audio
```
1. **STT (Whisper / ElevenLabs STT)**: Converts incoming audio waves into text transcripts.
2. **LLM Orchestrator (Playbook State Machine)**: Processes transcript, manages memory context, and decides whether to speak or trigger a backend webhook tool call.
3. **TTS (ElevenLabs Voice Generator)**: Converts synthesized response text into human-like audio.

### 2. Latency & Perceived Responsiveness
In voice applications, humans expect responses within **800ms - 1200ms**. If latency exceeds 2 seconds, conversation feels awkward.
Backend optimizations for low latency include:
- **Short Conversational Responses**: Keeping responses to 1-2 sentences.
- **Asynchronous I/O**: Ensuring FastAPI database lookups complete in under 50ms.
- **Streaming Tokens**: Sending text chunks to TTS as soon as they are generated.

### 3. Webhook Protocol & Security Verification
When ElevenLabs invokes our backend webhook during a phone call, it sends an HTTP POST request containing tool details. To prevent malicious third parties from invoking our endpoints, our server verifies the `X-ElevenLabs-Signature` or `ELEVENLABS_WEBHOOK_SECRET` header.

---

## Free-Tier Notes

- **Zero Voice Minute Costs**: Testing ElevenLabs agents via real telephone webhooks consumes voice tier credits. To allow students to develop 100% free, we provide a **Local Interactive CLI Voice Simulator** (`playbooks/voice_cli_simulator.py`) that simulates the exact ElevenLabs webhook protocol locally in your terminal!

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
│   ├── Phase-08.md
│   └── Phase-09.md            # This documentation file
├── backend/
│   ├── api/
│   │   └── v1/
│   │       └── elevenlabs.py  # ElevenLabs webhook handler
│   ├── schemas/
│   │   └── elevenlabs.py      # Pydantic ElevenLabs webhook schemas
│   └── services/
│       └── elevenlabs_service.py # Webhook payload parser & response builder
├── playbooks/
│   ├── elevenlabs_agent_config.json # Importable ElevenLabs agent config
│   └── voice_cli_simulator.py       # Terminal interactive CLI voice simulator
└── tests/
    └── test_elevenlabs.py     # Webhook unit & integration tests
```

---

## ElevenLabs Webhook Payload & Response Format

### Incoming ElevenLabs Webhook Request:
```json
{
  "agent_id": "agent_abc123",
  "conversation_id": "conv_998877",
  "tool_name": "request_access",
  "parameters": {
    "employee_id": "EMP-1001",
    "software_name": "VS Code"
  }
}
```

### Server Webhook Response:
```json
{
  "status": "success",
  "tool_name": "request_access",
  "response": "Your request for VS Code has been automatically approved. The license is now assigned to Sarah Jenkins."
}
```

---

## Data Flow Diagram

```
Phone Caller
      | Spoken Voice
      v
ElevenLabs Playbook Agent (STT + Conversation Manager)
      |
      | HTTP POST /api/v1/elevenlabs/webhook (Tool Call Payload)
      v
FastAPI ElevenLabs Controller (elevenlabs.py)
      |
      | Verifies Webhook Secret Header
      v
ElevenLabsService -> Calls GPTService/Backend Services -> Gets Speech String
      |
      | Returns {"status": "success", "response": "..."}
      v
ElevenLabs TTS -> Converts response text to voice audio stream -> Spoken to Caller
```

---

## What Was Learned & What Is Next

### Summary of What Was Learned:
- How voice AI pipelines chain STT, LLM, and TTS models.
- How to structure low-latency webhook servers for real-time voice agents.
- How to test voice webhooks locally using a CLI simulator without consuming paid API minutes.

### What Will Be Implemented Next:
In **Phase 10**, we will complete the **Conversation Design & System Playbooks**. We will write system prompts, set up conversational state machines, and document prompt engineering decisions for voice agents.
