# KAP Module Map

> **Version:** 1.0.0 | **Last updated:** 2026-07-05

---

## Bootstrap Repos

| Repo | Role | Status |
| :--- | :--- | :--- |
| `yj000018/kap-control-plane` (private) | Control plane, MPM runtime, gate reports | active bootstrap |
| `yj000018/yos-cognitive-os` (public) | Architecture, schemas, registries | active bootstrap |

## Asset Migration Map

| Asset Type | Bootstrap Location | YOS Canonical Path | Status |
| :--- | :--- | :--- | :--- |
| Architecture protocols | `yos-cognitive-os/02_Architecture/Synthesis/*.md` | `01_BACKBONE/KAP/00_PROTOCOLS/` | copied |
| JSON schemas | `yos-cognitive-os/02_Architecture/Synthesis/_schemas/*.json` | `01_BACKBONE/KAP/01_SCHEMAS/` | copied |
| Registries | `yos-cognitive-os/05_Registries/*.md` | `01_BACKBONE/KAP/04_REGISTRIES/` | copied |
| Gate reports | `kap-control-plane/06_REPORTS/` | `01_BACKBONE/KAP/06_REPORTS/` | deferred |
| Source acquisition | `yos-cognitive-os/02_Source_Acquisition/` | `07_SOURCE_CORPUS/` | deferred |
| KAP MPM run history | `kap-control-plane/02_MPMs/executed/` | `01_BACKBONE/KAP/05_RUNS/bootstrap-history/` | deferred |

## Schemas Available

| Schema | File |
| :--- | :--- |
| Source Fragment | `source_fragment.schema.json` |
| Claim | `claim.schema.json` |
| Thought Line | `thought_line.schema.json` |
| Decision Thread | `decision_thread.schema.json` |
| Evolution Event | `evolution_event.schema.json` |
| Impasse | `impasse.schema.json` |
| Current Best Synthesis | `current_best_synthesis.schema.json` |

## Key Protocols Available

- `EVOLUTIONARY-KNOWLEDGE-MERGE-ARCHITECTURE.md`
- `DEDUPLICATION-AND-MERGE-POLICY.md`
- `HUMAN-AI-EXPLOITATION-MODEL.md`
- `SYNTHESIS-GATE-SEQUENCE.md`
- `CLAIM-MODEL.md` + `CLAIM-EXTRACTION-RUNBOOK.md`
- `THOUGHT-LINE-MODEL.md` + `THOUGHT-LINE-SEEDING-RUNBOOK.md`
- `DECISION-THREAD-MODEL.md` + `DECISION-THREAD-RECONSTRUCTION-RUNBOOK.md`
- `CONTRADICTION-SUPERSESSION-POLICY.md` + `CONTRADICTION-SUPERSESSION-RUNBOOK.md`
- `SOURCE-FRAGMENT-MODEL.md` + `SOURCE-INTAKE-RUNBOOK.md`

---

*KAP Module Map v1.0.0 — 2026-07-05*
