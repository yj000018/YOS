# Deduplication and Merge Policy

> Y-OS / KAP Cognitive Architecture
> Gate: DEDUPLICATION-AND-MERGE-POLICY-GATE
> Status: ACTIVE

---

## 1. Core Principle
Deduplication in the Y-OS knowledge architecture is **non-destructive**. We never delete a source fragment or claim simply because it looks similar to another. True deduplication only occurs at the synthesis layer, never at the evidence layer.

## 2. Source Fragment Deduplication
- **Exact Match (Hash):** If two files or fragments are byte-for-byte identical, only one is registered in the Source Fragment Registry. The other is recorded as an alternate location/provenance for the same fragment.
- **Semantic Match:** If two fragments say the same thing but use different words, BOTH are preserved. They are linked to the same Claim.

## 3. Claim Deduplication
- Claims are normalized statements. If two fragments support the exact same logical claim, they are linked to the same `claim_id`.
- If a new claim is proposed that is semantically identical to an existing claim, the new claim is discarded, and its source fragments are appended to the existing claim's `source_fragment_ids`.

## 4. Thought Line Merge Policy
When two Thought Lines are discovered to be exploring the exact same concept:
1. A new parent Thought Line is created, OR the more mature Thought Line is designated as the parent.
2. The absorbed Thought Line is marked `merge_status: merged_into_parent`.
3. All Claims and Source Fragments from the absorbed line are linked to the parent.
4. The absorbed Thought Line ID is preserved for historical linking and redirects. It is NEVER deleted.

## 5. Decision Thread Merge Policy
Decisions are rarely deduplicated, as context usually differs. If two identical decisions are found:
1. The earlier decision is usually kept as primary.
2. The later decision is marked `duplicates` and linked to the primary.
3. If the later decision adds new rationale, the rationale is merged into the primary decision, and the later decision is marked `merged_into`.

## 6. Synthesis Layer Deduplication
The Current Best Synthesis (CBS) is where true, destructive deduplication happens.
- Redundant claims are collapsed into single, concise statements.
- The CBS only presents the final synthesized view, hiding the redundant evidence trail (though links remain available).
