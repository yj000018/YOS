# Contradiction & Supersession Examples

> Y-OS / KAP Cognitive Architecture
> Gate: CONTRADICTION-SUPERSESSION-POLICY-GATE
> Status: EXAMPLES ONLY — not registered unless explicitly noted

---

## Example 1 — Direct Contradiction (EXAMPLE ONLY)

**Scenario:** Two source fragments from different sessions state opposing facts about the same tool.

```yaml
relation_id: REL-EXAMPLE-DC01
relation_type: contradiction
source_object_id: SF-EXAMPLE-A
source_object_type: source_fragment
target_object_id: SF-EXAMPLE-B
target_object_type: source_fragment
contradiction_type: direct_conflict
contradiction_status: confirmed
supersession_type: none
supersession_status: not_superseded
current_validity_effect: contested
evidence_fragment_ids: [SF-EXAMPLE-A, SF-EXAMPLE-B]
review_requirement: guardian_review
resolution_status: unresolved
notes: "Fragment A (2025-11) says Obsidian is canonical. Fragment B (2026-03) says Obsidian is consultation-only. Later fragment does not auto-supersede earlier."
```

---

## Example 2 — Partial Contradiction (EXAMPLE ONLY)

**Scenario:** Two claims agree on the main point but conflict on scope.

```yaml
relation_id: REL-EXAMPLE-PC01
relation_type: contradiction
source_object_id: CLAIM-EXAMPLE-X
source_object_type: claim
target_object_id: CLAIM-EXAMPLE-Y
target_object_type: claim
contradiction_type: scope_conflict
contradiction_status: suspected
supersession_type: none
supersession_status: not_superseded
current_validity_effect: active_with_conditions
review_requirement: content_review
resolution_status: unresolved
notes: "Both claims agree KAP is inside YOS, but disagree on whether KAP includes the synthesis layer or only acquisition."
```

---

## Example 3 — Full Supersession (REGISTERED)

**Relation ID:** REL-20260703-CS02
**Status:** REGISTERED in CONTRADICTION-SUPERSESSION-REGISTRY.md

```yaml
relation_id: REL-20260703-CS02
relation_type: supersession
source_object_id: DT-20260703-YOS3
source_object_type: decision_thread
target_object_id: broad-acquisition-first-workflow
target_object_type: decision_thread
contradiction_type: none
contradiction_status: not_applicable
supersession_type: full_supersession
supersession_status: supersedes_other
current_validity_effect: rejected
evidence_fragment_ids: [SF-001, SF-002, SF-005]
review_requirement: none
resolution_status: resolved_by_guardian
notes: "Architecture Before Absorption doctrine fully supersedes any broad-acquisition-first approach."
```

---

## Example 4 — Partial Supersession (EXAMPLE ONLY)

**Scenario:** A new pipeline replaces only part of an old workflow.

```yaml
relation_id: REL-EXAMPLE-PS01
relation_type: supersession
source_object_id: DT-EXAMPLE-PIPE-NEW
source_object_type: decision_thread
target_object_id: DT-EXAMPLE-PIPE-OLD
target_object_type: decision_thread
contradiction_type: none
contradiction_status: not_applicable
supersession_type: partial_supersession
supersession_status: partially_supersedes_other
current_validity_effect: partially_superseded
review_requirement: metadata_review
resolution_status: partially_resolved
notes: "New pipeline replaces the ChatGPT2Notion import path. The Notion workspace as reference source remains active."
```

---

## Example 5 — Reversal (EXAMPLE ONLY)

**Scenario:** A decision explicitly negates a prior accepted position.

```yaml
relation_id: REL-EXAMPLE-REV01
relation_type: supersession
source_object_id: DT-EXAMPLE-NEW-DIRECTION
source_object_type: decision_thread
target_object_id: DT-EXAMPLE-OLD-DIRECTION
target_object_type: decision_thread
contradiction_type: decision_conflict
contradiction_status: resolved
supersession_type: reversal
supersession_status: reversed
current_validity_effect: rejected
evidence_decision_thread_ids: [DT-EXAMPLE-NEW-DIRECTION]
review_requirement: none
resolution_status: resolved_by_guardian
notes: "Decision to use Notion as canonical store was reversed. Git/Markdown is now the durable authority."
```

---

## Example 6 — Deprecated Approach (EXAMPLE ONLY)

**Scenario:** An old workflow is no longer recommended but not explicitly replaced.

```yaml
relation_id: REL-EXAMPLE-DEP01
relation_type: supersession
source_object_id: DT-EXAMPLE-CHATGPT2NOTION
source_object_type: decision_thread
target_object_id: null
target_object_type: null
contradiction_type: none
contradiction_status: not_applicable
supersession_type: deprecation
supersession_status: deprecated
current_validity_effect: deprecated
review_requirement: metadata_review
resolution_status: resolved_by_later_decision
notes: "ChatGPT2Notion pipeline deprecated (DEC-BOOT-010). No active replacement yet. Notion content remains accessible as reference source."
```

---

## Example 7 — Rejected Option (EXAMPLE ONLY)

**Scenario:** An alternative was considered and explicitly not adopted.

```yaml
relation_id: REL-EXAMPLE-REJ01
relation_type: supersession
source_object_id: DT-20260703-YOS2
source_object_type: decision_thread
target_object_id: notion-as-canonical-store
target_object_type: decision_thread
contradiction_type: none
contradiction_status: not_applicable
supersession_type: full_supersession
supersession_status: supersedes_other
current_validity_effect: rejected
evidence_decision_thread_ids: [DT-20260703-YOS2]
review_requirement: none
resolution_status: resolved_by_guardian
notes: "Notion-as-canonical was explicitly rejected in favor of Git/Markdown. Preserved to prevent future re-evaluation of the same path."
```

---

## Example 8 — Historical-Only Source (EXAMPLE ONLY)

**Scenario:** A source fragment from an early session is no longer actionable but preserved for provenance.

```yaml
relation_id: REL-EXAMPLE-HIST01
relation_type: supersession
source_object_id: SF-EXAMPLE-LEGACY
source_object_type: source_fragment
target_object_id: null
target_object_type: null
contradiction_type: none
contradiction_status: not_applicable
supersession_type: historical_retention
supersession_status: historical_only
current_validity_effect: historical_context
review_requirement: none
resolution_status: deferred
notes: "Early 2025 Obsidian note describing KAP as a standalone system. Preserved as provenance. Superseded by DT-20260703-YOS1."
```

---

## Example 9 — Active-With-Conditions Decision (EXAMPLE ONLY)

**Scenario:** A decision is active but only under specific conditions.

```yaml
relation_id: REL-EXAMPLE-AWC01
relation_type: contradiction
source_object_id: DT-20260703-YOS5
source_object_type: decision_thread
target_object_id: obsidian-real-vault-scan
target_object_type: decision_thread
contradiction_type: implementation_conflict
contradiction_status: confirmed
supersession_type: none
supersession_status: not_superseded
current_validity_effect: active_with_conditions
review_requirement: guardian_review
resolution_status: deferred
notes: "Obsidian real vault scan is active-with-conditions: blocked until OBSIDIAN-PIPELINE-VALIDATION-GATE passes. Condition must be met before activation."
```
