# Contradiction & Supersession Registry

> Y-OS / KAP Cognitive Architecture
> Gate: CONTRADICTION-SUPERSESSION-POLICY-GATE
> Status: SKELETON — seeded with control-plane examples only

---

## Registry Table

| Relation ID | Relation Type | Source Object | Target Object | Contradiction Status | Supersession Status | Current Validity Effect | Evidence | Review Requirement | Resolution Status | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| REL-20260703-CS01 | supersession | DT-20260703-YOS4 (ZIP is transport only) | ZIP-as-primary-corpus pattern | not_applicable | supersedes_other | rejected | SF-005, SF-006 | none | resolved_by_guardian | Doctrine YOS-004. ZIP is transport only, never primary corpus. |
| REL-20260703-CS02 | supersession | DT-20260703-YOS3 (Architecture Before Absorption) | broad-acquisition-first workflow | not_applicable | supersedes_other | rejected | SF-001, SF-002, SF-005 | none | resolved_by_guardian | Doctrine YOS-003. Architecture must be validated before any broad acquisition. |
| REL-20260703-CS03 | supersession | DT-20260703-YOS2 (Git/Markdown durable authority) | chat-only doctrine persistence | not_applicable | supersedes_other | deprecated | SF-005, SF-006, SF-007 | none | resolved_by_guardian | Doctrine YOS-002. Git/Markdown is the durable canonical store. Chat sessions are ephemeral. |
| REL-20260703-CS04 | contradiction | CLAIM-20260703-YOS4 (Source Fragment ≠ Claim) | direct-claim-extraction-from-unregistered-source | confirmed | not_superseded | rejected | SF-005, SF-007 | none | resolved_by_gate | SOURCE-FRAGMENT-MODEL-GATE-REPORT commit ff199ef. Fragments must be registered before claims can be extracted. |

---

## Pending Contradictions / Supersessions

| Item | Status | Notes |
|---|---|---|
| Obsidian-as-canonical vs Obsidian-as-consultation | suspected | DT-20260703-YOS5 marks consultation-only. Historical Obsidian usage as primary store needs review. |
| Notion-as-canonical vs Notion-as-reference | suspected | DT-20260703-YOS6 marks Notion merge as gated. Prior ChatGPT2Notion pipeline deprecated. |
| KAP-as-standalone-repo vs KAP-as-YOS-module | superseded | DT-20260703-YOS1 supersedes initial KAP standalone conception. |
