# Thought Line Examples

> Y-OS / KAP Cognitive Architecture
> Gate: THOUGHT-LINE-MODEL-GATE
> Status: EXAMPLES ONLY — not real extracted Thought Lines unless explicitly noted

---

> **Important:** Examples marked `[REGISTERED]` are actual entries in THOUGHT-LINE-REGISTRY.md. Examples marked `[EXAMPLE ONLY]` are hypothetical illustrations of the model.

---

## Example 1 — Architecture Thought Line `[REGISTERED]`

```json
{
  "thought_line_id": "TL-20260703-CP01",
  "title": "YOS Control Plane Architecture",
  "short_title": "YOS Control Plane",
  "thought_line_type": "architecture",
  "domain": "YOS",
  "status": "seeded",
  "maturity_level": "candidate_architecture",
  "canonical_status": "active_control_plane",
  "review_status": "content_reviewed",
  "claim_ids": ["CLAIM-20260703-YOS1", "CLAIM-20260703-YOS2", "CLAIM-20260703-YOS4"],
  "source_fragment_ids": ["SF-005", "SF-006", "SF-007"],
  "current_best_status": "not_allowed_yet",
  "synthesis_allowed": "false",
  "contradiction_status": "none_known",
  "supersession_status": "active",
  "confidence_level": "high",
  "authority_hint": "guardian_architect_decision",
  "human_summary": "Tracks the evolving architecture of the YOS control plane — how YOS contains KAP, how Git is the durable authority, and how the Fragment/Claim/TL pipeline is structured.",
  "agent_summary": "YOS architecture thread: YOS>KAP hierarchy, Git authority, Fragment-Claim-TL pipeline model."
}
```

---

## Example 2 — Source Policy Thought Line `[REGISTERED]`

```json
{
  "thought_line_id": "TL-20260703-CP03",
  "title": "Git/Markdown Durable Authority",
  "short_title": "Git Authority",
  "thought_line_type": "doctrine",
  "domain": "YOS",
  "status": "seeded",
  "maturity_level": "active_doctrine",
  "canonical_status": "active_control_plane",
  "review_status": "approved_for_decision_threading",
  "claim_ids": ["CLAIM-20260703-YOS2"],
  "source_fragment_ids": ["SF-005", "SF-006", "SF-007"],
  "current_best_status": "not_allowed_yet",
  "synthesis_allowed": "false",
  "confidence_level": "high",
  "authority_hint": "guardian_architect_decision"
}
```

---

## Example 3 — Workflow Thought Line `[EXAMPLE ONLY]`

```json
{
  "thought_line_id": "TL-EXAMPLE-WF01",
  "title": "Session Capture and Git Persistence Workflow",
  "short_title": "Session Capture Workflow",
  "thought_line_type": "workflow",
  "domain": "KAP",
  "status": "candidate",
  "maturity_level": "emerging_pattern",
  "canonical_status": "candidate_evidence",
  "review_status": "metadata_reviewed",
  "current_best_status": "not_allowed_yet",
  "synthesis_allowed": "false",
  "confidence_level": "medium",
  "human_summary": "Tracks the evolving workflow for capturing session outputs and persisting them to Git — covering ChatGPT, Manus, and other LLM sessions.",
  "notes": "EXAMPLE ONLY — not registered in THOUGHT-LINE-REGISTRY.md"
}
```

---

## Example 4 — Tooling Thought Line `[EXAMPLE ONLY]`

```json
{
  "thought_line_id": "TL-EXAMPLE-TL01",
  "title": "Notion as Structured Navigation Layer",
  "short_title": "Notion Navigation",
  "thought_line_type": "tooling",
  "domain": "Notion",
  "status": "candidate",
  "maturity_level": "exploratory",
  "canonical_status": "candidate_evidence",
  "review_status": "metadata_reviewed",
  "current_best_status": "not_allowed_yet",
  "synthesis_allowed": "false",
  "confidence_level": "medium",
  "human_summary": "Tracks the evolving role of Notion in YOS — from primary store to structured navigation layer, with governance rules for controlled pipeline intake.",
  "notes": "EXAMPLE ONLY — not registered in THOUGHT-LINE-REGISTRY.md"
}
```

---

## Example 5 — Agent Governance Thought Line `[EXAMPLE ONLY]`

```json
{
  "thought_line_id": "TL-EXAMPLE-AG01",
  "title": "Agent Role Governance in YOS/KAP",
  "short_title": "Agent Governance",
  "thought_line_type": "agent_system",
  "domain": "Agents",
  "status": "candidate",
  "maturity_level": "exploratory",
  "canonical_status": "candidate_evidence",
  "review_status": "metadata_reviewed",
  "current_best_status": "not_allowed_yet",
  "synthesis_allowed": "false",
  "confidence_level": "medium",
  "human_summary": "Tracks the evolving definition of agent roles — Manus as executor, ChatGPT as Guardian Architect, and future specialized agents.",
  "notes": "EXAMPLE ONLY — not registered in THOUGHT-LINE-REGISTRY.md"
}
```

---

## Example 6 — Contradicted Thought Line `[EXAMPLE ONLY]`

```json
{
  "thought_line_id": "TL-EXAMPLE-CT01",
  "title": "Obsidian as Primary Long-Term Knowledge Store",
  "short_title": "Obsidian Primary Store",
  "thought_line_type": "tooling",
  "domain": "Obsidian",
  "status": "superseded",
  "maturity_level": "deprecated",
  "canonical_status": "historical_source",
  "review_status": "needs_human_review",
  "current_best_status": "not_allowed_yet",
  "synthesis_allowed": "false",
  "contradiction_status": "contains_contradicting_claims",
  "supersession_status": "superseded",
  "confidence_level": "low",
  "human_summary": "Early assumption that Obsidian was the primary long-term store. Superseded by Doctrine YOS-012 which establishes Git/Markdown as durable authority and Obsidian as consultation layer only.",
  "notes": "EXAMPLE ONLY. Retained for historical context. Do not delete."
}
```

---

## Example 7 — Superseded Thought Line `[EXAMPLE ONLY]`

```json
{
  "thought_line_id": "TL-EXAMPLE-SS01",
  "title": "n8n as Primary YOS Automation Engine",
  "short_title": "n8n Automation",
  "thought_line_type": "automation",
  "domain": "Automation",
  "status": "superseded",
  "maturity_level": "deprecated",
  "canonical_status": "historical_source",
  "supersession_status": "superseded",
  "current_best_status": "not_allowed_yet",
  "synthesis_allowed": "false",
  "confidence_level": "low",
  "human_summary": "Early architecture assumed n8n as the primary automation engine. Superseded by pivot to Manus-first architecture. Retained for historical context.",
  "notes": "EXAMPLE ONLY. Do not delete."
}
```

---

## Example 8 — Open Question Cluster Thought Line `[EXAMPLE ONLY]`

```json
{
  "thought_line_id": "TL-EXAMPLE-OQ01",
  "title": "Claim Extraction Granularity — Session vs. Prompt Level",
  "short_title": "Claim Extraction Granularity",
  "thought_line_type": "open_question_cluster",
  "domain": "KAP",
  "status": "candidate",
  "maturity_level": "seed",
  "canonical_status": "requires_review",
  "review_status": "needs_human_review",
  "current_best_status": "not_allowed_yet",
  "synthesis_allowed": "false",
  "confidence_level": "unknown",
  "human_summary": "Open question: should ChatGPT conversation fragments be extracted at session granularity or at prompt/response granularity? Impacts claim density and noise.",
  "notes": "EXAMPLE ONLY. Identified as open question in SOURCE-FRAGMENT-MODEL.md §15."
}
```
