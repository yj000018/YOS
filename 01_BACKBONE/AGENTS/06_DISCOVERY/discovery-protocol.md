# Discovery Protocol

> **Version:** v1.0.0
> **Gate:** MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE

---

## Discovery Principle

```
Discovery is protocolized.
No agent is assumed available without explicit registration.
Capability discovery precedes task assignment.
```

---

## Discovery Flow

```
1. Agent registers → agents.json
2. Agent declares capabilities → capabilities.json
3. Orchestrator queries registry → capability-query.md
4. Orchestrator selects agent → ART/CRT
5. Orchestrator sends YARP CAPABILITY_QUERY
6. Agent responds with YARP CAPABILITY_RESPONSE
7. Session established
```

---

## YARP Discovery Messages

| Message Type | Direction | Purpose |
|---|---|---|
| `CAPABILITY_QUERY` | orchestrator → agent | Query agent capabilities |
| `CAPABILITY_RESPONSE` | agent → orchestrator | Declare capabilities |
| `PING` | any → any | Liveness check |
| `PONG` | any → any | Liveness response |

---

## Static vs. Dynamic Discovery

- **Static discovery:** Read `agents.json` and `capabilities.json` directly
- **Dynamic discovery:** Send `CAPABILITY_QUERY` via YARP transport

Current yOS implementation: **static discovery** (v1.0.0)
Dynamic discovery: planned for Phase 2 (YARP-PHASE2-VALIDATION-GATE)
