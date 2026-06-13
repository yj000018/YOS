---
id: yos-adr-0040-knowledge-graph-compiler
title: ADR-0040 Knowledge Graph Compiler v1
type: adr
status: ACCEPTED
mission: MISSION-013
date: '2026-06-13'
owner: Brahma
parent: '[[02_ADR_MOC]]'
related_adrs:
- '[[ADR-0039]]'
- '[[ADR-0038]]'
- '[[ADR-0037]]'
related_missions:
- '[[mission_013]]'
constitutional_articles:
- 'Article I: Artifact Primacy'
- 'Article II: Preservation Principle'
- 'Article III: Derivation Transparency'
tags:
- '#adr'
- '#artifact'
- '#accepted'
- '#yos'
aliases:
- Knowledge Graph Compiler v1
- KGC v1
source_branch: y-os-doctrine
canonical: true
implements:
- '[[CCR_Runtime]]'
- '[[Living_Memory]]'
- '[[Session_Delta]]'
governed_by:
- '[[Lakshmi_Governance]]'
constrained_by:
- '[[Artifact_Primacy]]'
- '[[Preservation_Principle]]'
- '[[Derivation_Transparency]]'
executed_by:
- '[[Brahma]]'
- '[[Ganesha]]'
- '[[Lakshmi]]'
- '[[Saraswati]]'
---

# ADR-0040 — Knowledge Graph Compiler v1

**Status:** ACCEPTED  
**Date:** 2026-06-13  
**Deciders:** Brahma (Architecture), Lakshmi (Governance), Ganesha (CEO)  
**Mission:** MISSION-013  
**Related:** ADR-0039 (Living Memory Pipeline), ADR-0038 (Session Delta), ADR-0037 (CCR Runtime v2)

---

## Context

The Y-OS Markdown corpus (301 files, 66 commits, `y-os-doctrine` branch) was a readable Git archive but lacked Obsidian-native structure:

- 13/301 files had YAML frontmatter (4.3%)
- 0 wikilinks in corpus
- 0 MOC files
- No typed relationships between ADRs, missions, governance artifacts
- No Dataview-compatible metadata
- Obsidian graph view: near-empty

The corpus needed to become a **living knowledge graph** without rewriting any canonical content.

---

## Decision

Y-OS adopts the **Knowledge Graph Compiler v1 (KGC v1)** as the canonical tool for transforming the Markdown corpus into an Obsidian-native knowledge graph.

The compiler is non-destructive, additive-only, and reversible. It operates as a 10-stage pipeline.

---

## Pipeline

```
Scan → Classify → Extract → Infer → Frontmatter → Related → MOCs → Index → Report → Commit
```

| Stage | Operation | Output |
| :---: | :--- | :--- |
| 1 | Scan corpus | File list (301 .md) |
| 2 | Classify files | 13 type categories |
| 3 | Extract metadata | date, version, status, owner |
| 4 | Infer relationships | ADR↔mission, constitutional articles |
| 5 | Add YAML frontmatter | 20-field schema, additive only |
| 6 | Add Related section | Safe append, body untouched |
| 7 | Generate MOCs | 8 index files |
| 8 | Generate graph index | kg_graph_index.json |
| 9 | Generate validation report | Before/after metrics |
| 10 | Commit to Git | `y-os-doctrine` branch only |

---

## File Classification Schema

| Type | Pattern | Count |
| :--- | :--- | :--- |
| `adr` | `ADR-\d+` | 33 |
| `mission` | `mission_\d+/` | 75 |
| `governance_report` | Lakshmi, Governance, Risk | 39 |
| `artifact` | _Schema, _Model, _Framework | 32 |
| `unknown` | No pattern match | 84 |
| `context_pack` | CCR, Context_Pack | 10 |
| `learning_report` | Saraswati, Learning | 8 |
| `diagram` | Diagram, .mmd | 7 |
| `runtime_spec` | Runtime, _runtime | 5 |
| `ceo_briefing` | CEO_Briefing, Ganesha | 4 |
| `constitution` | Y-OS_Constitution | 2 |
| `index` | MOC, Canonical_Map | 2 |

---

## YAML Frontmatter Schema

20 fields per file:

```yaml
id, title, type, status, mission, date, version,
owner, worker, provider, model,
parent, parents, children,
related_adrs, related_missions, related_concepts,
constitutional_articles, tags, aliases,
source_branch, canonical
```

---

## Hard Constraints (all satisfied)

| Constraint | Verified |
| :--- | :--- |
| No body content rewritten | ✅ Body preserved byte-for-byte |
| No file deleted | ✅ 0 deletions |
| No force push | ✅ Standard push only |
| All changes additive | ✅ Prepend frontmatter only |
| Reversible | ✅ `git revert` restores original |
| Dry-run before apply | ✅ Dry-run executed and validated |

---

## Results

| Metric | Before | After |
| :--- | :--- | :--- |
| Files with frontmatter | 13 (4.3%) | 301 (100%) |
| Wikilinks in corpus | 0 | 565 |
| Files with wikilinks | 1 | 200 |
| MOC files | 0 | 8 |
| ADR link coverage | 0% | 42.4% |
| Mission link coverage | 0% | 100% |
| Orphan files (no links) | ~290 | ~101 |
| Graph index | None | kg_graph_index.json |

---

## Rationale

| Alternative | Rejected Because |
| :--- | :--- |
| Manual frontmatter | Not scalable (301 files) |
| LLM-based enrichment | Risk of semantic rewriting, expensive |
| Obsidian plugin only | Not reproducible, not version-controlled |
| **KGC v1 (Python)** | **Deterministic, auditable, reversible, fast** ✅ |

---

## Consequences

### Positive
- Obsidian graph view becomes materially useful (200 linked files)
- Dataview queries now possible across all 301 files
- ADRs, missions, governance artifacts are typed and discoverable
- MOCs provide structured navigation entry points
- Corpus is now a living knowledge graph, not just a file archive

### Negative / Risks
- ADR link coverage at 42.4% (below 80% target) — ADRs that don't reference other ADRs in body text won't auto-link
- 84 "unknown" type files — need manual classification in v2
- Wikilinks are in YAML frontmatter, not body — Obsidian reads them, but body navigation requires manual [[]] addition

### Mitigations
- KGC v2 can improve ADR link coverage via semantic inference
- Unknown files can be reclassified by adding patterns to CLASSIFIERS
- Body wikilinks can be added in a future "body enrichment" pass (separate from this ADR)

---

## Governance Verdict

**Lakshmi Risk Assessment:**
- Constitutional compliance: ✅ Article I (Artifact Primacy), Article II (Preservation), Article III (Transparency)
- Risk Score: **18/100 — APPROVE (Low Risk)**
- No blocking reasons
- Note: ADR link coverage 42.4% < 80% target → flagged as WARNING, not blocker

**CEO Recommendation (Ganesha): ADOPT**

---

## Next Steps

- KGC v2: improve ADR link coverage via content-based inference
- Body wikilinks pass: add `[[...]]` inline references in mission bodies
- Dataview dashboard: create `.md` with Dataview queries for corpus analytics
- Obsidian vault sync: configure git plugin for auto-pull on local Mac


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **constrained_by:** [[Artifact_Primacy]]
- **constrained_by:** [[Preservation_Principle]]
- **constrained_by:** [[Derivation_Transparency]]
- **executed_by:** [[Brahma]]
- **executed_by:** [[Ganesha]]
- **executed_by:** [[Lakshmi]]
- **executed_by:** [[Saraswati]]
- **governed_by:** [[Lakshmi_Governance]]
- **implements:** [[CCR_Runtime]]
- **implements:** [[Living_Memory]]
- **implements:** [[Session_Delta]]
