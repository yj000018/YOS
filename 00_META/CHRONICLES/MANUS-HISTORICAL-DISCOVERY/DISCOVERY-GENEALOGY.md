# Discovery Genealogy

> **Source Gate:** MPM-20260705-YOS-CHRONICLES-MANUS-HISTORICAL-DISCOVERY-EXCAVATION-GATE
> **Type:** Idea genealogy — not a chronology. Shows how one idea generated another.
> **Status:** v1.0.0

---

## Genealogy Map

```
PROBLEM: Git too slow for real-time agent exchange
  → INSIGHT: Transport ≠ Persistence
    → IDEA: Separate transport layer from durable storage
      → MODULE: BUS (universal transport substrate)
        → DISCOVERY: BUS ≠ Protocol
          → INSIGHT: BUS moves packets; something else must define meaning
            → MODULE: YARP (YOS Agent Relay Protocol)
              → DISCOVERY: Protocol requires Actors
                → INSIGHT: Actors need identity, capabilities, trust
                  → MODULE: AGENTS
                    → DISCOVERY: System requires self-observation
                      → FUTURE: OBSERVABILITY
                        → FUTURE: Living Architecture
                          → FUTURE: Ontology of Genesis
                            → FUTURE: KOSMOS relation

PROBLEM: MPM needs to receive MPs from ChatGPT
  → DISCOVERY: Manual upload is the current bridge
    → INSIGHT: First-mile = how MPs enter BUS
      → PROTOCOL: bus-first-last-mile-protocol.md
        → INSIGHT: Last-mile = how MPRs reach ChatGPT
          → DISCOVERY: GitHub is the current last-mile
            → FUTURE: Webhook last-mile (push notification)
              → FUTURE: task.sendMessage + structured_output = direct last-mile

PROBLEM: Where does Manus store files durably?
  → PROBE: Manus workspace filesystem (/home/ubuntu/)
    → DISCOVERY: /home/ubuntu/ persists cross-session
      → CANONICAL: /home/ubuntu/yos-bus-runtime = persistent BUS runtime
        → DISCOVERY: /tmp is ephemeral (not suitable for BUS)
          → RULE: Never use /tmp for BUS runtime

PROBLEM: How does ChatGPT write to Manus workspace?
  → CENSUS: All Manus connectivity mechanisms
    → DISCOVERY: No direct workspace write from ChatGPT
      → PATTERN: Async Task Relay Pattern
        → FUTURE: ChatGPT POST task.create → Manus agent → BUS inbox

PROBLEM: What is the canonical repo structure?
  → DECISION: Single monorepo (yj000018/YOS)
    → RULE: KAP is a backbone module, not a project
      → RULE: MPM is a backbone module
        → TOPOLOGY: 01_BACKBONE/ = all backbone modules
          → DISCOVERY: BUS, YARP, AGENTS are also backbone modules
            → TOPOLOGY: 01_BACKBONE/{BUS,YARP,AGENTS}/

PROBLEM: How do agents trust each other?
  → INSIGHT: Trust is not inherited from vendor or runtime
    → MODEL: T0 → T5 trust levels (explicit declaration)
      → RULE: No agent receives corpus mutation permission by default
        → RULE: All permissions must be explicitly granted

PROBLEM: How do we select the right agent for a task?
  → INSIGHT: Selection by name alone is insufficient
    → PRINCIPLE: Routing is capability-based
      → PROTOCOL: ART (Agent Routing Table) + CRT (Capability Routing Table)
        → DISCOVERY: Capabilities must be declarative, not imperative
          → RULE: Claims must be validated before being marked proven
```

---

## Genealogy Nodes (Structured)

### Node 001 — Transport ≠ Persistence

```yaml
idea_id: DISC-001
title: Transport ≠ Persistence
first_seen_source: MPM-20260705-YOS-BUS-MPM-FUSION-AND-DIRECT-RUNTIME-GATE
supporting_sources:
  - bus-canonical-doctrine.md
  - MPM-20260705-YOS-BUS-MPM-TRANSPORT-TEST-GATE-REPORT.md
child_ideas: [DISC-002]
parent_ideas: []
status: canonical
canonical_consequence: BUS module created as separate transport substrate
```

### Node 002 — BUS ≠ Protocol

```yaml
idea_id: DISC-002
title: BUS is a transport substrate, not a protocol
first_seen_source: MPM-20260705-YOS-AGENT-RELAY-PROTOCOL-CONSTITUTION-GATE
supporting_sources:
  - YARP-CONSTITUTION.md v1.1.0
  - bus-canonical-doctrine.md §1
child_ideas: [DISC-003]
parent_ideas: [DISC-001]
status: canonical
canonical_consequence: YARP created as peer backbone module (not inside BUS)
canonical_phrase: "YARP defines meaning. BUS moves packets."
```

### Node 003 — Protocol Requires Actors

```yaml
idea_id: DISC-003
title: A protocol requires actors with identity and capabilities
first_seen_source: MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE
supporting_sources:
  - YARP-SPEC-v1.md §8
  - AGENT-CONSTITUTION.md
child_ideas: [DISC-004]
parent_ideas: [DISC-002]
status: canonical
canonical_consequence: AGENTS module created as backbone peer
```

### Node 004 — Trust is Explicit

```yaml
idea_id: DISC-004
title: Trust is explicit, not inherited
first_seen_source: MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE
supporting_sources:
  - AGENT-CONSTITUTION.md Article VI
  - trust-levels.json
child_ideas: [DISC-005]
parent_ideas: [DISC-003]
status: canonical
canonical_phrase: "Trust is not inherited from vendor or runtime."
```

### Node 005 — Capabilities are Declarative

```yaml
idea_id: DISC-005
title: Capabilities are declarative, not imperative
first_seen_source: MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE
supporting_sources:
  - AGENT-CONSTITUTION.md Article VII
  - capabilities.json
child_ideas: []
parent_ideas: [DISC-004]
status: canonical
canonical_phrase: "A capability declaration is a claim, not a proof."
```

### Node 006 — JSON First

```yaml
idea_id: DISC-006
title: JSON is primary; Markdown is audit
first_seen_source: YOS-CONSTITUTION.md v1.0.0
supporting_sources:
  - YARP-CONSTITUTION.md Article I
  - bus-canonical-doctrine.md §3
child_ideas: []
parent_ideas: []
status: canonical
canonical_phrase: "JSON is primary. Markdown is audit."
```

### Node 007 — Workspace Filesystem as Canonical Runtime

```yaml
idea_id: DISC-007
title: /home/ubuntu/ persists cross-session — canonical BUS runtime
first_seen_source: MPM-20260705-YOS-BUS-MANUS-WORKSPACE-PROBE-GATE-REPORT.md
supporting_sources:
  - direct-file-runtime-probe-latest.json
  - manus-workspace-probe-latest.json
child_ideas: [DISC-008]
parent_ideas: []
status: canonical
canonical_consequence: /home/ubuntu/yos-bus-runtime = canonical persistent BUS runtime
```

### Node 008 — /tmp is Ephemeral

```yaml
idea_id: DISC-008
title: /tmp is ephemeral — never use for BUS runtime
first_seen_source: MPM-20260705-YOS-BUS-DIRECT-FILE-RUNTIME-PROBE-GATE-REPORT.md
supporting_sources:
  - direct-file-runtime-probe-latest.json
child_ideas: []
parent_ideas: [DISC-007]
status: canonical
canonical_consequence: Recommendation documented in direct-file-runtime-probe-latest.json
```

### Node 009 — Async Task Relay Pattern

```yaml
idea_id: DISC-009
title: ChatGPT cannot write directly to Manus workspace — Async Task Relay Pattern
first_seen_source: MPM-20260705-YOS-MANUS-API-CAPABILITY-VERIFICATION-GATE-REPORT.md
supporting_sources:
  - manus-api-capability-matrix.md
  - manus-connectivity-matrix.md
child_ideas: []
parent_ideas: []
status: candidate
canonical_consequence: Phase 1 of bus-migration-roadmap.md
```

### Node 010 — Single Monorepo

```yaml
idea_id: DISC-010
title: YOS = single canonical Git repository for the entire yOS system
first_seen_source: YOS-CONSTITUTION.md v1.0.0
supporting_sources:
  - YOS-MONOREPO-CANONICAL-REORGANIZATION-GATE-REPORT.md
  - YOS-MAIN-PR-MERGE-GATE-REPORT.md
child_ideas: [DISC-011]
parent_ideas: []
status: canonical
canonical_phrase: "Everything important to yOS must be findable in one clear place."
```

### Node 011 — Backbone Topology

```yaml
idea_id: DISC-011
title: 01_BACKBONE/ = all backbone modules (MPM, KAP, BUS, YARP, AGENTS, ...)
first_seen_source: YOS-CONSTITUTION.md v1.0.0
supporting_sources:
  - YOS-MODULE-REGISTRY.md
  - MIGRATION-INDEX.md
child_ideas: []
parent_ideas: [DISC-010]
status: canonical
canonical_consequence: All backbone modules live under 01_BACKBONE/
```
