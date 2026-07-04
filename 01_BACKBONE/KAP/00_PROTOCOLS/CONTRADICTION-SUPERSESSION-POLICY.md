# Contradiction & Supersession Policy

> Y-OS / KAP Cognitive Architecture
> Gate: CONTRADICTION-SUPERSESSION-POLICY-GATE
> Status: ACTIVE

---

## 1. Purpose

This policy defines how the YOS/KAP cognitive architecture handles contradictions, supersessions, reversals, deprecated knowledge, rejected options, historical context, and current validity across Source Fragments, Claims, Thought Lines, and Decision Threads.

The goal is to preserve provenance, chronology, and rationale without prematurely forcing a single "truth" or deleting historical evidence.

---

## 2. Definitions

- **Contradiction:** A documented tension between two or more YOS/KAP objects whose claims, decisions, implications, or statuses cannot all be simultaneously accepted without review.
- **Supersession:** An explicit relationship where one object, decision, claim, or model replaces, narrows, revises, or invalidates another while preserving the earlier object for provenance and historical context.
- **Deprecated:** No longer recommended for active use, while still preserved as historical evidence.
- **Rejected Option:** An alternative that was considered and not adopted, preserved because it explains decision rationale and prevents repeated dead ends.
- **Reversal:** A later decision that explicitly negates or abandons a prior accepted position.
- **Partial Supersession:** Occurs when only part of an earlier object is replaced while some portion remains active, useful, or historically relevant.

---

## 3. What is / is not a Contradiction

**Is a contradiction:**
- Two claims stating opposite facts about the same entity.
- A decision thread that mandates a workflow while an active pipeline implements a different one.
- A source fragment from a recent session stating X, while an older fragment states NOT X.

**Is NOT a contradiction:**
- An evolution in terminology (e.g., "KAP" vs "YOS-KAP").
- A change in scope (e.g., Phase 1 vs Phase 2).
- A rejected option documented alongside an accepted decision.

---

## 4. What is / is not Supersession

**Is supersession:**
- A new architecture decision explicitly replacing an old one.
- A new pipeline deprecating an old manual workflow.
- A gate report validating a new model over an older draft.

**Is NOT supersession:**
- Simply being newer. A later fragment does not automatically supersede an earlier decision.
- A claim contradicting another claim without explicit review/decision.

---

## 5. Controlled Vocabularies

### 5.1 `contradiction_type`
`none`, `direct_conflict`, `partial_conflict`, `scope_conflict`, `temporal_conflict`, `terminology_conflict`, `implementation_conflict`, `authority_conflict`, `evidence_conflict`, `decision_conflict`, `unknown`

### 5.2 `contradiction_status`
`none_known`, `suspected`, `confirmed`, `contested`, `resolved`, `partially_resolved`, `needs_review`, `not_applicable`, `unknown`

### 5.3 `supersession_type`
`none`, `full_supersession`, `partial_supersession`, `reversal`, `deprecation`, `implementation_supersession`, `gate_supersession`, `guardian_supersession`, `human_directive_supersession`, `historical_retention`, `unknown`

### 5.4 `supersession_status`
`not_superseded`, `suspected_superseded`, `superseded`, `partially_superseded`, `supersedes_other`, `partially_supersedes_other`, `deprecated`, `reversed`, `historical_only`, `needs_review`, `unknown`

### 5.5 `current_validity`
`active`, `active_with_conditions`, `candidate`, `historical_context`, `superseded`, `partially_superseded`, `deprecated`, `rejected`, `contested`, `uncertain`, `requires_review`, `not_applicable`

### 5.6 `review_requirement`
`none`, `metadata_review`, `content_review`, `evidence_review`, `authority_review`, `contradiction_review`, `supersession_review`, `guardian_review`, `human_review`, `blocked`

### 5.7 `resolution_status`
`unresolved`, `resolved_by_gate`, `resolved_by_guardian`, `resolved_by_user`, `resolved_by_implementation`, `resolved_by_later_decision`, `partially_resolved`, `deferred`, `blocked`, `unknown`

---

## 6. Cross-Layer Relationship Rules

### 6.1 Source Fragment ↔ Source Fragment
1. Fragments may contradict each other.
2. Contradicting fragments are never deleted.
3. Later fragments are not automatically more correct.
4. Contradiction must be recorded as relationship metadata.

### 6.2 Claim ↔ Claim
1. Claims may support, contradict, refine, duplicate, or supersede each other.
2. Contradicted Claims are not deleted.
3. Rejected Claims may still be useful historically.
4. A validated Claim is only validated within a defined context.

### 6.3 Thought Line ↔ Thought Line
1. Thought Lines may overlap, split, merge, contradict, or supersede each other.
2. Merging Thought Lines must preserve original IDs.
3. Splitting Thought Lines must preserve parent/child lineage.
4. A Thought Line may contain both active and superseded Claims.

### 6.4 Decision Thread ↔ Decision Thread
1. Decision Threads may supersede, partially supersede, reverse, contradict, or depend on each other.
2. Supersession must preserve rejected alternatives and rationale.
3. A later decision does not automatically supersede an earlier decision.
4. Supersession must be explicit or marked `needs_review`.

### 6.5 Cross-Layer
1. A Decision Thread may supersede a Claim’s active usage without deleting the Claim.
2. A Thought Line may remain active even if some contained Claims are superseded.
3. A Source Fragment may continue to exist as historical evidence even if all related Claims are rejected.
4. Current Best Knowledge must later cite which contradictions were resolved, deferred, or left contested.

---

## 7. Current Validity Rules

1. **Active:** Currently enforced and supported by evidence.
2. **Historical Context:** No longer active, but preserved for provenance.
3. **Contested:** Multiple active objects claim opposing truths.
4. **Uncertain:** Lacks sufficient evidence or authority to determine validity.

---

## 8. Historical Retention Rules

1. **Never delete:** Superseded, deprecated, reversed, or rejected objects are never deleted.
2. **Tagging:** Mark them with appropriate `current_validity` and `supersession_status`.
3. **Linkage:** Always link the historical object to the new object that supersedes it.

---

## 9. Rejected Options Policy

1. Rejected options must be preserved within Decision Threads.
2. They explain *why* a path was not taken, preventing repeated work.
3. They are not Claims or Decision Threads themselves, but metadata within a Decision Thread.

---

## 10. Deprecated Knowledge Policy

1. Knowledge that is no longer useful but not explicitly replaced is marked `deprecated`.
2. It remains searchable for historical context but is excluded from active routing.

---

## 11. Partial Supersession Policy

1. When only part of an object is replaced, mark `partially_superseded`.
2. Document exactly which part remains active in the `notes` or `resolution_status`.
3. Link to the new object(s) that replace the superseded parts.

---

## 12. Reversal Policy

1. A reversal is an explicit negation of a prior decision.
2. Mark the old decision `reversed` (or `rejected`).
3. Create a new Decision Thread documenting the reversal, the rationale, and the new direction.
4. Link the two.

---

## 13. Human Review Rules

1. Ambiguous contradictions or supersessions must be marked `needs_review`.
2. AI agents cannot autonomously resolve complex contradictions without a clear policy or gate report.
3. Human or Guardian Architect review is required to transition from `needs_review` to `resolved`.

---

## 14. AI Retrieval/Routing Implications

1. AI agents must filter by `current_validity: active` for operational routing.
2. AI agents must include `historical_context` when researching the *evolution* of a topic.
3. AI agents must flag `contested` or `requires_review` items to the user before acting on them.

---

## 15. Validation Rules

- A supersession relationship must have both a source object and a target object.
- A contradiction relationship must link at least two objects.
- `current_validity` must accurately reflect the object's state in the control plane.

---

## 16. Open Questions

- How should we visualize complex contradiction webs across multiple Thought Lines?
- What is the threshold for a "suspected" contradiction to be automatically flagged by an AI agent during ingestion?
