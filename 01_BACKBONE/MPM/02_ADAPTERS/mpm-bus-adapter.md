# MPM BUS Adapter

**Version:** 1.0.0
**Status:** active
**Created by:** MPM-20260705-YOS-BUS-MPM-FUSION-AND-DIRECT-RUNTIME-GATE

---

## Purpose

Defines how Manus `MP` command resolves input via the YOS BUS transport layer. BUS is the preferred fast transport; MPM/04_QUEUE/ready is the canonical Git fallback.

---

## MP Command Resolution Order

```
1. If YOS_BUS_RUNTIME_ROOT exists:
   read $YOS_BUS_RUNTIME_ROOT/inbox/mpm/

2. If exactly one valid MPM packet exists:
   claim it by moving to $YOS_BUS_RUNTIME_ROOT/workspace/mpm/
   materialize/record it into MPM execution context
   execute it

3. Else fallback to:
   01_BACKBONE/MPM/04_QUEUE/ready/*.md

4. Else fallback to Git BUS domain:
   01_BACKBONE/BUS/04_DOMAINS/mpm/inbox/

5. If none: report no ready MP.
6. If multiple or risk_flags not empty: show micro-menu/manual selection.
```

---

## Important Constraints

```
No broad repository search.
No legacy kap-control-plane runtime unless explicit fallback override.
No source corpus scan.
```

---

## Auto-Run Eligibility

Auto-run (no micro-menu) requires ALL of:
- Exactly one ready MP packet found.
- `risk_flags` is empty.
- `auto_run_eligible: true` in packet metadata.

If any condition fails: show micro-menu.

---

## MPR Fast Path (Preserved)

ChatGPT A&G always reads MPR via:

```
1. 01_BACKBONE/MPM/06_REPORTS/indexes/latest-mpr.json
2. latest_mpr_path field
3. Read the MPR file
4. A&G review
```

This fast path is NOT affected by BUS integration.

---

## BUS Tool Integration

Use `bus.py` to inspect BUS inbox before MP execution:

```bash
python 01_BACKBONE/BUS/08_TOOLS/bus.py inbox --domain mpm
python 01_BACKBONE/BUS/08_TOOLS/bus.py claim --domain mpm --dry-run
```

---

## Relationship to Other Adapters

| Adapter | Role |
|---|---|
| `mpm-manus-adapter.md` | Core Manus execution adapter |
| `mpm-bus-adapter.md` | BUS transport layer adapter (this file) |
| `mpm-generic-llm-adapter.md` | Generic LLM adapter |

BUS adapter defines input resolution order. Manus adapter defines execution behavior.
