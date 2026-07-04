# Claim Examples

> Y-OS / KAP Cognitive Architecture
> Gate: CLAIM-MODEL-GATE
> Status: EXAMPLES ONLY — not real extracted claims unless explicitly noted

---

> **Important:** Examples below are illustrative. Claims marked `[REGISTERED]` are actual entries in CLAIM-REGISTRY.md. Claims marked `[EXAMPLE ONLY]` are hypothetical illustrations of the model.

---

## Example 1 — Architecture Claim `[REGISTERED]`

```json
{
  "claim_id": "CLAIM-20260703-YOS1",
  "claim_text": "YOS is the global cognitive operating system that contains KAP as a module/process.",
  "claim_type": "architecture_principle",
  "claim_scope": "YOS",
  "source_fragment_ids": ["SF-005", "SF-007"],
  "source_systems": ["Manus"],
  "created_at": "2026-07-03T00:00:00Z",
  "created_by": "Manus",
  "extraction_method": "control_plane_axiom",
  "canonical_status": "active_control_plane",
  "review_status": "content_reviewed",
  "truth_status": "supported",
  "contradiction_status": "none_known",
  "supersession_status": "active",
  "confidence_level": "high",
  "confidence_rationale": "Stated explicitly in CANONICAL-DOCTRINE-REGISTRY and ARCHITECTURE-BEFORE-ABSORPTION",
  "authority_hint": "guardian_architect_decision",
  "maturity_hint": "active_doctrine",
  "sensitivity_level": "internal"
}
```

---

## Example 2 — Source Policy Claim `[REGISTERED]`

```json
{
  "claim_id": "CLAIM-20260703-YOS2",
  "claim_text": "Git/Markdown is the durable authority for YOS/KAP strategic doctrine.",
  "claim_type": "architecture_principle",
  "claim_scope": "YOS",
  "source_fragment_ids": ["SF-005", "SF-006", "SF-007"],
  "canonical_status": "active_control_plane",
  "review_status": "approved_for_thought_line_linking",
  "truth_status": "validated",
  "contradiction_status": "none_known",
  "supersession_status": "active",
  "confidence_level": "high",
  "authority_hint": "guardian_architect_decision"
}
```

---

## Example 3 — Workflow Claim `[EXAMPLE ONLY]`

```json
{
  "claim_id": "CLAIM-EXAMPLE-WF01",
  "claim_text": "Every new doctrine produced in a ChatGPT or Manus session must be persisted to Git within the same session.",
  "claim_type": "workflow_rule",
  "claim_scope": "KAP",
  "source_fragment_ids": ["SF-001", "SF-002"],
  "canonical_status": "candidate_evidence",
  "review_status": "metadata_reviewed",
  "truth_status": "supported",
  "contradiction_status": "none_known",
  "supersession_status": "active",
  "confidence_level": "high",
  "authority_hint": "guardian_architect_decision",
  "notes": "EXAMPLE ONLY — not registered in CLAIM-REGISTRY.md"
}
```

---

## Example 4 — Tooling Claim `[EXAMPLE ONLY]`

```json
{
  "claim_id": "CLAIM-EXAMPLE-TL01",
  "claim_text": "Notion is used for structured knowledge storage and navigation, not as the durable authority.",
  "claim_type": "tooling_observation",
  "claim_scope": "YOS",
  "source_fragment_ids": ["SF-001"],
  "canonical_status": "candidate_evidence",
  "review_status": "metadata_reviewed",
  "truth_status": "supported",
  "contradiction_status": "none_known",
  "supersession_status": "active",
  "confidence_level": "medium",
  "notes": "EXAMPLE ONLY — not registered in CLAIM-REGISTRY.md"
}
```

---

## Example 5 — Implementation Fact Claim `[EXAMPLE ONLY]`

```json
{
  "claim_id": "CLAIM-EXAMPLE-IF01",
  "claim_text": "The KAP Source Fragment schema uses JSON Schema Draft-07 with additionalProperties: false.",
  "claim_type": "implementation_fact",
  "claim_scope": "KAP",
  "source_fragment_ids": ["SF-007"],
  "canonical_status": "active_control_plane",
  "review_status": "content_reviewed",
  "truth_status": "validated",
  "contradiction_status": "none_known",
  "supersession_status": "active",
  "confidence_level": "high",
  "authority_hint": "manus_execution_report",
  "notes": "EXAMPLE ONLY — not registered in CLAIM-REGISTRY.md"
}
```

---

## Example 6 — Contradicted Claim `[EXAMPLE ONLY]`

```json
{
  "claim_id": "CLAIM-EXAMPLE-CT01",
  "claim_text": "Obsidian is the primary long-term knowledge store for YOS.",
  "claim_type": "assertion",
  "claim_scope": "YOS",
  "source_fragment_ids": ["SF-001"],
  "canonical_status": "historical_source",
  "review_status": "needs_human_review",
  "truth_status": "contradicted",
  "contradiction_status": "contested_by_decision",
  "contradicting_fragment_ids": ["SF-005"],
  "supersession_status": "superseded",
  "confidence_level": "low",
  "authority_hint": "memory_hint",
  "notes": "EXAMPLE ONLY. Contradicted by Doctrine YOS-012 which establishes Git/Markdown as durable authority and Obsidian as consultation layer only."
}
```

---

## Example 7 — Superseded Claim `[EXAMPLE ONLY]`

```json
{
  "claim_id": "CLAIM-EXAMPLE-SS01",
  "claim_text": "n8n is the primary automation engine for YOS.",
  "claim_type": "assertion",
  "claim_scope": "YOS",
  "source_fragment_ids": [],
  "canonical_status": "historical_source",
  "review_status": "metadata_reviewed",
  "truth_status": "obsolete",
  "contradiction_status": "contested_by_implementation",
  "supersession_status": "superseded",
  "confidence_level": "low",
  "notes": "EXAMPLE ONLY. Superseded by pivot to Manus-first architecture. Retained for historical context."
}
```

---

## Example 8 — Open Question Claim `[EXAMPLE ONLY]`

```json
{
  "claim_id": "CLAIM-EXAMPLE-OQ01",
  "claim_text": "Should ChatGPT conversation fragments be extracted at session granularity or at prompt/response granularity?",
  "claim_type": "open_question",
  "claim_scope": "KAP",
  "source_fragment_ids": ["SF-007"],
  "canonical_status": "requires_review",
  "review_status": "needs_human_review",
  "truth_status": "unverified",
  "contradiction_status": "none_known",
  "supersession_status": "unknown",
  "confidence_level": "unknown",
  "notes": "EXAMPLE ONLY. Identified as open question in SOURCE-FRAGMENT-MODEL.md §15."
}
```
