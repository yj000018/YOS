# YOS Source of Truth

> **Version:** 1.0.0 | **Last updated:** 2026-07-05

---

## Primary Sources

| Domain | Source of Truth | Format | Location |
| :--- | :--- | :--- | :--- |
| yOS system architecture | This repo (`yj000018/YOS`) | Git | `main` branch |
| MPM runtime | `kap-control-plane` (bootstrap) → `01_BACKBONE/MPM/` | Git | migrating |
| KAP pipeline | `kap-control-plane` + `yos-cognitive-os` → `01_BACKBONE/KAP/` | Git | migrating |
| Knowledge base | `yos-vault/knowledge/Y-WORLD/` | Obsidian MD | `05_KNOWLEDGE_DOMAINS/Y-WORLD/` |
| Governance | `yos-governance/` | MD + JSON | `01_BACKBONE/GOVERNANCE/` |
| Execution ledger | `kap-control-plane/00_META/inter_llm_execution_ledger.json` | JSON | bootstrap |
| Agent skills | `yos-agents/manus/yos-skills/` | MDX | `02_AGENTS/skills/` |

## JSON-First Rule

```
JSON = canonical machine source
MD   = generated human-readable view

Never edit MD as source of truth.
Always update JSON first, then regenerate or patch MD.
```

## Bootstrap Repos (transitional)

| Repo | Role | Status |
| :--- | :--- | :--- |
| `kap-control-plane` | MPM runtime + KAP control plane | bootstrap — active |
| `yos-cognitive-os` | KAP architecture + schemas | bootstrap — active |
| `new-to-be-merged` | Artifact buffer | active |

These repos remain operational until migration to `YOS/01_BACKBONE/` is Guardian-approved.

---

*YOS Source of Truth v1.0.0 — 2026-07-05*
