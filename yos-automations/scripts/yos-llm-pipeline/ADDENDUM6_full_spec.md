# yOS LLM Knowledge System — Architecture & Implementation Specification

**Version:** Add6 (Master Spec)
**Date:** 2026-03-09

---

## 1. Objective

Implement a robust long-term knowledge system for LLM chat exports.

The system transforms conversations from multiple LLMs into a structured knowledge base that:
- consolidates ideas
- preserves decisions
- tracks issues and actions
- avoids duplication
- maintains stable project syntheses
- scales to thousands of sessions

**Guiding rule:** `append first, merge carefully, rewrite rarely`

---

## 2. Memory Architecture

```
LLM Chats
    ↓
Episodic Memory       → Chat_Export_Sessions
    ↓
Semantic Memory       → Knowledge
    ↓
Concept Graph         → Concept_Clusters
    ↓
Working Memory        → Active_Context          [NEW — Add6]
    ↓
Signal Scoring        → Knowledge (fields)      [NEW — Add6]
    ↓
Project Synthesis     → Notion pages (manual)
```

---

## 3. Memory Layers

### 3.1 Episodic Memory — `Chat_Export_Sessions`
Raw interaction history. Each row = one exported chat session.

### 3.2 Semantic Memory — `Knowledge`
Atomic knowledge items: decisions, insights, issues, actions, constraints, principles, hypotheses, open questions.

### 3.3 Concept Graph — `Concept_Clusters`
Groups related knowledge items into conceptual domains.

### 3.4 Working Memory — `Active_Context` *(missing layer #1)*
Temporary active context used by the agent during reasoning.
- Active project focus
- Currently relevant decisions
- Active issues
- Selected knowledge items
- Reasoning notes

### 3.5 Signal Scoring Memory *(missing layer #2)*
Each knowledge item receives signals:

| Field | Purpose |
|---|---|
| Importance | Strategic relevance |
| Confidence | Reliability |
| Freshness | Recency |
| Evidence_Count | Supporting sessions |

---

## 4. Data Stores — Full Schema

### 4.1 Chat_Export_Sessions

| Field | Type |
|---|---|
| Title | Title |
| Source_LLM | Select |
| Source_Export | Select |
| Session_ID | Text |
| Date_Session | Date |
| Created_Time | Created time |
| Content_Raw | Long text |
| Content_Clean | Long text |
| Keywords | Multi-select |
| Projects | Multi-select |
| Subprojects | Multi-select |
| Short_Summary | Text |
| Processed | Checkbox |
| Processed_Date | Date |
| Knowledge_Items | Relation |
| Token_Size_Est | Number |
| Language | Select |
| Quality_Flag | Select |
| Notes_System | Text |

### 4.2 Knowledge

| Field | Type |
|---|---|
| Title | Title |
| Item_Type | Select |
| Project | Select |
| Subproject | Select |
| Keywords | Multi-select |
| Content | Long text |
| Short_Summary | Text |
| Status | Select |
| Priority | Select |
| Confidence | Select |
| Importance | Select |
| Freshness | Select |
| Canonical_Key | Text |
| Evidence_Count | Number |
| First_Seen | Date |
| Last_Seen | Date |
| Validity | Select |
| Supersedes | Relation |
| Superseded_By | Relation |
| Merge_Status | Select |
| Conflict_Flag | Checkbox |
| Source_Sessions | Relation |
| Related_Items | Relation |
| Parent_Concept | Relation |
| Derived_From | Relation |
| Supports | Relation |
| Contradicts | Relation |
| Concept_Cluster | Relation |
| Last_AI_Update | Date |

### 4.3 Concept_Clusters

| Field | Type |
|---|---|
| Title | Title |
| Canonical_Key | Text |
| Project | Select |
| Keywords | Multi-select |
| Concept_Summary | Long text |
| Knowledge_Items | Relation |
| Evidence_Count | Number |
| Last_Update | Date |

### 4.4 Active_Context *(NEW)*

| Field | Type |
|---|---|
| Context | Title |
| Project | Select |
| Active_Knowledge | Relation |
| Active_Decisions | Relation |
| Active_Issues | Relation |
| Reasoning_Notes | Text |
| Last_Update | Date |

### 4.5 Pipeline_State

| Field | Type |
|---|---|
| Pipeline | Title |
| Last_Processed | Date |
| Last_Run_Status | Select |
| Last_Run_Notes | Text |
| Processed_Count | Number |

---

## 5. Processing Pipeline

```
Step 1 — Session Ingestion
Step 2 — Session Classification (keywords, project, summary, language)
Step 3 — Candidate Knowledge Extraction
Step 4 — Canonical Key Generation
Step 5 — Merge Engine (6 cases)
Step 6 — Concept Cluster Assignment
Step 7 — Knowledge Graph Relations
Step 8 — Active Context Update (Working Memory)
Step 9 — Project Synthesis Update
```

---

## 6. Canonical Key Generation

Format: `concept_domain_qualifier`

Examples:
- `pipeline_state_storage_notion`
- `ingestion_no_realtime`
- `ingestion_batch_interval`

---

## 7. Merge Logic (6 Cases)

| Case | Condition | Action |
|---|---|---|
| 1 — Duplicate | Same canonical key, same content | Merge evidence, Evidence_Count++, Last_Seen |
| 2 — Reformulation | Same key, different wording | Update wording, keep item |
| 3 — Extension | Same key, new detail | Append to content |
| 4 — Replacement | Explicit supersession | Create new, mark old Validity=superseded |
| 5 — Conflict | Contradiction detected | Create Open_Question, Conflict_Flag=true |
| 6 — Low-value | < 30 chars or noise | Ignore |

---

## 8. Concept Cluster Assignment

Create cluster when ≥3 related items share a conceptual domain.

---

## 9. Knowledge Graph Relations

Types: `Parent_Concept`, `Derived_From`, `Supports`, `Contradicts`, `Related_Items`

Limit: 3–5 relations per item. No speculative links.

---

## 10. Project Synthesis

Sections per project:
- Executive_Summary
- Current_State
- Active_Decisions
- Active_Issues
- Action_Items
- Open_Questions
- Constraints
- Recent_Changes
- Next_Steps

**Update strategy:** update only affected sections, never regenerate full synthesis.

Mapping:

| Knowledge Item Type | Synthesis Section |
|---|---|
| Decision | Active_Decisions |
| Issue | Active_Issues |
| Action_Item | Action_Items |
| Open_Question | Open_Questions |
| Constraint | Constraints |
| Next_Step | Next_Steps |
| Insight | Current_State |

---

## 11. System Modules

| Module | Role |
|---|---|
| `session_ingest` | Import sessions |
| `session_classifier` | Extract metadata |
| `knowledge_extractor` | Generate candidates |
| `canonical_key_generator` | Create canonical keys |
| `merge_engine` | Create/merge/update/supersede |
| `cluster_engine` | Manage concept clusters |
| `synthesis_engine` | Update project syntheses |
| `context_builder` | Maintain working memory |

---

## 12. Implementation Philosophy

Priority order:
1. preserve knowledge
2. merge evidence
3. update carefully
4. rewrite rarely

Avoid: speculative synthesis, aggressive rewriting, concept duplication.

---

## 13. Final Architecture Flow

```
Chat_Export_Sessions
        ↓
Session classification
        ↓
Knowledge extraction
        ↓
Canonical key detection
        ↓
Merge engine
        ↓
Concept clusters
        ↓
Knowledge graph
        ↓
Active context (working memory)
        ↓
Project synthesis
```
