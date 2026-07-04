# CLAIM-EXTRACTION-RUNBOOK

> Y-OS / KAP Cognitive Architecture
> Gate: PROCESS-DOCS-RUNBOOK-GATE
> Last Updated: 2026-07-03

## 1. Prerequisites for Extraction

Claim extraction is strictly controlled. It may only proceed when a Source Fragment has been formally registered with a canonical `SF-*` ID. Extracting claims directly from raw Source Objects or unverified corpora is strictly forbidden.

## 2. Extraction Methodology

Claims must be atomic, meaning they express a single, indivisible concept, decision, or fact. They must be extracted verbatim or faithfully paraphrased without adding external LLM knowledge or context not present in the Source Fragment.

Each extracted Claim must be explicitly linked to its parent Source Fragment using the `source_fragment_id` field. This ensures absolute traceability from Claim to Fragment to Object to Instance.

## 3. Required Fields

When creating a new Claim in `CLAIM-REGISTRY.md`, the following fields are mandatory:
- `claim_id`: Unique identifier (e.g., `C-001`).
- `claim_text`: The atomic statement.
- `source_fragment_id`: Canonical `SF-*` ID of the origin fragment.
- `truth_status`: Must be initialized as `supported` (evidence exists), `contradicted` (conflicts exist), or `superseded` (newer evidence exists).
- `extraction_confidence`: High, medium, or low based on the clarity of the source text.

## 4. Review and Stopping Conditions

Extraction must pause and trigger human or Guardian Architect review under specific conditions. If a newly extracted Claim directly contradicts an existing `validated` Claim, it must be flagged for review. If the Source Fragment is highly ambiguous or contains potentially sensitive information, extraction must halt.

Claims must not be promoted to `validated` status automatically. Validation requires explicit architectural approval during a Synthesis Gate.

## 5. Examples of Atomic Claims

**Good Claim:** "The canonical repository for YOS architecture is yj000018/yos-cognitive-os." (Atomic, verifiable, directly linked to a fragment).
**Bad Claim:** "YOS uses Git for architecture and Obsidian is just for reading because Notion is too slow." (Compound, contains multiple distinct concepts, mixes facts with subjective reasoning).
