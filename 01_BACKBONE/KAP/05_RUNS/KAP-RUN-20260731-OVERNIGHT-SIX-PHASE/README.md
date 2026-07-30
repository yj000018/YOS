---
document_id: KAP-RUN-20260731-OVERNIGHT-SIX-PHASE
document_type: kap_run
status: active
authority: non_canonical_evidence_run
created_at: 2026-07-31
projects: [Fusion, ChatGPT Corpus, Manus Corpus, KAP]
canon_promotions: 0
---

# YOS Overnight Six-Phase Run

This run executes the six ordered operations authorized by Yannick on 2026-07-31:

1. Attach the rich curated classifications of the frozen ChatGPT-239 cohort to the 3,060-row native ledger as a separate overlay.
2. Audit raw bodies, verbatim, Fact Sheets and summaries for all 3,060 ChatGPT ledger identities.
3. Discover the Manus identity universe from committed evidence and freeze the incomplete-content queue.
4. Recover missing Manus sessions by native `task_id`, preserving raw API JSON before derivative transcript Markdown.
5. Generate only summaries missing after successful raw recovery.
6. Re-audit every layer and emit a durable validation JSON and exact-resume checkpoint.

## Safety and authority

- Native ledgers are read-only inputs.
- Generated overlays never rewrite source identity or source history.
- No evidence is promoted to Canon.
- Raw recovery is checkpointed in batches.
- Summary provenance records the provider or the extractive fallback method.
- The final gate fails when raw or summary gaps remain, while retaining all completed evidence.

## Durable outputs

All outputs are written under `generated/`; the exact resumption artifact is written under `checkpoints/`.
