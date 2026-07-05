# yOS MPM — Branch Runtime Policy

> **System:** yOS MPM — Mega Prompt Manager
> **Version:** 1.0.0
> **Status:** canonical
> **Created:** 2026-07-05

---

## Core Doctrine

```
YOS = single canonical repo.
main = canonical active runtime branch.
YOS feature/test branches = staging/test runtimes.
01_BACKBONE/MPM/ = canonical MP/MPM/MPR machinery.
kap-control-plane = legacy/bootstrap only, never default runtime.
```

---

## MP Resolver — Runtime Resolution Order

```
1. If command includes branch=<branch_name>:
   → use yj000018/YOS @ <branch_name> / 01_BACKBONE/MPM/

2. Else (plain MP / MP queue / MP next):
   → use yj000018/YOS @ main / 01_BACKBONE/MPM/

3. Only if YOS runtime is inaccessible (network error, repo unavailable):
   → optionally inspect kap-control-plane as legacy/bootstrap fallback
   → log the fallback explicitly

4. Never use kap-control-plane as default runtime.
5. Never mix multiple runtimes silently.
```

---

## Supported Commands

| Command | Runtime resolved |
| :--- | :--- |
| `MP` | `yj000018/YOS @ main / 01_BACKBONE/MPM/` |
| `MP next` | `yj000018/YOS @ main / 01_BACKBONE/MPM/` |
| `MP queue` | `yj000018/YOS @ main / 01_BACKBONE/MPM/` |
| `MP branch=<name>` | `yj000018/YOS @ <name> / 01_BACKBONE/MPM/` |
| `MP queue branch=<name>` | `yj000018/YOS @ <name> / 01_BACKBONE/MPM/` |
| `MP run <mp_id>` | `yj000018/YOS @ main / 01_BACKBONE/MPM/` |
| `MP status` | Both ledgers (YOS main + kap-control-plane legacy) |

---

## Auto-Run Rule

For any resolved runtime:

```
IF exactly one MP has status ready_for_execution
AND risk_flags are empty or absent
AND canonical_mp_path exists
THEN auto-run without menu.
```

Micro-menu only if:
- multiple ready MPs
- no ready MP
- risk flags present
- missing packet path
- ambiguous runtime
- runtime inaccessible

---

## Branch Lifecycle

```
draft → staging/test branch → staging_validated_pending_merge → merged to main
```

Branches are registered in `active-branches.json`.

---

## Legacy Bootstrap Note

`kap-control-plane` was the bootstrap runtime before the YOS monorepo topology was established. It contains historical MPM executions and schemas. It is preserved for traceability but is never the default runtime.

---

*BRANCH-RUNTIME-POLICY.md — yOS MPM v1.0.0 — 2026-07-05*
