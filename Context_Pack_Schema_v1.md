# Context Pack Schema v1

**Date:** 2026-06-13  
**Status:** Canonical Schema  
**Mission:** CCR-001

## 1. Schema Definition

The Context Pack is the canonical unit of state transfer from the Y-OS organization to a specific LLM execution session.

It is structured as a YAML document.

```yaml
context_pack_id: string
mission_id: string
target_capability: string
target_worker: string
target_provider: string
target_model: string

lineage:
  parent_artifact_ids: list[string]
  current_artifact_chain: list[string]

state:
  mission_objective: string
  current_state: string
  open_loops: list[string]
  known_risks: list[string]
  missing_context: list[string]

constraints:
  relevant_decisions: list[string]
  relevant_adrs: list[string]
  relevant_laws: list[string]
  relevant_doctrine: list[string]
  active_constraints: list[string]

knowledge:
  relevant_memory: list[string]

execution:
  expected_output_artifact: string
  success_criteria: list[string]
  output_format: string

meta:
  token_budget: integer
  freshness_timestamp: string (ISO 8601)
```

## 2. Rationale

This schema ensures that every fresh LLM session receives exactly what it needs to execute its capability, without the noise of past conversational turns. It enforces the Y-OS principle that **Artifacts are the source of truth**.
