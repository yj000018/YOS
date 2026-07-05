# YOS Migration Index

> **Version:** 1.0.0 | **Last updated:** 2026-07-05
> Tracks all migrations from legacy structure to canonical topology.

---

## Active Migration: YOS-MONOREPO-CANONICAL-REORGANIZATION-GATE

| Gate | Branch | Status | Commit |
| :--- | :--- | :--- | :--- |
| YOS-MONOREPO-CANONICAL-REORGANIZATION | `yos-monorepo-canonical-reorganization` | in_progress | TBD |

---

## Migration Log

| Date | Action | From | To | Status |
| :--- | :--- | :--- | :--- | :--- |
| 2026-07-05 | scaffold | — | `01_BACKBONE/MPM/` | done |
| 2026-07-05 | scaffold | — | `01_BACKBONE/KAP/` | done |
| 2026-07-05 | copy | `kap-control-plane/02_MPMs/_runtime/` | `01_BACKBONE/MPM/00_PROTOCOLS/` + `01_SCHEMAS/` + `02_ADAPTERS/` + `03_TEMPLATES/` | done |
| 2026-07-05 | copy | `yos-governance/` | `01_BACKBONE/GOVERNANCE/` | done |
| 2026-07-05 | copy | `yos-agents/routing/` | `01_BACKBONE/ROUTING/` | done |
| 2026-07-05 | copy | `plugins/yos-reader/` | `04_INTERFACES/obsidian/yos-reader/` | done |

## Deferred Migrations

| Path | Reason | Next Action |
| :--- | :--- | :--- |
| `yos-related/undecided/` | Classification unclear (Y-Browser-Admin, YMap) | A&G decision required |
| `yos-related/legacy/` | Empty folder | Archive when ready |
| `archive/` | Only .gitkeep | Archive when ready |
| `yos-vault/` → `05_KNOWLEDGE_DOMAINS/Y-WORLD/` | Large vault (281 files) — copy safe but deferred | Next gate |
| `yos-agents/` → `02_AGENTS/` | Safe but large | Next gate |
| `yos-apps/` → `06_APPS_PRODUCTS/` | Safe but large | Next gate |
| `yos-automations/` → `03_AUTOMATIONS/` | Safe | Next gate |

---

*YOS Migration Index v1.0.0 — 2026-07-05*
