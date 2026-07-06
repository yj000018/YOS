# Emergence Events Master

> **Source Gate:** MPM-20260705-YOS-CHRONICLES-MANUS-HISTORICAL-DISCOVERY-EXCAVATION-GATE
> **Type:** Emergence events — moments where a new architectural truth became visible
> **Status:** v1.0.0

---

## EE-001 — The BUS/YARP Separation

```yaml
event_id: EE-001
title: BUS and YARP are peers, not parent/child
trigger: >
  During YARP-CONSTITUTION-GATE, initial design placed YARP inside BUS
  (01_BACKBONE/BUS/00_PROTOCOLS/yarp/). A&G pushed back.
prior_confusion: >
  YARP was conceived as a BUS protocol — a way to format packets
  that travel through BUS. This made BUS the container and YARP the content.
friction: >
  If YARP is inside BUS, then BUS references YARP for message format,
  AND YARP references BUS for transport. Circular dependency.
  Also: YARP must outlive any specific transport.
realization: >
  BUS is the physical/transport layer. YARP is the semantic/protocol layer.
  They are peers at the same architectural level.
  BUS is one possible YARP transport — not the other way around.
new_responsibility: >
  YARP gets its own backbone module: 01_BACKBONE/YARP/
  BUS remains the transport substrate.
architectural_consequence: >
  Two separate backbone modules. YARP-CONSTITUTION.md establishes the
  immutable separation: "YARP defines meaning. BUS moves packets."
canonical_phrase: "YARP defines meaning. BUS moves packets."
source_refs:
  - MPM-20260705-YOS-AGENT-RELAY-PROTOCOL-CONSTITUTION-GATE-REPORT.md
  - MPM-20260705-YOS-YARP-CONSTITUTION-CLARIFICATION-PATCH-GATE-REPORT.md
  - YARP-CONSTITUTION.md v1.1.0
status: canonical
```

---

## EE-002 — The Protocol Requires Actors

```yaml
event_id: EE-002
title: A protocol without actors is incomplete — AGENTS emerges
trigger: >
  After YARP was constituted, the question arose: who are the senders
  and receivers in YARP envelopes? The answer required a formal model
  of agents with identity, capabilities, and trust.
prior_confusion: >
  Agents were informally referenced as "ChatGPT" and "Manus" without
  formal identity, capability declarations, or trust boundaries.
friction: >
  YARP envelope has sender_id and receiver_id fields. Without a registry,
  these are just strings. Without trust levels, any agent could claim
  any identity. Without capability declarations, routing is arbitrary.
realization: >
  A protocol requires actors. Actors require identity. Identity requires
  a registry. The registry requires governance. Governance requires
  a constitution.
new_responsibility: >
  AGENTS module created as a backbone peer.
  agents.json, capabilities.json, trust-levels.json as canonical registries.
architectural_consequence: >
  AGENTS becomes the identity and capability layer for all of yOS.
  YARP uses AGENTS for sender/receiver validation.
  BUS uses AGENTS for routing rules and trust boundaries.
  MPM uses AGENTS for executor selection.
canonical_phrase: "Agents have identities. Agents expose capabilities. Trust is explicit."
source_refs:
  - MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE-REPORT.md
  - AGENT-CONSTITUTION.md v1.0.0
status: canonical
```

---

## EE-003 — The Workspace Persistence Discovery

```yaml
event_id: EE-003
title: /home/ubuntu/ persists cross-session — canonical BUS runtime discovered
trigger: >
  During MANUS-WORKSPACE-PROBE-GATE, empirical testing of filesystem
  persistence across Manus sandbox sessions.
prior_confusion: >
  Uncertainty about whether Manus sandbox files persist between sessions.
  /tmp was initially used for BUS runtime in DIRECT-FILE-RUNTIME-PROBE-GATE.
friction: >
  /tmp is ephemeral. If BUS runtime is at /tmp, all state is lost
  between sessions. This would make BUS unreliable.
realization: >
  /home/ubuntu/ persists cross-session in Manus sandbox.
  This is the canonical location for the BUS runtime.
new_responsibility: >
  All BUS runtime operations use /home/ubuntu/yos-bus-runtime/
  /tmp is explicitly forbidden for BUS runtime.
architectural_consequence: >
  Stable, persistent BUS runtime established.
  direct-file backend classified as production_ready.
canonical_phrase: "/home/ubuntu/yos-bus-runtime = canonical persistent BUS runtime"
source_refs:
  - MPM-20260705-YOS-BUS-MANUS-WORKSPACE-PROBE-GATE-REPORT.md
  - MPM-20260705-YOS-BUS-DIRECT-FILE-RUNTIME-PROBE-GATE-REPORT.md
  - direct-file-runtime-probe-latest.json
status: canonical
```

---

## EE-004 — The Monorepo Consolidation

```yaml
event_id: EE-004
title: Fragmented repos → single canonical monorepo
trigger: >
  The existence of kap-control-plane, yos-cognitive-os, yos-agents,
  yos-automations, yos-governance, yos-vault as separate repos
  made yOS impossible to navigate.
prior_confusion: >
  Which repo is canonical? Where do new modules go?
  Is KAP a project or a backbone module?
friction: >
  Multiple repos = multiple sources of truth = inconsistency.
  New modules had no clear home.
realization: >
  One repo. One topology. Everything findable in one place.
  KAP and MPM are backbone modules, not projects.
new_responsibility: >
  yj000018/YOS = single canonical monorepo.
  01_BACKBONE/ = all backbone modules.
  Migration from legacy repos = ongoing.
architectural_consequence: >
  YOS-CONSTITUTION.md v1.0.0 established.
  YOS-MODULE-REGISTRY.md created.
  All new backbone modules go to 01_BACKBONE/.
canonical_phrase: "Everything important to yOS must be findable in one clear place."
source_refs:
  - YOS-MONOREPO-CANONICAL-REORGANIZATION-GATE-REPORT.md
  - YOS-MAIN-PR-MERGE-GATE-REPORT.md
  - YOS-CONSTITUTION.md v1.0.0
status: canonical
```

---

## EE-005 — The No-Direct-Write Discovery

```yaml
event_id: EE-005
title: ChatGPT cannot write directly to Manus workspace — Async Task Relay Pattern emerges
trigger: >
  During MANUS-API-CAPABILITY-VERIFICATION-GATE, systematic testing
  of all Manus API endpoints for workspace write capability.
prior_confusion: >
  Assumption that Manus API would provide a way for ChatGPT to
  directly write files to the Manus workspace.
friction: >
  file.upload → S3 CDN (not workspace). task.create → creates a task
  but does not write files directly. No direct workspace write endpoint exists.
realization: >
  The gap is architectural. ChatGPT can send messages to Manus via
  task.sendMessage. Manus agent can then write to workspace.
  This is the Async Task Relay Pattern.
new_responsibility: >
  Design the Async Task Relay Pattern as the canonical ChatGPT → Manus write path.
  Document in bus-migration-roadmap.md as Phase 1.
architectural_consequence: >
  Manual upload bridge remains operational for Phase 0.
  Phase 1 = task.create + structured_output_schema.
  Latency: 30-120s async (acceptable for MP execution).
canonical_phrase: "The canonical pattern is: task.sendMessage + structured_output_schema → MPR as JSON result."
source_refs:
  - MPM-20260705-YOS-MANUS-API-CAPABILITY-VERIFICATION-GATE-REPORT.md
  - manus-api-capability-matrix.md
  - bus-migration-roadmap.md
status: candidate
```

---

## EE-006 — The First-Mile / Last-Mile Naming

```yaml
event_id: EE-006
title: First-mile and last-mile as canonical BUS concepts
trigger: >
  During FIRST-LAST-MILE-INTEGRATION-GATE, the need to name
  the two ends of the BUS transport chain.
prior_confusion: >
  "How does an MP enter BUS?" and "How does an MPR reach ChatGPT?"
  were treated as separate problems without a unified vocabulary.
friction: >
  Without names, the concepts could not be designed, documented,
  or communicated precisely.
realization: >
  First-mile = how MPs enter BUS (from ChatGPT to Manus).
  Last-mile = how MPRs reach ChatGPT (from Manus to ChatGPT).
  Both are BUS concerns, not MPM concerns.
new_responsibility: >
  bus-first-last-mile-protocol.md created.
  bus.py extended with write, ingest, latest-report, report-pointer commands.
architectural_consequence: >
  BUS now owns both ends of the transport chain.
  MPM is the executor in the middle.
canonical_phrase: "First-mile: MP enters BUS. Last-mile: MPR reaches ChatGPT."
source_refs:
  - MPM-20260705-YOS-BUS-FIRST-LAST-MILE-INTEGRATION-GATE-REPORT.md
  - bus-first-last-mile-protocol.md
status: canonical
```
