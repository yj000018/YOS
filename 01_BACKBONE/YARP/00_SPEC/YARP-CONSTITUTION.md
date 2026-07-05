# YARP Constitution

> **Version:** v1.0.0
> **Status:** candidate
> **Immutable after:** canonical designation
> **Gate:** MPM-20260705-YOS-AGENT-RELAY-PROTOCOL-CONSTITUTION-GATE

---

## Article I — Identity

YARP (YOS Agent Relay Protocol) is the universal inter-agent and inter-LLM communication protocol for the YOS cognitive operating system.

YARP defines how agents exchange messages, artifacts, and execution results — regardless of the transport layer, vendor, or runtime environment.

---

## Article II — Core Doctrine

```
YARP is transport-independent.
Transports are adapters.
Agents are peers.
JSON is primary.
Markdown is audit/human-readable.
Git is durable memory, not the protocol.
BUS is the operational transport substrate, not the protocol itself.
```

These seven principles are immutable. No gate may override them.

---

## Article III — Scope

YARP governs communication between:

- ChatGPT (Architect & Guardian)
- Manus (executor)
- Claude (architect/reviewer)
- Gemini (long-doc/analysis)
- Codex / OpenAI Agents
- Future yOS agents
- Human operators
- Automation runtimes (n8n, Zapier, webhooks)

YARP does not govern:

- Internal agent reasoning (chain-of-thought)
- File storage format (governed by BUS)
- Mega Prompt execution logic (governed by MPM)
- Report content format (governed by MPM/MPR spec)

---

## Article IV — Layered Architecture

YARP is defined as five layers:

| Layer | Name | Responsibility |
|---|---|---|
| 1 | Transport | Physical delivery of YARP messages |
| 2 | Session | Identity, version, role, capability negotiation |
| 3 | Messages | Typed message exchange (EXECUTE_MP, ACK, RESULT, ...) |
| 4 | Artifacts | MP, MPR, Context Pack, OCA, KAP Pack, blobs |
| 5 | Governance | IDs, correlation, idempotency, timeout, retry, audit |

Each layer is independently evolvable. A change in Layer 1 (transport) must not require changes in Layers 3-5.

---

## Article V — Relationship to BUS, MPM, MPR

```
YARP = protocol (this module)
BUS  = transport/runtime substrate (01_BACKBONE/BUS/)
MPM  = orchestration of Mega Prompts (01_BACKBONE/MPM/)
MPR  = report artifact (produced by MPM execution)
```

**Invariant:** YARP rides on BUS. YARP carries MPM packets. YARP returns MPR results.

YARP must not replace BUS or MPM. YARP must not be replaced by BUS or MPM.

---

## Article VI — JSON-First Principle

All YARP messages MUST be valid JSON at the protocol layer.

Markdown representations are permitted as audit/human-readable companions but are never the canonical form.

The canonical result shape is:

```json
{
  "yarp_version": "1.0",
  "message_type": "RESULT",
  "status": "completed|failed|partial|blocked",
  "correlation_id": "...",
  "mp_id": "...",
  "task_id": "...",
  "commit": "...",
  "mpr_path": "...",
  "artifacts": [],
  "validation": {
    "bus": "PASS|PASS_WITH_WARNINGS|FAIL",
    "mpm": "PASS|PASS_WITH_WARNINGS|FAIL"
  },
  "errors": []
}
```

---

## Article VII — Versioning

YARP versions follow semantic versioning: `MAJOR.MINOR.PATCH`.

- MAJOR: breaking changes to message schema or state machine
- MINOR: new message types or optional fields
- PATCH: documentation, error catalogue, adapter updates

Current version: `1.0.0`

Session handshake MUST include `yarp_version`. Agents MUST reject sessions with incompatible MAJOR versions.

---

## Article VIII — Immutability of the Constitution

This constitution may be amended only by a dedicated MPM marathon gate with `guardian_required: true`.

No sprint or run gate may amend the constitution.

Amendments must increment MAJOR version if they change Articles I-VI.
