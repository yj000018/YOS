# AGENT Lifecycle

> **Version:** v1.0.0
> **Gate:** MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE

---

## Lifecycle States

```
UNKNOWN → REGISTERED → AVAILABLE → ENGAGED → COMPLETING → IDLE
                                      │
                                   SUSPENDED
                                      │
                                  DEREGISTERED
```

| State | Description |
|---|---|
| `unknown` | Agent has not been declared in the registry |
| `registered` | Agent is declared in agents.json with identity and capabilities |
| `available` | Agent is ready to receive YARP messages |
| `engaged` | Agent is actively executing a task |
| `completing` | Agent has finished execution, producing final artifacts |
| `idle` | Agent has completed a task and is awaiting next assignment |
| `suspended` | Agent is temporarily unavailable (rate limit, maintenance) |
| `deregistered` | Agent has been removed from the registry |

---

## Allowed Transitions

| From | To | Trigger |
|---|---|---|
| `unknown` | `registered` | Agent declared in agents.json |
| `registered` | `available` | Agent confirms readiness (CAPABILITY_RESPONSE) |
| `available` | `engaged` | EXECUTE_MP received and ACK sent |
| `engaged` | `completing` | Task execution finished |
| `completing` | `idle` | RESULT message sent |
| `idle` | `available` | Ready for next task |
| `available` | `suspended` | Rate limit or maintenance |
| `suspended` | `available` | Suspension lifted |
| `any` | `deregistered` | Explicit deregistration |

---

## Session vs. Persistent Lifecycle

| Agent Type | Lifecycle Scope |
|---|---|
| Manus | Session-scoped (sandbox resets between sessions) |
| ChatGPT | Conversation-scoped |
| Claude | Conversation-scoped |
| Gemini | Conversation-scoped |
| Human Operator | Persistent (identity persists across sessions) |
| n8n Automation | Persistent (service lifecycle) |

---

## Lifecycle and Trust

- Trust level is assigned at registration and may be elevated by a guardian_approved gate.
- Trust level does not change during a session without explicit guardian action.
- A `suspended` agent retains its trust level but loses `available` status.
