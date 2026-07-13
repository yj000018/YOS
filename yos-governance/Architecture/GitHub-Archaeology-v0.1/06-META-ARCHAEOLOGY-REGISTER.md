# Meta-Archaeology Register

**Program:** GitHub Account Archaeology v0.1  
**Branch:** `agent/github-account-archaeology-wave1`  
**Status:** ACTIVE / EVIDENCE RECOVERY  
**Rule:** Archaeologize prior archaeology before creating a replacement.

## Purpose

This register inventories prior attempts to acquire, process, classify, reconcile, preserve, or canonize the Y-OS/KOSMOS corpus.

It prevents duplicate work and identifies which methods, agents, gates, scripts, registries, and conclusions remain reusable.

## Status vocabulary

- `RECOVERED` — artifact found and readable.
- `PARTIAL` — artifact or execution state found, but evidence incomplete.
- `CATALOGUED` — known to exist; content review pending.
- `SUPERSEDED` — replaced by later evidence or policy; retained historically.
- `REUSABLE` — method/invariant remains applicable.
- `REQUIRES_RECONCILIATION` — conflicts with later doctrine or another source.
- `BLOCKED` — inaccessible without user/platform action.

## Register

| ID | Prior effort / artifact | Repository / location | Period | Purpose | Sources processed | Outputs | Current assessment | Reuse / next action |
|---|---|---|---|---|---|---|---|---|
| MA-001 | Manus Historical Discovery Excavation | `YOS/00_META/CHRONICLES/MANUS-HISTORICAL-DISCOVERY/` | 2026-07-05 to 2026-07-06 | Preserve the discovery process behind MPM, KAP, BUS, YARP, AGENTS and related architecture | MPMs, MPRs, constitutions, reports and artifacts from the 2026-07-05 marathon | Discovery genealogy, epistemology, fulgurances, emergence events, hypotheses, KOSMOS↔Y-OS fragments | `RECOVERED` · scope limited to one day | Preserve method and extend to pre-monorepo, `kap-control-plane`, and `yos-cognitive-os` eras |
| MA-002 | KAP Prior Work Archaeology | `KAP`, commit family around `31d18ce...` | 2026-07 | Prevent reinvention and extract earlier reusable operating principles | Earlier KAP/source-management artifacts | Nine principles, invariants, layers, delta-ready engineering foundation | `RECOVERED` · `REUSABLE` · some conclusions require supersession review | Compare each adopted principle with current Git/Obsidian/Notion doctrine |
| MA-003 | KAP WP2 source-acquisition program | `KAP/02_Source_Acquisition/`, WP2-E1 through WP2-M7 | 2026-07-01 onward | Acquire and normalize source families at scale | Manus history, Mem0, Notion, Git, uploads and related surfaces | Corpus areas, scripts, reports, registries, checksums, metadata and partial content extraction | `RECOVERED` · processing depth varies by source | Audit completion state by sprint before running any equivalent acquisition |
| MA-004 | Complete Manus harvest / surface mapping | `KAP/02_Source_Acquisition/WP2-M1*`, `WP2-M2*`, `WP2-M4*`, `WP2-M5*` | 2026-07 | Recover Manus tasks, metadata, outputs, sites and internal context | Manus task/session surfaces and deployed-site evidence | Large raw mirrors, metadata, reports and recovery artifacts | `PARTIAL` · evidence indicates 363 session metadata records and additional task/output captures | Determine exact body-content coverage versus metadata-only coverage |
| MA-005 | Manus Memory / factsheet archive | KAP factsheet commit series and Notion/Mem0 bridges | 2026-07 | Convert historical work into structured factsheets and searchable memory | Manus sessions/tasks, Notion Memory, Mem0 | 194 factsheets in one report; later corpus reports reference 363 Manus session metadata records | `REQUIRES_RECONCILIATION` due to differing counts and units | Establish count semantics: sessions, tasks, factsheets, or records; never treat totals as equivalent |
| MA-006 | Source Access Readiness Audit | `YOS/01_BACKBONE/KAP/04_REGISTRIES/SOURCE-ACCESS-READINESS-MATRIX.md` | 2026-07-03 | Determine safe read access, blockers, and next gates for every source family | Git, ChatGPT, Manus, Obsidian, Notion, Mem0, other LLMs, generated sites/apps | Access matrix, blockers, next-safe-gate sequence | `RECOVERED` · partially stale | Refresh against current 40-repository census and newly available connectors |
| MA-007 | Source Instance / Pipeline / Matrix system | `YOS/01_BACKBONE/KAP/04_REGISTRIES/` | 2026-07-03 onward | Model source channels, instances, objects, fragments and pipeline readiness | All catalogued source families | L0→L3 registries, source matrix, pipeline registry, decision and contradiction registries | `RECOVERED` · central reusable substrate | Update rather than replace; record deltas and stale assumptions |
| MA-008 | Y-WORLD / Obsidian metadata dry run | `Y-WORLD`, `YOS/yos-vault/knowledge/Y-WORLD/`, KAP reports | 2026-07-03 | Discover vault topology without unauthorized content mutation | Git-backed and local Obsidian vaults | File counts, folders, wikilinks, frontmatter, duplicate and path findings | `RECOVERED` · content acquisition incomplete | Reuse scanner methodology; reconcile 17/229/235-note snapshots by source/date |
| MA-009 | Notion metadata and block extraction pilots | `KAP/WP2-M6*` and YOS/KAP registries | 2026-07 | Inventory and partially extract Notion workspaces/databases/pages | Y-OS, Y-World, Yannick, ELYSIUM, KOSMOS roots and Manus Memory surfaces | Root/L2 inventories, database records, block extraction artifacts | `PARTIAL` · multiple reported totals and scopes | Build exact acquisition ledger before any new Notion crawl |
| MA-010 | `yos-cognitive-os` source-of-truth and quarantine studies | `yos-cognitive-os/00_Control_Plane/` and related gates | pre-monorepo / 2026-07 | Compare GitHub, GDrive, iCloud and vault surfaces; isolate canonical candidates | GitHub Y-WORLD, Google Drive, iCloud, capture packs | Surface maps, fingerprints, duplicate comparisons, quarantine decisions | `RECOVERED` · high lineage value | Integrate into Timeline & Supersession and Memory/Knowledge lanes |
| MA-011 | Session-synthesis skill family | `yos-skills`, migrated under `YOS/yos-agents/manus/yos-skills/session-synthesis/`, KAP factsheets | pre-monorepo to monorepo | Collect, summarize, generate session cards and archive to Notion | Individual interactive sessions | Skill contract, scripts, templates, API references, live validation factsheet | `RECOVERED` · destination policy may be superseded | Preserve processing logic; reassess Git/Markdown-first durable output target |
| MA-012 | Continuity Protocol | `yos-continuity-protocol` and migrated YOS artifacts | pre-monorepo | Carry canonical context safely across LLM sessions and platforms | Session state, canonical core, platform wrappers | Continuity pack schema, wrappers and examples | `RECOVERED` · likely reusable | Compare with current Context Pack and Chronicle requirements |
| MA-013 | Monorepo canonical reorganization | `YOS`, merge commit `20dc47f...` | 2026-07-05 | Establish canonical backbone and migrate fragmented repos/artifacts | KAP, MPM, agents, governance, memory and source registries | `01_BACKBONE`, canonical structure, migrations and policy statements | `RECOVERED` · later baseline exists | Map migrated, unmigrated and duplicated artifacts before further consolidation |
| MA-014 | Architecture Baseline v0.5 | `YOS/yos-governance/Architecture/Baseline-v0.5/`, branch `agent/yos-baseline-v0.5` | 2026-07 | Consolidate ChatGPT architectural understanding into a reviewable baseline | Git evidence and ChatGPT architectural synthesis | 15 baseline files | `PARTIAL` · review pending; not canon | Reconcile with archaeology findings; do not merge yet |
| MA-015 | GitHub Account Archaeology Wave 1 | `YOS` issues #3–#15 and branch `agent/github-account-archaeology-wave1` | 2026-07-13 onward | Recover account-wide technical, conceptual and historical strata | All 40 owned repositories plus prior archaeology artifacts | Census, lane issues, README, Chronicle and registers | `ACTIVE` | Continue evidence-first; no disposition actions yet |

## Known reconciliation problems

### Counts are not yet semantically aligned

Existing artifacts cite at least:

- 194 Manus historical sessions or factsheets;
- 363 Manus Memory Session metadata records;
- 316 Mem0 memories;
- 593 entries across seven Notion databases;
- 41 repositories in an earlier registry versus 40 currently owned repositories.

These values must not be merged into one total. Each requires a definition, source, date, deduplication method, and coverage statement.

### Source-authority doctrine evolved

Historical artifacts variously position:

- Notion as primary structured memory;
- JSON as primary runtime record and Markdown as audit;
- Git/KAP as source of truth;
- Markdown/Obsidian as durable human-readable center;
- Mem0 as active memory, semantic index, or signal-only layer.

This is a supersession lineage, not an error to erase. The current program must date each position and recover the reason for transition.

### Acquisition and processing are different states

A source can be:

- discovered;
- catalogued;
- metadata-acquired;
- body-acquired;
- normalized;
- fragment-extracted;
- factsheet-processed;
- compared;
- synthesized;
- canonized.

No artifact should be called “complete” without stating which state is complete.

## Immediate next passes

1. Audit MA-003 through MA-009 at file level and identify exact completion boundaries.
2. Build a Manus capability and historical-work matrix from recovered skills, agents, gates and WP2 reports.
3. Build a source-count reconciliation table with definitions and evidence.
4. Map prior pipeline stages to the current two-week ChatGPT preparation phase and future Manus continuation.
5. Register every new prior-archaeology artifact before designing any missing method.
