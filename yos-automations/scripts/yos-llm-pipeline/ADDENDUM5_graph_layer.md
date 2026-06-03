# Appendix — Graph Layer for Knowledge Navigation

**Version:** 1.2 — 2026-03-08  
**Extends:** `ADDENDUM4_concept_clusters.md`

This layer turns the Knowledge database into a concept graph rather than a flat list of knowledge items.

---

## Concept

Each Knowledge item can reference other Knowledge items via typed relations. This creates a semantic graph.

```
Knowledge Item A
   └ relates_to → Knowledge Item B
   └ relates_to → Knowledge Item C
```

---

## Graph Properties (add to Knowledge database)

| Property | Type | Purpose |
|---|---|---|
| `Related_Items` | Relation → Knowledge | General conceptual link |
| `Parent_Concept` | Relation → Knowledge | Higher-level abstraction |
| `Derived_From` | Relation → Knowledge | Concept evolution |
| `Supports` | Relation → Knowledge | Supporting evidence |
| `Contradicts` | Relation → Knowledge | Conflicting knowledge |
| `Concept_Cluster` | Relation → Concept_Clusters | Cluster grouping |

---

## Relationship Types

**Parent Concept** — higher-level abstraction:
```
knowledge_merge_conservative
   ↑ parent
knowledge_merge_append_first
knowledge_merge_update_strategy
```

**Derived From** — concept evolution:
```
ingestion_batch_interval
      ↓ derived from
ingestion_batch_interval_2_to_4h
```

**Supports** — evidence reinforcement:
```
"Avoid realtime ingestion"
      supports
"Batch ingestion strategy"
```

**Contradicts** — conflict tracking:
```
"Near realtime ingestion useful"
      contradicts
"Realtime ingestion unnecessary"
```

---

## Minimal Graph Creation Rule

Create relations **only when obvious**. Do not over-link.

Good links:
- Direct conceptual parent
- Clear contradiction
- Clear derivation
- Strong support relationship

**Limit:** max 3–5 relations per item.

---

## Graph Creation Workflow

```python
for new knowledge item:
    find similar concepts
    if broader concept exists:
        set Parent_Concept
    if item refines existing concept:
        set Derived_From
    if item reinforces another concept:
        set Supports
    if item conflicts with existing item:
        set Contradicts
```

---

## Example Knowledge Graph

```
knowledge_distillation_strategy
        ↑
knowledge_merge_conservative
        ↑
append_first_merge_carefully

pipeline_ingestion_strategy
        ↑
ingestion_batch_interval
        ↑
ingestion_batch_interval_2_to_4h
```

---

## Impact on Project Syntheses

```
Project_Synthesis
     ↓ reads
Concept_Clusters
     ↓ navigates
Knowledge Graph
     ↓ contains
Atomic Knowledge Items
```

---

## Final Complete Architecture

```
Chat_Export_Sessions
        ↓
Session classification
        ↓
Knowledge (atomic distilled items)
        ↓
Canonical Key system (deduplication)
        ↓
Merge / update logic (6 cases)
        ↓
Concept_Clusters (grouping, active at 150+ items)
        ↓
Knowledge Graph relations (links)
        ↓
Project_Synthesis
```

---

## Activation

Graph relations are created by the pipeline during `_create_knowledge_item()` and `apply_merge_decision()` when `GRAPH_ENABLED = true` in `yos_config.json`.

**Default:** disabled. Enable when Knowledge base > 150 items and Concept_Clusters are active.

---

## Operational Guidance

Treat the knowledge graph as a **living conceptual map**. Avoid over-structuring early. Prefer incremental linking, stable concepts, and careful consolidation.

> The graph should remain readable. If it becomes complex, it has failed its purpose.
