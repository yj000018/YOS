# Identity Card — Claude

> **agent_id:** claude
> **Version:** v1.0.0
> **Gate:** MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE

---

| Field | Value |
|---|---|
| **agent_id** | `claude` |
| **display_name** | Claude (Anthropic) |
| **agent_type** | llm |
| **vendor** | Anthropic |
| **runtime** | Claude API / Claude.ai |
| **primary_roles** | architect, reviewer |
| **trust_level** | T2 (sandboxed_write) |

---

## Known Capabilities

| Capability | Status | Notes |
|---|---|---|
| reasoning | proven | Strong analytical and architectural reasoning |
| planning | proven | Architectural planning, spec writing |
| coding | proven | Code generation, review, refactoring |
| vision | candidate | Claude 3+ multimodal |
| api | unknown | Not tested in yOS context |
| memory | unknown | Session-scoped; external tools not yet configured |
| filesystem | unsupported | No direct FS access |
| execution | unsupported | No direct execution |

---

## Supported Transports

| Transport | Status |
|---|---|
| Manus API (via OPENAI_API_BASE proxy) | proven |
| Direct Anthropic API | candidate |
| Manual upload | candidate |

---

## Supported YARP Roles

| Role | Status |
|---|---|
| yarp_sender | candidate |
| yarp_receiver | candidate |

---

## Routing Notes

- Preferred for: architectural review, long-document analysis, spec writing
- Fallback for: ChatGPT when unavailable for architectural tasks
