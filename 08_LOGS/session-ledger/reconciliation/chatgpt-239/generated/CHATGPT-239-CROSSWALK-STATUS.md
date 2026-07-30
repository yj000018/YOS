---
document_id: CHATGPT-239-CROSSWALK-STATUS-v1.0
document_type: reconciliation_checkpoint
status: blocked_missing_durable_ledger
created_at: 2026-07-30
updated_at: 2026-07-30
authority: verified_git_and_library_evidence
canon_promotions: 0
---

# ChatGPT 239 → YOS ledger crosswalk status

## Executive result

The identity source is valid, but the requested crosswalk cannot yet be completed from durable evidence.

- Frozen curated registry: **239 rows**.
- Native UUIDs already known: **236 unique nonblank IDs**.
- Rows lacking UUID: **3**.
- Raw acquisition: **239 distinct conversations** across five immutable Library batches.
- Current Git ledger: **537 Manus rows, 0 ChatGPT rows**.
- Every Git-reachable ledger version: **one blob only**, still 537 Manus rows.
- Commit `ac472da1864f338c9ac36209ed02becd1d96d4f5` reports ingestion of 3,060 ChatGPT conversations, but it did **not** change the ledger blob.
- Therefore the 3,060-row ChatGPT ledger is an operationally attested output that was not durably committed.

No missing UUID or crosswalk relationship is fabricated.

## Frozen identity registry

| Metric | Result |
|---|---:|
| Curated rows | 239 |
| Known UUID rows | 236 |
| Unique known UUIDs | 236 |
| Blank UUID rows | 3 |
| Identity source | `source/identity.rows.00.jsonl` … `identity.rows.05.jsonl` |
| Concatenated source SHA-256 | `aeb05f4aad05e039b14c694de893baa1b0a58fa8d279d5bc3d0462678e256b7c` |

## Three missing UUIDs

| Title | Batch | Created | Updated | Evidence status |
|---|---|---|---|---|
| `--GARDEN--` | BATCH-01 | 2026-07-17T22:05:09.741Z | 2026-07-20T08:08:31.192Z | JSON-only source; no Markdown URL |
| `Animation vidéo Street View` | BATCH-02 | 2026-06-28T09:09:51.992Z | 2026-07-01T12:02:16.873Z | JSON-only source; no Markdown URL |
| `Design logo Y` | BATCH-02 | 2026-06-29T17:54:43.456Z | 2026-06-29T17:58:49.924Z | JSON-only source; no Markdown URL |

The acquisition manifests establish that Markdown exports preserve native ChatGPT URLs, while these three conversations exist only in the JSON exports. Their native UUIDs must therefore be extracted from the raw JSON objects if the AI Toolbox payload includes `conversation_id`, or reacquired from the live ChatGPT history. Title-only matching is not authorized as native identity.

### Authoritative raw packages

| Batch | Library file ID | SHA-256 | Relevant conversations |
|---|---|---|---|
| BATCH-01 JSON | `file_00000000dcf481f4a4afc317ed0a9c51` | `25cb25fccb82531c931442cdd777a8fd16543c41a0625aa31c4ce653bf5c76fb` | `--GARDEN--` |
| BATCH-02 JSON | `file_00000000192881f4ae8c63fde68e38e0` | `38d0f3382b9304c24f550473a7e9a4d4a414c42547d0d963c9e1080d9d5082d8` | `Animation vidéo Street View`; `Design logo Y` |

The current Library binary-materialization service returned an internal `NO_MICROSHARD` error during this pass. The ZIP identities and hashes are preserved; no re-export is required before retrying access.

## FUSION lineage

| Node | UUID | Status |
|---|---|---|
| ONE FUSION | `6a5de467-6844-83eb-9a4f-849597c24605` | verified from curated registry |
| FUSION 1 | `6a62566a-9b14-83eb-90a9-83c700b9f331` | verified from raw JSON and PAC |
| FUSION 2 | unresolved | current thread title known; native thread UUID not exposed in durable evidence |

FUSION 2 is outside the frozen 239 acquisition window. Its UUID requires the current ChatGPT thread URL/export metadata; it cannot be inferred from title or chronology.

## Ledger durability audit

`generated/CHATGPT-LEDGER-GIT-HISTORY-AUDIT.json` proves:

```yaml
reachable_blob_versions: 1
maximum_total_rows_in_any_git_blob: 537
maximum_chatgpt_rows_in_any_git_blob: 0
durable_3060_chatgpt_ledger_present: false
claim_commit_changed_ledger_blob: false
ledger_blob: 0ee92d8afd28400df062c5266c81ba9442999753
```

The 3,060 ingestion claim remains useful operational provenance, but it is not a durable ledger artifact.

## Exact resume point

1. Retry materialization of the two already-preserved JSON ZIPs; extract the three named JSON objects and read `conversation_id` or equivalent native ID.
2. Recover or regenerate the 3,060 ChatGPT ledger on the original Cloud Computer, then commit it as a new immutable source snapshot rather than overwriting the Manus ledger.
3. Rerun `build_crosswalk_v2.py`; require at least the 236 known UUIDs to appear before the gate can pass.
4. Capture the native URL or raw export of the active `FUSION 2` thread and append it as a post-239 lineage delta.
5. Preserve curated classifications from the 239 registry; use the larger ledger only for native identity and acquisition coverage.
6. Do not merge ChatGPT and Manus native IDs and do not promote any row to Canon automatically.
