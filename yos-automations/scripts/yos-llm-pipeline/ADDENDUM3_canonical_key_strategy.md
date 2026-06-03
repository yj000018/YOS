# Appendix — Canonical Key Strategy

**Version:** 1.2 — 2026-03-08  
**Extends:** `APPENDIX_merge_strategy.md` + `ADDENDUM2_operational_rules.md`

This appendix extends the knowledge merge system by defining a Canonical Key mechanism. The purpose is to allow the agent to detect conceptual duplicates across sessions, even when wording differs significantly. Without this mechanism, the knowledge base will slowly accumulate duplicates and diluted concepts.

---

## Concept

Each knowledge item must have a `Canonical_Key`. The Canonical Key is a normalized conceptual identifier representing the core idea of the item.

| Knowledge Statement | Canonical Key |
|---|---|
| Store pipeline state in Notion | `pipeline_state_storage_notion` |
| Pipeline state should live in Notion | `pipeline_state_storage_notion` |
| Notion should hold the ingestion state | `pipeline_state_storage_notion` |

Different wording → same conceptual key.

---

## Canonical Key Format

Structure: `domain_object_action`

| Concept | Canonical Key |
|---|---|
| Store pipeline state in Notion | `pipeline_state_storage_notion` |
| Batch ingestion every few hours | `ingestion_batch_interval` |
| Avoid real-time ingestion | `ingestion_no_realtime` |
| Incremental knowledge processing | `knowledge_incremental_processing` |
| Conservative merge strategy | `knowledge_merge_conservative` |

Rules:
- Lowercase
- Underscore-separated
- Concise but descriptive (max 5 tokens)
- Conceptual meaning, not sentence fragments

**Good:** `knowledge_merge_conservative`  
**Bad:** `we_should_merge_items_conservatively_to_avoid_duplication`

---

## Key Matching Strategy

Matching must be tolerant. The agent considers:
- Exact match
- Prefix match
- Strong token overlap (Jaccard ≥ 0.72)

Example — these should resolve to the same concept:
```
pipeline_state_storage_notion
pipeline_state_notebook_storage
pipeline_state_store_in_notion
```

---

## Evidence Aggregation

When multiple sessions support the same concept, do not duplicate. Instead:
- Add session to `Source_Sessions`
- Increment `Evidence_Count`
- Update `Last_Seen`

```
Canonical_Key: pipeline_state_storage_notion
Evidence_Count: 7
First_Seen: 2026-03-07
Last_Seen: 2026-03-12
```

Strong `Evidence_Count` = strong reinforcement signal.

---

## Canonical Key Stability

Keys should rarely change. Even if wording improves, the conceptual key remains stable.

Change only if:
- The concept itself changes
- The item splits into separate concepts

---

## Concept Expansion

When a concept becomes more precise:

```
Before: ingestion_batch_interval
        "Prefer periodic batch ingestion instead of realtime"

After:  ingestion_batch_interval_2_to_4h
        "Batch ingestion every 2–4 hours provides optimal simplicity"
```

Action: update existing item, optionally refine key, maintain link history.

---

## Concept Split

If one item contains two distinct ideas:

```
Before: ingestion_batch_strategy
        "Use batch ingestion and store state in Notion"

After (split):
  ingestion_batch_interval
  pipeline_state_storage_notion
```

---

## Recommended Key Domains

**Pipeline**
```
pipeline_state_storage
pipeline_ingestion_schedule
pipeline_incremental_processing
pipeline_merge_strategy
```

**Knowledge System**
```
knowledge_merge_conservative
knowledge_distillation_strategy
knowledge_duplicate_detection
knowledge_evidence_aggregation
```

**Infrastructure**
```
chrome_export_pipeline
notion_storage_layer
manus_processing_loop
```

**Projects**
```
yos_memory_architecture
yos_model_routing
yos_distillation_pipeline
```

---

## Integration With Merge Logic

```
generate canonical key
    ↓
search knowledge items with similar keys (first filter)
    ↓
if match found:
    merge evidence
else:
    semantic comparison (title, content)
    → create / merge / update / supersede / conflict
```

Canonical keys act as the **first filter** before semantic comparison. This makes merge decisions faster and more reliable at scale.

---

## Integration in Pipeline

Canonical key generation is part of the LLM distillation prompt. The model generates a `canonical_key` for each extracted knowledge item. The `find_similar_knowledge_items()` function uses this key as the primary search vector before falling back to title/content similarity.
