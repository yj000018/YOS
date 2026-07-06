# Fulgurances Master

> **Source Gate:** MPM-20260705-YOS-CHRONICLES-MANUS-HISTORICAL-DISCOVERY-EXCAVATION-GATE
> **Type:** Strong formulations, canonical phrases, architectural revelations
> **Status:** v1.0.0

---

## F-001 — The Core Separation

```yaml
phrase: "YARP defines meaning. BUS moves packets."
source: YARP-CONSTITUTION.md v1.1.0 (Article I)
context: >
  Emerged during the YARP-CONSTITUTION-CLARIFICATION-PATCH-GATE when A&G
  pushed back on the initial conflation of transport and protocol.
  This phrase became the canonical separator between BUS and YARP.
category: architectural_revelation
status: canonical
related_modules: [YARP, BUS]
wording_status: exact
```

---

## F-002 — Transport Independence

```yaml
phrase: "YARP is transport-independent. Transports are adapters."
source: YARP-CONSTITUTION.md v1.1.0 (Article I)
context: >
  Crystallized the insight that YARP must outlive any specific transport.
  BUS is one possible transport; it is not YARP itself.
category: architectural_revelation
status: canonical
related_modules: [YARP, BUS]
wording_status: exact
```

---

## F-003 — JSON is Primary

```yaml
phrase: "JSON is primary. Markdown is audit."
source: YARP-CONSTITUTION.md v1.1.0 + YOS-CONSTITUTION.md v1.0.0
context: >
  Repeated across multiple constitutions and protocols.
  Establishes the machine-readable layer as canonical,
  Markdown as human-readable generated view only.
category: documentation_doctrine
status: canonical
related_modules: [YARP, BUS, MPM, YOS]
wording_status: exact
```

---

## F-004 — Git is Memory, Not Protocol

```yaml
phrase: "Git is durable memory, not the protocol."
source: YARP-CONSTITUTION.md v1.1.0 (Article I)
context: >
  Emerged when clarifying that Git commits are too slow for real-time
  agent exchange. Git is where durable artifacts land, not where
  live communication happens.
category: architectural_revelation
status: canonical
related_modules: [YARP, BUS, Git]
wording_status: exact
```

---

## F-005 — BUS is Substrate, Not Protocol

```yaml
phrase: "BUS is the operational transport substrate, not the protocol itself."
source: YARP-CONSTITUTION.md v1.1.0 (Article I)
context: >
  The final clarification that resolved the BUS/YARP confusion.
  BUS is the physical layer; YARP is the semantic layer.
category: architectural_revelation
status: canonical
related_modules: [BUS, YARP]
wording_status: exact
```

---

## F-006 — Agents are Peers

```yaml
phrase: "Agents are peers. No agent is architecturally privileged."
source: YARP-SPEC-v1.md §1 + AGENT-CONSTITUTION.md Article II
context: >
  Established the symmetry principle. ChatGPT is not the master;
  Manus is not the servant. Both are peers with different capabilities
  and trust levels.
category: constitutional_discovery
status: canonical
related_modules: [YARP, AGENTS]
wording_status: reconstructed (paraphrase of multiple sources)
```

---

## F-007 — Trust is Not Inherited

```yaml
phrase: "Trust is not inherited from vendor or runtime."
source: AGENT-CONSTITUTION.md Article VI
context: >
  Emerged when designing the trust model. The fact that an agent
  is made by OpenAI or Anthropic does not grant it trust in yOS.
  Trust must be explicitly declared and validated.
category: constitutional_discovery
status: canonical
related_modules: [AGENTS]
wording_status: exact
```

---

## F-008 — Capabilities are Claims

```yaml
phrase: "A capability declaration is a claim, not a proof. Claims must be validated before being marked proven."
source: AGENT-CONSTITUTION.md Article VII
context: >
  Established the epistemological rigor of the capability model.
  Unknown capabilities must be declared as unknown, not omitted.
category: epistemology_of_discovery
status: canonical
related_modules: [AGENTS]
wording_status: exact
```

---

## F-009 — Everything in One Place

```yaml
phrase: "Everything important to yOS must be findable in one clear place."
source: YOS-CONSTITUTION.md v1.0.0 §1
context: >
  The founding principle of the monorepo. Emerged from the fragmentation
  of kap-control-plane, yos-cognitive-os, yos-agents, yos-automations
  across multiple repos.
category: architectural_revelation
status: canonical
related_modules: [YOS]
wording_status: exact
```

---

## F-010 — Routing is Capability-Based

```yaml
phrase: "No agent is selected by name alone. Selection criteria: capability match + trust level + permission boundary + availability."
source: AGENT-CONSTITUTION.md Article VIII
context: >
  Emerged when designing the routing model. The naive approach
  (always send to ChatGPT, always send to Manus) was rejected
  in favor of capability-based routing.
category: architectural_revelation
status: canonical
related_modules: [AGENTS, YARP]
wording_status: reconstructed (paraphrase of Article VIII)
```

---

## F-011 — The Backbone Diagram

```yaml
phrase: |
  yOS
   │
  KAP · MPM · YARP · AGENTS
   │
  BUS
  Runtime / Transport Substrate
source: YARP-CONSTITUTION.md v1.1.0 (Article III) + AGENTS/README.md
context: >
  The backbone diagram that emerged progressively. First KAP + MPM,
  then YARP added, then AGENTS added, then BUS as substrate.
  Each addition was a discovery, not a plan.
category: living_architecture
status: canonical
related_modules: [KAP, MPM, YARP, AGENTS, BUS]
wording_status: reconstructed (composite of multiple versions)
```

---

## F-012 — The Workspace is Canonical

```yaml
phrase: "/home/ubuntu/ persists cross-session. This is the canonical BUS runtime."
source: MPM-20260705-YOS-BUS-MANUS-WORKSPACE-PROBE-GATE-REPORT.md
context: >
  Discovered empirically during the workspace probe gate.
  Resolved a critical architectural uncertainty: where does
  Manus store BUS runtime files durably?
category: implementation_consequence
status: canonical
related_modules: [BUS]
wording_status: reconstructed
```

---

## F-013 — The Manual Upload Bridge

```yaml
phrase: "The manual upload bridge is the current first-mile. It is operational but not the target state."
source: bus-migration-roadmap.md (Phase 0)
context: >
  Honest acknowledgment of the current operational reality.
  The target is ChatGPT → task.create → BUS inbox (Phase 1).
  The bridge is temporary but fully functional.
category: implementation_consequence
status: candidate
related_modules: [BUS, MPM]
wording_status: reconstructed
```

---

## F-014 — Constitutions are Immutable by Design

```yaml
phrase: "This constitution may be amended only by a dedicated MPM marathon gate with guardian_required: true."
source: YARP-CONSTITUTION.md Article IX + AGENT-CONSTITUTION.md Article IX
context: >
  The meta-constitutional principle. Constitutions protect themselves
  from casual amendment. Only the highest-weight gate type (marathon + guardian)
  can change them.
category: constitutional_discovery
status: canonical
related_modules: [YARP, AGENTS, MPM]
wording_status: exact
```

---

## F-015 — The Async Task Relay Pattern

```yaml
phrase: "ChatGPT cannot write directly to Manus workspace. The canonical pattern is: task.sendMessage + structured_output_schema → MPR as JSON result."
source: MPM-20260705-YOS-MANUS-API-CAPABILITY-VERIFICATION-GATE-REPORT.md
context: >
  Discovered during the API capability verification gate.
  The absence of direct workspace write from ChatGPT forced
  the design of the Async Task Relay Pattern.
category: implementation_consequence
status: candidate
related_modules: [BUS, YARP, MPM]
wording_status: reconstructed
```
