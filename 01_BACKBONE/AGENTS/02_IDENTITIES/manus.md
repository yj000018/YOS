# Identity Card — Manus

> **agent_id:** manus
> **Version:** v1.0.0
> **Gate:** MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE

---

| Field | Value |
|---|---|
| **agent_id** | `manus` |
| **display_name** | Manus |
| **agent_type** | llm + executor |
| **vendor** | Manus Team |
| **runtime** | Manus Sandbox (Ubuntu 24.04, ephemeral + persistent) |
| **primary_roles** | executor, orchestrator |
| **trust_level** | T3 (runtime_operator) |

---

## Known Capabilities

| Capability | Status | Notes |
|---|---|---|
| reasoning | proven | LLM-based reasoning |
| planning | proven | Built-in task plan tool |
| coding | proven | Python3, Node.js, bash — sandbox execution |
| vision | proven | Multimodal — screenshot, image, PDF |
| filesystem | proven | /home/ubuntu/ persistent, /tmp/ ephemeral |
| api | proven | HTTP requests, curl, Python requests |
| execution | proven | Shell, Python, Node.js, git — full OS access |
| memory | proven | /home/ubuntu/ persistence + Git + Notion/Mem0 via tools |

---

## Known Limitations

- Sandbox resets between sessions (ephemeral /tmp/)
- /home/ubuntu/ persists but may be cleared by platform
- Rate limits on browser operations
- No direct ChatGPT API access (uses OPENAI_API_BASE proxy)
- Context window limits per session

---

## Supported Transports

| Transport | Status |
|---|---|
| Workspace Filesystem (/home/ubuntu/) | proven |
| Git (GitHub PAT) | proven |
| Manus API (task.create, sendMessage) | proven |
| Manual upload (file attachment) | proven |
| Webhooks (inbound) | candidate |
| MCP bridge | candidate |

---

## Supported YARP Roles

| Role | Status |
|---|---|
| yarp_receiver | proven |
| yarp_sender | proven |
| yarp_relay | candidate |

---

## Permission Notes

- Trust level T3 (runtime_operator) — can write to runtime, execute code
- Authorized to: execute MPs, write to /home/ubuntu/, commit to Git, call APIs
- Not authorized to: approve canonical gates (requires T4+), access 1Password without explicit instruction

---

## Routing Notes

- Preferred for: MP execution, code generation + execution, filesystem operations, long-running tasks
- Not preferred for: architectural design decisions, A&G review
- Fallback: none (Manus is the primary executor)
