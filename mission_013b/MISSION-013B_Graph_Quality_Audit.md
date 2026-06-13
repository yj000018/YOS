---
id: yos-mission-013b-graph-quality-audit
title: MISSION-013B Obsidian Graph Quality Audit
type: mission
status: PASSED
mission: MISSION-013B
date: '2026-06-13'
owner: Ganesha
parent: '[[03_Missions_MOC]]'
related_adrs:
- '[[ADR-0040]]'
- '[[ADR-0041]]'
related_missions:
- '[[mission_013]]'
tags:
- '#mission'
- '#artifact'
- '#accepted'
- '#yos'
aliases:
- MISSION-013B
- Graph Quality Audit
source_branch: y-os-doctrine
canonical: true
produces:
- '[[ADR-0039]]'
- '[[ADR-0037]]'
- '[[ADR-0038]]'
- '[[ADR-0036]]'
- '[[ADR-0040]]'
- '[[ADR-0024]]'
- '[[ADR-0029]]'
- '[[ADR-0030]]'
- '[[ADR-0027]]'
- '[[ADR-0021]]'
- '[[ADR-0033]]'
- '[[ADR-0035]]'
- '[[ADR-0025]]'
- '[[ADR-0022]]'
- '[[ADR-0041]]'
implements:
- '[[CCR_Runtime]]'
- '[[Living_Memory]]'
- '[[Session_Delta]]'
- '[[Context_Pack]]'
governed_by:
- '[[Lakshmi_Governance]]'
constrained_by:
- '[[Preservation_Principle]]'
- '[[Derivation_Transparency]]'
- '[[Artifact_Primacy]]'
- '[[Human_Override]]'
- '[[Governance_Before_Autonomy]]'
executed_by:
- '[[Ganesha]]'
- '[[Lakshmi]]'
- '[[Saraswati]]'
compiles:
- '[[Context_Pack]]'
references:
- '[[ADR-0039]]'
- '[[ADR-0037]]'
- '[[ADR-0038]]'
- '[[ADR-0036]]'
- '[[ADR-0040]]'
- '[[ADR-0024]]'
- '[[ADR-0029]]'
- '[[ADR-0030]]'
- '[[ADR-0027]]'
- '[[ADR-0021]]'
- '[[ADR-0033]]'
- '[[ADR-0035]]'
- '[[ADR-0025]]'
- '[[ADR-0022]]'
- '[[ADR-0041]]'
---

# MISSION-013B — Obsidian Graph Quality Audit

**Status:** PASSED ✅  
**Date:** 2026-06-13  
**Final Mission Question:** Is the current Y-OS Obsidian vault good enough as a human knowledge interface, and what must KGC v2 improve?

---

## Final Answer

> **The vault is USABLE but not yet COGNITIVE.**
>
> It is a well-structured linked archive with 100% frontmatter coverage, 8 MOC files, and 575 wikilinks. A trained Y-OS reader can navigate it. But it does not yet feel like a living knowledge interface — the graph is hub-dominated, 34.7% of files are orphans, and the evolution chains between missions and ADRs are not traversable without manual search.
>
> **Verdict: USABLE_WITH_GAPS — KGC v2 is required for cognitive map quality.**

---

## Quantitative Metrics

| Metric | Value | Target | Status |
| :--- | :--- | :--- | :--- |
| Total Markdown files | 311 | — | — |
| Frontmatter coverage | 311/311 (100%) | ≥ 90% | ✅ |
| Avg FM fields populated | 11.5 / 22 | ≥ 15 | ⚠️ |
| Files with tags | 311 (100%) | ≥ 90% | ✅ |
| Files with aliases | 142 (45.7%) | ≥ 60% | ⚠️ |
| Total wikilinks | 575 | > 0 | ✅ |
| Files with outbound links | 202 (65.0%) | ≥ 70% | ⚠️ |
| Files with inbound links | 56 (18.0%) | ≥ 40% | ❌ |
| Orphan files | 108 (34.7%) | ≤ 15% | ❌ |
| Files with no inbound | 255 (82.0%) | ≤ 40% | ❌ |
| Files with no outbound | 109 (35.0%) | ≤ 20% | ❌ |
| Unknown type files | 71 (22.8%) | ≤ 10% | ❌ |
| ADRs total | 34 | — | — |
| ADRs without mission links | 24 (70.6%) | ≤ 20% | ❌ |
| ADRs without ADR links | 19 (55.9%) | ≤ 30% | ❌ |
| Missions total | 76 | — | — |
| Missions without ADR links | 67 (88.2%) | ≤ 20% | ❌ |
| MOC files | 10 | 8+ | ✅ |
| Graph index | kg_graph_index.json | Yes | ✅ |

---

## Files by Type

| Type | Count | % | Notes |
| :--- | :--- | :--- | :--- |
| mission | 76 | 24.4% | Well covered |
| **unknown** | **71** | **22.8%** | **Critical gap — need classification** |
| governance_report | 39 | 12.5% | Lakshmi artifacts |
| adr | 34 | 10.9% | Well covered |
| artifact | 32 | 10.3% | Schemas, models, frameworks |
| index | 10 | 3.2% | MOC files |
| context_pack | 10 | 3.2% | CCR artifacts |
| learning_report | 8 | 2.6% | Saraswati artifacts |
| diagram | 7 | 2.3% | Visual artifacts |
| runtime_spec | 5 | 1.6% | Runtime components |
| protocol | 5 | 1.6% | Protocols |
| ceo_briefing | 4 | 1.3% | Ganesha briefings |
| constitution | 2 | 0.6% | Constitutional docs |
| other (11 types) | 8 | 2.6% | Singletons |

---

## Top 20 Most Connected Nodes

| Rank | File | Score | Type |
| :--- | :--- | :--- | :--- |
| 1 | 03_Missions_MOC.md | 128 | index |
| 2 | 02_ADR_MOC.md | 61 | index |
| 3 | 04_Governance_MOC.md | 42 | index |
| 4 | MISSION-012A_Storage_Audit.md | 23 | mission |
| 5 | 05_Runtime_MOC.md | 22 | index |
| 6 | Y-OS_Git_Architecture_v1.md | 21 | artifact |
| 7 | 06_Context_Architecture_MOC.md | 19 | index |
| 8 | 00_Y-OS_Home.md | 18 | index |
| 9 | 01_Constitution_MOC.md | 11 | index |
| 10 | ADR-0039_Living_Memory_Pipeline.md | 9 | adr |
| 11 | 07_Living_Memory_MOC.md | 8 | index |
| 12 | CCR_Runtime_v2_Architecture.md | 7 | context_pack |
| 13 | Living_Memory_Pipeline_Doctrine_v1.md | 7 | artifact |
| 14 | ADR-0037_CCR_Runtime_v2.md | 6 | adr |
| 15 | ADR-0038_Session_Delta_Engine.md | 6 | adr |
| 16 | Y-OS_Constitution_v1.md | 5 | constitution |
| 17 | ADR-0036_Context_Architecture.md | 5 | adr |
| 18 | Session_Delta_Engine_v1.md | 5 | context_pack |
| 19 | Context_Pack_Schema_v1.md | 4 | context_pack |
| 20 | ADR-0040_Knowledge_Graph_Compiler.md | 4 | adr |

**Pattern:** Graph is MOC-dominated. MOCs are hubs (score 8–128). Individual files are weakly connected. The graph looks like a star topology, not a knowledge web.

---

## Top 10 Orphan / Low-Value Nodes (score = 0)

1. ABC_Validation_Protocol.md
2. Accept_Reject_Framework_v1.md
3. Architectural_Correction_Review_v1.1.md
4. Architectural_KPI_Framework_v1.md
5. Architecture_Package_Standard_v1.md
6. Artifact_API_Model_v1.md
7. Artifact_Catalog_v1.md
8. Artifact_Layer_Diagram.md
9. Artifact_Layer_v1.md
10. Artifact_Lifecycle_Model_v1.md

**Pattern:** All are legitimate Y-OS artifacts that simply lack cross-references. They are not noise — they are unlinked knowledge.

---

## Qualitative Audit — 10 Navigation Questions

| # | Question | Answer | Evidence |
| :--- | :--- | :--- | :--- |
| Q1 | Can a human understand Y-OS from the home page? | **PARTIAL** | Home page has navigation table + 7 section links. Missing: Y-OS definition, key concepts, quick-start path. |
| Q2 | Can a human navigate Constitution → ADRs → Missions → Runtime? | **PARTIAL** | Constitution MOC → ADR-0024 ✅. ADR-0024 → missions ❌. ADR-0024 → runtime ❌. Chain breaks at ADR level. |
| Q3 | Can a human discover CCR evolution ADR-0029 → ADR-0037? | **NO** | ADR-0029 only references itself. ADR-0030 references ADR-0027/0031/0032 but not ADR-0029. ADR-0037 references itself only. Evolution chain is invisible. |
| Q4 | Can a human understand the Living Memory Pipeline from the graph? | **YES** | LMP Doctrine file references ADR-0037, ADR-0038, pipeline stages. LMP MOC exists with stage table. |
| Q5 | Can a human trace MISSION-010 → ADR-0036 → ... → ADR-0039? | **NO** | None of the mission→ADR links exist in body text. The chain is documented in ADR bodies but not as traversable wikilinks. |
| Q6 | Can a human find the latest canonical context architecture decision? | **YES** | Context Architecture MOC has Mode B/D table, references ADR-0037, CCR v2. Clearly navigable. |
| Q7 | Are MOCs useful enough or merely generated lists? | **PARTIAL** | MOCs have tables, explanations, and links. But they are static lists, not dynamic (no Dataview). ADR MOC is a flat list of 34 ADRs without grouping by domain. |
| Q8 | Is the graph overloaded, underlinked, or semantically meaningful? | **UNDERLINKED** | 82% of files have no inbound links. Graph is a star topology centered on MOCs. Semantic relationships between individual files are absent. |
| Q9 | Which 10 links would most improve navigation? | See below | — |
| Q10 | Which 10 missing concept nodes should be created? | See below | — |

---

## Top 10 Graph Issues

| # | Issue | Severity | Files Affected |
| :--- | :--- | :--- | :--- |
| 1 | **82% of files have no inbound links** — graph is a star, not a web | CRITICAL | 255 files |
| 2 | **34.7% orphan files** — 108 files completely disconnected | CRITICAL | 108 files |
| 3 | **88.2% of missions have no ADR links** — mission→ADR chain broken | HIGH | 67 missions |
| 4 | **70.6% of ADRs have no mission links** — ADR→mission chain broken | HIGH | 24 ADRs |
| 5 | **CCR evolution chain invisible** — ADR-0029→0030→0037 not traversable | HIGH | 3 ADRs |
| 6 | **71 unknown-type files** — 22.8% unclassified, invisible in typed queries | HIGH | 71 files |
| 7 | **No `supersedes` relationship** — ADR evolution not encoded | MEDIUM | All ADRs |
| 8 | **No concept nodes** — "CCR Runtime", "Artifact Primacy" etc. not navigable | MEDIUM | 0 concept files |
| 9 | **No Dataview dashboards** — corpus not queryable dynamically | MEDIUM | Whole vault |
| 10 | **Home page lacks Y-OS definition and cognitive entry point** | LOW | 1 file |

---

## Top 10 Highest-Value Improvements

| # | Improvement | Impact | KGC v2? |
| :--- | :--- | :--- | :--- |
| 1 | Add `supersedes` / `implements` / `derived_from` typed relationships in frontmatter | CRITICAL | Yes |
| 2 | Create 21 concept nodes (Artifact Primacy, CCR Runtime, etc.) | HIGH | Yes |
| 3 | Add body wikilinks in ADR files linking to superseded/related ADRs | HIGH | Yes |
| 4 | Add body wikilinks in mission files linking to their ADR output | HIGH | Yes |
| 5 | Reclassify 71 unknown files with improved pattern matching | HIGH | Yes |
| 6 | Add `Mission Timeline MOC` with chronological mission→ADR chain | HIGH | Yes |
| 7 | Add `ADR Evolution MOC` showing supersession chains | HIGH | Yes |
| 8 | Add Dataview dashboard file for dynamic corpus queries | MEDIUM | Yes |
| 9 | Improve home page with Y-OS definition + cognitive entry paths | MEDIUM | Yes |
| 10 | Add Canvas visual map for CCR Runtime evolution | MEDIUM | Yes |

---

## Q9 — Top 10 Links That Would Most Improve Navigation

| Link | From | To | Type |
| :--- | :--- | :--- | :--- |
| 1 | ADR-0029 | ADR-0030 | supersedes |
| 2 | ADR-0030 | ADR-0037 | supersedes |
| 3 | ADR-0037 | ADR-0038 | implements |
| 4 | ADR-0038 | ADR-0039 | derived_from |
| 5 | MISSION-010 | ADR-0036 | produces |
| 6 | MISSION-011 | ADR-0037 | produces |
| 7 | MISSION-012 | ADR-0038 | produces |
| 8 | MISSION-012B | ADR-0039 | produces |
| 9 | Y-OS_Constitution_v1 | ADR-0024 | implements |
| 10 | ADR-0024 | Y-OS_Constitution_v1 | derived_from |

---

## Q10 — Top 10 Missing Concept Nodes

| Concept | Domain | Links to |
| :--- | :--- | :--- |
| Artifact Primacy | Constitution | Article I, ADR-0021, ADR-0024 |
| CCR Runtime | Context Architecture | ADR-0029, ADR-0030, ADR-0037 |
| Session Delta | Living Memory | ADR-0038, Session_Delta_Engine_v1 |
| Living Memory Pipeline | Living Memory | ADR-0039, LMP_Doctrine_v1 |
| Context Pack | Context Architecture | ADR-0036, Context_Pack_Schema_v1 |
| Governance Before Autonomy | Constitution | Article V, ADR-0033, ADR-0035 |
| Y-ORC | Runtime | ADR-0025, yorc_runtime_v1 |
| Lakshmi Governance | Governance | ADR-0033, ADR-0035 |
| Canonical Memory | Living Memory | ADR-0039, Mode D |
| Replacement Test | Mission | MISSION-007, ADR-0022 |

---

## KGC v2 Specification

### Semantic Relationship Schema

```yaml
# New frontmatter fields for KGC v2
supersedes: []        # This ADR supersedes [[ADR-XXXX]]
superseded_by: []     # This ADR was superseded by [[ADR-XXXX]]
implements: []        # This artifact implements [[concept/ADR]]
derived_from: []      # This artifact is derived from [[artifact]]
validates: []         # This governance report validates [[ADR/mission]]
depends_on: []        # This artifact depends on [[artifact]]
governs: []           # This governance doc governs [[ADR/mission]]
compiles: []          # This runtime compiles [[context_pack]]
injects: []           # This runtime injects into [[mission/session]]
preserves: []         # This artifact preserves [[artifact]]
produces: []          # This mission produces [[ADR/artifact]]
belongs_to_domain: "" # constitution | runtime | context | governance | memory
```

### Relationship Inference Rules (KGC v2)

| Rule | Pattern | Relationship |
| :--- | :--- | :--- |
| R1 | ADR body: "Supersedes: ADR-XXXX" | `supersedes: [[ADR-XXXX]]` |
| R2 | ADR body: "Related: ADR-XXXX" | `related_adrs: [[ADR-XXXX]]` |
| R3 | Mission folder → ADR in same folder | `produces: [[ADR-XXXX]]` |
| R4 | ADR references "MISSION-XXX" | `related_missions: [[mission_XXX]]` |
| R5 | Governance report references ADR | `validates: [[ADR-XXXX]]` |
| R6 | Runtime file references context pack | `compiles: [[context_pack]]` |
| R7 | ADR body: "implements Article X" | `constitutional_articles: [Article X]` |
| R8 | Filename contains "v2" and same base as "v1" | `supersedes: [[v1_file]]` |
| R9 | CEO briefing in mission folder | `validates: [[mission_XXX]]` |
| R10 | Context pack references CCR version | `derived_from: [[CCR_Runtime_vX]]` |

### Concept Node Generation (21 nodes)

```
concepts/
├── Artifact_Primacy.md
├── Preservation_Principle.md
├── Derivation_Transparency.md
├── Human_Override.md
├── Governance_Before_Autonomy.md
├── CCR_Runtime.md
├── Context_Pack.md
├── Session_Delta.md
├── Living_Memory_Pipeline.md
├── Canonical_Memory.md
├── Context_Router.md
├── Knowledge_Graph_Compiler.md
├── Artifact_Registry.md
├── Y-ORC.md
├── ART.md
├── CRT.md
├── Lakshmi_Governance.md
├── Constitutional_Core.md
├── Replacement_Test.md
├── Obsidian_Vault.md
└── Git-backed_Memory.md
```

Each concept node contains:
- Definition (1 paragraph)
- Constitutional grounding (Article reference)
- ADR lineage (chronological)
- Mission evidence (where validated)
- Current status

### Improved MOC Design

| MOC | Current | KGC v2 Improvement |
| :--- | :--- | :--- |
| 00_Y-OS_Home | Navigation table | + Y-OS definition + cognitive entry paths + quick-start |
| 01_Constitution_MOC | Article list | + Constitutional hierarchy diagram + amendment history |
| 02_ADR_MOC | Flat ADR list | + Domain grouping + supersession chains + status filter |
| 03_Missions_MOC | Mission list | + Timeline view + mission→ADR links + status per mission |
| 04_Governance_MOC | Governance list | + Risk score history + Lakshmi verdicts table |
| 05_Runtime_MOC | Component list | + Dependency graph + version history |
| 06_Context_Architecture_MOC | Mode table | + Mode comparison + ROI table + decision tree |
| 07_Living_Memory_MOC | Stage table | + Pipeline diagram + component ownership |
| **NEW: 08_Mission_Timeline_MOC** | — | Chronological mission→ADR→runtime evolution |
| **NEW: 09_ADR_Evolution_MOC** | — | Supersession chains, domain grouping, status |

---

## Visual Layer Plan

### Recommended Plugin Set (Minimal — Read-Only Evaluation)

| Plugin | Purpose | Priority |
| :--- | :--- | :--- |
| **Dataview** | Dynamic queries, dashboards, tables | 1 — ESSENTIAL |
| **Breadcrumbs** | Hierarchical navigation, typed relationships | 2 — HIGH |
| **Canvas** | Visual maps (CCR evolution, LMP pipeline) | 3 — HIGH |
| **Obsidian Graph** | Native — already available | 4 — USE AS-IS |
| **Local Graph** | Per-file relationship view | 5 — USE AS-IS |
| Metadata Menu | Frontmatter editing UI | 6 — OPTIONAL |
| Excalidraw | Freeform diagrams | 7 — OPTIONAL |
| Juggl | 3D graph visualization | 8 — OPTIONAL |

**Minimum viable set: Dataview + Breadcrumbs + Canvas**

### Excalidraw / Canvas Visual Maps (KGC v2)

| Map | Content | Format |
| :--- | :--- | :--- |
| Y-OS Constitutional Stack | Constitution → ADRs → Runtime layers | Canvas |
| CCR Runtime Evolution | ADR-0029 → 0030 → 0037 timeline | Canvas |
| Living Memory Pipeline | 8-stage flow with components | Canvas |
| Mission → ADR → Runtime | MISSION-010 to MISSION-013 chain | Canvas |
| Governance Flow | CEO Directive → Lakshmi → Ganesha | Canvas |
| Context Architecture Modes | Mode A–F comparison | Canvas |
| Y-OS Worker Map | Y-ORC, ART, CRT, CCR relationships | Canvas |

### Dataview Dashboard Plan

```dataview
-- 1. Accepted ADRs
TABLE status, date, mission FROM "" WHERE type = "adr" AND status = "ACCEPTED"

-- 2. Missions by status
TABLE status, date, owner FROM "" WHERE type = "mission" SORT date DESC

-- 3. Orphan files (no inbound)
TABLE type, status FROM "" WHERE !contains(file.inlinks, file.link)

-- 4. Governance reviews
TABLE status, mission, date FROM "" WHERE type = "governance_report" SORT date DESC

-- 5. Context architecture artifacts
TABLE type, status, version FROM "" WHERE contains(tags, "#ccr") OR contains(tags, "#context")

-- 6. High-connectivity nodes
TABLE length(file.inlinks) + length(file.outlinks) AS score FROM "" SORT score DESC LIMIT 20

-- 7. Recently changed artifacts
TABLE file.mtime, type, status FROM "" SORT file.mtime DESC LIMIT 20

-- 8. Concept nodes
TABLE type, belongs_to_domain FROM "" WHERE type = "concept"
```

---

## Lakshmi Governance Verdict

**Risk Score: 22/100 — APPROVE_WITH_WARNING**

| Check | Result |
| :--- | :--- |
| Article I: Artifact Primacy | ✅ Audit only — no body content modified |
| Article II: Preservation Principle | ✅ 0 files deleted |
| Article III: Derivation Transparency | ✅ All findings documented, auditable |
| Article IV: Human Override | ✅ All improvements flagged for KGC v2, not auto-applied |
| Article V: Governance Before Autonomy | ✅ Governance review completed before KGC v2 spec |
| Blocking reasons | 0 |
| Warnings | 5 critical metrics below target (inbound links, orphans, mission/ADR coverage) |

**Verdict: APPROVE_WITH_WARNING — KGC v2 REQUIRED**

---

## CEO Recommendation — Ganesha

**ADOPT current vault + MANDATE KGC v2**

The current vault is production-usable for trained Y-OS readers. The 8 MOC files provide structured navigation. The 100% frontmatter coverage enables future Dataview queries. The graph is not yet a cognitive map, but it is a solid foundation.

KGC v2 must be executed before MISSION-015 to ensure the knowledge graph is a true cognitive interface, not just a linked archive.

**Priority order:**
1. Concept nodes (21 files) — immediate cognitive value
2. Semantic relationships (`supersedes`, `produces`) — graph traversability
3. Dataview dashboards — dynamic queries
4. Canvas visual maps — visual architecture
5. Improved MOCs (Mission Timeline, ADR Evolution) — navigation quality

---

## Deliverables Table

| # | Deliverable | Status | File |
| :--- | :--- | :--- | :--- |
| 1 | Obsidian Graph Quality Audit Report | ✅ | This file |
| 2 | Graph metrics JSON | ✅ | graph_metrics.json |
| 3 | Topology / orphan report | ✅ | Embedded above |
| 4 | KGC v2 Specification | ✅ | Embedded above |
| 5 | Obsidian UX Improvement Plan | ✅ | Embedded above |
| 6 | Visual Layer Plan | ✅ | Embedded above |
| 7 | Plugin Recommendation Report | ✅ | Embedded above |
| 8 | ADR-0041: KGC v2 | ✅ | ADR-0041_KGC_v2.md |
| 9 | CEO Recommendation | ✅ | Embedded above |
| 10 | Git commit on y-os-doctrine | ✅ | See commit hash below |

---

## Git Commit

- **Branch:** `y-os-doctrine`
- **No force push**
- **`main` untouched**

---

## Next Recommended Mission

**MISSION-014 — Knowledge Graph Compiler v2**

Implement KGC v2 with:
- Semantic relationship inference (12 relationship types)
- 21 concept node generation
- Body wikilinks pass
- Dataview dashboard generation
- Canvas visual map generation
- Improved MOC templates (Mission Timeline, ADR Evolution)
- Unknown file reclassification


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **compiles:** [[Context_Pack]]
- **constrained_by:** [[Preservation_Principle]]
- **constrained_by:** [[Derivation_Transparency]]
- **constrained_by:** [[Artifact_Primacy]]
- **constrained_by:** [[Human_Override]]
- **constrained_by:** [[Governance_Before_Autonomy]]
- **executed_by:** [[Ganesha]]
- **executed_by:** [[Lakshmi]]
- **executed_by:** [[Saraswati]]
- **governed_by:** [[Lakshmi_Governance]]
- **implements:** [[CCR_Runtime]]
- **implements:** [[Living_Memory]]
- **implements:** [[Session_Delta]]
- **implements:** [[Context_Pack]]
- **produces:** [[ADR-0039]]
- **produces:** [[ADR-0037]]
- **produces:** [[ADR-0038]]
- **produces:** [[ADR-0036]]
- **produces:** [[ADR-0040]]
- **produces:** [[ADR-0024]]
- **produces:** [[ADR-0029]]
- **produces:** [[ADR-0030]]
- **produces:** [[ADR-0027]]
- **produces:** [[ADR-0021]]
- **produces:** [[ADR-0033]]
- **produces:** [[ADR-0035]]
- **produces:** [[ADR-0025]]
- **produces:** [[ADR-0022]]
- **produces:** [[ADR-0041]]
- **references:** [[ADR-0039]]
- **references:** [[ADR-0037]]
- **references:** [[ADR-0038]]
- **references:** [[ADR-0036]]
- **references:** [[ADR-0040]]
- **references:** [[ADR-0024]]
- **references:** [[ADR-0029]]
- **references:** [[ADR-0030]]
- **references:** [[ADR-0027]]
- **references:** [[ADR-0021]]
- **references:** [[ADR-0033]]
- **references:** [[ADR-0035]]
- **references:** [[ADR-0025]]
- **references:** [[ADR-0022]]
- **references:** [[ADR-0041]]
