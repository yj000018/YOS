# yOS MPM — Active Branch Runtime Registry

> **SOURCE OF TRUTH:** `active-branches.json`
> **This MD is a generated view. Never edit directly. Update JSON first, then regenerate.**
> Version: 1.0.0 | Last updated: 2026-07-05

---

## Canonical Runtime

| Parameter | Value |
| :--- | :--- |
| **Canonical repo** | `yj000018/YOS` |
| **Default runtime branch** | `main` |
| **Runtime path** | `01_BACKBONE/MPM/` |
| **Queue path** | `01_BACKBONE/MPM/04_QUEUE/` |
| **Ledger** | `01_BACKBONE/MPM/05_LEDGER/mp-ledger.json` |
| **Reports** | `01_BACKBONE/MPM/06_REPORTS/` |

---

## Legacy Bootstrap

| Parameter | Value |
| :--- | :--- |
| **Repo** | `yj000018/kap-control-plane` |
| **Status** | `legacy_bootstrap_only` |
| **Default runtime** | NO |
| **Usage** | Fallback only if YOS runtime inaccessible |

---

## Test/Staging Branches

| Branch | Status | Allowed Commands |
| :--- | :--- | :--- |
| `yos-monorepo-canonical-reorganization` | `staging_validated_pending_merge` | `MP branch=yos-monorepo-canonical-reorganization` / `MP queue branch=yos-monorepo-canonical-reorganization` |

---

*Generated from `active-branches.json` v1.0.0 — 2026-07-05*
