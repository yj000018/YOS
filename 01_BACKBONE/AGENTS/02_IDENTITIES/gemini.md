# Identity Card — Gemini

> **agent_id:** gemini
> **Version:** v1.0.0
> **Gate:** MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE

---

| Field | Value |
|---|---|
| **agent_id** | `gemini` |
| **display_name** | Gemini (Google DeepMind) |
| **agent_type** | llm |
| **vendor** | Google DeepMind |
| **runtime** | Gemini API / Google AI Studio |
| **primary_roles** | reviewer, assimilator |
| **trust_level** | T1 (read_only) |

---

## Known Capabilities

| Capability | Status | Notes |
|---|---|---|
| reasoning | proven | Strong reasoning, especially long-context |
| planning | candidate | Not yet tested in yOS context |
| coding | candidate | Code generation — not yet validated in yOS |
| vision | proven | Multimodal — image, PDF, video |
| api | unknown | Not tested in yOS context |
| memory | unknown | Session-scoped; external tools not configured |
| filesystem | unsupported | No direct FS access |
| execution | unsupported | No direct execution |

---

## Supported Transports

| Transport | Status |
|---|---|
| Direct Google AI API | candidate |
| Manual upload | candidate |

---

## Supported YARP Roles

| Role | Status |
|---|---|
| yarp_receiver | candidate |

---

## Routing Notes

- Preferred for: long-document analysis (2M token context), multimodal tasks
- Not yet integrated into yOS YARP transport
