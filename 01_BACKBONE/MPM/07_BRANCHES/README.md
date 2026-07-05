# 07_BRANCHES — Branch Runtime Registry

This folder contains the yOS MPM branch runtime registry and policy.

## Files

| File | Description |
| :--- | :--- |
| `active-branches.json` | **JSON source of truth** — canonical branch registry |
| `active-branches.md` | Generated view of `active-branches.json` |
| `BRANCH-RUNTIME-POLICY.md` | Canonical branch runtime resolution policy |

## Quick Reference

```
Default runtime:  yj000018/YOS @ main / 01_BACKBONE/MPM/
Explicit branch:  MP branch=<branch_name>
Legacy fallback:  kap-control-plane (never default)
```

See `BRANCH-RUNTIME-POLICY.md` for full resolution order.
