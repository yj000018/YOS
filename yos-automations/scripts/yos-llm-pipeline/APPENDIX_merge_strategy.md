# Appendix — Incremental Knowledge Merge Strategy

**Version:** 1.1 — 2026-03-08  
**Extends:** `manus_llm_knowledge_pipeline_brief.md`

---

## Integration With Main Pipeline

This logic runs after Phase 1 ingestion and during Phase 2 distillation.

```
Chat_Export_Sessions
        ↓
Session classification
        ↓
Candidate knowledge extraction
        ↓
Merge / update logic  ← this document
        ↓
Knowledge database update
        ↓
Project synthesis partial update
```

New sessions enrich existing knowledge rather than rewriting it.

---

## Core Principle

> New chat data must not trigger a full re-analysis of the project knowledge.

For each candidate item extracted from a new session:

1. Extract candidate knowledge items
2. Compare with existing knowledge
3. Decide: **create / merge / update / supersede / ignore**

---

## Knowledge Merge Decision Tree

### Step 1 — Search Similar Existing Items

Search in Knowledge database using:

- same `Project`
- similar `Subproject`
- similar `Item_Type`
- overlapping `Keywords`
- `Canonical_Key` overlap

Only items within the same conceptual scope are considered.

---

### Case A — Exact or Near Duplicate

| | |
|---|---|
| **Condition** | Similarity ≥ 0.72 |
| **Example** | Existing: "Store pipeline state in Notion" / New: "Pipeline state should live in Notion" |
| **Action** | Do not create new item. Link session in `Source_Sessions`, increment `Evidence_Count`, update `Last_Seen`, set `Merge_Status = merged` |

---

### Case B — Reformulation With Same Meaning

| | |
|---|---|
| **Condition** | Similarity 0.45–0.72, same semantic intent |
| **Example** | Existing: "Prefer batch ingestion every 2–4 hours" / New: "Real-time ingestion is unnecessary" |
| **Action** | Merge with existing. If wording is clearer, update `Content`. Update `Last_Seen`. |

---

### Case C — Meaningful Extension

| | |
|---|---|
| **Condition** | Similarity 0.45–0.72, new detail adds information |
| **Example** | Existing: "Store pipeline state in Notion" / New: "Only store last_processed timestamp to keep it simple" |
| **Action** | Update existing item. Append new detail to `Content`. Update `Last_Seen`. Set `Merge_Status = updated`. |

---

### Case D — New Decision Replaces Previous One

| | |
|---|---|
| **Condition** | `Item_Type = Decision`, similarity 0.45–0.72, content is a replacement |
| **Example** | Old: "Run ingestion every 4 hours" / New: "Run ingestion every 2 hours" |
| **Action** | Create new item. Mark old item `Validity = superseded`. Link old → new via `Superseded_By`. Never silently overwrite. |

---

### Case E — Contradiction Without Resolution

| | |
|---|---|
| **Condition** | Same topic, opposing stance detected (negation heuristic) |
| **Example** | Chat A: "Real-time ingestion unnecessary" / Chat B: "Near-real-time useful for debugging" |
| **Action** | Do not merge. Create `Item_Type = Open_Question` with `Conflict_Flag = true`. Both ideas remain visible until resolved. |

---

### Case F — Low Value Repetition

| | |
|---|---|
| **Condition** | Content < 30 chars, or pure repetition without new insight |
| **Action** | Ignore. No new knowledge item created. |

---

## Required Knowledge Fields for Merge Logic

| Property | Type | Purpose |
|---|---|---|
| `Canonical_Key` | Text | Normalized concept identifier for deduplication |
| `Evidence_Count` | Number | Number of supporting sessions |
| `First_Seen` | Date | First occurrence of this concept |
| `Last_Seen` | Date | Last occurrence of this concept |
| `Validity` | Select | `active` / `superseded` / `tentative` / `archived` |
| `Supersedes` | Relation | Link to replaced item |
| `Superseded_By` | Relation | Link to replacement |
| `Merge_Status` | Select | `new` / `merged` / `updated` / `conflicted` |
| `Conflict_Flag` | Checkbox | Contradiction marker |

> **Note:** The Notion MCP API does not support adding columns to existing databases via ALTER TABLE. These fields must be added manually in Notion, or the pipeline will write them as text properties where supported.

---

## Project Synthesis Update Strategy

Project syntheses must remain **stable over time**.

They are derived from `Knowledge`, not rewritten from chat sessions.

**Rule:** Do not regenerate entire synthesis each run. Only update affected sections.

### Synthesis Page Sections

Each project synthesis page contains:

- `Executive_Summary`
- `Current_State`
- `Active_Decisions`
- `Active_Issues`
- `Action_Items`
- `Open_Questions`
- `Constraints`
- `Recent_Changes`
- `Next_Steps`

### Selective Update Mapping

| `Item_Type` | Section Updated |
|---|---|
| `Decision` | `Active_Decisions` |
| `Issue` | `Active_Issues` |
| `Action_Item` | `Action_Items` |
| `Open_Question` | `Open_Questions` |
| `Constraint` | `Constraints` |
| `Next_Step` | `Next_Steps` |
| `Insight` | `Current_State` |

### Recent Changes Block

Each pipeline run appends to `Recent_Changes`:

```
Added decision: store pipeline state in Notion
Updated principle: prefer batch ingestion every 2–4 hours
Added issue: duplicate risk in weak merge logic
Open question: how aggressive merge detection should be
```

### Stability Rule

`Executive_Summary` must change rarely. Update only if:

- Major decisions change
- Architecture changes
- Project direction changes

---

## Merge Philosophy

The system must prioritize:

- **Stability** — knowledge base does not drift with each run
- **Traceability** — every change is linked to a source session
- **Incremental enrichment** — new data adds, not replaces

Avoid:

- Rewriting history
- Collapsing conflicting ideas
- Generating synthetic consensus

> The knowledge base should behave like a research notebook, not a constantly rewritten report.

---

## Script-Level Integration

The merge logic is implemented in `llm_distillation_pipeline.py` in the `apply_merge_decision()` function.

**Pseudo-logic:**

```python
for each candidate knowledge item extracted:

    find similar items in Knowledge

    if near duplicate (sim >= 0.72):
        merge evidence
        update Last_Seen
        increment Evidence_Count

    elif extension of existing item (sim 0.45–0.72):
        update existing item
        set Merge_Status = updated

    elif replacement decision:
        create new item
        mark old item superseded

    elif unresolved contradiction:
        create Open_Question
        set Conflict_Flag = true

    elif new meaningful concept:
        create new Knowledge item

    else:
        ignore

then:
    for each affected project:
        update only relevant synthesis sections
        append Recent_Changes
        update Last_Update
```

---

## Final Operational Rule

When uncertain, prefer:

- **merge**
- **link**
- **defer decision**

over creating unnecessary new knowledge entries.

> Knowledge growth should be slow, deliberate, and cumulative.
