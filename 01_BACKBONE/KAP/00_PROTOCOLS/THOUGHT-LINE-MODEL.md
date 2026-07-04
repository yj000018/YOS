# Thought Line Model

> Y-OS / KAP Cognitive Architecture
> Gate: THOUGHT-LINE-MODEL-GATE
> Status: ACTIVE

---

## 1. Definition

A **Thought Line** is an evolving, reviewable thematic thread that groups related Claims, Source Fragments, Decisions, Impasses, and future Syntheses while preserving chronology, provenance, maturity, contradictions, and supersession history.

## 2. Purpose

The Thought Line Model bridges the gap between atomic Claims and final Current-Best Knowledge synthesis. It provides a structured, time-aware container for tracking how a theme or intellectual thread evolves across sessions, sources, and decisions — without prematurely collapsing it into a single truth.

## 3. What is / is not a Thought Line

**A Thought Line MAY represent:**
- architecture theme
- project theme
- source strategy
- tooling theme
- workflow theme
- doctrine theme
- ontology theme
- infrastructure theme
- agent capability theme
- memory theme
- automation theme
- civilizational / symbolic theme
- personal system theme
- open research theme

**A Thought Line IS NOT:**
- simple tag
- folder
- project
- claim
- decision
- source fragment
- current-best synthesis
- final truth
- deduplicated conclusion
- topic label without evolution

## 4. Field Model

Every Thought Line must preserve the following metadata:

- `thought_line_id`: Unique identifier (e.g., `TL-20260703-ABCD`)
- `title`: Full descriptive title
- `short_title`: Short label for navigation
- `description`: 1-3 sentence summary of the theme
- `thought_line_type`: Category of the thread
- `domain`: Primary domain (YOS, KAP, ELYSIUM, etc.)
- `scope`: Boundary note
- `status`: Lifecycle state
- `maturity_level`: Epistemic maturity
- `canonical_status`: Status within YOS control plane
- `review_status`: Human/AI review state
- `source_fragment_ids`: All linked Source Fragment IDs
- `claim_ids`: All linked Claim IDs
- `decision_thread_ids`: Linked Decision Thread IDs
- `impasse_ids`: Linked Impasse IDs
- `related_thought_line_ids`: Related Thought Lines
- `parent_thought_line_id`: Parent TL if this is a child
- `child_thought_line_ids`: Child TLs if this is a parent
- `first_seen_at`: Timestamp of earliest evidence
- `last_seen_at`: Timestamp of most recent evidence
- `created_at`: When the TL was registered
- `updated_at`: Last modification
- `created_by`: Agent or user who created it
- `origin_source_fragment_ids`: Fragments that triggered the TL
- `origin_claim_ids`: Claims that triggered the TL
- `active_claim_ids`: Currently active/supported claims
- `contested_claim_ids`: Claims under dispute
- `superseded_claim_ids`: Claims replaced by newer ones
- `open_question_claim_ids`: Unresolved questions
- `current_best_synthesis_id`: ID of synthesis (if authorized)
- `current_best_status`: Status of synthesis authorization
- `synthesis_allowed`: Whether synthesis is authorized
- `confidence_level`: Overall confidence in the thread
- `authority_hint`: Expected authority level
- `maturity_hint`: Expected maturity level
- `contradiction_status`: State of internal conflict
- `supersession_status`: Temporal validity state
- `merge_status`: Integration state
- `sensitivity_level`: Privacy/security flag
- `tags`: Thematic tags
- `human_summary`: Human-readable summary for navigation
- `agent_summary`: AI-readable summary for routing
- `review_notes`: Notes from review sessions
- `next_review_gate`: Gate that should trigger next review
- `notes`: Operational notes

## 5. Controlled Vocabularies

### 5.1 `thought_line_type`
`architecture`, `doctrine`, `workflow`, `source_strategy`, `tooling`, `pipeline`, `agent_system`, `memory_system`, `automation`, `project`, `ontology`, `symbolic_system`, `civilizational_project`, `personal_system`, `research_thread`, `open_question_cluster`, `unknown`

### 5.2 `domain`
`YOS`, `KAP`, `KOSMOS`, `CasaTAO`, `ELYSIUM`, `YOUniverse`, `Obsidian`, `Notion`, `Manus`, `ChatGPT`, `Git`, `Automation`, `Memory`, `Agents`, `Source_Acquisition`, `Synthesis`, `Unknown`

### 5.3 `status`
`candidate`, `seeded`, `active`, `under_review`, `merged`, `split`, `superseded`, `deprecated`, `archived`, `requires_review`

### 5.4 `maturity_level`
`seed`, `exploratory`, `emerging_pattern`, `candidate_architecture`, `validated_architecture`, `active_doctrine`, `implementation_supported`, `canonical_candidate`, `canonical`, `deprecated`, `unknown`

### 5.5 `canonical_status`
`not_canonical`, `candidate_evidence`, `active_control_plane`, `historical_source`, `implementation_evidence`, `superseded_source`, `requires_review`
*(Note: `active_control_plane` may only be used when the Thought Line is explicitly validated by gate or decision. Most Thought Lines begin as `candidate_evidence` or `requires_review`.)*

### 5.6 `review_status`
`unreviewed`, `metadata_reviewed`, `content_reviewed`, `claim_links_reviewed`, `decision_links_reviewed`, `approved_for_decision_threading`, `approved_for_synthesis_consideration`, `needs_human_review`, `blocked`

### 5.7 `current_best_status`
`not_allowed_yet`, `not_started`, `draft_candidate`, `review_required`, `validated`, `superseded`, `blocked`
*(Default for this gate: `not_allowed_yet` — synthesis is not authorized.)*

### 5.8 `synthesis_allowed`
`false`, `requires_current_best_gate`, `true_after_gate`
*(Default for this gate: `false`)*

### 5.9 `contradiction_status`
`none_known`, `contains_contested_claims`, `contains_contradicting_claims`, `contains_superseded_claims`, `contains_unreviewed_claims`, `needs_contradiction_review`

### 5.10 `supersession_status`
`unknown`, `active`, `historical`, `partially_superseded`, `superseded`, `supersedes_other`, `needs_supersession_review`

### 5.11 `merge_status`
`not_merged`, `candidate_for_merge`, `merged_into_parent`, `split_into_children`, `merge_blocked`, `requires_review`

### 5.12 `confidence_level`
`high`, `medium`, `low`, `unknown`

### 5.13 `authority_hint`
`user_directive`, `guardian_architect_decision`, `manus_execution_report`, `git_commit_evidence`, `source_document`, `implementation_evidence`, `memory_hint`, `external_reference`, `unknown`

### 5.14 `sensitivity_level`
`public`, `internal`, `private`, `sensitive`, `secret_reference_only`, `unknown`

## 6. Relationship Model

### 6.1 Thought Line ↔ Source Fragment
**Cardinality:** N:N
**Rules:**
1. One Thought Line may contain many Source Fragments.
2. One Source Fragment may belong to multiple Thought Lines.
3. Source Fragments are evidence, not conclusions.
4. Thought Lines must never overwrite Source Fragments.
5. Source chronology must be preserved.

### 6.2 Thought Line ↔ Claim
**Cardinality:** N:N
**Rules:**
1. One Thought Line may contain many Claims.
2. One Claim may belong to multiple Thought Lines.
3. A Thought Line may contain supported, contested, rejected, or superseded Claims.
4. A Thought Line must preserve contradiction state.
5. A Thought Line must not automatically validate its Claims.

### 6.3 Thought Line ↔ Thought Line
Thought Lines may relate by:
`parent_of`, `child_of`, `sibling_of`, `overlaps_with`, `depends_on`, `supports`, `contradicts`, `refines`, `supersedes`, `superseded_by`, `merged_into`, `split_from`, `needs_review_against`

### 6.4 Thought Line ↔ Decision Thread
A Thought Line may provide context for decisions.
**Allowed statuses:** `candidate_decision_context`, `candidate_decision_evidence`, `candidate_decision_rationale`, `candidate_rejected_option_cluster`, `candidate_supersession_context`

### 6.5 Thought Line ↔ Impasse
A Thought Line may contain recurring dead ends or failed approaches.
**Allowed statuses:** `contains_candidate_impasse`, `contains_validated_impasse`

### 6.6 Thought Line ↔ Current Best Knowledge
A Thought Line may later produce current-best synthesis, but this gate must not generate it.
**Allowed status for now:** `current_best_not_allowed_yet`

## 7. Lifecycle

1. `candidate_detected`
2. `seeded`
3. `source_linked`
4. `claim_linked`
5. `reviewed`
6. `contradiction_mapped`
7. `decision_context_linked`
8. `synthesis_candidate`
9. `current_best_ready`
10. `active_or_superseded_or_archived`

**Rules:**
1. Thought Lines begin as candidates or seeds.
2. Thought Lines do not become canonical automatically.
3. Thought Lines can remain useful even if superseded.
4. Thought Lines must preserve source provenance.
5. Thought Lines must preserve Claim status diversity.
6. Thought Lines must preserve contradiction state.
7. Thought Lines must never erase Claims or Source Fragments.
8. Later Thought Lines are not automatically more correct.
9. Merging Thought Lines must preserve old IDs and redirection history.
10. Splitting Thought Lines must preserve parent/child lineage.

## 8. Boundary Policy

A good Thought Line should be:
- thematic
- evolving
- reviewable
- linkable to Claims
- linkable to Source Fragments
- not too broad
- not too narrow
- not a simple tag
- not a one-off note
- useful for human navigation
- useful for AI routing

**Bad Thought Line examples:**
- AI
- Notes
- Important
- Ideas
- Misc
- Architecture
- Tools

**Good Thought Line examples:**
- YOS Control Plane Architecture
- Architecture Before Absorption Doctrine
- Git/Markdown Durable Authority
- Source Fragment and Claim Provenance Model
- Manus as High-Value Selective Execution Corpus
- Obsidian Markdown Metadata Pipeline
- Notion Controlled Pipeline Governance
- Current Best Knowledge Gating
- Agent Role Governance

## 9. Merge/Split Policy

**Merge:** When two Thought Lines are found to be substantially overlapping:
1. Create a new parent TL or designate one as parent.
2. Mark the absorbed TL `merge_status: merged_into_parent`.
3. Preserve the old TL ID and add a redirect note.
4. Transfer all Claim and Fragment links to the parent.
5. Do not delete the absorbed TL.

**Split:** When a Thought Line becomes too broad:
1. Create two or more child TLs.
2. Mark the parent `merge_status: split_into_children`.
3. Assign Claims and Fragments to appropriate children.
4. Preserve the parent TL for lineage tracking.

## 10. Contradiction Handling

When a Thought Line contains contradicting Claims:
1. Set `contradiction_status: contains_contradicting_claims`.
2. Populate `contested_claim_ids` with the conflicting Claim IDs.
3. Do not resolve automatically.
4. Flag for human review with `review_status: needs_human_review`.
5. Elevate to a Decision Thread if resolution is required.

## 11. Supersession Handling

When a Thought Line is officially replaced:
1. Mark the old TL `supersession_status: superseded`.
2. Mark the new TL `supersession_status: supersedes_other`.
3. Link them via `supersedes` / `superseded_by` in `related_thought_line_ids`.
4. Retain the old TL for historical context.

## 12. Human Navigation Implications

Thought Lines are the primary navigation layer for human review. They allow the Guardian Architect or user to navigate the knowledge base by theme rather than by source. `human_summary` must be written in plain language.

## 13. AI Retrieval / Routing Implications

AI agents will query Thought Lines by `thought_line_type`, `domain`, `canonical_status`, and `maturity_level` to route queries to the right thematic cluster. `agent_summary` must be structured for semantic search. Agents must respect `synthesis_allowed: false` and not generate synthesis from Thought Lines at this stage.

## 14. Examples

See `THOUGHT-LINE-EXAMPLES.md`.

## 15. Validation Rules

- `thought_line_id` must follow pattern `TL-YYYYMMDD-XXXX`.
- `title` must be descriptive, not a single generic word.
- If `contradiction_status` is `contains_contradicting_claims`, `contested_claim_ids` must not be empty.
- `synthesis_allowed` must be `false` until a CURRENT-BEST-KNOWLEDGE-GATE authorizes it.
- `current_best_status` must be `not_allowed_yet` until synthesis is authorized.

## 16. Open Questions

- At what scale should Thought Line seeding be automated vs. human-curated?
- How to handle Thought Lines that span both `scope:yos` and `scope:youniverse`?
- Should Thought Lines have a maximum Claim count before mandatory split?
