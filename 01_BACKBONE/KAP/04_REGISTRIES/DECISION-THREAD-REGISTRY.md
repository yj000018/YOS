# Decision Thread Registry

> Y-OS / KAP Cognitive Architecture
> Gate: DECISION-THREAD-MODEL-GATE
> Status: UPDATED — prior entries preserved + new model-compliant entries added
> Last updated: 2026-07-03

---

## Purpose

This registry tracks all Decision Threads in the YOS/KAP cognitive architecture. Decision Threads are structured records of decisions — not tags, not thought lines, not final truths. They preserve what was decided, why, what alternatives were rejected, and whether the decision is still active.

---

## Prior Registry (from CAPTURE-PATCH — preserved verbatim)

### Architecture Decisions

| ID | Decision | Status | Source |
|---|---|---|---|
| DEC-YOS-001 | YOS is the global container; KAP is a module inside YOS | CONFIRMED | Manus KAP 2026-07-03 |
| DEC-YOS-002 | Architecture cognitive avant absorption massive | CONFIRMED | Both packs |
| DEC-YOS-003 | Git + Markdown is the durable authority | CONFIRMED | Both packs |
| DEC-YOS-004 | New doctrine → Control Plane; recovered sources → Source Staging | CONFIRMED | Manus KAP 2026-07-03 |
| DEC-YOS-012 | Scope is a tag on fragments, not a pipeline branch | CONFIRMED | Manus KAP 2026-07-03 |
| REPO-001 | Root repo = `yos-cognitive-os` (YOS-level, not KAP-level) | CONFIRMED (done) | ChatGPT 2026-07-03 |
| REPO-002 | KAP at `03_Modules/KAP/` | CONFIRMED (done) | ChatGPT 2026-07-03 |
| REPO-003 | Master repo + submodules/linked repos (mechanism TBD) | CANDIDATE | ChatGPT 2026-07-03 |
| REPO-004 | REPO-REGISTRY.md + repo_index.json mandatory | CONFIRMED (done) | ChatGPT 2026-07-03 |
| REPO-005 | New strategic docs captured in Git immediately | CONFIRMED (done) | ChatGPT 2026-07-03 |

### Source / Pipeline Decisions

| ID | Decision | Status | Source |
|---|---|---|---|
| DEC-YOS-008 | LLM Internal Memory extraction deferred until full taxonomy known | DEFERRED | Manus KAP 2026-07-03 |
| DEC-YOS-009 | Mem0 = ACQUIRED; derivative source; no dedicated gate needed | CONFIRMED | Manus KAP 2026-07-03 |
| DEC-YOS-010 | YOUniverse sources catalogued now; connectors built in Phase 3 | DEFERRED | Manus KAP 2026-07-03 |
| DEC-YOS-011 | ZIPs are transport only, not source of truth | CONFIRMED | Both packs |
| PIPE-001 | Manus: high-value, selective, gated | ACTIVE | ChatGPT 2026-07-03 |
| PIPE-002 | ChatGPT: core source; capture packs now; export schema later | ACTIVE | ChatGPT 2026-07-03 |
| PIPE-003 | Obsidian: high-feasibility; fake-vault allowed; real scan gated | ACTIVE | ChatGPT 2026-07-03 |
| PIPE-004 | Notion: active controlled pipeline; verification required | ACTIVE_WITH_VERIFICATION | ChatGPT 2026-07-03 |
| PIPE-005 | Git/Repos: master YOS repo + linked repos + registry; no legacy merge yet | ACTIVE | ChatGPT 2026-07-03 |
| PIPE-006 | Mem0: hint layer, not source of truth | ACTIVE | ChatGPT 2026-07-03 |
| DEC-BOOT-009 | Notion is frozen legacy / future migration target | ACTIVE | Bootstrap 2026-07-02 |
| DEC-BOOT-010 | ChatGPT2Notion deprecated as active path | DEPRECATED | Bootstrap 2026-07-02 |
| DEC-BOOT-011 | WP2-NOTION-DECOMMISSION sprint needed (future) | PLANNED | Bootstrap 2026-07-02 |

### Gate / Roadmap Decisions

| ID | Decision | Status | Source |
|---|---|---|---|
| DEC-BOOT-005 | STRUCTURE-GATE = PASS_WITH_MINOR_GAPS | ACCEPTED | Bootstrap 2026-07-02 |
| DEC-BOOT-006 | CONNECTOR-DESIGN-GATE defined and MPM created | DEFINED | Bootstrap 2026-07-02 |
| DEC-BOOT-012 | Corrected roadmap: ARCH-1-PATCH → STRUCTURE-GATE → CONNECTOR-DESIGN-GATE → PHASE-1-SEED-PLAN | ACTIVE | Bootstrap 2026-07-02 |
| DEC-YOS-007 | Phase 1 = yOS/KAP self-knowledge; Phase 2 = Project Knowledge; Phase 3 = YOUniverse | CONFIRMED | Manus KAP 2026-07-03 |

### Workflow / Governance Decisions

| ID | Decision | Status | Source |
|---|---|---|---|
| DEC-YOS-006 | Session doctrine capture mandatory; uncaptured items → backlog | CONFIRMED | Manus KAP 2026-07-03 |
| DEC-BOOT-008 | All Architect → Manus handoffs must be real downloadable Markdown files | ACTIVE | Bootstrap 2026-07-02 |
| DEC-BOOT-007 | ConvoFlow = REFERENCE_ONLY + SANDBOX_TEST; requires CONVOFLOW-AUDIT-1 | REFERENCE | Bootstrap 2026-07-02 |
| HAI-001 | KAP/YOS must support human navigation (dashboards, decision trails, review queues) | ACTIVE | ChatGPT 2026-07-03 |
| HAI-002 | KAP/YOS must support AI exploitation (machine-readable registries, routing indexes) | ACTIVE | ChatGPT 2026-07-03 |
| HAI-003 | Goal is not document accumulation — it is provenance, chronology, maturity, decisions | ACTIVE | ChatGPT 2026-07-03 |

---

## Model-Compliant Registry (DECISION-THREAD-MODEL-GATE — 2026-07-03)

| DT ID | Decision | Type | Domain | Status | Current Validity | Canonical Status | Thought Lines | Claims | Source Fragments | Supersedes | Superseded By | Review Needed | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DT-20260703-YOS1 | YOS contains KAP as module/process | architecture | YOS | active | active | active_control_plane | TL-20260703-CP01 | CLAIM-20260703-YOS1 | SF-005, SF-006 | — | — | No | Validated across multiple sessions and gate reports |
| DT-20260703-YOS2 | Git/Markdown is the durable authority for strategic doctrine | architecture | YOS | active | active | active_control_plane | TL-20260703-CP03 | CLAIM-20260703-YOS2 | SF-005, SF-006, SF-007 | — | — | No | Doctrine YOS-011 |
| DT-20260703-YOS3 | Broad acquisition is blocked until cognitive architecture is validated | gate_policy | KAP | active | active | active_control_plane | TL-20260703-CP02 | CLAIM-20260703-YOS3 | SF-001, SF-002, SF-005 | — | — | No | Architecture Before Absorption doctrine |
| DT-20260703-YOS4 | ZIP is transport only, not primary corpus | source_policy | KAP | active | active | active_control_plane | TL-20260703-CP02 | CLAIM-20260703-YOS6 | SF-005 | — | — | No | Stated in all MPM rules |
| DT-20260703-YOS5 | Obsidian real vault scan is blocked until metadata dry-run gate | source_policy | Obsidian | active | active_with_conditions | candidate_evidence | TL-20260703-CP06 | CLAIM-20260703-YOS7 | SF-001, SF-002 | — | — | Yes | OBSIDIAN-PIPELINE-VALIDATION-GATE pending |
| DT-20260703-YOS6 | Notion canonical merge is blocked until controlled pipeline validation | source_policy | Notion | active | active_with_conditions | candidate_evidence | TL-20260703-CP07 | CLAIM-20260703-YOS6 | SF-005 | — | — | Yes | NOTION-PIPELINE-CONTROLLED-EXECUTION-GATE pending |
| DT-20260703-YOS7 | Current-best synthesis is blocked until SF/Claim/TL/DT models are validated | gate_policy | KAP | active | active | active_control_plane | TL-20260703-CP08 | CLAIM-20260703-YOS3, CLAIM-20260703-YOS5 | SF-005, SF-007 | — | — | No | Validated by 4 model gates |
| DT-20260703-YOS8 | Manus is executor, not architectural authority | agent_role | Agents | active | active | active_control_plane | TL-20260703-CP01 | CLAIM-20260703-YOS1 | SF-005, SF-006 | — | — | No | Doctrine YOS-019 |

---

## Notes

- Prior registry entries (DEC-YOS-*, REPO-*, PIPE-*, DEC-BOOT-*, HAI-*) are preserved verbatim from CAPTURE-PATCH.
- Model-compliant entries (DT-20260703-*) follow the DECISION-THREAD-MODEL schema.
- Migration of prior entries to model-compliant format is pending DECISION-THREAD-MIGRATION-GATE.
- `current_validity: active_with_conditions` means the decision is active but depends on a pending gate.
