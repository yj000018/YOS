# Source Fragment Intake Policy

> Y-OS / KAP Cognitive Architecture
> Gate: SOURCE-FRAGMENT-MODEL-GATE
> Status: ACTIVE

---

## 1. What CAN be registered as a fragment

Any bounded, traceable unit of source material from a known `source_system` in the controlled vocabulary. The source must be:
- Identifiable (has a path, URL, or commit reference)
- Timestamped (at minimum `source_observed_at` is known)
- Bounded (clear start/end or a single document/file)

## 2. What CANNOT be registered yet

- Sources from systems not yet in the `source_system` vocabulary
- Fragments whose origin cannot be traced (no path, no timestamp, no agent)
- Secrets or credentials (never stored in any fragment field)
- Synthesized conclusions (these are Claims, not Fragments)
- Merged or deduplicated outputs (these are Syntheses, not Fragments)

## 3. Metadata-only intake

When full content is unavailable, a fragment may be registered with `content_boundary: metadata_only`. The fragment must include all required metadata fields. Content fields may be null. `review_status` must be `unreviewed`.

## 4. Content intake

Full content intake is authorized only when:
- The source system is in the controlled vocabulary
- The extraction pipeline has been validated (dry-run gate passed)
- The user or Guardian Architect has authorized the source for extraction

## 5. Review requirements

Every fragment must pass through at minimum `metadata_reviewed` before being used in claim extraction or decision threading. The Guardian Architect must approve `approved_for_claim_extraction` or `approved_for_decision_threading`.

## 6. How to handle missing timestamps

If `source_created_at` is unknown, use `source_observed_at` (the time KAP first saw the fragment). Never invent timestamps. Mark as `provenance_confidence: low` if timestamps are estimated.

## 7. How to handle unclear source origin

If the source system cannot be determined, set `source_system: Unknown` and `provenance_confidence: unknown`. Flag for human review with `review_status: needs_human_review`.

## 8. How to handle duplicates

Use `content_hash` to detect duplicates. If two fragments share the same hash, the second is marked `canonical_status: requires_review` and linked via `related_fragments`. Do not delete either. Do not merge automatically.

## 9. How to handle private/sensitive material

Set `sensitivity_level` appropriately. For `private` or `sensitive` fragments, `content_boundary` must be `metadata_only` until explicit authorization. For `secret_reference_only`, only a pointer (path/URL) may be stored — never the content.

## 10. How to prevent premature synthesis

Fragments must reach `synthesis_ready` lifecycle status before being used in synthesis. This requires:
1. `content_reviewed` review status
2. `approved_for_claim_extraction` or higher
3. Explicit Guardian Architect authorization for the synthesis gate

No fragment may be used to generate current-best knowledge until the CLAIM-MODEL-GATE and THOUGHT-LINE-SEEDING-GATE have passed.
