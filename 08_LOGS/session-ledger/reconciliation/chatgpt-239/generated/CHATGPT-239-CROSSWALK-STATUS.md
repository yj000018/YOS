---
document_id: CHATGPT-239-CROSSWALK-STATUS-v1.1
document_type: reconciliation_checkpoint
status: complete_with_two_ledger_absences
created_at: 2026-07-30
updated_at: 2026-07-30
authority: verified_git_and_library_evidence
canon_promotions: 0
---

# ChatGPT 239 → YOS account-ledger crosswalk status

## Executive result

The requested crosswalk is complete at classification level.

- Frozen curated registry: **239 rows**.
- Committed ChatGPT account ledger: **3,060 unique conversations** at `data/master_ledger.csv`.
- Previously known UUIDs: **236**.
- Exact UUID matches in ledger: **234**.
- Blank UUIDs deterministically recovered: **3/3**.
- Curated conversations present in ledger: **237/239**.
- Curated conversations with known UUID but absent from ledger: **2/239**.
- Duplicate ledger UUIDs: **0**.
- FUSION 2 UUID: **resolved**.
- Canon promotions: **0**.

The legacy file `08_LOGS/session-ledger/data/master_ledger.csv` is a distinct 537-row Manus ledger and remains separate.

## Correct ledger locations

| Ledger | Path | Rows | Source |
|---|---|---:|---|
| ChatGPT account ledger | `data/master_ledger.csv` | 3,060 | ChatGPT |
| Legacy Manus ledger | `08_LOGS/session-ledger/data/master_ledger.csv` | 537 | Manus |

The earlier blocked diagnosis resulted from inspecting the Manus path while expecting ChatGPT rows. Commit comparison proves that `ac472da1864f338c9ac36209ed02becd1d96d4f5` added the 3,060-row ledger at the root `data/` path.

## Three recovered UUIDs

| Title | Recovered UUID | Method | Confidence |
|---|---|---|---:|
| `--GARDEN--` | `6a5aa6e9-2828-83eb-b29b-33f1f40f985a` | unique exact title + creation timestamp | 0.995 |
| `Animation vidéo Street View` | `6a40e4ba-1ef8-83eb-a2ae-180707ac95e8` | unique exact title + creation + update timestamps | 1.000 |
| `Design logo Y` | `6a42b14d-d0b8-83ed-9fc6-0d9c1bbe9c81` | unique exact title + creation + update timestamps | 1.000 |

`--GARDEN--` has a later ledger update timestamp because the conversation continued after the frozen raw export; the title and creation timestamp identify one unique ledger row.

## Two known UUIDs absent from the 3,060 ledger

| Curated row | Title | Native UUID | Ledger analysis | Status |
|---:|---|---|---|---|
| 12 | `Continuity Handoff Watch` | `6a5de61f-9594-83eb-912e-979547fd8a49` | one same-title row exists under another UUID, but timestamps do not match | curated UUID preserved; ledger absence verified |
| 42 | `Gouvernance Créative Mondes` | `6a58ecce-0f74-83ed-a0d4-c023be2bc8c5` | no same-title ledger row | curated UUID preserved; ledger absence verified |

These are not unknown identities: their native UUIDs were already preserved from source URLs. They are classified as `known_native_conversation_absent_from_account_ledger`. No alternate UUID is substituted automatically.

## FUSION lineage

| Node | Native UUID | Ledger title | Status |
|---|---|---|---|
| FUSION lineage predecessor | `6a5de467-6844-83eb-9a4f-849597c24605` | `☯️☯️☯️ FUSION2 2 ☯️☯️☯️` | verified |
| FUSION 1 | `6a62566a-9b14-83eb-90a9-83c700b9f331` | `🔀 FUSION 1 🔀` | verified |
| FUSION 2 | `6a6a769b-539c-83eb-83ea-834c83691bdb` | `🔀 FUSION 2 🔀` | verified unique exact title in ledger |

## Durable evidence

- Identity source: `source/identity.rows.00.jsonl` … `identity.rows.05.jsonl`.
- Identity source SHA-256: `aeb05f4aad05e039b14c694de893baa1b0a58fa8d279d5bc3d0462678e256b7c`.
- Ledger SHA-256: `51417563521ecd21a19b444264353e6461b29413d68da3d2157f86cdbfaab4c0`.
- Crosswalk CSV: `generated/CHATGPT-239-TO-YOS-LEDGER-CROSSWALK.csv`.
- Validation JSON: `generated/CHATGPT-239-CROSSWALK-VALIDATION.json`.
- Known-absence analysis: `generated/CHATGPT-KNOWN-UUID-ABSENCE-ANALYSIS.json`.

## Exact next point

1. Preserve the two ledger absences as explicit exceptions rather than forcing a match.
2. Merge the reviewed crosswalk branch.
3. Attach the recovered three UUIDs and FUSION 2 UUID to the durable R1/R2 registries.
4. Use the 239 curated classifications as an overlay on the 3,060 native ledger; do not overwrite them.
5. Begin project/domain synthesis only after quality grading and source-content coverage checks.
6. Keep every automated crosswalk row non-Canon until review.
