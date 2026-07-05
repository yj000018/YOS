# YARP Constitution

> **Version:** v1.1.0
> **Status:** candidate
> **Immutable after:** canonical designation
> **Gate:** MPM-20260705-YOS-AGENT-RELAY-PROTOCOL-CONSTITUTION-GATE
> **Amended by:** MPM-20260705-YOS-YARP-CONSTITUTION-CLARIFICATION-PATCH-GATE

---

## Article I — Identity

YARP (YOS Agent Relay Protocol) is the universal inter-agent and inter-LLM communication protocol for the YOS cognitive operating system.

YARP defines how agents exchange messages, artifacts, and execution results — regardless of the transport layer, vendor, or runtime environment.

**YARP is a first-class backbone module of yOS.** It is a peer of KAP, MPM, and BUS — not a sub-module of any of them.

> **YARP is to yOS what HTTP is to the Web.**
>
> HTTP does not care whether data travels over fiber, WiFi, or satellite. It defines the meaning of requests and responses. Any server and any client can communicate as long as they speak HTTP.
>
> YARP does not care whether messages travel via Manus API, filesystem, Git, webhooks, or MCP. It defines the meaning of agent messages. Any agent — ChatGPT, Manus, Claude, Gemini, n8n, a future agent not yet invented — can communicate as long as it speaks YARP.
>
> YARP is independent of Manus. YARP is independent of ChatGPT. YARP is independent of Claude, Gemini, and all current transports. It will outlive all of them.

---

## Article II — Core Doctrine (Immutable)

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

These nine principles are immutable. No gate may override them.

---

## Article III — yOS Backbone Architecture

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

**Module roles:**

| Module | Full Name | Role |
|---|---|---|
| **KAP** | Knowledge Assimilation Protocol | Captures, structures, and assimilates knowledge into yOS |
| **MPM** | Mega Prompt Machine | Orchestrates and executes Mega Prompts |
| **YARP** | YOS Agent Relay Protocol | Defines communication between agents |
| **BUS** | YOS Bus | Runtime/transport substrate — moves packets between agents |

**Invariants:**
- YARP rides on BUS. YARP carries MPM packets. YARP returns MPR results.
- YARP must not replace BUS or MPM. YARP must not be replaced by BUS or MPM.
- BUS is YARP's primary transport substrate. BUS does not define YARP.

---

## Article IV — Scope

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
- Knowledge assimilation (governed by KAP)

---

## Article V — Layered Architecture

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

## Article VI — Relationship to BUS, MPM, MPR

```
YARP = protocol (this module)         → defines meaning
BUS  = transport/runtime substrate    → moves packets
MPM  = orchestration of Mega Prompts  → executes
MPR  = report artifact                → produced by MPM execution
```

**The distinction is fundamental:**

YARP defines *what* is communicated and *what it means*.
BUS defines *how* it is physically moved.

A YARP EXECUTE_MP message is meaningful regardless of whether it travels via Manus API, filesystem, Git, or a future quantum transport. The meaning is in YARP. The delivery is in BUS.

---

## Article VII — JSON-First Principle

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

## Article VIII — Versioning

YARP versions follow semantic versioning: `MAJOR.MINOR.PATCH`.

- MAJOR: breaking changes to message schema or state machine
- MINOR: new message types or optional fields
- PATCH: documentation, error catalogue, adapter updates

Current version: `1.1.0`

Session handshake MUST include `yarp_version`. Agents MUST reject sessions with incompatible MAJOR versions.

---

## Article IX — Immutability of the Constitution

This constitution may be amended only by a dedicated MPM marathon gate with `guardian_required: true`.

No sprint or run gate may amend Articles I-VII.

Amendments must increment MINOR version for clarifications (no breaking changes).
Amendments must increment MAJOR version if they change the core doctrine (Article II) or layered architecture (Article V).

---

## Changelog

| Version | Gate | Change |
|---|---|---|
| v1.0.0 | MPM-20260705-YOS-AGENT-RELAY-PROTOCOL-CONSTITUTION-GATE | Initial constitution |
| v1.1.0 | MPM-20260705-YOS-YARP-CONSTITUTION-CLARIFICATION-PATCH-GATE | Added HTTP analogy, backbone diagram, "YARP defines meaning / BUS moves packets" doctrine, first-class module declaration, Article IX |
