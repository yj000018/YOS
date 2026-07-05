# Identity Card — Codex / OpenAI Agents

> **agent_id:** codex
> **Version:** v1.0.0
> **Gate:** MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE

---

| Field | Value |
|---|---|
| **agent_id** | `codex` |
| **display_name** | Codex / OpenAI Agents |
| **agent_type** | llm + executor |
| **vendor** | OpenAI |
| **runtime** | OpenAI Codex API / Agents SDK |
| **primary_roles** | executor |
| **trust_level** | T1 (read_only) |

---

## Known Capabilities

| Capability | Status | Notes |
|---|---|---|
| reasoning | candidate | Not yet tested in yOS context |
| planning | candidate | Not yet tested |
| coding | proven | Core capability — code generation and execution |
| vision | unknown | Not tested |
| api | candidate | Via tools |
| memory | unknown | Not tested |
| filesystem | candidate | Via tools — not yet validated |
| execution | candidate | Via tools — not yet validated |

---

## Supported Transports

| Transport | Status |
|---|---|
| OpenAI Agents SDK | candidate |
| Manual upload | candidate |

---

## Supported YARP Roles

| Role | Status |
|---|---|
| yarp_receiver | candidate |

---

## Routing Notes

- Not yet integrated into yOS YARP transport
- Future gate: YOS-CODEX-INTEGRATION-GATE
