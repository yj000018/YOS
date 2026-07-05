---
mpr_id: MPM-20260705-YOS-AGENT-RELAY-PROTOCOL-CONSTITUTION-GATE-REPORT
mp_id: MPM-20260705-YOS-AGENT-RELAY-PROTOCOL-CONSTITUTION-GATE
title: YOS Agent Relay Protocol Constitution Gate — MPR
mode: marathon
status: executed_awaiting_architect_guardian_review
executor: Manus
guardian_required: true
branch: main
commit: pending_patch
executed_at: "2026-07-05T18:00:00Z"
---

# MPR — YOS Agent Relay Protocol Constitution Gate

## STATUS BLOCK

```
STATUS:                          EXECUTED_AWAITING_A_G_REVIEW
MODE:                            marathon
BRANCH:                          main
COMMIT:                          pending_patch
YARP_MODULE_CREATED:             yes
YARP_PLACEMENT:                  01_BACKBONE/YARP/ (justified — YARP is a peer backbone module, not a BUS sub-module)
YARP_CONSTITUTION_CREATED:       yes (YARP-CONSTITUTION.md v1.0.0)
YARP_SPEC_CREATED:               yes (YARP-SPEC-v1.md v1.0.0)
STATE_MACHINE_CREATED:           yes (YARP-STATE-MACHINE.md — 13 states, full transition table)
MESSAGE_TYPES_DEFINED:           yes (13 types — PING, HEARTBEAT, CANCEL, FINALIZE, CAPABILITY_QUERY, CAPABILITY_RESPONSE, EXECUTE_MP, ACK, NACK, PROGRESS, REQUEST_INFO, RESULT, ERROR)
JSON_SCHEMAS_CREATED:            yes (7 schemas — all valid JSON)
TRANSPORT_ABSTRACTION_CONFIRMED: yes (8 transports mapped)
BUS_INTEGRATION_DEFINED:         yes (inbox/workspace/outbox/archive mapping)
MPM_INTEGRATION_DEFINED:         yes (ledger + latest-mpr.json mapping)
JSON_FIRST_RESULT_DEFINED:       yes (canonical result shape in YARP-SPEC-v1.md §4)
MIGRATION_PLAN_CREATED:          yes (Phase 0 → Phase 4)
PROTOCOL_MATURITY:               candidate
VALIDATION_STATUS:               JSON_SCHEMAS=PASS (7/7) | BUS=PASS | MPM=PASS_WITH_WARNINGS (stale_running)
SOURCE_CORPUS_TOUCHED:           no
EXTERNAL_REPOS_TOUCHED:          no
READY_FOR_A_G_REVIEW:            yes
```

---

## 1. YARP Module — Delivered

### Placement Justification

YARP is placed at `01_BACKBONE/YARP/` (not `01_BACKBONE/BUS/00_PROTOCOLS/yarp/`) because:
- YARP is a protocol, BUS is a transport substrate — they are peers, not parent/child
- YARP will outlive any specific transport
- Placing YARP inside BUS would create a circular dependency (BUS references YARP for message format)

### File Inventory

| File | Location | Status |
|---|---|---|
| README.md | `01_BACKBONE/YARP/` | ✅ created |
| YARP-CONSTITUTION.md | `00_SPEC/` | ✅ created |
| YARP-SPEC-v1.md | `00_SPEC/` | ✅ created |
| YARP-MESSAGE-TYPES.md | `00_SPEC/` | ✅ created |
| YARP-ARTIFACT-MAPPING.md | `00_SPEC/` | ✅ created |
| YARP-STATE-MACHINE.md | `03_STATE_MACHINE/` | ✅ created |
| YARP-TRANSPORT-ADAPTERS.md | `02_ADAPTERS/` | ✅ created |
| YARP-ERROR-CATALOGUE.md | `04_GOVERNANCE/` | ✅ created |
| YARP-ID-CORRELATION-POLICY.md | `04_GOVERNANCE/` | ✅ created |
| YARP-MIGRATION-PLAN.md | `05_INTEGRATION/` | ✅ created |
| yarp_envelope.schema.json | `01_SCHEMAS/` | ✅ valid JSON |
| yarp_message.schema.json | `01_SCHEMAS/` | ✅ valid JSON |
| yarp_ack.schema.json | `01_SCHEMAS/` | ✅ valid JSON |
| yarp_result.schema.json | `01_SCHEMAS/` | ✅ valid JSON |
| yarp_error.schema.json | `01_SCHEMAS/` | ✅ valid JSON |
| yarp_capability.schema.json | `01_SCHEMAS/` | ✅ valid JSON |
| yarp_artifact_pointer.schema.json | `01_SCHEMAS/` | ✅ valid JSON |

**Total: 17 files (9 spec/governance + 7 schemas + 1 README)**

---

## 2. YARP Architecture Summary

### Five Layers

| Layer | Name | Key Decisions |
|---|---|---|
| 1 | Transport | 8 adapters mapped; Manus API + Workspace Filesystem = production_ready |
| 2 | Session | Handshake with yarp_version, agent_id, role, capabilities |
| 3 | Messages | 13 message types in 3 families (Control, Capability, Execution) |
| 4 | Artifacts | 11 artifact types; artifact_pointer schema for all |
| 5 | Governance | 10 ID types; full correlation chain; idempotency by mp_id |

### Core Doctrine (immutable)

```
YARP is transport-independent.
Transports are adapters.
Agents are peers.
JSON is primary.
Markdown is audit/human-readable.
Git is durable memory, not the protocol.
BUS is the operational transport substrate, not the protocol itself.
```

---

## 3. Key Design Decisions

| Decision | Rationale |
|---|---|
| YARP at `01_BACKBONE/YARP/` | Peer backbone module, not BUS sub-module |
| 13 message types (not fewer) | Covers all use cases without bloat; HEARTBEAT + FINALIZE needed for long marathons |
| Idempotency by `mp_id` | Prevents duplicate execution on retry |
| `correlation_id` as primary link | Decouples from transport-specific task_id |
| `attempt_id` = base_uuid + NNN | Enables retry tracking without losing correlation |
| `structured_output_schema` in EXECUTE_MP | Enables MPR as JSON result (eliminates MPR parsing) |
| Phase 0-4 migration | Incremental; no big-bang cutover required |
| `candidate` maturity (not `canonical`) | Correct — no live transport validated yet |

---

## 4. Protocol Maturity

```
draft:     spec exists, no schemas, no state machine
candidate: spec + schemas + state machine + migration plan  ← CURRENT
canonical: all of above + at least one live transport validated
```

**YARP v1.0.0 = candidate** after this gate.

**Path to canonical:** validate Phase 2 (Manus API async relay) end-to-end.

---

## 5. Migration Status

| Phase | Status | Blocker |
|---|---|---|
| Phase 0 — Manual bridge | ✅ operational | deprecate after Phase 2 |
| Phase 1 — BUS direct-file | ✅ operational | use as fallback |
| Phase 2 — Manus API async relay | 🔶 candidate | generate Manus API key |
| Phase 3 — Webhook push | 🔶 candidate | deploy webhook endpoint |
| Phase 4 — Multi-agent YARP | ⬜ future | Phase 2+3 must be live |

---

## 6. BUS / MPM Integration

| YARP Component | BUS Integration | MPM Integration |
|---|---|---|
| EXECUTE_MP delivery | `inbox/mpm/<mp_id>.md` | `04_QUEUE/ready/` |
| ACK | `bus.py claim` → workspace/ | ledger status: running |
| RESULT | `outbox/mpm/<mpr_id>.md` | ledger status: executed |
| FINALIZE | `archive/mpm/` | ledger status: archived |
| Fast-path pointer | `latest-bus-event.json` | `latest-mpr.json` |

---

## 7. Suggested Next Gates

1. `MPM-{DATE}-YOS-YARP-PHASE2-VALIDATION-GATE` — live test: ChatGPT → task.sendMessage → BUS inbox → MPM → RESULT JSON
2. `MPM-{DATE}-YOS-YARP-CANONICAL-DESIGNATION-GATE` — promote YARP from candidate to canonical after Phase 2 validated
3. `MPM-{DATE}-YOS-YARP-PYTHON-SDK-GATE` — implement YARP envelope wrapper in Python (stdlib only)
