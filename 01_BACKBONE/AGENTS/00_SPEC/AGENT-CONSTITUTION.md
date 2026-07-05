# AGENT Constitution

> **Version:** v1.0.0
> **Status:** candidate
> **Immutable after:** canonical designation
> **Gate:** MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE

---

## Article I — Identity

AGENTS (YOS Agents Module) is the yOS backbone module governing intelligent actor identity, capability, trust, permission, discovery, and routing.

AGENTS does not execute tasks directly.
AGENTS does not transport packets.
AGENTS does not define message semantics.
AGENTS defines who the actors are, what they can do, how they are trusted, and how they are selected.

**AGENTS is a first-class backbone module of yOS.** It is a peer of KAP, MPM, YARP, and BUS — not a sub-module of any of them.

---

## Article II — Core Doctrine (Immutable)

```
Agents have identities.
Agents expose capabilities.
Capabilities are declarative.
Trust is explicit.
Permissions are bounded.
Routing is capability-based.
Discovery is protocolized.
No agent is globally privileged by default.
Human operators are also agents.
```

These nine principles are immutable. No gate may override them.

---

## Article III — Relationship to YARP, BUS, MPM, KAP

```
YARP is the language.
AGENTS defines who can speak, what they can do, and under what trust boundaries.
BUS moves the messages.
MPM orchestrates work.
KAP assimilates knowledge.
```

**Integration invariants:**

| Module | AGENTS Role |
|---|---|
| YARP | AGENTS provides identity and capability declarations for YARP session negotiation |
| BUS | AGENTS provides routing rules and trust boundaries for BUS packet dispatch |
| MPM | AGENTS provides executor selection criteria for Mega Prompt assignment |
| KAP | AGENTS provides agent selection for knowledge assimilation and review |
| GOVERNANCE | AGENTS provides permission and approval boundaries |

---

## Article IV — Scope

AGENTS governs:

- Agent identity (who an agent is)
- Agent capabilities (what an agent can do)
- Trust levels (how much an agent is trusted)
- Permission boundaries (what an agent is allowed to do)
- Routing rules (how agents are selected for tasks)
- Discovery protocol (how agents announce and query capabilities)

AGENTS does not govern:

- Message format (governed by YARP)
- Transport mechanics (governed by BUS)
- Task execution logic (governed by MPM)
- Knowledge assimilation (governed by KAP)
- Internal agent reasoning (chain-of-thought)

---

## Article V — Agent Identity Model

Every agent in yOS MUST have:

- A unique `agent_id`
- A declared `agent_type` (llm | human | automation | hybrid)
- A declared `trust_level` (T0 through T5)
- A list of `known_capabilities` with validated status
- A list of `supported_transports`
- A list of `supported_yarp_roles`

Agents MUST NOT overclaim capabilities. Use status: `proven | candidate | unknown | unsupported`.

---

## Article VI — Trust Principle

```
No agent receives corpus mutation, secret access, or automation deployment permission by default.

All permissions must be explicitly granted.
All trust levels must be explicitly declared.
Trust is not inherited from vendor or runtime.
```

---

## Article VII — Capability Principle

```
Capabilities are declarative, not imperative.
A capability declaration is a claim, not a proof.
Claims must be validated before being marked proven.
Unknown capabilities must be declared as unknown, not omitted.
```

---

## Article VIII — Routing Principle

```
Routing decisions are capability-based.
No agent is selected by name alone.
Selection criteria: capability match + trust level + permission boundary + availability.
```

---

## Article IX — Immutability of the Constitution

This constitution may be amended only by a dedicated MPM marathon gate with `guardian_required: true`.

No sprint or run gate may amend Articles I-VIII.

Amendments must increment MINOR version for clarifications.
Amendments must increment MAJOR version if they change the core doctrine (Article II) or scope (Article IV).
