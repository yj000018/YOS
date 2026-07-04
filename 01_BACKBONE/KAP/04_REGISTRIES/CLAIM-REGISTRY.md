# Claim Registry

> Y-OS / KAP Cognitive Architecture
> Gate: CLAIM-MODEL-GATE
> Status: SKELETON — seeded with control-plane axioms only
> Last updated: 2026-07-03

---

## Purpose

This registry tracks all Claims extracted from Source Fragments in the YOS/KAP cognitive architecture. Claims here are not canonical truth — they are candidate statements awaiting review, linking, and eventual synthesis.

---

## Registry Table

| Claim ID | Claim Text | Type | Truth Status | Review Status | Source Fragments | Candidate Thought Lines | Candidate Decisions | Confidence | Notes |
|---|---|---|---|---|---|---|---|---|---|
| CLAIM-20260703-YOS1 | YOS is the global cognitive operating system that contains KAP as a module/process. | architecture_principle | supported | content_reviewed | SF-005, SF-007 | TL-YOS-ARCHITECTURE | — | high | Explicitly stated in CANONICAL-DOCTRINE-REGISTRY and ARCHITECTURE-BEFORE-ABSORPTION |
| CLAIM-20260703-YOS2 | Git/Markdown is the durable authority for YOS/KAP strategic doctrine. | architecture_principle | validated | approved_for_thought_line_linking | SF-005, SF-006, SF-007 | TL-YOS-ARCHITECTURE | DT-GIT-AUTHORITY | high | Doctrine YOS-011 — explicitly validated by Guardian Architect |
| CLAIM-20260703-YOS3 | Architecture cognitive avant absorption massive is the core operational doctrine for KAP. | architecture_principle | validated | approved_for_thought_line_linking | SF-001, SF-002, SF-005 | TL-KAP-METHODOLOGY | DT-ARCHITECTURE-FIRST | high | Doctrine YOS-001 — validated across multiple sessions |
| CLAIM-20260703-YOS4 | A Source Fragment is not a Claim. | definition | validated | content_reviewed | SF-007 | TL-KAP-METHODOLOGY | — | high | Defined in SOURCE-FRAGMENT-MODEL.md and CLAIM-MODEL.md |
| CLAIM-20260703-YOS5 | A Claim must link back to one or more Source Fragments unless it is a control-plane axiom. | constraint | validated | content_reviewed | SF-007 | TL-KAP-METHODOLOGY | — | high | Defined in CLAIM-MODEL.md §6.1 |
| CLAIM-20260703-YOS6 | Source Staging is not canonical truth until reviewed and linked. | constraint | supported | metadata_reviewed | SF-005 | TL-KAP-METHODOLOGY | — | high | Doctrine YOS-008 |
| CLAIM-20260703-YOS7 | Obsidian is a consultation/navigation layer only — not the durable authority. | architecture_principle | supported | metadata_reviewed | SF-001, SF-002 | TL-YOS-ARCHITECTURE | — | high | Doctrine YOS-012 |
| CLAIM-20260703-YOS8 | Mem0 is the cross-session semantic memory layer — not a primary source corpus. | definition | supported | metadata_reviewed | SF-001 | TL-YOS-ARCHITECTURE | — | high | Doctrine YOS-013 |

---

## Notes

- All claims seeded here are derived from Source Fragments already committed to `yj000018/yos-cognitive-os` or `yj000018/KAP`.
- `SF-001` = CURRENT-CHATGPT-YOS-KAP-SESSION-CAPTURE.md
- `SF-002` = YOS-KAP-SESSION-CAPTURE-PACK-Control-Plane-Bootstrap-2026-07-02.md
- `SF-005` = CANONICAL-DOCTRINE-REGISTRY.md
- `SF-006` = ACTIVE-DECISION-LOG.md
- `SF-007` = SOURCE-FRAGMENT-MODEL.md
- Real-scale claim extraction from Notion, Obsidian, ChatGPT, and GitHub corpora is pending pipeline gates.
