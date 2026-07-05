# BUS / MPM Bridge Protocol

**Version:** 1.0.0
**Status:** active

---

## Purpose

Defines the canonical bridge between the BUS transport layer and the MPM execution layer. BUS transports MPM packets; MPM executes them. This protocol ensures clean separation of concerns.

---

## Key Rule

```
BUS transports MPM packets.
MPM executes them.
MPM remains the canonical execution ledger/report owner.
```

---

## MPM as BUS Domain

MPM is registered as BUS domain `mpm`. The MPM BUS domain has a full inbox/workspace/outbox/archive structure at:

```
01_BACKBONE/BUS/04_DOMAINS/mpm/
├── inbox/      ← new MP packets awaiting claim
├── workspace/  ← claimed/active MP packets
├── outbox/     ← MPR pointers awaiting A&G consumption
└── archive/    ← completed MP packets
```

For fast transport, the runtime equivalent lives at:

```
$YOS_BUS_RUNTIME_ROOT/inbox/mpm/
$YOS_BUS_RUNTIME_ROOT/workspace/mpm/
$YOS_BUS_RUNTIME_ROOT/outbox/mpm/
$YOS_BUS_RUNTIME_ROOT/archive/mpm/
```

---

## MP Input Resolution Order

When Manus receives an `MP` command:

1. If `$YOS_BUS_RUNTIME_ROOT` is set: read `$YOS_BUS_RUNTIME_ROOT/inbox/mpm/`
2. If exactly one valid MPM packet exists: claim it (move to workspace/mpm/) and execute.
3. Else fallback to: `01_BACKBONE/MPM/04_QUEUE/ready/*.md`
4. Else fallback to Git BUS domain: `01_BACKBONE/BUS/04_DOMAINS/mpm/inbox/`
5. If none: report `no_ready_mp`.
6. If multiple or `risk_flags` non-empty: show micro-menu / manual selection.

---

## MPR Output Flow

After MP execution:

1. MPR written to: `01_BACKBONE/MPM/06_REPORTS/awaiting-review/`
2. MPR pointer written to: `$YOS_BUS_RUNTIME_ROOT/outbox/mpm/` (if runtime configured)
3. `latest-mpr.json` updated: `01_BACKBONE/MPM/06_REPORTS/indexes/latest-mpr.json`
4. MP moved to: `01_BACKBONE/MPM/04_QUEUE/executed/`
5. Ledger updated: `01_BACKBONE/MPM/05_LEDGER/mp-ledger.json`

---

## Canonical Paths That Must NOT Move

```
01_BACKBONE/MPM/06_REPORTS/          ← canonical MPR destination
01_BACKBONE/MPM/05_LEDGER/           ← canonical ledger
01_BACKBONE/MPM/04_QUEUE/            ← canonical Git fallback queue
01_BACKBONE/MPM/06_REPORTS/indexes/latest-mpr.json  ← A&G fast path
```

BUS does not replace or duplicate these paths. BUS adds a transport layer on top.

---

## A&G MPR Fast Path (Preserved)

ChatGPT A&G always reads MPR via:

```
1. 01_BACKBONE/MPM/06_REPORTS/indexes/latest-mpr.json
2. latest_mpr_path field
3. Read the MPR file
4. A&G review
```

This fast path is preserved and not affected by BUS integration.
