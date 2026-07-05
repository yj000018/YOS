# Decision Thread Model

> Y-OS / KAP Cognitive Architecture
> Gate: DECISION-THREAD-MODEL-GATE
> Status: ACTIVE

---

## 1. Definition

A **Decision Thread** is an evolving, reviewable record of a decision or decision family, preserving the accepted position, rationale, source evidence, rejected alternatives, tradeoffs, supersession history, implementation evidence, and current validity.

## 2. Purpose

The Decision Thread Model captures the *why* behind architectural and operational choices in YOS/KAP. Unlike Claims (atomic statements) or Thought Lines (thematic threads), a Decision Thread answers: what was decided, why, when, by whom, based on what evidence, what alternatives were rejected, what superseded what, and whether the decision is still active.

## 3. What is / is not a Decision Thread

**A Decision Thread MAY represent:**
- architecture decision
- workflow decision
- tooling decision
- source policy decision
- gate policy decision
- agent role decision
- data model decision
- repo architecture decision
- security / privacy decision
- normalization decision
- merge policy decision
- project direction decision
- pipeline decision
- automation decision
- human/AI exploitation decision

**A Decision Thread IS NOT:**
- claim
- thought line
- source fragment
- tag
- folder
- simple note
- final synthesis
- current-best knowledge
- unreviewed opinion
- automatically active doctrine

**Key distinctions:**
- A **Claim** is an atomic statement derived from fragments. A Decision Thread is a structured record of a decision with rationale and alternatives.
- A **Thought Line** is a thematic thread. A Decision Thread is a concrete decision record.
- An **MPM** is an execution prompt. A Decision Thread captures the decision that an MPM may have produced or referenced.

## 4. Field Model

Every Decision Thread must preserve the following metadata:

- `decision_thread_id`: Unique identifier (e.g., `DT-20260703-ABCD`)
- `title`: Full descriptive title
- `short_title`: Short label for navigation
- `decision_text`: The accepted decision, stated clearly
- `decision_type`: Category of the decision
- `domain`: Primary domain
- `scope`: Boundary note
- `status`: Lifecycle state
- `decision_status`: Decision-specific status
- `canonical_status`: Status within YOS control plane
- `review_status`: Human/AI review state
- `current_validity`: Whether the decision is still active
- `decision_date`: When the decision was made
- `first_seen_at`: Timestamp of earliest evidence
- `last_seen_at`: Timestamp of most recent evidence
- `created_at`: When the DT was registered
- `updated_at`: Last modification
- `decided_by`: Agent, user, or gate that made the decision
- `validated_by`: Guardian Architect or gate that validated it
- `source_fragment_ids`: Supporting Source Fragment IDs
- `claim_ids`: Supporting Claim IDs
- `thought_line_ids`: Related Thought Line IDs
- `impasse_ids`: Related Impasse IDs
- `related_decision_thread_ids`: Related Decision Thread IDs
- `parent_decision_thread_id`: Parent DT if this is a child
- `child_decision_thread_ids`: Child DTs
- `accepted_option`: The chosen option (text)
- `rejected_options`: List of rejected options with reasons
- `alternative_options`: Options considered but not chosen
- `rationale`: Why this decision was made
- `tradeoffs`: Known tradeoffs accepted
- `risks`: Known risks accepted
- `assumptions`: Assumptions underlying the decision
- `constraints`: Constraints that shaped the decision
- `implementation_evidence_ids`: Evidence that the decision was implemented
- `gate_evidence_ids`: Gate reports that reference this decision
- `mpm_ids`: MPMs that reference this decision
- `commit_ids`: Git commits that implement this decision
- `supersedes`: Decision Thread IDs this supersedes
- `superseded_by`: Decision Thread ID that supersedes this
- `partially_supersedes`: Partial supersession targets
- `partially_superseded_by`: Partial supersession sources
- `contradicts`: Decision Thread IDs this contradicts
- `supports`: Decision Thread IDs this supports
- `depends_on`: Decision Thread IDs this depends on
- `review_required`: Boolean flag
- `next_review_gate`: Gate that should trigger next review
- `confidence_level`: Overall confidence
- `authority_hint`: Expected authority level
- `maturity_hint`: Expected maturity level
- `contradiction_status`: State of internal conflict
- `supersession_status`: Temporal validity state
- `merge_status`: Integration state
- `sensitivity_level`: Privacy/security flag
- `human_summary`: Human-readable summary
- `agent_summary`: AI-readable summary for routing
- `review_notes`: Notes from review sessions
- `tags`: Thematic tags
- `notes`: Operational notes

## 5. Controlled Vocabularies

### 5.1 `decision_type`
`architecture`, `workflow`, `tooling`, `source_policy`, `gate_policy`, `agent_role`, `data_model`, `repo_architecture`, `security`, `privacy`, `normalization`, `merge_policy`, `project_direction`, `pipeline`, `automation`, `human_ai_exploitation`, `unknown`

### 5.2 `domain`
`YOS`, `KAP`, `KOSMOS`, `CasaTAO`, `ELYSIUM`, `YOUniverse`, `Obsidian`, `Notion`, `Manus`, `ChatGPT`, `Git`, `Automation`, `Memory`, `Agents`, `Source_Acquisition`, `Synthesis`, `Repo_Architecture`, `Unknown`

### 5.3 `status`
`candidate`, `proposed`, `accepted`, `active`, `under_review`, `superseded`, `partially_superseded`, `rejected`, `deprecated`, `archived`, `requires_review`

### 5.4 `decision_status`
`not_a_decision`, `decision_candidate`, `accepted_decision`, `active_decision`, `historical_decision`, `superseded_decision`, `rejected_decision`, `deprecated_decision`, `requires_review`

### 5.5 `canonical_status`
`not_canonical`, `candidate_evidence`, `active_control_plane`, `historical_source`, `implementation_evidence`, `superseded_source`, `requires_review`
*(Note: `active_control_plane` may only be used when the Decision Thread has been explicitly validated by a gate, Guardian Architect validation, or durable Git control-plane artifact. Most reconstructed historical DTs begin as `candidate_evidence` or `requires_review`.)*

### 5.6 `review_status`
`unreviewed`, `metadata_reviewed`, `content_reviewed`, `rationale_reviewed`, `alternatives_reviewed`, `evidence_reviewed`, `approved_for_active_control_plane`, `approved_for_synthesis_consideration`, `needs_human_review`, `blocked`

### 5.7 `current_validity`
`active`, `active_with_conditions`, `historical_context`, `superseded`, `partially_superseded`, `rejected`, `deprecated`, `uncertain`, `requires_review`

### 5.8 `contradiction_status`
`none_known`, `contains_contested_claims`, `contradicted_by_claim`, `contradicted_by_decision`, `contradicted_by_implementation`, `internally_inconsistent`, `needs_contradiction_review`

### 5.9 `supersession_status`
`unknown`, `active`, `historical`, `superseded`, `partially_superseded`, `supersedes_other`, `partially_supersedes_other`, `needs_supersession_review`

### 5.10 `merge_status`
`not_merged`, `candidate_for_merge`, `merged_into_parent`, `split_into_children`, `linked_to_thought_line`, `eligible_for_synthesis`, `merge_blocked`, `requires_review`

### 5.11 `confidence_level`
`high`, `medium`, `low`, `unknown`

### 5.12 `authority_hint`
`user_directive`, `guardian_architect_decision`, `manus_execution_report`, `gate_report`, `mpm`, `git_commit_evidence`, `source_document`, `implementation_evidence`, `memory_hint`, `external_reference`, `unknown`

### 5.13 `maturity_hint`
`raw`, `rough_note`, `exploratory`, `proposal`, `accepted_decision`, `validated_gate_output`, `implementation_evidence`, `active_doctrine`, `canonical_candidate`, `deprecated`, `unknown`

### 5.14 `sensitivity_level`
`public`, `internal`, `private`, `sensitive`, `secret_reference_only`, `unknown`

## 6. Relationship Model

### 6.1 Decision Thread ↔ Source Fragment
**Cardinality:** N:N
**Rules:**
1. One Decision Thread may rely on many Source Fragments.
2. One Source Fragment may provide evidence for many Decision Threads.
3. Source Fragments are evidence, not decisions.
4. Decision Threads must never overwrite Source Fragments.
5. Source chronology must be preserved.

### 6.2 Decision Thread ↔ Claim
**Cardinality:** N:N
**Rules:**
1. Claims may support, contradict, refine, or contextualize Decision Threads.
2. A Decision Thread may rely on multiple Claims.
3. A Claim may support multiple Decision Threads.
4. Decision Threads must preserve Claim status diversity.
5. A Decision Thread must not automatically validate its Claims.

### 6.3 Decision Thread ↔ Thought Line
**Cardinality:** N:N
**Rules:**
1. One Decision Thread may belong to multiple Thought Lines.
2. One Thought Line may contain multiple Decision Threads.
3. Thought Lines provide thematic context.
4. Decision Threads provide concrete decision memory.
5. A Thought Line must not replace the Decision Thread.

### 6.4 Decision Thread ↔ Decision Thread
Decision Threads may relate by:
`supports`, `contradicts`, `refines`, `supersedes`, `superseded_by`, `partially_supersedes`, `partially_superseded_by`, `depends_on`, `blocks`, `unblocks`, `is_parent_of`, `is_child_of`, `duplicates`, `partially_duplicates`, `merged_into`, `split_from`, `needs_review_against`

### 6.5 Decision Thread ↔ Impasse
A Decision Thread may preserve rejected approaches, failed approaches, or recurring traps.
**Allowed statuses:** `contains_candidate_impasse`, `contains_validated_impasse`, `rejects_impasse`, `replaced_by_impasse_policy`

### 6.6 Decision Thread ↔ Current Best Knowledge
Decision Threads may later support current-best synthesis, but this gate must not generate it.
**Allowed status for now:** `eligible_for_future_synthesis`

## 7. Lifecycle

1. `candidate_detected`
2. `registered`
3. `source_linked`
4. `claim_linked`
5. `rationale_captured`
6. `alternatives_captured`
7. `reviewed`
8. `supersession_checked`
9. `active_or_historical_status_assigned`
10. `synthesis_eligible_or_archived`

**Rules:**
1. Decision Threads begin as candidates unless explicitly created from current active control-plane decisions.
2. Decision Threads do not become active doctrine automatically.
3. Decision Threads can remain useful even if rejected, deprecated, or superseded.
4. Decision Threads must preserve source provenance.
5. Decision Threads must preserve rejected alternatives.
6. Decision Threads must preserve rationale and tradeoffs.
7. Decision Threads must preserve contradiction state.
8. Decision Threads must never erase Claims or Source Fragments.
9. Later decisions are not automatically more correct.
10. Supersession must be explicit or marked `needs_supersession_review`.

## 8. Boundary Policy

A good Decision Thread should be:
- decision-centered
- traceable
- reviewable
- linked to evidence
- linked to rationale
- linked to alternatives
- bounded
- not too broad
- not too narrow
- useful for human explanation
- useful for AI routing

**Bad Decision Thread examples:**
- AI strategy
- Important decision
- Use tools
- Architecture
- Do better ingestion

**Good Decision Thread examples:**
- YOS contains KAP as module/process.
- Git/Markdown is the durable authority for strategic doctrine.
- Broad acquisition is blocked until cognitive architecture is validated.
- ZIP is transport only, not primary corpus.
- Obsidian real vault scan is blocked until metadata dry-run gate.
- Notion canonical merge is blocked until controlled pipeline validation.
- Current-best synthesis is blocked until Source Fragment, Claim, Thought Line, and Decision Thread models are validated.

## 9. Supersession Policy

**Types of supersession:**

1. **Full supersession:** The old decision is entirely replaced. Mark old DT `supersession_status: superseded`, new DT `supersession_status: supersedes_other`.
2. **Partial supersession:** Only part of the old decision is replaced. Mark both with `partially_superseded` / `partially_supersedes_other`. Document which part remains active.
3. **Reversal:** A decision is explicitly reversed. Mark old DT `decision_status: rejected`. Preserve rationale for the reversal.
4. **Deprecation:** A decision is no longer relevant but not replaced. Mark `decision_status: deprecated_decision`.
5. **Historical retention:** Superseded decisions are never deleted. They remain for historical context.
6. **Implementation-confirmed supersession:** A commit or gate report confirms the new approach. Link via `commit_ids` or `gate_evidence_ids`.
7. **Gate-confirmed supersession:** A gate explicitly validates the supersession. Link via `gate_evidence_ids`.
8. **Human/Guardian-confirmed supersession:** Guardian Architect explicitly confirms. Set `validated_by: guardian_architect_decision`.
9. **Ambiguous supersession:** Mark `supersession_status: needs_supersession_review` and flag for human review.

**Rules:**
- Superseded decisions are not deleted.
- Superseded decisions preserve rationale and historical context.
- A later decision does not automatically supersede an earlier decision.
- Supersession must be explicit or marked for review.
- Partial supersession must preserve which part remains active.

## 10. Reversal and Deprecation Handling

**Reversal:** When a decision is explicitly reversed:
1. Mark `decision_status: rejected`.
2. Set `current_validity: rejected`.
3. Preserve `rationale` and `rejected_options`.
4. Add reversal reason to `review_notes`.
5. Link to the new decision via `superseded_by`.

**Deprecation:** When a decision is no longer relevant:
1. Mark `decision_status: deprecated_decision`.
2. Set `current_validity: deprecated`.
3. Preserve all historical fields.
4. Add deprecation reason to `notes`.

## 11. Rationale and Alternative Preservation

Every Decision Thread must preserve:
- `accepted_option`: The chosen option stated clearly.
- `rejected_options`: List of options that were considered and rejected, with reasons.
- `alternative_options`: Options that were considered but not formally rejected.
- `rationale`: The reasoning behind the accepted option.
- `tradeoffs`: What was given up.
- `risks`: Known risks accepted.
- `assumptions`: Assumptions underlying the decision.
- `constraints`: Constraints that shaped the decision.

Rejected options must never be deleted, even if the decision is superseded.

## 12. Implementation Evidence Handling

When a decision has been implemented:
1. Populate `implementation_evidence_ids` with Source Fragment IDs from implementation.
2. Populate `commit_ids` with relevant Git commit hashes.
3. Populate `gate_evidence_ids` with gate report IDs.
4. Update `current_validity` to `active` if confirmed.
5. Update `maturity_hint` to `implementation_evidence`.

## 13. Human Navigation Implications

Decision Threads are the primary navigation layer for understanding *why* the system is the way it is. `human_summary` must answer: what was decided, why, and whether it is still active. Navigation by `decision_type` and `domain` is the primary access pattern.

## 14. AI Retrieval / Routing Implications

AI agents query Decision Threads by `decision_type`, `domain`, `current_validity`, and `canonical_status` to understand current constraints before executing tasks. `agent_summary` must be structured for semantic search. Agents must respect `current_validity: superseded` and not act on superseded decisions.

## 15. Examples

See `DECISION-THREAD-EXAMPLES.md`.

## 16. Validation Rules

- `decision_thread_id` must follow pattern `DT-YYYYMMDD-XXXX`.
- `decision_text` must be a clear, bounded statement — not a vague theme.
- `accepted_option` must be populated for any DT with `decision_status: accepted_decision` or higher.
- `rejected_options` must be populated if alternatives were considered.
- `superseded_by` must be populated if `supersession_status: superseded`.
- `current_validity` must be `active` or `active_with_conditions` only if supported by evidence.

## 17. Open Questions

- How to handle decisions made informally across multiple sessions without a clear decision date?
- Should Decision Threads have a maximum age before mandatory supersession review?
- How to represent decisions that were never explicitly made but are implied by implementation?
