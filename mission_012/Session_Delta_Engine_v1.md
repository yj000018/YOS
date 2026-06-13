# Session Delta Engine v1 — Architecture & Schema

## 1. Executive Summary
The Session Delta Engine replaces raw conversational history with a structured, compressed, and actionable state representation. It bridges the gap between ephemeral session context and permanent organizational memory (Context Packs), ensuring LLMs receive only high-signal, operationally relevant information.

## 2. Core Principles

### 2.1 What Must Be Preserved
Session Delta must capture actionable state and forward-looking intent:
- **Decisions made** (but not yet formalized in artifacts)
- **Assumptions and constraints** introduced during the session
- **Open questions** and unresolved issues
- **Temporary user preferences** (e.g., "Use Python for this script")
- **Current mission state** (Step X of Y)
- **Corrections and course-changes** requested by the user

### 2.2 What Must NEVER Enter Session Delta
Session Delta strictly filters out noise and backward-looking verbosity:
- **Chatter and pleasantries**
- **Duplicate reasoning** (chain-of-thought dumps)
- **Obsolete discussion** (paths explored and abandoned)
- **Raw source text** (should be referenced via artifacts)
- **Low-signal content** ("I will do that now")

## 3. Session Delta Schema (YAML)

The schema is designed for maximum token efficiency and immediate operational clarity.

```yaml
session_delta_v1:
  metadata:
    mission_id: MISS-012
    last_update: "2026-06-13T10:00:00Z"
    delta_turn_count: 4
  
  mission_state:
    current_step: "Design Schema"
    overall_progress: "In Progress"
    blocking_issues: []

  decisions_log:
    - "Adopt incremental delta approach over rolling summary"
    - "Use YAML for schema definition"

  open_questions:
    - "Should archive access be completely removed or kept as fallback?"

  temporary_constraints:
    - "Do not design for ChatGPT; focus on Y-OS Git/Obsidian architecture"

  recent_corrections:
    - "User clarified: Focus on production architecture, not implementation"

  pending_actions:
    - "Draft Compression Strategy"
    - "Draft Migration Roadmap"
```

## 4. Evolution Strategy: Incremental Delta

**Decision:** We adopt **Incremental Delta (C)** combined with **Hierarchical Delta (D)** for structural organization.

- **Why not Last N Turns (A)?** Arbitrary cutoff loses critical early decisions.
- **Why not Rolling Summary (B)?** Summaries degrade over time, losing specificity and hallucinating connections.
- **Incremental Delta:** The engine maintains a structured state object. Each turn, it applies a *patch* (add, update, remove) to the state. If a decision is made, it is added to `decisions_log`. If a question is answered, it is removed from `open_questions`.

## 5. Compression Strategy

Compression is event-driven, not time-driven.

- **Delta Creation Trigger:** Start of a new mission or explicit user directive.
- **Delta Update Trigger:** After every user input or significant worker output. The LLM is prompted to output a JSON patch to update the YAML state.
- **Delta Merge Trigger:** When an artifact is formalized and written to the Registry. The relevant `decisions_log` and `temporary_constraints` are flushed from the Delta and moved to the Context Pack or Artifact.
- **Delta Archival Trigger:** Mission completion. The final Delta is attached to the Session Archive Summary.

## 6. Automatic Session Summary

**Can Session Delta become the automatic session summary? YES.**

Because the Delta maintains a structured representation of decisions, open questions, and state, the final state of the Delta at mission completion *is* the executive summary of the session. 
- **Runtime context:** Used actively during the session.
- **Archive summary:** Stored in Notion/Obsidian as the session record.
- **Restart pack:** If the mission is paused, loading the last Delta instantly restores the exact operational state.

## 7. Context Integration Design

The assembly pipeline for LLM execution:

```text
1. Base Truth: Canonical Memory (Constitution, ADRs)
      +
2. Mission Truth: Context Pack (Compiled from Artifact Registry)
      +
3. Current State: Session Delta (YAML state object)
      =
Final Prompt Context
```

## 8. Archive Integration Design

**Decision:** Archive access is restricted to an **Escalation Mode**.

- **Normal Execution:** Context Pack + Session Delta. (Sufficient for 99% of tasks).
- **Escalation Mode:** If the LLM explicitly detects missing historical context required to resolve an open question, it can invoke a specific capability (`query_archive`) to retrieve specific past Session Deltas or raw logs. Raw archive is *never* injected by default.

## 9. Session Delta Lifecycle

1. **Conversation:** User and Worker interact.
2. **Delta Update:** Background process applies state patch to YAML.
3. **Artifact Creation:** Worker produces an artifact.
4. **Delta Compression (Merge):** State elements resolved by the artifact are flushed from the Delta.
5. **Mission Complete:** Final Delta is frozen.
6. **Archive Summary:** Delta is committed to Long-Term Storage (Git/Obsidian).

## 10. Migration Roadmap

### Phase 1: Manual Generation
- Workers manually output the YAML Delta at the end of their response.
- Y-ORC passes this YAML to the next worker.

### Phase 2: Automatic Generation
- A dedicated background LLM call (fast model, e.g., GPT-4o-mini) processes the last turn and outputs a JSON patch to update the master Delta object.

### Phase 3: Continuous Background Generation
- Delta engine runs asynchronously. It monitors the event stream and maintains the YAML state in real-time, decoupling state management from worker execution latency.

### Phase 4: Self-Healing Delta Maintenance
- The Delta engine periodically audits itself against the Context Pack to remove redundant information that has already been formalized into artifacts.
