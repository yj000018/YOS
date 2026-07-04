# Thought Line Intake Policy

> Y-OS / KAP Cognitive Architecture
> Gate: THOUGHT-LINE-MODEL-GATE
> Status: ACTIVE

---

## 1. What can become a Thought Line

A Thought Line may be created when:
- A cluster of 2 or more Claims share a common theme that is not already covered by an existing Thought Line.
- A recurring pattern is observed across multiple Source Fragments from different sessions or sources.
- A Guardian Architect or gate explicitly designates a theme as a Thought Line.
- A control-plane axiom is broad enough to require thematic tracking over time.

---

## 2. What cannot become a Thought Line yet

A theme must NOT be registered as a Thought Line if:
- It is a single-occurrence observation with no expected recurrence.
- It is a simple tag or label without evolution potential.
- The source Claims or Fragments have not been registered.
- The theme is too broad to be bounded (e.g., "AI", "Architecture").
- The theme is too narrow to be thematic (e.g., a single implementation detail).
- The source corpus for this theme has not yet been acquired (pending pipeline gate).

---

## 3. Metadata-only Thought Line registration

When a theme is detected but Claims are not yet fully linked:
1. Register the TL with `status: candidate`.
2. Set `review_status: metadata_reviewed`.
3. Set `canonical_status: requires_review`.
4. Set `synthesis_allowed: false`.
5. Set `current_best_status: not_allowed_yet`.
6. Do not link to Decision Threads.

---

## 4. Claim-based Thought Line seeding

When Claims are available and linked:
1. Create the TL with `status: seeded`.
2. Populate `claim_ids` with all relevant Claim IDs.
3. Populate `source_fragment_ids` with supporting Fragment IDs.
4. Set `review_status: content_reviewed` after review.
5. Set `maturity_level` based on evidence density.

---

## 5. Review requirements

Before a Thought Line may be promoted to `approved_for_decision_threading` or higher:
- At least 2 Claims must be linked.
- `contradiction_status` must be assessed.
- `maturity_level` must be set (not `unknown`).
- A human or Guardian Architect review is required for `active_control_plane` status.

---

## 6. How to handle unclear scope

If the scope of a Thought Line cannot be clearly bounded:
1. Set `scope` to a descriptive note explaining the ambiguity.
2. Set `canonical_status: requires_review`.
3. Flag with `review_status: needs_human_review`.
4. Do not promote until scope is resolved.

---

## 7. How to handle duplicates

If a new Thought Line appears to duplicate an existing one:
1. Check for exact title match → mark as duplicate candidate.
2. Check for substantial overlap → mark as `merge_status: candidate_for_merge`.
3. Keep both until a merge decision is made.
4. Flag for human review.
5. Resolution may result in one TL being merged into the other.

---

## 8. How to handle overlaps

If two Thought Lines overlap substantially but are not duplicates:
1. Link them via `overlaps_with` in `related_thought_line_ids`.
2. Document the overlap in `notes`.
3. Do not merge automatically.
4. Elevate to a merge decision if overlap exceeds 70% of Claims.

---

## 9. How to handle merge/split

**Merge:**
1. Designate one TL as parent or create a new parent.
2. Mark absorbed TL `merge_status: merged_into_parent`.
3. Preserve old TL ID with redirect note.
4. Transfer all Claim and Fragment links.

**Split:**
1. Create 2+ child TLs.
2. Mark parent `merge_status: split_into_children`.
3. Assign Claims and Fragments to appropriate children.
4. Preserve parent TL for lineage.

---

## 10. How to handle sensitive material

Thought Lines must not expose:
- API keys, passwords, or secrets.
- Personal identification information beyond provenance.
- Content marked `secret_reference_only`.

If sensitive material is detected:
1. Set `sensitivity_level: sensitive` or higher.
2. Redact from `human_summary` and `agent_summary`.
3. Add a note explaining the redaction.

---

## 11. How to prevent premature synthesis

A Thought Line must not be used for synthesis until:
- `review_status` is `approved_for_synthesis_consideration`.
- `synthesis_allowed` is `true_after_gate`.
- `current_best_status` is `validated`.
- No active `merge_blocked` flag is set.
- A CURRENT-BEST-KNOWLEDGE-GATE has explicitly authorized it.

Until then, `synthesis_allowed: false` and `current_best_status: not_allowed_yet` are mandatory defaults.
