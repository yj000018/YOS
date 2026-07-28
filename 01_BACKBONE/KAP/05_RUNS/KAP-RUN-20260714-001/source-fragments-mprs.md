# KAP Source Fragments — MPRs
## KAP-RUN-20260714-001 / Phase A

**Source:** `01_BACKBONE/MPM/06_REPORTS/awaiting-review/` (21 files)
**Extracted:** 2026-07-14
**Evidence level:** 9/10 (durable gate reports, committed to Git)

---

## SF-MPR-001 — BUS Module Creation
**Source:** MPM-20260705-YOS-BUS-MPM-FUSION-AND-DIRECT-RUNTIME-GATE-REPORT.md
**Commit:** bce8abb
**Fragment:**
Module `01_BACKBONE/BUS/` créé de zéro — 62 fichiers, 3860 insertions. BUS = transport substrate for MPM packets. 7 protocols, 6 schemas JSON, 6 adapters, 4 templates, 6 domains, 6 runtime backends, 3 indexes, CLI tool `bus.py`.

**Key assertions:**
- BUS transports MPM packets. MPM executes them. MPM owns the ledger/reports.
- MP resolution order: `$YOS_BUS_RUNTIME_ROOT/inbox/mpm/` → `MPM/04_QUEUE/ready/` → `BUS/04_DOMAINS/mpm/inbox/`
- Direct-file backend = preferred (no network dependency)

---

## SF-MPR-002 — BUS Transport Test
**Source:** MPM-20260705-YOS-BUS-MPM-TRANSPORT-TEST-GATE-REPORT.md
**Commit:** 3fa0c3d
**Fragment:**
BUS inbox/mpm transport path validated end-to-end. `bus.py claim --dry-run` PASS. `bus.py claim --apply` applied. BUS lifecycle complete (inbox → workspace → outbox). MPM adapter doctrine confirmed.

**Key assertions:**
- BUS inbox detection works with Git fallback
- Claim apply moves packet from inbox to workspace atomically
- BUS-first policy confirmed operational

---

## SF-MPR-003 — Direct-File Runtime
**Source:** MPM-20260705-YOS-BUS-DIRECT-FILE-RUNTIME-PROBE-GATE-REPORT.md
**Commit:** 915085c
**Fragment:**
Direct-file runtime initialized at `/home/ubuntu/yos-bus-runtime`. Cross-session persistence proven. `YOS_BUS_RUNTIME_ROOT` env var activates direct-file mode. Claim dry-run ~43ms. `/tmp` is ephemeral — use `/home/ubuntu/` for persistence.

**Key assertions:**
- `/home/ubuntu/` persists cross-session in Manus sandbox
- Direct-file runtime = production_ready
- Canonical persistent path: `/home/ubuntu/yos-bus-runtime`

---

## SF-MPR-004 — First/Last Mile Integration
**Source:** MPM-20260705-YOS-BUS-FIRST-LAST-MILE-INTEGRATION-GATE-REPORT.md
**Commit:** 8244928
**Fragment:**
`bus.py` upgraded to v1.1.0 with 6 new commands: `write`, `ingest`, `latest-report`, `report-pointer`, `entry-backends`, `report-backends`. First-mile (entry adapters) and last-mile (report adapters) protocols defined. 5 entry adapters, 1 report adapter. MPM protocols patched to v1.6.0.

**Key assertions:**
- First-mile = how MPs enter BUS (manual-upload, direct-file, git, google-drive, manus-workspace)
- Last-mile = how MPRs exit BUS to reach A&G (report-fast-path = latest-mpr.json)
- `bus.py ingest` = canonical first-mile command
- `bus.py latest-report` = canonical last-mile command

---

## SF-MPR-005 — Manus Workspace Probe
**Source:** MPM-20260705-YOS-BUS-MANUS-WORKSPACE-PROBE-GATE-REPORT.md
**Commit:** f67a834
**Fragment:**
Probe A (filesystem) PASS. Probe B (MCP) = probe_required (0 servers configured). Probe C (API) = probe_required. `manus_workspace` classified as `candidate`. `manus-upload-file` = S3 CDN public, not a workspace write backend.

**Key assertions:**
- Workspace filesystem = production_ready backend
- MCP bridge available but no servers configured
- S3 CDN upload ≠ workspace write (different mechanism)
- ChatGPT → Manus write path = indirect (via task instruction relay)

---

## SF-MPR-006 — Manus Connectivity Census
**Source:** MPM-20260705-YOS-MANUS-CONNECTIVITY-CENSUS-GATE-REPORT.md
**Commit:** 9ec42f8
**Fragment:**
Full census of all Manus connectivity mechanisms. 8 mechanisms ranked. Connectivity matrix: JSON + MD. Migration roadmap: 5 phases. Entry/report backend registries updated with new backends.

**Key assertions:**
- Best backend: workspace_filesystem (production_ready)
- Fallback chain: filesystem → git → api_task → webhook → connector → mcp → blob
- 252 connectors available, 0 enabled for yOS
- Webhooks supported (task_created, task_stopped)

---

## SF-MPR-007 — Manus API Capability Verification
**Source:** MPM-20260705-YOS-MANUS-API-CAPABILITY-VERIFICATION-GATE-REPORT.md
**Commit:** adc5211
**Fragment:**
OpenAPI spec analyzed. task.create, sendMessage, file.upload (3 methods: file_id 512MB, file_url 20MB, file_data 20MB) all proven. Workspace write = unsupported direct / supported indirect. Best pattern: Async Task Relay (task.sendMessage + structured_output_schema). Rate limit: 10/min.

**Key assertions:**
- `task.sendMessage` + `agent-default-main_task` = conversation continuation shortcut
- `structured_output_schema` → `structured_output_result` event = JSON result extraction
- No direct workspace write via API — must relay through agent instruction
- Auth: `x-manus-api-key` header (need to generate key)

---

## SF-MPR-008 — YARP Constitution
**Source:** MPM-20260705-YOS-AGENT-RELAY-PROTOCOL-CONSTITUTION-GATE-REPORT.md
**Commit:** 98513cf
**Fragment:**
Module `01_BACKBONE/YARP/` created. 9 spec/governance files, 7 JSON schemas, 13 message types, 8 transport adapters, 5 layers. YARP v1.0.0-candidate.

**Key assertions:**
- YARP defines meaning. BUS moves packets.
- YARP is transport-independent.
- JSON is primary. Markdown is audit.
- Git is durable memory, not the protocol.
- Agents are peers.

---

## SF-MPR-009 — YARP Constitution Clarification
**Source:** MPM-20260705-YOS-YARP-CONSTITUTION-CLARIFICATION-PATCH-GATE-REPORT.md
**Commit:** 5546463
**Fragment:**
YARP-CONSTITUTION.md patched v1.0.0 → v1.1.0. HTTP analogy added. Backbone diagram added. 9 immutable principles formalized. Consistency check: 17 YARP files — no conflicts.

**Key assertions:**
- "YARP is to yOS what HTTP is to the Web"
- "YARP is independent of Manus. YARP is independent of ChatGPT."
- "YARP will outlive all current transports."
- Backbone: yOS → KAP · MPM · YARP · AGENTS · BUS

---

## SF-MPR-010 — AGENTS Backbone Constitution
**Source:** MPM-20260705-YOS-AGENTS-BACKBONE-CONSTITUTION-GATE-REPORT.md
**Commit:** 0385844
**Fragment:**
Module `01_BACKBONE/AGENTS/` created. 35 files. 6 agents registered (chatgpt-ag, manus, claude, gemini, codex, yannick). 8 capability schemas. Trust levels T0→T5. ART + CRT routing. Discovery protocol.

**Key assertions:**
- Agents have identities.
- Capabilities are declarative.
- Trust is explicit.
- No agent is globally privileged by default.
- Human operators are also agents.
- A capability declaration is a claim, not a proof.

---

## SF-MPR-011 — KAP Knowledge Adapter Census
**Source:** MPM-20260705-YOS-KAP-KNOWLEDGE-ADAPTER-CENSUS-AND-PROBE-GATE-REPORT.md
**Commit:** 25a0114
**Fragment:**
19 adapters catalogued. 5 protocols, 4 schemas, 2 registries, 1 census, 1 probe-results. Stack: workspace_filesystem (production_ready) + git-repository (production_ready) + manus-api + openai-api + notion-api.

**Key assertions:**
- Consumer apps (ChatGPT.com, Claude.ai, etc.) = unsupported programmatically — architectural constraint
- Workspace filesystem = canonical KAP entry point
- KAP pipeline = 4 phases: Acquisition → Analysis → Human Validation → Synthesis
- Human validation required before CBS promotion to CANON

---

## SF-MPR-012 — Chronicles Historical Discovery
**Source:** MPM-20260705-YOS-CHRONICLES-MANUS-HISTORICAL-DISCOVERY-EXCAVATION-GATE-REPORT.md
**Commit:** c05dad1
**Fragment:**
`00_META/CHRONICLES/MANUS-HISTORICAL-DISCOVERY/` created. 11 discoveries, 15 fulgurances, 6 emergence events, 7 Chronicles passages, 8 open hypotheses. Sources: 11 MPRs from 2026-07-05 session.

**Key assertions (top fulgurances):**
- "YARP defines meaning. BUS moves packets."
- "JSON is primary. Markdown is audit."
- "Git is durable memory, not the protocol."
- "Trust is not inherited from vendor or runtime."
- "A capability declaration is a claim, not a proof."
- "Everything important to yOS must be findable in one clear place."

---

## SF-MPR-013 — Monorepo Canonical Reorganization
**Source:** YOS-MONOREPO-CANONICAL-REORGANIZATION-GATE-REPORT.md
**Fragment:**
yOS monorepo reorganized with canonical structure. `01_BACKBONE/` = backbone modules. `00_META/` = meta/chronicles. `08_LOGS/` = operational logs. `yos-governance/` = governance docs.

**Key assertions:**
- Everything important to yOS must be findable in one clear place
- Monorepo = single source of truth for yOS architecture

---

## SF-MPR-014 — MPM Local Runtime Optimization
**Source:** MPM-20260705-YOS-MPM-LOCAL-RUNTIME-OPTIMIZATION-GATE-REPORT.md
**Fragment:**
MPM local runtime optimized. `mpm.py` enhanced with reconcile-ledger, validate, run-next commands. Stale_running detection added.

**Key assertions:**
- MPM validate = canonical health check
- reconcile-ledger = ledger consistency enforcement
- stale_running = MPs stuck in running state without commit

---

## SF-MPR-015 — Architecture Baseline v0.5 (Codex)
**Source:** `yos-governance/Architecture/Baseline-v0.5/` (branch agent/yos-baseline-v0.5, PR #2)
**Fragment:**
15 files, 2920 insertions. 5-plane architecture (Experience/Control/Cognitive/Knowledge/Growth). 50+ modules. Concept lineage for 18 concept families. Canon promotion rules. Source-of-truth matrix. Open questions queue.

**Key assertions:**
- yOS has 5 architectural planes
- 50+ modules across all planes
- Canon promotion requires evidence, not just assertion
- Git = durable memory, not the protocol
- ChatGPT consolidation phase complete — next: GitHub archaeology

---

## Summary

| SF ID | Gate | Domain | Evidence Level |
|---|---|---|---|
| SF-MPR-001 | BUS-MPM-FUSION | BUS | 9/10 |
| SF-MPR-002 | BUS-TRANSPORT-TEST | BUS | 9/10 |
| SF-MPR-003 | DIRECT-FILE-RUNTIME | BUS | 9/10 |
| SF-MPR-004 | FIRST-LAST-MILE | BUS | 9/10 |
| SF-MPR-005 | MANUS-WORKSPACE-PROBE | BUS/KAP | 9/10 |
| SF-MPR-006 | CONNECTIVITY-CENSUS | BUS/KAP | 9/10 |
| SF-MPR-007 | API-CAPABILITY-VERIFICATION | KAP/YARP | 9/10 |
| SF-MPR-008 | YARP-CONSTITUTION | YARP | 9/10 |
| SF-MPR-009 | YARP-CLARIFICATION | YARP | 9/10 |
| SF-MPR-010 | AGENTS-CONSTITUTION | AGENTS | 9/10 |
| SF-MPR-011 | KAP-ADAPTER-CENSUS | KAP | 9/10 |
| SF-MPR-012 | CHRONICLES-EXCAVATION | META | 9/10 |
| SF-MPR-013 | MONOREPO-REORGANIZATION | BACKBONE | 8/10 |
| SF-MPR-014 | MPM-RUNTIME-OPTIMIZATION | MPM | 8/10 |
| SF-MPR-015 | BASELINE-V0.5 | GOVERNANCE | 8/10 |

**Total: 15 Source Fragments from MPR source**
