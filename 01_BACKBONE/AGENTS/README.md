# AGENTS — YOS Agent Identity, Capabilities, Trust & Routing

> **Version:** v1.0.0-candidate
> **Status:** candidate
> **Gate:** MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE
> **Created:** 2026-07-05

---

## What is AGENTS?

> **AGENTS answers the fundamental yOS question: Who speaks YARP?**
>
> YARP is the language.
> AGENTS defines who can speak, what they can do, and under what trust boundaries.
> BUS moves the messages.
> MPM orchestrates work.
> KAP assimilates knowledge.

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
 │                │                │
 └────────────────┼────────────────┘
                  │
               AGENTS
  Identity · Capabilities · Trust · Routing
                  │
                 BUS
      Runtime / Transport Substrate
```

| Module | Full Name | Role |
|---|---|---|
| **KAP** | Knowledge Assimilation Protocol | Captures, structures, and assimilates knowledge into yOS |
| **MPM** | Mega Prompt Machine | Orchestrates and executes Mega Prompts |
| **YARP** | YOS Agent Relay Protocol | Defines communication between agents |
| **AGENTS** | YOS Agents Module | Identity, capabilities, trust, permissions, discovery, routing |
| **BUS** | YOS Bus | Runtime/transport substrate — moves packets between agents |

---

## Core Doctrine

```
YARP is the language.
AGENTS defines who can speak, what they can do, and under what trust boundaries.
BUS moves the messages.
MPM orchestrates work.
KAP assimilates knowledge.

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

---

## Placement Justification

AGENTS is placed at `01_BACKBONE/AGENTS/` because:

1. **AGENTS is a first-class backbone module.** It sits alongside KAP, MPM, YARP, and BUS as a peer.
2. **AGENTS does not execute tasks.** That is MPM's role.
3. **AGENTS does not transport packets.** That is BUS's role.
4. **AGENTS does not define message semantics.** That is YARP's role.
5. **AGENTS defines who the actors are** — their identity, capabilities, trust level, and routing rules.

---

## Module Structure

```
01_BACKBONE/AGENTS/
├── README.md                              ← this file
├── 00_SPEC/
│   ├── AGENT-CONSTITUTION.md              ← immutable doctrine
│   ├── AGENT-LIFECYCLE.md                 ← agent lifecycle states
│   ├── AGENT-ROLES.md                     ← role taxonomy
│   └── AGENT-CAPABILITY-MODEL.md          ← capability ontology
├── 01_REGISTRY/
│   ├── agents.json                        ← canonical agent registry
│   ├── capabilities.json                  ← capability registry
│   ├── transports.json                    ← transport registry
│   └── trust-levels.json                  ← trust level definitions
├── 02_IDENTITIES/
│   ├── chatgpt.md                         ← ChatGPT identity card
│   ├── manus.md                           ← Manus identity card
│   ├── claude.md                          ← Claude identity card
│   ├── gemini.md                          ← Gemini identity card
│   ├── codex.md                           ← Codex identity card
│   └── yos-agent-template.md              ← generic template
├── 03_CAPABILITIES/
│   ├── reasoning.schema.json
│   ├── coding.schema.json
│   ├── vision.schema.json
│   ├── filesystem.schema.json
│   ├── api.schema.json
│   ├── memory.schema.json
│   ├── planning.schema.json
│   └── execution.schema.json
├── 04_ROUTING/
│   ├── ART/                               ← Agent Routing Table
│   ├── CRT/                               ← Cognitive Routing Table
│   ├── routing-rules.md
│   ├── capability-selection.md
│   └── model-selection.md
├── 05_TRUST/
│   ├── trust-model.md
│   ├── permissions.md
│   ├── authentication.md
│   └── execution-boundaries.md
├── 06_DISCOVERY/
│   ├── discovery-protocol.md
│   ├── capability-query.md
│   └── registry-sync.md
└── 99_ARCHIVE/
```

---

## Integration with Other Backbone Modules

| Module | Integration |
|---|---|
| **YARP** | Uses AGENTS for identity and capability negotiation during session handshake |
| **BUS** | Uses AGENTS for routing decisions and trust boundary enforcement |
| **MPM** | Uses AGENTS to select executors for Mega Prompt execution |
| **KAP** | Uses AGENTS to select assimilation/review agents |
| **GOVERNANCE** | Uses AGENTS for permission and approval boundaries |
