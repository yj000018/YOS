---
id: yos-adr-0042
title: 'ADR-0042: KGC v2 + Visual Drill-Down Layer'
type: adr
status: ACCEPTED
date: '2026-06-14'
owner: Brahma
parent: '[[02_ADRs_MOC]]'
mission: MISSION-015
supersedes: '[[ADR-0041]]'
governed_by:
  - '[[Governance_Determinism]]'
  - '[[Lakshmi_Governance]]'
constrained_by:
  - '[[Artifact_Primacy]]'
  - '[[Preservation_Principle]]'
  - '[[Derivation_Transparency]]'
  - '[[Governance_Before_Autonomy]]'
produces:
  - '[[kg_compiler_v2]]'
  - '[[kg_semantic_graph_v2]]'
  - '[[08_Visual_Maps]]'
  - '[[09_Dashboards]]'
tags:
  - '#adr'
  - '#accepted'
  - '#yos'
  - '#knowledge-graph'
  - '#visual'
aliases:
  - ADR-0042
  - KGC v2
  - Visual Drill-Down Layer
source_branch: y-os-doctrine
canonical: true
---

# ADR-0042: KGC v2 + Visual Drill-Down Layer

**Status:** ACCEPTED  
**Date:** 2026-06-14  
**Owner:** Brahma  
**Mission:** MISSION-015  
**Supersedes:** ADR-0041 (Cognitive Graph Architecture)

---

## Context

MISSION-013 created the document graph (301 files, 100% frontmatter, 565 wikilinks, 8 MOCs).  
MISSION-013B audited it: orphan rate 34.7%, 0 concept nodes, 0 typed relationships, no visual maps.  
MISSION-014 defined the Cognitive Graph Architecture: 12 concept nodes, 12 typed relationships, ADR-0041 ACCEPTED.

MISSION-015 must now **operationalize** the architecture:
- Implement the semantic inference engine (KGC v2)
- Expand concept nodes to 30+
- Generate visual drill-down maps (Canvas + Mermaid)
- Generate Dataview dashboards
- Produce machine-readable semantic graph

---

## Decision

**Implement KGC v2 as a Python-based semantic inference engine with the following capabilities:**

### A. Semantic Relationship Inference (21 types)

The engine infers typed relationships from file content, filename patterns, and frontmatter:

| Rule | Trigger | Relationship |
| :--- | :--- | :--- |
| R1 | "Supersedes: ADR-XXXX" in body | `supersedes` |
| R2 | `_v2` filename supersedes `_v1` | `supersedes` |
| R3 | Mission file mentions ADR | `produces` |
| R4 | Governance report mentions ADR/mission | `validates` |
| R5 | Body mentions "Governance Determinism" | `governed_by` |
| R6 | Body mentions CCR/Context Compiler | `implements` |
| R7 | Body mentions Article I–V | `constrained_by` |
| R8 | Body mentions worker names | `executed_by` |
| R9 | Body mentions "Living Memory Pipeline" | `implements` |
| R10 | Body mentions "Session Delta" | `implements` |
| R11 | Non-ADR file mentions ADR | `references` |
| R12 | Compiler + Context Pack mention | `compiles` |

### B. Relationship Storage

All inferred relationships are stored in YAML frontmatter (additive only).  
A machine-readable `kg_semantic_graph_v2.json` is generated with typed nodes and edges.

### C. Body Semantic Links (Additive Only)

A `## Semantic Links` section is appended to relevant files.  
**No canonical body text is modified.**

### D. Concept Node Expansion (12 → 39)

27 new concept nodes generated across 5 domains:
- Constitution/Governance: Constitutional Core, Replacement Test, Amendment Procedure, Lakshmi Governance
- Runtime: Y-ORC, ART, CRT, Context Compiler, Provider Adapter, Worker Registry, Model Registry, Artifact Registry
- Memory: Canonical Memory, Archive Reference, Knowledge Graph Compiler, Cognitive Graph, Organizational Digital Twin
- Organization: Ganesha, Brahma, Lakshmi, Saraswati, Hanuman, Krishna
- Technical: Git-backed Memory, Obsidian Vault, Markdown Corpus, GitHub Remote

### E. Visual Drill-Down Layer

**8 Canvas maps** (Obsidian-native, file-linked, drill-down capable):
1. YOS_Organizational_Digital_Twin — 7-layer system map (45 nodes)
2. YOS_Constitutional_Stack — Constitution → Governance chain
3. YOS_Runtime_Flow — Y-ORC → ART → CRT → CCR sequence
4. YOS_Context_Architecture — CCR v2 modes A/B/C/D
5. YOS_Living_Memory_Pipeline — 8-stage LMP cycle
6. YOS_Mission_Evolution — M-001 → M-015 timeline
7. YOS_ADR_Dependency_Map — ADR-0024 → ADR-0042 dependencies
8. YOS_Governance_Flow — Proposal → Lakshmi → CEO → ACCEPTED

**8 Mermaid fallback maps** (`.md` files with Mermaid diagrams)

**Excalidraw:** Not generated in MISSION-015 (see assessment). Canvas preferred for navigability.

### F. Dataview Dashboards (8)

`09_Dashboards/`: Dashboard_ADRs, Dashboard_Missions, Dashboard_Concepts, Dashboard_Governance, Dashboard_Runtime, Dashboard_Memory, Dashboard_Orphans, Dashboard_High_Connectivity

---

## Consequences

### Positive

- Vault upgraded from "linked archive" to "cognitive navigation interface"
- 39 concept nodes provide semantic anchors for graph traversal
- 1620 typed edges enable Dataview queries and Breadcrumbs navigation
- 8 Canvas maps provide visual entry points with drill-down to source notes
- 8 Dataview dashboards enable dynamic queries across the corpus
- All transformations are additive and reversible via Git

### Negative / Limitations

- Orphan rate improved but still high (72.5%) — many files are implementation artifacts not yet linked
- ADR↔mission coverage: 100% ADRs reference missions, but only 33% of mission files reference ADRs (mission files are numerous and include sub-reports)
- Excalidraw not generated — Canvas is the primary visual layer
- Dataview requires plugin installation in Obsidian

### Risks

- Inferred relationships are probabilistic — marked as `inferred: true` in graph JSON
- Semantic Links sections are additive but increase file size
- Canvas maps are static snapshots — must be regenerated when corpus evolves

---

## Governance

**Lakshmi Review:** APPROVE — Risk Score 18/100  
**Ganesha CEO Recommendation:** ADOPT  
**Constitutional Compliance:** All 5 Articles satisfied

---

## Implementation

- `mission_015/kg_compiler_v2.py` — semantic inference engine
- `mission_015/generate_concepts_v2.py` — concept node generator
- `mission_015/generate_visual_maps.py` — Canvas + Mermaid generator
- `mission_015/generate_dashboards.py` — Dataview dashboard generator
- `mission_015/kg_semantic_graph_v2.json` — machine-readable graph (363 nodes, 1620 edges)

---

## Semantic Links

- **supersedes:** [[ADR-0041]]
- **governed_by:** [[Governance_Determinism]], [[Lakshmi_Governance]]
- **constrained_by:** [[Artifact_Primacy]], [[Preservation_Principle]], [[Derivation_Transparency]], [[Governance_Before_Autonomy]]
- **produces:** [[Knowledge_Graph_Compiler]], [[Cognitive_Graph]], [[Organizational_Digital_Twin]]
- **implements:** [[Cognitive_Graph]]
