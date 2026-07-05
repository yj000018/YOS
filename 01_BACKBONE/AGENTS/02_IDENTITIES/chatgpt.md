# Identity Card — ChatGPT (Architect & Guardian)

> **agent_id:** chatgpt-ag
> **Version:** v1.0.0
> **Gate:** MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE

---

| Field | Value |
|---|---|
| **agent_id** | `chatgpt-ag` |
| **display_name** | ChatGPT — Architect & Guardian |
| **agent_type** | llm |
| **vendor** | OpenAI |
| **runtime** | ChatGPT (web / API) |
| **primary_roles** | architect, guardian |
| **trust_level** | T5 (guardian_approved) |

---

## Known Capabilities

| Capability | Status | Notes |
|---|---|---|
| reasoning | proven | Core strength — multi-step, architectural |
| planning | proven | MP authoring, system design |
| coding | proven | Code generation, review |
| vision | proven | GPT-4V — image analysis, screenshot reading |
| api | candidate | Via tools/plugins |
| memory | candidate | Native memory (limited) + external tools |
| filesystem | unsupported | No direct FS access — indirect via Manus relay |
| execution | unsupported | No direct execution — indirect via Manus relay |

---

## Known Limitations

- No direct filesystem access
- No direct code execution
- No direct BUS inbox write (indirect via task.create → Manus relay)
- Rate limits: 10 task.create/min (Manus API)
- Session-scoped context (no persistent memory without external tools)

---

## Supported Transports

| Transport | Status |
|---|---|
| Manus API (task.create, sendMessage) | proven |
| Manual upload (file attachment) | proven |
| Webhooks (outbound) | candidate |
| Git (indirect) | candidate |
| MCP | unknown |

---

## Supported YARP Roles

| Role | Status |
|---|---|
| yarp_sender | proven |
| yarp_guardian | proven |
| yarp_receiver | candidate |

---

## Permission Notes

- Trust level T5 (guardian_approved) for the session owner (Yannick Jolliet)
- Authorized to: create MPs, approve MPRs, designate canonical gates
- Not authorized to: directly write to corpus, execute code, access secrets

---

## Routing Notes

- Preferred for: architectural design, MP authoring, A&G review
- Not preferred for: code execution, filesystem operations, long-running tasks
- Fallback: Claude for architectural review when ChatGPT unavailable
