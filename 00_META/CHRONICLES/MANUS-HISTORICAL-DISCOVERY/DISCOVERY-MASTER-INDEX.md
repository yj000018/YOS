# Discovery Master Index

> **Source Gate:** MPM-20260705-YOS-CHRONICLES-MANUS-HISTORICAL-DISCOVERY-EXCAVATION-GATE
> **Type:** Master index of all discoveries
> **Status:** v1.0.0

---

## Discovery Registry

| ID | Title | Category | Status | Source |
|---|---|---|---|---|
| DISC-001 | Transport ≠ Persistence | architectural_revelation | canonical | BUS-MPM-FUSION-GATE |
| DISC-002 | BUS ≠ Protocol | architectural_revelation | canonical | YARP-CONSTITUTION-GATE |
| DISC-003 | Protocol Requires Actors | architectural_revelation | canonical | AGENTS-BACKBONE-GATE |
| DISC-004 | Trust is Explicit | constitutional_discovery | canonical | AGENTS-BACKBONE-GATE |
| DISC-005 | Capabilities are Declarative | constitutional_discovery | canonical | AGENTS-BACKBONE-GATE |
| DISC-006 | JSON is Primary | documentation_doctrine | canonical | YOS-CONSTITUTION |
| DISC-007 | Workspace Filesystem is Canonical Runtime | implementation_consequence | canonical | WORKSPACE-PROBE-GATE |
| DISC-008 | /tmp is Ephemeral | implementation_consequence | canonical | DIRECT-FILE-PROBE-GATE |
| DISC-009 | Async Task Relay Pattern | implementation_consequence | candidate | API-CAPABILITY-GATE |
| DISC-010 | Single Monorepo | architectural_revelation | canonical | MONOREPO-REORGANIZATION-GATE |
| DISC-011 | Backbone Topology | architectural_revelation | canonical | YOS-CONSTITUTION |

---

## Fulgurance Registry

| ID | Phrase | Source | Status |
|---|---|---|---|
| F-001 | "YARP defines meaning. BUS moves packets." | YARP-CONSTITUTION v1.1.0 | canonical |
| F-002 | "YARP is transport-independent. Transports are adapters." | YARP-CONSTITUTION v1.1.0 | canonical |
| F-003 | "JSON is primary. Markdown is audit." | YARP-CONSTITUTION + YOS-CONSTITUTION | canonical |
| F-004 | "Git is durable memory, not the protocol." | YARP-CONSTITUTION v1.1.0 | canonical |
| F-005 | "BUS is the operational transport substrate, not the protocol itself." | YARP-CONSTITUTION v1.1.0 | canonical |
| F-006 | "Agents are peers. No agent is architecturally privileged." | YARP-SPEC + AGENT-CONSTITUTION | canonical |
| F-007 | "Trust is not inherited from vendor or runtime." | AGENT-CONSTITUTION Article VI | canonical |
| F-008 | "A capability declaration is a claim, not a proof." | AGENT-CONSTITUTION Article VII | canonical |
| F-009 | "Everything important to yOS must be findable in one clear place." | YOS-CONSTITUTION v1.0.0 | canonical |
| F-010 | "No agent is selected by name alone." | AGENT-CONSTITUTION Article VIII | canonical |
| F-011 | Backbone diagram (KAP · MPM · YARP · AGENTS / BUS) | YARP-CONSTITUTION + AGENTS README | canonical |
| F-012 | "/home/ubuntu/yos-bus-runtime = canonical persistent BUS runtime" | WORKSPACE-PROBE-GATE | canonical |
| F-013 | "The manual upload bridge is operational but not the target state." | bus-migration-roadmap.md | candidate |
| F-014 | "This constitution may be amended only by marathon + guardian." | YARP-CONSTITUTION Article IX | canonical |
| F-015 | "task.sendMessage + structured_output_schema → MPR as JSON result" | API-CAPABILITY-GATE | candidate |

---

## Emergence Event Registry

| ID | Title | Status | Source |
|---|---|---|---|
| EE-001 | BUS/YARP Separation | canonical | YARP-CONSTITUTION-CLARIFICATION-GATE |
| EE-002 | Protocol Requires Actors → AGENTS | canonical | AGENTS-BACKBONE-GATE |
| EE-003 | Workspace Persistence Discovery | canonical | WORKSPACE-PROBE-GATE |
| EE-004 | Monorepo Consolidation | canonical | MONOREPO-REORGANIZATION-GATE |
| EE-005 | No-Direct-Write Discovery | candidate | API-CAPABILITY-GATE |
| EE-006 | First-Mile / Last-Mile Naming | canonical | FIRST-LAST-MILE-GATE |

---

## Gate Genealogy (Chronological)

| # | Gate | Mode | Key Discovery |
|---|---|---|---|
| 1 | YOS-MONOREPO-CANONICAL-REORGANIZATION | marathon | Single monorepo topology |
| 2 | YOS-MAIN-PR-MERGE | run | Monorepo on main |
| 3 | YOS-MPM-LOCAL-RUNTIME-OPTIMIZATION | marathon | mpm.py CLI + local runtime |
| 4 | YOS-MPM-MPR-COMMIT-SUMMARY-MICROPATCH | sprint | Commit hash hygiene |
| 5 | YOS-MPM-METADATA-TBD-MICROPATCH | sprint | TBD field cleanup |
| 6 | YOS-BUS-MPM-FUSION-AND-DIRECT-RUNTIME-GATE | marathon | BUS module created |
| 7 | YOS-BUS-MPM-TRANSPORT-TEST-GATE | sprint | BUS transport validated |
| 8 | YOS-BUS-DIRECT-FILE-RUNTIME-PROBE-GATE | run | /tmp ephemeral, /home/ubuntu/ persistent |
| 9 | YOS-MANUS-CONNECTIVITY-CENSUS-GATE | marathon | All Manus mechanisms mapped |
| 10 | YOS-MANUS-API-CAPABILITY-VERIFICATION-GATE | sprint | No direct workspace write |
| 11 | YOS-AGENT-RELAY-PROTOCOL-CONSTITUTION-GATE | marathon | YARP constituted |
| 12 | YOS-YARP-CONSTITUTION-CLARIFICATION-PATCH-GATE | sprint | BUS ≠ YARP separation |
| 13 | YOS-AGENTS-BACKBONE-CONSTITUTION-GATE | marathon | AGENTS constituted |
| 14 | YOS-BUS-MANUS-WORKSPACE-PROBE-GATE | run | Workspace classified candidate |
| 15 | YOS-BUS-FIRST-LAST-MILE-INTEGRATION-GATE | marathon | First/last mile named + implemented |
| 16 | YOS-CHRONICLES-MANUS-HISTORICAL-DISCOVERY-EXCAVATION-GATE | marathon | This gate |

---

## Open Hypotheses Registry

| ID | Title | Status |
|---|---|---|
| OH-001 | Pre-Monorepo History | requires_excavation |
| OH-002 | KOSMOS Definition | requires_ag_synthesis |
| OH-003 | ELYSIUM Connection | requires_ag_synthesis |
| OH-004 | A&G Decision Protocol | requires_ag_clarification |
| OH-005 | N100 Lambda Integration | future_gate |
| OH-006 | MCP Server Setup | future_gate |
| OH-007 | Webhook Last-Mile | future_gate |
| OH-008 | Reflex Architecture Activation | future_gate |
