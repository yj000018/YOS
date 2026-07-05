# Claim Model

> Y-OS / KAP Cognitive Architecture
> Gate: CLAIM-MODEL-GATE
> Status: ACTIVE

---

## 1. Definition

A **Claim** is an atomic, reviewable statement derived from one or more Source Fragments, preserved with provenance, status, confidence, contradiction state, and future linkage capacity.

## 2. Purpose

The Claim Model bridges the gap between raw source material (Source Fragments) and active cognitive truth (Current-Best Synthesis). It allows YOS/KAP to extract, evaluate, debate, and track individual statements of fact, policy, or intent without prematurely treating them as canonical truth.

## 3. What is / is not a Claim

**A Claim MAY express:**
- definition
- assertion
- recommendation
- constraint
- risk
- decision candidate
- architecture principle
- tooling observation
- implementation fact
- open question
- impasse candidate
- supersession candidate

**A Claim IS NOT:**
- final truth
- current-best synthesis
- active decision
- thought line
- source fragment
- merged conclusion
- deduplicated knowledge

## 4. Field Model

Every Claim must preserve the following metadata:

- `claim_id`: Unique identifier (e.g., `CLAIM-20260703-ABCD`)
- `claim_text`: The atomic statement
- `claim_type`: Category of the statement
- `claim_scope`: Project or domain boundary
- `claim_language`: Primary language (default `en`)
- `source_fragment_ids`: Array of Source Fragment IDs this claim is derived from
- `source_systems`: Array of origin systems (inherited from fragments)
- `first_seen_at`: Timestamp of the earliest supporting fragment
- `last_seen_at`: Timestamp of the most recent supporting fragment
- `created_at`: When the claim was extracted
- `updated_at`: Last modification of the claim record
- `created_by`: Agent or user who extracted the claim
- `extraction_method`: Pipeline or tool used
- `claim_boundary`: Granularity note
- `supporting_fragment_ids`: Array of fragment IDs supporting the claim
- `contradicting_fragment_ids`: Array of fragment IDs contradicting the claim
- `related_claim_ids`: Array of linked claims
- `parent_claim_id`: ID of a broader parent claim (if applicable)
- `child_claim_ids`: Array of narrower child claims
- `candidate_thought_line_ids`: Array of thought lines this claim might inform
- `candidate_decision_thread_ids`: Array of decisions this claim might inform
- `candidate_impasse_ids`: Array of impasses this claim might document
- `confidence_level`: Assessment of certainty
- `confidence_rationale`: Justification for the confidence level
- `authority_hint`: Expected authority level
- `maturity_hint`: Expected maturity level
- `canonical_status`: Status within the YOS control plane
- `review_status`: Human/AI review state
- `truth_status`: Epistemic state within YOS/KAP
- `contradiction_status`: State of internal/external conflict
- `supersession_status`: Temporal validity state
- `merge_status`: Integration state
- `sensitivity_level`: Privacy/security flag
- `tags`: Array of thematic tags
- `notes`: Operational notes

## 5. Controlled Vocabularies

### 5.1 `claim_type`
`definition`, `assertion`, `recommendation`, `constraint`, `risk`, `architecture_principle`, `workflow_rule`, `tooling_observation`, `implementation_fact`, `decision_candidate`, `open_question`, `impasse_candidate`, `supersession_candidate`, `unknown`

### 5.2 `canonical_status`
`not_canonical`, `candidate_evidence`, `active_control_plane`, `historical_source`, `implementation_evidence`, `superseded_source`, `requires_review`
*(Note: `active_control_plane` should be rare and only used when the Claim has been explicitly promoted by a gate or decision).*

### 5.3 `review_status`
`unreviewed`, `metadata_reviewed`, `content_reviewed`, `approved_for_thought_line_linking`, `approved_for_decision_threading`, `approved_for_synthesis_consideration`, `rejected`, `needs_human_review`, `blocked`

### 5.4 `truth_status`
`unverified`, `supported`, `contested`, `contradicted`, `validated`, `rejected`, `obsolete`, `unknown`
*(Note: `validated` does not mean universally true; it means validated within the YOS/KAP review context).*

### 5.5 `contradiction_status`
`none_known`, `has_supporting_fragments`, `has_contradicting_fragments`, `internally_inconsistent`, `contested_by_later_source`, `contested_by_decision`, `contested_by_implementation`, `needs_contradiction_review`

### 5.6 `supersession_status`
`unknown`, `active`, `historical`, `superseded`, `supersedes_other`, `partially_superseded`, `needs_supersession_review`

### 5.7 `merge_status`
`not_merged`, `linked_to_source_fragment`, `linked_to_thought_line`, `linked_to_decision_thread`, `linked_to_impasse`, `eligible_for_synthesis`, `merged_into_synthesis`, `merge_blocked`

### 5.8 `confidence_level`
`high`, `medium`, `low`, `unknown`

### 5.9 `authority_hint`
`user_directive`, `guardian_architect_decision`, `manus_execution_report`, `git_commit_evidence`, `source_document`, `implementation_evidence`, `memory_hint`, `external_reference`, `unknown`

### 5.10 `maturity_hint`
`raw`, `rough_note`, `exploratory`, `proposal`, `validated_gate_output`, `implementation_evidence`, `active_doctrine`, `canonical_candidate`, `deprecated`, `unknown`

### 5.11 `sensitivity_level`
`public`, `internal`, `private`, `sensitive`, `secret_reference_only`, `unknown`

## 6. Relationship Model

### 6.1 Claim ↔ Source Fragment
**Cardinality:** N:N
**Rules:**
1. One Source Fragment may support many Claims.
2. One Claim may be supported by many Source Fragments.
3. A Claim must always link to at least one Source Fragment unless it is manually created as a control-plane Claim.
4. A Claim without source provenance must be marked `requires_review`.
5. Claims must never replace Source Fragments.
6. Claims must point back to fragments.
7. Contradictory fragments must be linked, not erased.

### 6.2 Claim ↔ Claim
Claims may relate by:
`supports`, `contradicts`, `refines`, `duplicates`, `partially_duplicates`, `supersedes`, `superseded_by`, `depends_on`, `is_child_of`, `is_parent_of`, `needs_review_against`

### 6.3 Claim ↔ Thought Line
Claims may become evidence for Thought Lines, but this gate must not create final Thought Lines.
**Allowed status:** `candidate_thought_line_link`

### 6.4 Claim ↔ Decision Thread
Claims may support, challenge, or contextualize decisions.
**Allowed statuses:** `candidate_decision_evidence`, `candidate_decision_rationale`, `candidate_rejected_option`, `candidate_supersession_evidence`

### 6.5 Claim ↔ Impasse
Claims may identify failed approaches or recurring traps.
**Allowed status:** `candidate_impasse`

### 6.6 Claim ↔ Current Best Knowledge
Claims may later be considered by current-best synthesis, but this gate must not produce current-best synthesis.
**Allowed status:** `eligible_for_synthesis`

## 7. Lifecycle

1. `candidate_detected`
2. `registered`
3. `source_linked`
4. `metadata_completed`
5. `reviewed`
6. `contradiction_checked`
7. `thought_line_linked`
8. `decision_thread_linked`
9. `synthesis_eligible`
10. `active_or_superseded_or_rejected`

**Rules:**
1. Claims begin as candidates.
2. Claims do not become active doctrine automatically.
3. Claims can remain useful even if rejected or superseded.
4. Claims must preserve source provenance.
5. Claims must preserve contradiction state.
6. Claims must preserve review state.
7. Claims must never erase earlier claims.
8. Later claims are not automatically more correct.

## 8. Claim Boundary Policy

A good Claim should be:
- atomic
- reviewable
- traceable
- bounded
- not too broad
- not too vague
- not overloaded

**Bad Claim examples:**
- YOS is important.
- KAP has many things.
- Manus is useful.
- Notion contains knowledge.

**Good Claim examples:**
- YOS is the global cognitive operating system that contains KAP as a module/process.
- Git/Markdown is the durable authority for YOS/KAP strategic doctrine.
- Source Staging is not canonical truth until reviewed and linked.
- A Source Fragment is not a Claim.
- A Claim must link back to one or more Source Fragments.

## 9. Contradiction Handling

When a new Claim contradicts an existing Claim:
1. Do not delete the old Claim.
2. Link them via `contradicts` relationship.
3. Update `contradiction_status` to `has_contradicting_fragments` or `contested_by_later_source`.
4. If resolution is needed, elevate to a Decision Thread.

## 10. Supersession Handling

When a Claim is officially replaced:
1. Mark the old Claim `superseded_status` = `superseded`.
2. Mark the new Claim `superseded_status` = `supersedes_other`.
3. Link them via `superseded_by` / `supersedes`.
4. Retain the old Claim for historical context.

## 11. Human Review Implications

Claims must be written in clear, atomic natural language to allow human review. Metadata must track exactly which fragments support the claim so the Guardian Architect can verify the extraction logic.

## 12. AI Retrieval Implications

AI agents will query Claims by `claim_type`, `truth_status`, and `canonical_status` to build Current-Best Synthesis or propose Decisions. Agents must respect `contradiction_status` and not present contested claims as absolute truth.

## 13. Examples

See `CLAIM-EXAMPLES.md`.

## 14. Validation Rules

- A Claim must have at least one `source_fragment_id` unless explicitly created as a control-plane axiom.
- `claim_text` must be a single, complete sentence.
- If `contradiction_status` is `has_contradicting_fragments`, `contradicting_fragment_ids` must not be empty.

## 15. Open Questions

- Should Claims be automatically generated by an LLM pipeline, or strictly extracted via specific gates?
- How to handle "near-duplicate" Claims extracted from different sessions without creating excessive noise?
