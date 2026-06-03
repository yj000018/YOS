# Y-OS LLM Knowledge Distillation Pipeline

**Version:** 1.2 — 2026-03-08  
**Scope:** yOS / Notion-Memory / Distillation pipeline

---

## Architecture

The pipeline is built on 6 architectural layers:

| Layer | Name | Description | Status |
|---|---|---|---|
| 1 | Ingestion | `Chat_Export_Sessions` ← chatgpt2notion extension | Active |
| 2 | Distillation | Sessions → Knowledge items via LLM | Active |
| 3 | Merge Logic | Canonical Keys + 6-case conservative merge | Active |
| 4 | Concept Groups | `Concept_Clusters` grouping | Ready, inactive (activate at 150+ items) |
| 5 | Graph Layer | Typed relations between Knowledge items | Ready, inactive |
| 6 | Synthesis | Project-level incremental synthesis | Manual |

```
chatgpt2notion Auto-Sync (03:00 daily, Overwrite, Latest 28)
        ↓
Chat_Export_Sessions (Notion)
        ↓
Session classification (LLM: project, language, quality)
        ↓
Candidate knowledge extraction (LLM: items + canonical keys + graph hints)
        ↓
Canonical Key deduplication (first filter, token overlap)
        ↓
6-case merge decision tree
        ↓
Knowledge (atomic distilled items)
        ↓  [Layer 4 — active when items > 150]
Concept_Clusters (concept grouping)
        ↓  [Layer 5 — active with Clusters]
Knowledge Graph relations (typed links)
        ↓
Project_Synthesis (incremental, section-level updates)
```

---

## Notion Databases

| Database | Data Source ID | URL | Status |
|---|---|---|---|
| `Chat_Export_Sessions` | `13633cbd-7c08-475e-b610-a5377fbdfa91` | [Open](https://www.notion.so/97ecdc13e4be409bacb0ef1040f8d0dc) | Active |
| `Knowledge` | `1895910b-b8d4-4773-85b6-300d01a8d53d` | [Open](https://www.notion.so/270ebe6cf7df4b43b91ad96010cad4b7) | Active |
| `Pipeline_State` | `cb53fe34-b848-4375-aa90-6a74db18375b` | [Open](https://www.notion.so/8e13463eb8c94857afad53101a49a783) | Active |
| `Concept_Clusters` | `90fc337f-704e-4ba8-997d-d1137d6f49c6` | [Open](https://www.notion.so/d8a9f15ba04543baa84ef47971c9f583) | Ready, inactive |

All databases are located under the **MEMORY** page in the Notion workspace.

---

## Schedule

| Component | Time | Behavior |
|---|---|---|
| chatgpt2notion Auto-Sync | **03:00 daily** | Overwrite mode, Latest 28 conversations |
| Pipeline (Manus scheduler) | **05:00 daily** | Processes new/unprocessed sessions |

**Constraint:** Keep daily conversations < 28 to ensure full coverage by the extension window.

---

## Files

| File | Purpose |
|---|---|
| `llm_distillation_pipeline.py` | Main pipeline script (v1.2, all layers) |
| `import_sessions.py` | Bulk JSON import for bootstrap (200 chats) |
| `run_pipeline.sh` | Shell runner with logging |
| `yos_config.json` | **Central config — all parameters here** |
| `APPENDIX_merge_strategy.md` | Merge strategy reference (6 cases) |
| `ADDENDUM2_operational_rules.md` | 10 operational rules for LLM behavior |
| `ADDENDUM3_canonical_key_strategy.md` | Canonical Key format and matching strategy |
| `ADDENDUM4_concept_clusters.md` | Concept Clusters architecture |
| `ADDENDUM5_graph_layer.md` | Graph Layer for knowledge navigation |
| `db_ids.md` | Quick reference for all Notion IDs |

---

## Configuration (`yos_config.json`)

All parameters are centralized. Key settings:

```json
{
  "llm": {
    "model": "gpt-4o-mini",
    "max_content_chars": 12000,
    "temperature": 0.2
  },
  "merge": {
    "similarity_threshold_duplicate": 0.72,
    "similarity_threshold_extension": 0.45,
    "min_content_length_chars": 30
  },
  "features": {
    "clusters_enabled": false,
    "clusters_activation_threshold": 150,
    "graph_enabled": false
  }
}
```

---

## Usage

```bash
# Normal daily run (automated)
python3.11 llm_distillation_pipeline.py

# Preview without writing to Notion
python3.11 llm_distillation_pipeline.py --dry-run

# Bootstrap: reprocess all sessions
python3.11 llm_distillation_pipeline.py --force-all

# Import 200 existing chats (one-time)
python3.11 import_sessions.py --dir ./exports/ --source ChatGPT
python3.11 import_sessions.py --file export.json --dry-run
```

---

## Merge Decision Tree (Layer 3)

| Case | Condition | Action |
|---|---|---|
| **A** | Similarity ≥ 0.72 | Merge evidence, `Evidence_Count++`, update `Last_Seen` |
| **B/C** | Similarity 0.45–0.72 | Update existing item, append new content |
| **D** | Similarity 0.45–0.72, both Decisions | Create new, mark old as `superseded` |
| **E** | Contradiction detected | Create `Open_Question` with `Conflict_Flag=true` |
| **F** | Content < 30 chars | Ignore |
| **new** | No similar item | Create new item |

Similarity: `max(canonical_key_sim × 1.0, title_sim × 0.85, content_sim × 0.6)`

---

## Canonical Key Strategy (Layer 3)

Format: `domain_object_action` — lowercase, underscore-separated, max 5 tokens.

| Concept | Canonical Key |
|---|---|
| Store pipeline state in Notion | `pipeline_state_storage_notion` |
| Batch ingestion every few hours | `ingestion_batch_interval` |
| Conservative merge strategy | `knowledge_merge_conservative` |

The canonical key is the **primary deduplication signal**, generated by the LLM and applied before semantic comparison.

---

## Operational Rules (Layer 2 — LLM behavior)

10 rules injected into the LLM system prompt (Addendum 2):

1. Never rewrite entire project syntheses
2. Avoid knowledge duplication
3. Preserve historical decisions (supersede, never overwrite)
4. Distinguish Idea / Hypothesis / Decision / Action_Item
5. Prefer fewer, stronger items
6. Do not assume newer = better
7. Ignore low-value repetition
8. Handle conflicts explicitly (Open_Question + Conflict_Flag)
9. Maintain traceability (Source_Sessions)
10. Prefer stability over creativity

**Guiding principle:** `append first, merge carefully, rewrite rarely`

---

## Activation Roadmap

| Milestone | Action |
|---|---|
| Now | Run daily at 05:00. Bootstrap 200 chats with `--force-all`. |
| Knowledge > 150 items | Set `features.clusters_enabled = true` in `yos_config.json`. |
| Knowledge > 300 items | Set `features.graph_enabled = true`. |
| Knowledge > 3000 items | Consider semantic embedding for canonical key matching. |

---

## Knowledge Item Types

| Type | When to use |
|---|---|
| `Decision` | A clear choice made |
| `Action_Item` | Something to do |
| `Issue` | A problem identified |
| `Open_Question` | Unresolved question or contradiction |
| `Insight` | A reusable observation |
| `Principle` | A stable rule or guideline |
| `Hypothesis` | An idea to validate |
| `Idea` | A concept to explore |
| `Constraint` | A limitation to respect |
| `Next_Step` | Immediate next action |
| `Resource` | A useful reference |
| `Summary_Block` | High-level session summary |

---

## Logs

Pipeline execution logs: `/home/ubuntu/pipeline/pipeline.log`

Check `Pipeline_State` in Notion for last run status and count.

---

## Appendix Index

| File | Content |
|---|---|
| `APPENDIX_merge_strategy.md` | 6-case merge decision tree with examples |
| `ADDENDUM2_operational_rules.md` | 10 LLM behavioral rules with rationale |
| `ADDENDUM3_canonical_key_strategy.md` | Canonical Key format, matching, domains |
| `ADDENDUM4_concept_clusters.md` | Concept Clusters schema, activation, merge logic |
| `ADDENDUM5_graph_layer.md` | Graph Layer relations, workflow, size control |
