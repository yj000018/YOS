---
id: yos-adr-0041-kgc-v2
title: ADR-0041 Knowledge Graph Compiler v2
type: adr
status: PROPOSED
mission: MISSION-013B
date: '2026-06-13'
owner: Brahma
parent: '[[02_ADR_MOC]]'
supersedes:
- '[[ADR-0040]]'
- '[[ADR-0041_KGC_v1]]'
related_adrs:
- '[[ADR-0040]]'
- '[[ADR-0039]]'
- '[[ADR-0038]]'
- '[[ADR-0037]]'
related_missions:
- '[[mission_013]]'
- '[[mission_013b]]'
constitutional_articles:
- 'Article I: Artifact Primacy'
- 'Article II: Preservation Principle'
- 'Article III: Derivation Transparency'
tags:
- '#adr'
- '#artifact'
- '#proposed'
- '#yos'
aliases:
- KGC v2
- Knowledge Graph Compiler v2
source_branch: y-os-doctrine
canonical: true
implements:
- '[[CCR_Runtime]]'
- '[[Context_Pack]]'
governed_by:
- '[[Lakshmi_Governance]]'
constrained_by:
- '[[Human_Override]]'
- '[[Derivation_Transparency]]'
executed_by:
- '[[Brahma]]'
- '[[Ganesha]]'
- '[[Lakshmi]]'
compiles:
- '[[Context_Pack]]'
---

# ADR-0041 — Knowledge Graph Compiler v2

**Status:** PROPOSED  
**Date:** 2026-06-13  
**Deciders:** Brahma (Architecture), Lakshmi (Governance), Ganesha (CEO)  
**Supersedes:** ADR-0040 (KGC v1)  
**Mission:** MISSION-013B (Graph Quality Audit)

---

## Context

MISSION-013B audit revealed that KGC v1 produced a **linked archive**, not a **cognitive map**:

| Problem | Metric | Target |
| :--- | :--- | :--- |
| Files with no inbound links | 82.0% | ≤ 40% |
| Orphan files | 34.7% | ≤ 15% |
| Missions without ADR links | 88.2% | ≤ 20% |
| ADRs without mission links | 70.6% | ≤ 20% |
| Unknown type files | 22.8% | ≤ 10% |
| Concept nodes | 0 | ≥ 21 |
| Semantic relationship types | 0 | ≥ 12 |
| Dataview dashboards | 0 | ≥ 8 |
| Canvas visual maps | 0 | ≥ 5 |

The graph is a star topology centered on MOC hubs. Individual files are weakly connected. Evolution chains (ADR-0029 → ADR-0037) are not traversable.

---

## Decision

Y-OS adopts **Knowledge Graph Compiler v2 (KGC v2)** as the canonical tool for transforming the linked archive into a cognitive knowledge interface.

KGC v2 extends KGC v1 with five new pipeline stages:
1. Semantic relationship inference
2. Concept node generation
3. Body wikilinks injection
4. Dataview dashboard generation
5. Canvas visual map generation

All constraints from ADR-0040 remain: non-destructive, additive-only, reversible, dry-run first.

---

## Semantic Relationship Schema

12 new typed relationship fields added to YAML frontmatter:

```yaml
supersedes: []          # This ADR supersedes [[ADR-XXXX]]
superseded_by: []       # This ADR was superseded by [[ADR-XXXX]]
implements: []          # This artifact implements [[concept/ADR]]
derived_from: []        # Derived from [[artifact]]
validates: []           # Governance doc validates [[ADR/mission]]
depends_on: []          # Depends on [[artifact]]
governs: []             # Governance doc governs [[ADR/mission]]
compiles: []            # Runtime compiles [[context_pack]]
injects: []             # Runtime injects into [[mission/session]]
preserves: []           # Artifact preserves [[artifact]]
produces: []            # Mission produces [[ADR/artifact]]
belongs_to_domain: ""   # constitution|runtime|context|governance|memory|mission
```

---

## Inference Rules (10 rules)

| Rule | Source Pattern | Inferred Relationship |
| :--- | :--- | :--- |
| R1 | ADR body: `Supersedes: ADR-XXXX` | `supersedes: [[ADR-XXXX]]` + `superseded_by` on target |
| R2 | ADR body: `Related: ADR-XXXX` | `related_adrs: [[ADR-XXXX]]` (bidirectional) |
| R3 | Mission folder contains ADR file | mission `produces: [[ADR-XXXX]]` |
| R4 | ADR references `MISSION-XXX` in body | `related_missions: [[mission_XXX]]` |
| R5 | Governance report in mission folder | `validates: [[mission_XXX]]` |
| R6 | Runtime file references context pack | `compiles: [[context_pack]]` |
| R7 | ADR body: `implements Article X` | `constitutional_articles: [Article X]` |
| R8 | Filename `_v2` with same base as `_v1` | `supersedes: [[v1_file]]` |
| R9 | CEO briefing in mission folder | `validates: [[mission_XXX]]` |
| R10 | Context pack references CCR version | `derived_from: [[CCR_Runtime_vX]]` |

---

## Concept Node Generation (21 nodes)

Target folder: `concepts/`

| Concept | Domain | Key Links |
| :--- | :--- | :--- |
| Artifact_Primacy | constitution | Article I, ADR-0021, ADR-0024 |
| Preservation_Principle | constitution | Article II, ADR-0040 |
| Derivation_Transparency | constitution | Article III |
| Human_Override | constitution | Article IV |
| Governance_Before_Autonomy | constitution | Article V, ADR-0033 |
| CCR_Runtime | context | ADR-0029, ADR-0030, ADR-0037 |
| Context_Pack | context | ADR-0036, Context_Pack_Schema_v1 |
| Session_Delta | memory | ADR-0038, Session_Delta_Engine_v1 |
| Living_Memory_Pipeline | memory | ADR-0039, LMP_Doctrine_v1 |
| Canonical_Memory | memory | ADR-0039, Mode D |
| Context_Router | context | ADR-0037, Mode B/D |
| Knowledge_Graph_Compiler | artifact | ADR-0040, ADR-0041 |
| Artifact_Registry | artifact | ADR-0016, ADR-0017 |
| Y-ORC | runtime | ADR-0025, yorc_runtime_v1 |
| ART | runtime | ADR-0026, art_runtime_v1 |
| CRT | runtime | ADR-0028, crt_runtime_v1 |
| Lakshmi_Governance | governance | ADR-0033, ADR-0035 |
| Constitutional_Core | constitution | ADR-0024, ADR-0034 |
| Replacement_Test | mission | MISSION-007, ADR-0022 |
| Obsidian_Vault | artifact | ADR-0040, ADR-0041 |
| Git-backed_Memory | artifact | Y-OS_Git_Architecture_v1 |

---

## Body Wikilinks Pass

KGC v2 adds `[[...]]` inline wikilinks in body text for:
- ADR `Supersedes:` lines → `[[ADR-XXXX]]`
- ADR `Related:` lines → `[[ADR-XXXX]]`
- Mission definition files → `[[ADR-XXXX]]` for their output ADR
- Concept mentions in body → `[[Concept_Node]]`

**Constraint:** Body wikilinks are added only at the end of existing lines, never replacing text.

---

## Dataview Dashboards (8 files)

| File | Query |
| :--- | :--- |
| `dv_accepted_adrs.md` | ADRs WHERE status = "ACCEPTED" |
| `dv_missions_by_status.md` | Missions sorted by date |
| `dv_runtime_components.md` | type = "runtime_spec" |
| `dv_governance_reviews.md` | type = "governance_report" sorted by date |
| `dv_context_artifacts.md` | tags contains "#ccr" OR "#context" |
| `dv_orphan_files.md` | Files with no inlinks |
| `dv_recent_artifacts.md` | Sorted by file.mtime DESC |
| `dv_high_connectivity.md` | Sorted by inlinks+outlinks DESC |

---

## Canvas Visual Maps (5 files)

| File | Content |
| :--- | :--- |
| `canvas_constitutional_stack.canvas` | Constitution → ADRs → Runtime layers |
| `canvas_ccr_evolution.canvas` | ADR-0029 → 0030 → 0037 timeline |
| `canvas_living_memory_pipeline.canvas` | 8-stage LMP flow |
| `canvas_mission_adr_chain.canvas` | MISSION-010 → ADR-0039 evolution |
| `canvas_context_modes.canvas` | Mode A–F comparison |

---

## Improved MOC Templates

Two new MOCs:
- `08_Mission_Timeline_MOC.md` — chronological mission→ADR chain
- `09_ADR_Evolution_MOC.md` — supersession chains, domain grouping

---

## Success Criteria

| Metric | KGC v1 | KGC v2 Target |
| :--- | :--- | :--- |
| Files with inbound links | 18.0% | ≥ 50% |
| Orphan files | 34.7% | ≤ 15% |
| Missions with ADR links | 11.8% | ≥ 80% |
| ADRs with mission links | 29.4% | ≥ 80% |
| Unknown type files | 22.8% | ≤ 10% |
| Concept nodes | 0 | 21 |
| Semantic relationship types | 0 | 12 |
| Dataview dashboards | 0 | 8 |
| Canvas visual maps | 0 | 5 |
| ADR evolution traversable | No | Yes |

---

## Governance Verdict

**Lakshmi pre-review:** APPROVE_CONDITIONAL  
Condition: Dry-run validation required before body wikilinks pass.  
Risk Score estimate: 25/100 (additive only, reversible)

---

## Consequences

### Positive
- Graph transforms from star topology to semantic web
- ADR evolution chains become traversable
- Concept nodes provide semantic anchors
- Dataview enables dynamic corpus queries
- Canvas maps provide visual architecture

### Negative / Risks
- Body wikilinks pass requires careful validation (body integrity)
- Concept node generation requires semantic accuracy
- Canvas files are not Markdown — require Obsidian to render

### Mitigations
- Dry-run mode mandatory before apply
- Body wikilinks only appended to existing lines, never replacing text
- Canvas files are additive — no existing files modified


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **compiles:** [[Context_Pack]]
- **constrained_by:** [[Human_Override]]
- **constrained_by:** [[Derivation_Transparency]]
- **executed_by:** [[Brahma]]
- **executed_by:** [[Ganesha]]
- **executed_by:** [[Lakshmi]]
- **governed_by:** [[Lakshmi_Governance]]
- **implements:** [[CCR_Runtime]]
- **implements:** [[Context_Pack]]
- **supersedes:** [[ADR-0041_KGC_v1]]
