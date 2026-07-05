# YARP — YOS Agent Relay Protocol

> **Version:** v1.1.0-candidate
> **Status:** candidate
> **Gate:** MPM-20260705-YOS-AGENT-RELAY-PROTOCOL-CONSTITUTION-GATE
> **Amended by:** MPM-20260705-YOS-YARP-CONSTITUTION-CLARIFICATION-PATCH-GATE
> **Created:** 2026-07-05

---

## What is YARP?

> **YARP is to yOS what HTTP is to the Web.**
>
> HTTP does not care whether data travels over fiber, WiFi, or satellite. It defines the meaning of requests and responses.
>
> YARP does not care whether messages travel via Manus API, filesystem, Git, webhooks, or MCP. It defines the meaning of agent messages. Any agent — ChatGPT, Manus, Claude, Gemini, n8n, or a future agent not yet invented — can communicate as long as it speaks YARP.

---

## yOS Backbone Architecture

```
                 yOS
                  │
 ┌────────────────┼────────────────┐
 │                │                │
 KAP             MPM             YARP
Knowledge     Orchestration     Communication
Assimilation  & Execution       Between Agents
                  │
                 BUS
      Runtime / Transport Substrate
```

| Module | Full Name | Role |
|---|---|---|
| **KAP** | Knowledge Assimilation Protocol | Captures, structures, and assimilates knowledge into yOS |
| **MPM** | Mega Prompt Machine | Orchestrates and executes Mega Prompts |
| **YARP** | YOS Agent Relay Protocol | Defines communication between agents |
| **BUS** | YOS Bus | Runtime/transport substrate — moves packets between agents |

---

## Core Doctrine

```
YARP defines meaning.
BUS moves packets.

YARP is transport-independent.
Transports are adapters.
Agents are peers.
JSON is primary.
Markdown is audit/human-readable.
Git is durable memory, not the protocol.
BUS is the operational transport substrate, not the protocol itself.
```

---

## Placement Justification

YARP is placed at `01_BACKBONE/YARP/` (not `01_BACKBONE/BUS/00_PROTOCOLS/yarp/`) because:

1. **YARP is a protocol, not a transport.** BUS is the transport substrate. YARP defines the message format, state machine, and governance layer that rides on top of BUS (and other transports).
2. **YARP is a first-class backbone module.** It sits alongside KAP, BUS, and MPM as a peer, not as a sub-module of any of them.
3. **YARP will outlive any specific transport.** As BUS evolves (new backends, MCP, webhooks), YARP remains stable.
4. **Avoids circular dependency.** BUS references YARP for message format; YARP references BUS as a transport adapter.

---

## Module Structure

```
01_BACKBONE/YARP/
├── README.md                          ← this file
├── 00_SPEC/
│   ├── YARP-SPEC-v1.md                ← canonical specification
│   ├── YARP-CONSTITUTION.md           ← immutable doctrine (v1.1.0)
│   ├── YARP-MESSAGE-TYPES.md          ← all 13 message types
│   └── YARP-ARTIFACT-MAPPING.md       ← MP/MPR/OCA/KAP artifact mapping
├── 01_SCHEMAS/
│   ├── yarp_envelope.schema.json
│   ├── yarp_message.schema.json
│   ├── yarp_ack.schema.json
│   ├── yarp_result.schema.json
│   ├── yarp_error.schema.json
│   ├── yarp_capability.schema.json
│   └── yarp_artifact_pointer.schema.json
├── 02_ADAPTERS/
│   └── YARP-TRANSPORT-ADAPTERS.md     ← all transport adapter specs
├── 03_STATE_MACHINE/
│   └── YARP-STATE-MACHINE.md          ← lifecycle + transitions
├── 04_GOVERNANCE/
│   ├── YARP-ID-CORRELATION-POLICY.md  ← IDs, correlation, idempotency
│   └── YARP-ERROR-CATALOGUE.md        ← error codes + recovery
├── 05_INTEGRATION/
│   └── YARP-MIGRATION-PLAN.md         ← Phase 0 → Phase 4 migration
└── 99_ARCHIVE/
```

---

## Quick Reference

| Layer | Name | Description |
|---|---|---|
| 1 | Transport | API, MCP, Workspace, BUS, Git, GDrive, Webhooks |
| 2 | Session | Handshake, version, identity, role, capabilities |
| 3 | Messages | EXECUTE_MP, ACK, NACK, PROGRESS, RESULT, ERROR, ... |
| 4 | Artifacts | MP, MPR, Context Pack, OCA, KAP Pack, blobs |
| 5 | Governance | IDs, correlation, idempotency, timeout, retry, audit |
