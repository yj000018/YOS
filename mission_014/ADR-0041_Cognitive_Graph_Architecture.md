---
id: yos-adr-0041-cognitive-graph-architecture
title: ADR-0041 Cognitive Graph Architecture v1
type: adr
status: ACCEPTED
mission: MISSION-014
date: '2026-06-13'
owner: Brahma
parent: '[[02_ADR_MOC]]'
supersedes: '[[ADR-0040]]'
derives_from: '[[ADR-0040]]'
related_adrs:
- '[[ADR-0040]]'
- '[[ADR-0039]]'
- '[[ADR-0038]]'
- '[[ADR-0037]]'
- '[[ADR-0033]]'
related_missions:
- '[[mission_013]]'
- '[[mission_013b]]'
- '[[mission_014]]'
constitutional_articles:
- 'Article I: Artifact Primacy'
- 'Article II: Preservation Principle'
- 'Article III: Derivation Transparency'
tags:
- '#adr'
- '#artifact'
- '#accepted'
- '#yos'
- '#memory'
aliases:
- CGA v1
- Cognitive Graph Architecture
- ADR-0041
source_branch: y-os-doctrine
canonical: true
implements:
- '[[CCR_Runtime]]'
- '[[Living_Memory]]'
- '[[Session_Delta]]'
- '[[Context_Pack]]'
governed_by:
- '[[Governance_Determinism]]'
- '[[Lakshmi_Governance]]'
constrained_by:
- '[[Preservation_Principle]]'
- '[[Derivation_Transparency]]'
- '[[Artifact_Primacy]]'
- '[[Human_Override]]'
- '[[Governance_Before_Autonomy]]'
executed_by:
- '[[Brahma]]'
- '[[Ganesha]]'
- '[[Lakshmi]]'
compiles:
- '[[Context_Pack]]'
---

# ADR-0041 — Cognitive Graph Architecture v1

**Status:** ACCEPTED  
**Date:** 2026-06-13  
**Deciders:** Brahma (Architecture), Lakshmi (Governance), Ganesha (CEO)  
**Supersedes:** ADR-0040 (KGC v1 — Knowledge Graph Compiler)  
**Mission:** MISSION-014 (Cognitive Graph Architecture)

---

## Context

MISSION-013 produced a document graph (311 files, 575 wikilinks, 100% frontmatter).  
MISSION-013B audit revealed the graph is **structurally correct but cognitively weak**:

- 82% of files have no inbound links
- 34.7% of files are orphans
- 0 concept nodes exist
- 0 semantic relationship types encoded
- Evolution chains (ADR-0029 → ADR-0037) not traversable
- Graph is a star topology centered on MOC hubs

**Root cause:** The graph is document-centric. Y-OS requires a concept-centric architecture.

> A document is not knowledge.  
> An ADR is not a concept.  
> A mission is not a capability.  
> **Knowledge emerges from relationships.**

---

## Decision

Y-OS adopts **Cognitive Graph Architecture v1 (CGA v1)** as the canonical evolution path from document graph to cognitive graph.

CGA v1 introduces three new architectural layers:

```
Layer 4: COGNITIVE NAVIGATION  (Dataview · Canvas · Breadcrumbs)
Layer 3: CONCEPT LAYER         (12 Concept Nodes · Semantic Anchors)
Layer 2: RELATIONSHIP LAYER    (12 Typed Relationships · Evolution Graph)
Layer 1: DOCUMENT LAYER        (existing — 311 files · 575 wikilinks)
```

---

## Three-Stage Evolution Model

```
Stage 1: Document Graph    ← MISSION-013 (COMPLETE)
Stage 2: Concept Graph     ← MISSION-014 (THIS ADR)
Stage 3: Cognitive Graph   ← MISSION-015+ (FUTURE)
```

| Stage | Primary Entity | Relationships | Navigation | Queries |
| :--- | :--- | :--- | :--- | :--- |
| Document Graph | File | Generic wikilinks | Filename-based | Manual search |
| **Concept Graph** | **Concept** | **12 typed edges** | **Concept-based** | **Dataview** |
| Cognitive Graph | Reasoning chain | Causal + temporal | Intent-based | Semantic |

---

## Layer 2: Semantic Relationship Schema (12 types)

```yaml
derives_from: []      # A is derived from B
supersedes: []        # A replaces B
superseded_by: []     # A was replaced by B
validates: []         # A validates B (governance)
validated_by: []      # A was validated by B
produces: []          # A produces B (mission → ADR)
produced_by: []       # A was produced by B
implements: []        # A implements B (concept)
implemented_by: []    # A is implemented by B
governed_by: []       # A is governed by B
governs: []           # A governs B
depends_on: []        # A depends on B
enables: []           # A enables B
evolves_into: []      # A evolved into B
evolved_from: []      # A evolved from B
canonical_source: []  # A is the canonical source for B
contradicts: []       # A contradicts B (tension)
belongs_to_domain: "" # constitution|runtime|context|governance|memory|mission|concept
```

---

## Layer 3: Concept Node Schema

12 concept nodes created in `concepts/`:

| # | Concept | Domain | ADR Lineage |
| :--- | :--- | :--- | :--- |
| 1 | [[Artifact_Primacy]] | constitution | ADR-0021, ADR-0024 |
| 2 | [[Preservation_Principle]] | constitution | ADR-0024, ADR-0040 |
| 3 | [[Derivation_Transparency]] | constitution | ADR-0024, ADR-0016 |
| 4 | [[Human_Override]] | constitution | ADR-0024, ADR-0034 |
| 5 | [[Governance_Before_Autonomy]] | constitution | ADR-0024, ADR-0033 |
| 6 | [[CCR_Runtime]] | context | ADR-0029 → ADR-0030 → ADR-0037 |
| 7 | [[Session_Delta]] | memory | ADR-0038 |
| 8 | [[Living_Memory]] | memory | ADR-0039 |
| 9 | [[Context_Pack]] | context | ADR-0036, ADR-0037 |
| 10 | [[Context_Router]] | context | ADR-0037 |
| 11 | [[Constitutional_Governance]] | governance | ADR-0033, ADR-0034, ADR-0035 |
| 12 | [[Governance_Determinism]] | governance | ADR-0033 |

---

## Layer 4: Cognitive Navigation Architecture

### Cognitive Query Capability

| Query | Answer Path | Enabled By |
| :--- | :--- | :--- |
| "What created CCR Runtime?" | CCR_Runtime → `canonical_source` → ADR-0029 | Concept node + Breadcrumbs |
| "What ADRs depend on Governance Determinism?" | Governance_Determinism → `governed_by` backlinks | Dataview |
| "Show evolution: Constitution → Living Memory" | Constitution → ADR-0024 → ADR-0039 → Living_Memory | Canvas |
| "Which missions contributed to Context Architecture?" | Context_Pack → `produced_by` → MISSION-010, 011 | Dataview |

### Plugin Stack (Minimal Viable Set)

| Plugin | Role | Priority |
| :--- | :--- | :--- |
| **Dataview** | Dynamic queries on typed relationships | 1 — ESSENTIAL |
| **Breadcrumbs** | Hierarchical navigation via typed edges | 2 — ESSENTIAL |
| **Canvas** | Visual cognitive maps | 3 — HIGH |
| Local Graph | Per-file relationship view | 4 — USE AS-IS |
| Metadata Menu | Frontmatter editing UI | 5 — OPTIONAL |
| Juggl | Force-directed semantic graph | 6 — OPTIONAL |

---

## Organizational Memory Graph

The Living Memory Pipeline as a typed graph:

```
Session (raw)
  └─compress──→ Context Pack
                 └─delta──→ Session Delta
                             └─summarize──→ Canonical Summary
                                            └─archive──→ Artifact Store
                                                          └─canonicalize──→ Canonical Memory
                                                                             └─compile──→ Context Pack v2
                                                                                          └─inject──→ Mission Context
```

Each stage is a typed edge (`compress`, `delta`, `summarize`, `archive`, `canonicalize`, `compile`, `inject`). Each artifact is a concept node. The graph IS the pipeline.

---

## Visual Cognitive Maps (6 maps — KGC v2 deliverable)

| Map | Content |
| :--- | :--- |
| `Concept_Map.canvas` | 12 concept nodes + typed relationships |
| `ADR_Evolution_Map.canvas` | ADR-0020 → ADR-0041 supersession chain |
| `Mission_Timeline_Map.canvas` | MISSION-001 → MISSION-014 + ADR outputs |
| `Runtime_Architecture_Map.canvas` | Y-ORC, ART, CRT, CCR relationships |
| `Constitutional_Dependency_Map.canvas` | Constitution → ADRs → Concepts |
| `Living_Memory_Map.canvas` | LMP 8-stage pipeline as graph |

---

## Implementation Roadmap

| Phase | Mission | Deliverable |
| :--- | :--- | :--- |
| **Phase 1 — Concept Layer** | MISSION-014 (this) | 12 concept nodes, 10_Concepts_MOC |
| Phase 2 — Relationship Inference | MISSION-015 (KGC v2) | kg_compiler_v2.py, body wikilinks, Canvas maps |
| Phase 3 — Cognitive Navigation | MISSION-016 | Dataview dashboards, Breadcrumbs config, Juggl eval |

---

## Rationale

| Alternative | Rejected Because |
| :--- | :--- |
| More MOC files | MOCs are lists, not semantic anchors |
| Better wikilinks only | Wikilinks without types are still document-centric |
| Obsidian plugin only | Not reproducible, not version-controlled |
| **Concept nodes + typed relationships** | **First-class semantic entities + traversable evolution chains** ✅ |

---

## Consequences

### Positive
- Graph becomes concept-centric, not document-centric
- ADR evolution chains become traversable (`supersedes` / `evolves_into`)
- Mission→ADR→Concept→Runtime navigation becomes possible
- Dataview queries can target concepts by domain, status, lineage
- Living Memory Pipeline becomes a typed graph, not a stage list

### Negative / Risks
- 12 concept nodes are manually authored — risk of semantic drift
- Typed relationships require KGC v2 inference rules for automation
- Canvas maps require Obsidian to render (not plain Markdown)

### Mitigations
- Concept node schema is strict (YAML + definition + lineage + evidence)
- KGC v2 inference rules automate relationship extraction from ADR bodies
- Canvas maps are additive — no existing files modified

---

## Governance Verdict — Lakshmi

**Risk Score: 15/100 — APPROVE (Low Risk)**

| Check | Result |
| :--- | :--- |
| Article I: Artifact Primacy | ✅ All concept nodes are explicit artifacts |
| Article II: Preservation Principle | ✅ 0 files deleted, additive only |
| Article III: Derivation Transparency | ✅ All concepts have ADR lineage + mission evidence |
| Article IV: Human Override | ✅ All concept content authored, not auto-generated |
| Article V: Governance Before Autonomy | ✅ Lakshmi review completed before adoption |
| Blocking reasons | 0 |

**Verdict: APPROVE**

---

## CEO Recommendation — Ganesha

**ADOPT immediately.**

CGA v1 is the architectural foundation that transforms Y-OS from a document archive into a cognitive operating system. The 12 concept nodes are the semantic anchors that make the graph navigable by intent, not by filename. This is the correct next evolution after MISSION-013.

**Priority:** Execute MISSION-015 (KGC v2) to implement the relationship inference engine and Canvas visual maps.


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **compiles:** [[Context_Pack]]
- **constrained_by:** [[Preservation_Principle]]
- **constrained_by:** [[Derivation_Transparency]]
- **constrained_by:** [[Artifact_Primacy]]
- **constrained_by:** [[Human_Override]]
- **constrained_by:** [[Governance_Before_Autonomy]]
- **executed_by:** [[Brahma]]
- **executed_by:** [[Ganesha]]
- **executed_by:** [[Lakshmi]]
- **governed_by:** [[Governance_Determinism]]
- **governed_by:** [[Lakshmi_Governance]]
- **implements:** [[CCR_Runtime]]
- **implements:** [[Living_Memory]]
- **implements:** [[Session_Delta]]
- **implements:** [[Context_Pack]]
