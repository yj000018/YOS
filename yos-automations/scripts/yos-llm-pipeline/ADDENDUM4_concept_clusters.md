# Appendix — Concept Clusters

**Version:** 1.2 — 2026-03-08  
**Extends:** `ADDENDUM3_canonical_key_strategy.md`

This layer addresses the **Knowledge Item Explosion** problem that appears when scaling from ~200 to 3000+ chats.

---

## Problem: Knowledge Item Explosion

Even with conservative merge, canonical keys, and evidence aggregation, the Knowledge base eventually produces too many atomic items.

Typical example at scale:

| Type | Count |
|---|---|
| Insights | 450 |
| Issues | 180 |
| Action Items | 120 |
| Decisions | 60 |

Navigation becomes difficult. Memory becomes too fragmented. What is missing: **a conceptual grouping layer**.

---

## The Fix: Concept_Clusters Database

A lightweight third database that groups Knowledge items.

**Final architecture:**

```
Chat_Export_Sessions
        ↓
Knowledge (atomic items)
        ↓
Concept_Clusters
        ↓
Project_Synthesis
```

---

## Concept_Clusters Schema

| Property | Type | Purpose |
|---|---|---|
| `Title` | Title | Cluster name |
| `Canonical_Key` | Text | Conceptual identifier |
| `Project` | Select | Project scope |
| `Keywords` | Multi-select | Thematic tags |
| `Concept_Summary` | Long text | Synthesized cluster description |
| `Knowledge_Items` | Relation → Knowledge | Linked atomic items |
| `Evidence_Count` | Number | Total supporting items |
| `Last_Update` | Date | Last modification |

---

## How Clusters Are Created

Clusters appear only when multiple items converge.

**Example:**

Knowledge items:
- "Prefer batch ingestion"
- "Avoid realtime ingestion"
- "Run ingestion every 2–4h"

→ Cluster: `ingestion_batch_strategy`

Cluster summary:
> The system prefers periodic batch ingestion (2–4h) instead of real-time ingestion to maintain simplicity and reliability.

**Rule:** Create a cluster only when 3+ items converge on the same concept.

---

## Merge Logic With Clusters

```
generate canonical key
    ↓
check existing Knowledge items → merge or create
    ↓
check Concept_Clusters
    if cluster exists with matching key → attach item
    else → leave unclustered (until 3+ items converge)
```

---

## Impact on Project Syntheses

Project synthesis reads **Concept_Clusters**, not all atomic items.

```
Project_Synthesis
     ↓ reads
Concept_Clusters
     ↓ contains
Knowledge_Items
```

This stabilizes syntheses enormously as the base grows.

---

## Activation Threshold

**Do not activate clusters from the start.**

Activate when:
- `Knowledge items > ~150`
- Navigation becomes difficult

The pipeline checks `CLUSTERS_ENABLED` in `yos_config.json` before attempting cluster operations.

---

## Notion Database

- **Name:** `Concept_Clusters`
- **Status:** Prepared, inactive until threshold
- **Data Source ID:** stored in `yos_config.json` once created
