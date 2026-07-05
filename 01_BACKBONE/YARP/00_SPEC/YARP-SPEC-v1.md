# YARP Specification v1.0.0

> **Status:** candidate
> **Gate:** MPM-20260705-YOS-AGENT-RELAY-PROTOCOL-CONSTITUTION-GATE
> **Constitution:** YARP-CONSTITUTION.md v1.1.0
> **Amended by:** MPM-20260705-YOS-YARP-CONSTITUTION-CLARIFICATION-PATCH-GATE

---

## 1. Overview

YARP (YOS Agent Relay Protocol) is a five-layer, transport-independent protocol for inter-agent and inter-LLM communication in the YOS cognitive operating system.

### Design Goals

1. **Transport independence** — YARP messages are valid over any transport (API, MCP, filesystem, Git, webhooks)
2. **Agent symmetry** — All agents are peers; no agent is architecturally privileged
3. **JSON-first** — All protocol messages are JSON; Markdown is audit-only
4. **Idempotency** — All EXECUTE_MP messages are idempotent by `mp_id`
5. **Auditability** — All messages carry `correlation_id`, `attempt_id`, and timestamps
6. **Minimal surface** — 13 message types cover all use cases; no bloat

---

## 2. Five-Layer Architecture

### Layer 1 — Transport

Responsible for physical delivery of YARP envelopes between agents.

**Supported transports (v1.0):**
- Manus API (`task.sendMessage`, `task.create`)
- Direct-file BUS (`/home/ubuntu/yos-bus-runtime/`)
- Git BUS fallback (`01_BACKBONE/BUS/04_DOMAINS/`)
- Manual upload (operational bridge)
- Webhooks (last-mile push)
- MCP bridge (future)
- Google Drive (future)

Transport adapters are defined in `02_ADAPTERS/YARP-TRANSPORT-ADAPTERS.md`.

### Layer 2 — Session

Responsible for identity, version negotiation, role assignment, and capability exchange.

**Session fields:**
```json
{
  "yarp_version": "1.0",
  "session_id": "YARP-SESSION-{uuid}",
  "initiator_id": "agent-chatgpt-ag",
  "responder_id": "agent-manus-executor",
  "initiator_role": "orchestrator",
  "responder_role": "executor",
  "transport_id": "manus-api-task-relay",
  "initiated_at": "2026-07-05T17:00:00Z",
  "capabilities": {
    "initiator": ["EXECUTE_MP", "PING", "CAPABILITY_QUERY", "CANCEL"],
    "responder": ["ACK", "NACK", "PROGRESS", "RESULT", "ERROR", "REQUEST_INFO", "HEARTBEAT", "FINALIZE"]
  }
}
```

**Roles:**
- `orchestrator` — initiates EXECUTE_MP, receives RESULT
- `executor` — receives EXECUTE_MP, returns RESULT
- `reviewer` — receives MPR, returns ACK/NACK
- `operator` — human relay (manual bridge)

### Layer 3 — Messages

13 message types. See `YARP-MESSAGE-TYPES.md` for full definitions.

**Message families:**
- Control: `PING`, `HEARTBEAT`, `CANCEL`, `FINALIZE`
- Capability: `CAPABILITY_QUERY`, `CAPABILITY_RESPONSE`
- Execution: `EXECUTE_MP`, `ACK`, `NACK`, `PROGRESS`, `REQUEST_INFO`, `RESULT`, `ERROR`

### Layer 4 — Artifacts

Artifacts are typed payloads carried by YARP messages.

| Artifact Type | Description | Carrier Message |
|---|---|---|
| `mp` | Mega Prompt packet | EXECUTE_MP |
| `mpr` | Mega Prompt Report | RESULT |
| `context_pack` | Session context | EXECUTE_MP, REQUEST_INFO |
| `oca` | Orchestration Context Artifact | EXECUTE_MP |
| `kap_pack` | KAP context pack | EXECUTE_MP |
| `markdown_file` | Human-readable document | RESULT, ERROR |
| `json_payload` | Structured data | RESULT |
| `blob` | Binary file | EXECUTE_MP, RESULT |
| `url_pointer` | External reference | any |

### Layer 5 — Governance

Responsible for IDs, correlation, idempotency, timeout, retry, audit, and state lifecycle.

See `04_GOVERNANCE/YARP-ID-CORRELATION-POLICY.md` and `YARP-ERROR-CATALOGUE.md`.

---

## 3. YARP Envelope

Every YARP message is wrapped in a YARP envelope:

```json
{
  "yarp_version": "1.0",
  "envelope_id": "YARP-ENV-{uuid}",
  "message_type": "EXECUTE_MP",
  "correlation_id": "YARP-CORR-{uuid}",
  "conversation_id": "YARP-CONV-{uuid}",
  "sender_id": "agent-chatgpt-ag",
  "receiver_id": "agent-manus-executor",
  "sent_at": "2026-07-05T17:00:00Z",
  "attempt_id": "YARP-ATT-{uuid}-001",
  "attempt_number": 1,
  "ttl_seconds": 300,
  "transport_id": "manus-api-task-relay",
  "payload": { ... }
}
```

---

## 4. Canonical Result Shape

```json
{
  "yarp_version": "1.0",
  "message_type": "RESULT",
  "status": "completed",
  "correlation_id": "YARP-CORR-abc123",
  "mp_id": "MPM-20260705-YOS-...",
  "task_id": "manus-task-xyz",
  "commit": "abc1234",
  "mpr_path": "01_BACKBONE/MPM/06_REPORTS/awaiting-review/...",
  "artifacts": [
    {
      "artifact_type": "mpr",
      "artifact_id": "MPR-20260705-...",
      "path": "01_BACKBONE/MPM/06_REPORTS/awaiting-review/...",
      "url": null
    }
  ],
  "validation": {
    "bus": "PASS",
    "mpm": "PASS_WITH_WARNINGS"
  },
  "errors": []
}
```

---

## 5. ID Mapping

```
MP          ↔  YARP EXECUTE_MP (mp_id field)
EXECUTE_MP  ↔  task_id (Manus API task)
task_id     ↔  execution (Manus agent run)
execution   ↔  RESULT (YARP message)
RESULT      ↔  MPR (artifact)
MPR         ↔  latest-mpr.json (fixed pointer)
```

---

## 6. Protocol Maturity

| Maturity | Criteria |
|---|---|
| `draft` | Spec exists, no schemas, no state machine |
| `candidate` | Spec + schemas + state machine + migration plan |
| `canonical` | All of above + at least one live transport validated |

**Current maturity:** `candidate` (after this gate)

---

## 7. Compatibility with BUS, MPM, and AGENTS

YARP is compatible with BUS, MPM, and AGENTS by design:

- BUS `inbox/mpm/` = YARP EXECUTE_MP delivery point
- BUS `outbox/mpm/` = YARP RESULT delivery point
- MPM `mp-ledger.json` = YARP correlation registry
- MPM `latest-mpr.json` = YARP RESULT fast-path pointer
- MPM `mpm.py validate` = YARP governance check
- AGENTS `agents.json` = YARP sender/receiver identity registry
- AGENTS `capabilities.json` = YARP CAPABILITY_QUERY/RESPONSE source
- AGENTS `trust-levels.json` = YARP envelope trust validation
- AGENTS `04_ROUTING/ART/` = YARP target_agent selection

---

## 8. AGENTS Integration

YARP uses AGENTS for:

1. **Identity validation** — `sender_id` and `receiver_id` in YARP envelopes must match registered `agent_id` in `agents.json`
2. **Trust validation** — `sender_trust_level` in YARP envelopes must match declared trust level in `trust-levels.json`
3. **Capability negotiation** — `CAPABILITY_QUERY` / `CAPABILITY_RESPONSE` messages use `capabilities.json` as ground truth
4. **Routing** — `target_agent` in `EXECUTE_MP` is resolved via `04_ROUTING/ART/`

**AGENTS module:** `01_BACKBONE/AGENTS/` (gate: MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE)
