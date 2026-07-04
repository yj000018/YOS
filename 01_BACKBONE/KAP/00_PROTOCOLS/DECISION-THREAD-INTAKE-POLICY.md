# Decision Thread Intake Policy

> Y-OS / KAP Cognitive Architecture
> Gate: DECISION-THREAD-MODEL-GATE
> Status: ACTIVE

---

## Purpose

This policy defines what can and cannot become a Decision Thread, how Decision Threads are registered, and how edge cases (duplicates, conflicts, supersession, sensitivity) are handled.

---

## Rule 1 — What Can Become a Decision Thread

A Decision Thread may be created when:
1. A clear, bounded decision can be stated in one sentence.
2. The decision has a traceable source (gate report, MPM, session capture, commit, user directive).
3. The decision has at least one of: rationale, alternative, or evidence link.
4. The decision is relevant to YOS/KAP architecture, workflow, tooling, source policy, or governance.

---

## Rule 2 — What Cannot Become a Decision Thread Yet

A Decision Thread must NOT be created when:
1. The "decision" is a vague theme (e.g., "AI strategy", "use better tools").
2. The source is unavailable, unverified, or only from memory without corroboration.
3. The decision would require reconstructing large corpora (pending pipeline gates).
4. The decision is actually a Claim, Thought Line, or Source Fragment.
5. The decision is a current-best synthesis (blocked until synthesis gates pass).

---

## Rule 3 — Metadata-Only Registration

When a decision is known but full rationale/alternatives are not yet available:
1. Register the DT with `decision_status: decision_candidate`.
2. Set `review_status: metadata_reviewed`.
3. Set `canonical_status: candidate_evidence`.
4. Populate only: `decision_thread_id`, `title`, `decision_text`, `decision_type`, `domain`, `created_at`, `notes`.
5. Flag `review_required: true`.

---

## Rule 4 — Claim-Supported Seeding

When a Decision Thread is supported by existing Claims:
1. Populate `claim_ids` with verified Claim IDs from CLAIM-REGISTRY.md.
2. Do not create new Claims during DT intake.
3. Do not validate Claims through DT intake.
4. Mark `review_status: content_reviewed` only after Claim links are verified.

---

## Rule 5 — Review Requirements

Before a Decision Thread may be marked `canonical_status: active_control_plane`:
1. `decision_status` must be `accepted_decision` or `active_decision`.
2. `current_validity` must be `active` or `active_with_conditions`.
3. `review_status` must be `approved_for_active_control_plane`.
4. At least one source link must exist (`source_fragment_ids`, `claim_ids`, `gate_evidence_ids`, or `commit_ids`).
5. Guardian Architect validation or gate validation must be documented in `validated_by`.

---

## Rule 6 — Unclear Decision Authority

When the authority for a decision is unclear:
1. Set `authority_hint: unknown`.
2. Set `canonical_status: requires_review`.
3. Flag `review_required: true`.
4. Add a note in `review_notes` describing the ambiguity.
5. Do not mark `active_control_plane` without explicit validation.

---

## Rule 7 — Duplicate Decisions

When a potential duplicate is detected:
1. Check DECISION-THREAD-REGISTRY.md for existing entries.
2. If a duplicate exists: link via `related_decision_thread_ids` with relationship `duplicates` or `partially_duplicates`.
3. Do not delete either entry.
4. Flag both for human review with `review_required: true`.
5. Resolution (merge or keep separate) requires Guardian Architect or gate decision.

---

## Rule 8 — Conflicting Decisions

When two Decision Threads conflict:
1. Set `contradiction_status: contradicted_by_decision` on both.
2. Link via `contradicts` field.
3. Flag both with `review_required: true`.
4. Do not automatically resolve the conflict.
5. Resolution requires explicit Guardian Architect or gate decision.

---

## Rule 9 — Supersession

When a new decision supersedes an old one:
1. Set `supersession_status: superseded` on the old DT.
2. Set `superseded_by` on the old DT pointing to the new DT ID.
3. Set `supersession_status: supersedes_other` on the new DT.
4. Set `supersedes` on the new DT pointing to the old DT ID.
5. Preserve the old DT — never delete it.
6. If supersession is ambiguous, mark `needs_supersession_review` on both.

---

## Rule 10 — Rejected Options

When a decision was made with alternatives:
1. Populate `rejected_options` with each rejected option and its reason.
2. Populate `alternative_options` with options considered but not formally rejected.
3. Never delete rejected options, even if the decision is later superseded.
4. Rejected options are part of the historical record.

---

## Rule 11 — Sensitive Material

When a Decision Thread references sensitive material:
1. Set `sensitivity_level` appropriately (`internal`, `private`, `sensitive`, `secret_reference_only`).
2. Do not store secrets in the Decision Thread body.
3. Use `secret_reference_only` to indicate that a secret exists but is stored elsewhere.
4. Sensitive Decision Threads must not be published to public repos without review.

---

## Rule 12 — Preventing Premature Synthesis

1. `current_best_status` is not a field on Decision Threads — synthesis is handled at a higher layer.
2. Decision Threads must not be used to generate current-best knowledge directly.
3. Decision Threads may be marked `merge_status: eligible_for_synthesis` only after all model gates pass.
4. Any synthesis must go through the SYNTHESIS-GATE process.
