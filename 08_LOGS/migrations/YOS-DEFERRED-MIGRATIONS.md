# YOS Deferred Migrations

> Generated: 2026-07-05 | Branch: `yos-monorepo-canonical-reorganization`
> These migrations were NOT executed in this gate. They are queued for the next gate.

---

## Deferred — Next Gate

| Path | Target | Files | Reason | Next Gate |
| :--- | :--- | :--- | :--- | :--- |
| `yos-vault/` | `05_KNOWLEDGE_DOMAINS/Y-WORLD/` | 281 | Large vault — deferred to avoid oversized commit | YOS-KNOWLEDGE-MIGRATION-GATE |
| `yos-agents/` | `02_AGENTS/` | 173 | Large — deferred | YOS-AGENTS-MIGRATION-GATE |
| `yos-apps/` | `06_APPS_PRODUCTS/` | 191 | Large — deferred | YOS-APPS-MIGRATION-GATE |
| `yos-automations/` | `03_AUTOMATIONS/` | 70 | Standard — deferred | YOS-AUTOMATIONS-MIGRATION-GATE |
| `yos-related/experiments/` | `06_APPS_PRODUCTS/prototypes/` | ~186 | Deferred with yos-apps | YOS-APPS-MIGRATION-GATE |
| KAP run history | `01_BACKBONE/KAP/05_RUNS/bootstrap-history/` | ~20 | Deferred — requires KAP gate | KAP-RUN-HISTORY-MIGRATION-GATE |

## Deferred — Requires A&G Decision

| Path | Issue | Required Decision |
| :--- | :--- | :--- |
| `yos-related/undecided/Y-Browser-Admin/` | Unknown classification | Classify as app, archive, or delete |
| `yos-related/undecided/YMap/` | Unknown classification | Classify as app, archive, or delete |

---

*Worker F — Lane F | Manus — 2026-07-05*
