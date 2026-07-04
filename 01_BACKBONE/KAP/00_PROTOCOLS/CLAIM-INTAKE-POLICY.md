# Claim Intake Policy

> Y-OS / KAP Cognitive Architecture
> Gate: CLAIM-MODEL-GATE
> Status: ACTIVE

---

## 1. What can become a Claim

A Claim may be extracted when:
- A Source Fragment contains an explicit statement of fact, policy, principle, or intent.
- The statement is atomic — it expresses one idea.
- The statement can be linked to at least one Source Fragment ID.
- The statement is not already a verbatim copy of an existing Claim.

---

## 2. What cannot become a Claim yet

A statement must NOT be extracted as a Claim if:
- The source fragment has not been registered in the Source Fragment Registry.
- The source fragment is from a corpus not yet authorized for intake (e.g., Notion, Obsidian, ChatGPT export — pending pipeline gates).
- The statement is a synthesis of multiple ideas that cannot be decomposed.
- The statement is a question without a stated position.
- The statement requires secret or sensitive data to be stored.
- The source provenance is unknown and cannot be reconstructed.

---

## 3. Metadata-only claim registration

When a claim is detected but the source content is not yet fully available:
1. Register the claim with `review_status: metadata_reviewed`.
2. Set `truth_status: unverified`.
3. Set `canonical_status: requires_review`.
4. Mark `claim_boundary` as `metadata_only`.
5. Do not promote to any Thought Line or Decision Thread.

---

## 4. Content-based claim extraction

When the source content is fully available:
1. Extract the atomic statement.
2. Assign a `claim_id` in format `CLAIM-YYYYMMDD-XXXX`.
3. Link all supporting `source_fragment_ids`.
4. Set `review_status: content_reviewed` after human or agent review.
5. Set `truth_status` based on evidence.

---

## 5. Review requirements

Before a Claim may be promoted to `approved_for_thought_line_linking` or higher:
- At least one Source Fragment must be linked.
- `contradiction_status` must be assessed (not left empty).
- `truth_status` must be set (not `unknown`).
- A human or Guardian Architect review is required for `active_control_plane` status.

---

## 6. How to handle unclear source provenance

If the source of a Claim cannot be traced to a registered Source Fragment:
1. Set `canonical_status: requires_review`.
2. Set `authority_hint: unknown`.
3. Set `provenance_confidence: low`.
4. Add a note explaining the gap.
5. Do not promote the Claim until provenance is resolved.

---

## 7. How to handle duplicates

If a new Claim appears to duplicate an existing one:
1. Check for exact text match → mark as `duplicates` in `related_claim_ids`.
2. Check for near-duplicate → mark as `partially_duplicates`.
3. Keep both Claims; do not delete either.
4. Flag for human review with `review_status: needs_human_review`.
5. Resolution may result in one Claim being `superseded` by the other.

---

## 8. How to handle contradictions

If a new Claim contradicts an existing one:
1. Register the new Claim normally.
2. Link both Claims via `contradicts` / `needs_review_against`.
3. Update `contradiction_status` on both Claims.
4. Do not resolve the contradiction automatically.
5. Elevate to a Decision Thread if resolution is required.

---

## 9. How to handle sensitive material

Claims must never contain:
- API keys, passwords, or secrets.
- Personal identification information beyond what is necessary for provenance.
- Content marked `secret_reference_only` in the source fragment.

If sensitive material is detected:
1. Set `sensitivity_level: sensitive` or higher.
2. Redact the sensitive portion from `claim_text`.
3. Add a note explaining the redaction.

---

## 10. How to prevent premature synthesis

A Claim must not be used for synthesis until:
- `review_status` is `approved_for_synthesis_consideration`.
- `truth_status` is `supported` or `validated`.
- `contradiction_status` is resolved or explicitly acknowledged.
- No active `merge_blocked` flag is set.

Synthesis gates must verify these conditions before consuming Claims.
