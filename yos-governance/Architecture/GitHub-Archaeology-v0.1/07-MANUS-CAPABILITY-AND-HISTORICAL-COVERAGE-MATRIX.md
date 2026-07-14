# Manus Capability and Historical Coverage Matrix

**Program:** GitHub Account Archaeology v0.1  
**Branch:** `agent/github-account-archaeology-wave1`  
**Status:** EVIDENCE-BASED CONSOLIDATION  
**Purpose:** Define what Manus was asked to do, what it demonstrably completed, what remains uncertain, and what must not be redundantly rebuilt during the two-week ChatGPT-only preparation phase.

## Governing rule

Do not ask Manus to rediscover material already durably acquired, indexed, processed, or documented in Git.

Do not assume that a reported count proves full-body acquisition, complete synthesis, or canonization.

## Evidence classes

| Class | Meaning |
|---|---|
| `PROVEN_EXECUTED` | A durable artifact, script, gate report, commit, or output demonstrates execution. |
| `PROVEN_IMPLEMENTED` | Code, skill, contract, or pipeline exists, but complete historical execution is not proven. |
| `PARTIAL_EXECUTION` | Execution occurred on a bounded sample, subset, date range, or source surface. |
| `METADATA_ONLY` | Structure or records were acquired without proof of complete source bodies. |
| `CLAIM_REQUIRES_RECONCILIATION` | Multiple artifacts use different counts, scopes, or units. |
| `NOT_PROVEN` | No durable evidence yet demonstrates completion. |

## Capability matrix

| Capability | Durable evidence | Demonstrated state | Limits / uncertainty | Current action |
|---|---|---|---|---|
| Git/GitHub discovery and acquisition | KAP source registries, readiness matrix, WP2 corpus, GitHub census work | `PROVEN_EXECUTED` on several repositories and `PROVEN_IMPLEMENTED` account-wide | Older census used 41 registry entries; current owned-repository census is 40 | Reuse methodology; refresh deltas rather than rebuild |
| Manus task/session surface harvesting | `WP2-M1_Complete_Manus_Harvest`, `WP2-M2*`, `WP2-M4*`, corpus audit commit | `PROVEN_EXECUTED` at large scale | Exact relation between tasks, sessions, memory records, outputs, and factsheets remains unresolved | Build one semantic ledger of units and coverage |
| Manus Memory metadata acquisition | Corpus audit reports 363 Manus Memory Session metadata records | `METADATA_ONLY` proven for 363 records | Full body for all 363 is not proven | Never describe all 363 as fully processed until file-level verification |
| Historical factsheet production | Pipeline report references 194 archived factsheets; KAP contains a factsheet commit series | `PROVEN_EXECUTED` | The 194 count is not proven equivalent to sessions or tasks | Treat factsheets as processed derivatives with source links, not source-body substitutes |
| Notion acquisition and extraction | `WP2-M6`, `WP2-M6B`, `WP2-M6C`; seven databases / 593 entries reported | `PARTIAL_EXECUTION` to substantial execution | Scope varies between database records, pages, blocks, roots, and workspaces | Produce an acquisition ledger before any new Notion crawl |
| Mem0 acquisition | 316 memories reported and registered | `PROVEN_EXECUTED` | Mem0 is signal/index memory, not primary corpus evidence | Use for routing and discovery only; trace claims to durable artifacts |
| Obsidian discovery and metadata scan | Y-WORLD Git-backed scans; local vault discovery through desktop bridge | `PROVEN_EXECUTED` for topology/metadata; content coverage partial | Snapshots cite 17, 229, and 235 notes across distinct sources/dates; Ludivine is a separate 1842-note creative vault | Reconcile snapshots and authorization boundaries before content work |
| Session collection | `collect_session.py` and session-synthesis skill contract | `PROVEN_IMPLEMENTED`; live validation evidence exists | Does not prove every historic platform session was collected | Reuse collector design; target only missing sessions |
| Session-card generation | `generate_card.py`, templates, factsheet commit series | `PROVEN_IMPLEMENTED` and repeatedly executed | Quality and source fidelity may vary by generation epoch | Audit representative samples; do not regenerate wholesale |
| Archival to Notion | `archive_to_notion.py`; `memoriser`; `session-synthesis` | `PROVEN_IMPLEMENTED` and historically executed | Destination doctrine evolved toward Git/Markdown durable authority | Preserve transformation logic; change durable destination only through explicit supersession |
| Context hydration | `hydrater` skill and Notion Memory usage | `PROVEN_IMPLEMENTED` | Current authoritative source hierarchy differs from earlier Notion-first design | Map hydration to Git/Markdown/Context Packs without deleting legacy behavior |
| Persistent memory management | `memory-manager`, Mem0 and Notion bridge artifacts | `PROVEN_IMPLEMENTED`; partial operational evidence | Several memory layers were assigned overlapping roles over time | Consolidate responsibilities before implementation changes |
| Strategic/tactical synthesis | `summary`, `status`, factsheets, MPRs | `PROVEN_IMPLEMENTED` and executed | Summaries can lose emergence history and must not replace originals | Reuse formats while retaining provenance and Chronicle links |
| Development execution | `dev` skill / Claude code engine references; extensive generated repositories | `PROVEN_IMPLEMENTED` and clearly used | Not equivalent to architecture authority or canon approval | Reserve for bounded implementation after architecture acceptance criteria exist |
| Gate-based orchestration | MPM/MPR/gate corpus, source readiness gates, historical excavation gate | `PROVEN_EXECUTED` | Many gates are historical and may be stale or superseded | Reuse the gate discipline, not every historical sequence unchanged |
| Historical discovery archaeology | `MANUS-HISTORICAL-DISCOVERY` corpus; 15 files, 11 discoveries, 15 fulgurances, 6 events, 8 hypotheses | `PROVEN_EXECUTED` | Scope explicitly limited to the 2026-07-05 marathon and its immediate artifacts | Extend lineage to pre-monorepo eras; do not repeat the July 5 excavation |
| Deployed-site and URL recovery | `WP2-M5_Manus_Website_URL_Recovery_Content_Capture` | `PARTIAL_EXECUTION` | Unknown completeness; some deployed URLs may remain outside Git | Defer platform-specific recovery until Manus access returns |
| Local filesystem / desktop-bridge discovery | Obsidian local vault discovery reports | `PROVEN_EXECUTED` on a bounded machine/session | Requires platform access and may not be reproducible from ChatGPT | Manus-only continuation task; prepare exact target list now |

## What Manus demonstrably did

1. Built and executed a substantial KAP source-acquisition program across Git, Manus Memory, Notion, Mem0, Obsidian metadata, uploads, and related surfaces.
2. Produced durable registries, gates, reports, scripts, checksums, factsheets, session-processing skills, and partial/full source captures.
3. Acquired metadata for a large Manus historical corpus and generated a substantial factsheet archive.
4. Executed a sophisticated historical-discovery excavation for the 2026-07-05 architecture marathon.
5. Implemented reusable collection, card-generation, archival, hydration, memory-management, synthesis, status, and development skills.
6. Used local/desktop and platform access that ChatGPT cannot reproduce directly in this session.

## What is not yet proven

1. That all 363 Manus Memory records contain complete original session bodies in Git.
2. That the 194 archived factsheets map one-to-one to 194 sessions.
3. That every Manus task, output, attachment, website, and deployed artifact was captured.
4. That every Notion page/block across all relevant workspaces was fully acquired and normalized.
5. That all ChatGPT architect streams or other LLM sessions were exported.
6. That historical outputs were reconciled against the current Canon or Baseline v0.5.
7. That all earlier agents, skills, scripts, and gates remain current rather than superseded.

## No-redundancy boundary for ChatGPT

During the Manus-free preparation period, ChatGPT may:

- read and compare durable Git artifacts;
- reconstruct timelines, terminology, dependencies, contradictions, and supersession;
- classify acquisition depth and missing evidence;
- produce repo dossiers and cross-repository synthesis;
- define precise acceptance criteria and continuation packets;
- identify exact files, SHAs, gates, scripts, or source records Manus must inspect later.

ChatGPT must not pretend to:

- access unexported Manus-internal session history;
- reproduce local desktop-bridge discovery;
- re-run large Notion/Obsidian/platform crawls without explicit source access;
- declare acquisition complete from counts alone;
- regenerate all factsheets or replace the previous KAP pipeline without evidence of failure.

## Manus continuation boundary

When Manus access returns, its first work should be a bounded **Historical Handoff and Gap Closure**, not a new archaeology design.

Required input packet:

1. exact source and session registry;
2. file paths, branches, commits and SHAs;
3. prior agent/skill/script/gate inventory;
4. acquisition-state ledger per source;
5. unresolved count semantics;
6. missing-body and missing-platform list;
7. supersession map;
8. explicit acceptance criteria;
9. required MPR and persistence destination.

## Consolidated conclusion

Manus has already done a large amount of collection and processing. The central unfinished problem is not “collect everything again.” It is to determine precisely what each prior output represents, reconnect the outputs into one lineage-aware architecture, and isolate the genuinely missing source bodies or platform-only artifacts.
