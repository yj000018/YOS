# SOURCE-FRAGMENT-REGISTRY

> Y-OS / KAP — Level L3: Source Fragments
> **PATCHED:** SOURCE-FRAGMENT-ID-NORMALIZATION-PATCH 2026-07-03
> A **Source Fragment** is a bounded, traceable cognitive unit created from a Source Object after approved intake.
> **ID Format:** `SF-<CHANNELCODE>-<INSTANCESEQ>-<OBJECTSEQ>-<FRAGMENTSEQ>`
> Legacy IDs preserved as aliases. See crosswalk: `SOURCE-FRAGMENT-ID-CROSSWALK.md`
> Last Updated: 2026-07-03

---

## Four-Level Taxonomy

```
L0 Source Channel     (SOURCE-CHANNEL-REGISTRY.md)
  └── L1 Source Instance  (SOURCE-INSTANCE-REGISTRY.md)
        └── L2 Source Object  (SOURCE-OBJECT-REGISTRY.md)
              └── L3 Source Fragment  (this file)
```

---

## Fragment Registry

| Canonical Fragment ID | Legacy ID | Source Object ID | Source Instance ID | Channel | Source Type | Canonical Status | ID Normalization Status | Review Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| SF-GPT-002-0013-001 | FRAG-20260703-CP01 | SO-GPT-002-0013 | GPT-002 | CH-002 | session_capture_pack | active_control_plane | mapped_from_legacy | metadata_reviewed | CURRENT-CHATGPT-YOS-KAP-SESSION-CAPTURE. 10 doctrines, 8 decisions, 11 MPM stubs. |
| SF-GPT-001-0011-001 | FRAG-20260702-CP02 | SO-GPT-001-0011 | GPT-001 | CH-002 | session_capture_pack | active_control_plane | mapped_from_legacy | metadata_reviewed | YOS-KAP-SESSION-CAPTURE-PACK-Control-Plane-Bootstrap. 10 doctrines, 12 decisions, 5 MPM stubs. |
| SF-MAN-001-0016-001 | FRAG-20260703-GR01 | SO-MAN-001-0016 | MAN-001 | CH-003 | gate_report | active_control_plane | mapped_from_legacy | metadata_reviewed | YOS-CONTROL-PLANE-BOOTSTRAP-GATE-REPORT. Gate PASS. 55 files. |
| SF-MAN-001-0015-001 | FRAG-20260703-GR02 | SO-MAN-001-0015 | MAN-001 | CH-003 | gate_report | active_control_plane | mapped_from_legacy | metadata_reviewed | EVOLUTIONARY-KNOWLEDGE-MERGE-ARCHITECTURE-GATE-REPORT. Gate PASS. 4 registries. |
| SF-GIT-001-0018-001 | FRAG-20260703-AD01 | SO-GIT-001-0018 | GIT-001 | CH-001 | architecture_doc | active_control_plane | mapped_from_legacy | metadata_reviewed | ARCHITECTURE-BEFORE-ABSORPTION. Core doctrine document. |
| SF-GIT-001-0019-001 | FRAG-20260703-AD02 | SO-GIT-001-0019 | GIT-001 | CH-001 | architecture_doc | active_control_plane | mapped_from_legacy | metadata_reviewed | YOS-STRATEGIC-DOCTRINE. Strategic doctrine summary. |
| SF-GIT-001-0020-001 | FRAG-20260703-AD03 | SO-GIT-001-0020 | GIT-001 | CH-001 | architecture_doc | active_control_plane | mapped_from_legacy | metadata_reviewed | YOS-REPOSITORY-ARCHITECTURE-DECISION. Master repo + linked repos decision. |
| SF-GIT-001-0021-001 | FRAG-20260703-AD04 | SO-GIT-001-0021 | GIT-001 | CH-001 | architecture_doc | active_control_plane | mapped_from_legacy | content_reviewed | SOURCE-FRAGMENT-MODEL. Gate output. |
| SF-GIT-001-0022-001 | FRAG-20260703-AD05 | SO-GIT-001-0022 | GIT-001 | CH-001 | architecture_doc | active_control_plane | mapped_from_legacy | content_reviewed | SOURCE-FRAGMENT-INTAKE-POLICY. Gate output. |

---

## Registry Notes

- All 9 fragments above are mapped from legacy IDs. See `SOURCE-FRAGMENT-ID-CROSSWALK.md` for the full crosswalk.
- Legacy IDs (`FRAG-YYYYMMDD-XXXX`) are preserved as aliases and must not be deleted.
- Illustrative examples from `SOURCE-FRAGMENT-EXAMPLES.md` are NOT included here.
- Real source fragments from Notion, Obsidian, ChatGPT export, and other sources will be added when their respective pipeline gates pass.

---

## Next Available Fragment Sequence Numbers

| Source Object | Next SF Seq |
|---|---|
| SO-GPT-002-0013 | 002 |
| SO-GPT-001-0011 | 002 |
| SO-MAN-001-0016 | 002 |
| SO-MAN-001-0015 | 002 |
| SO-GIT-001-0018 through SO-GIT-001-0022 | 002 |
| All new SO-* | 001 |

---

## Pending Registrations

| Source | Gate Required | Status |
|---|---|---|
| Notion pages (1300+) | NOTION-METADATA-INVENTORY-GATE → NOTION-PIPELINE-CONTROLLED-EXECUTION-GATE | PENDING |
| Obsidian notes (9 vaults, ~4400+) | OBSIDIAN-MARKDOWN-METADATA-DRY-RUN-GATE | PENDING |
| ChatGPT parallel sessions | CAPTURE-PATCH-2 | PENDING |
| GitHub repos (36) | GITHUB-SOURCE-ACQUISITION-GATE | PENDING |
| Manus historical tasks (194) | MANUS-HISTORICAL-ACQUISITION-GATE | PENDING |
| Other LLM sessions | CAPTURE-PATCH-2 | BLOCKED |
| LLM Internal Knowledge | LLM-HEURISTIC-CONTEXT-USAGE-POLICY | HEURISTIC_ONLY |
