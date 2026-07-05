# BUS Domain: mpm

**Domain:** `mpm`
**Purpose:** Fast and/or durable transport of MPM packets, MPR pointers, execution requests, and status messages.
**Status:** active

---

## MPM BUS Flow

```
BUS inbox/mpm
-> BUS workspace/mpm
-> MPM execution runtime
-> MPM MPR/report/ledger/latest pointers
-> BUS outbox/mpm
-> BUS archive/mpm
```

---

## Critical Rule

```
BUS transports MPM packets.
MPM executes them.
MPM remains the canonical execution ledger/report owner.
```

Do not move canonical MPRs out of `01_BACKBONE/MPM/06_REPORTS/`.
Do not move canonical ledger out of `01_BACKBONE/MPM/05_LEDGER/`.
Do not remove `01_BACKBONE/MPM/04_QUEUE/`.

---

## MP Input Resolution Priority

```
1. BUS runtime inbox/mpm = preferred fast transport if $YOS_BUS_RUNTIME_ROOT configured.
2. MPM/04_QUEUE/ready = canonical Git fallback queue.
3. Git BUS domain inbox/mpm = durable fallback transport (this folder).
```

---

## Lifecycle Folders (Git-backed)

```
04_DOMAINS/mpm/
├── inbox/      ← new MP packets awaiting claim (Git fallback)
├── workspace/  ← claimed/active MP packets
├── outbox/     ← MPR pointers awaiting A&G consumption
└── archive/    ← completed MP packets
```

For fast transport, use `$YOS_BUS_RUNTIME_ROOT/{inbox,workspace,outbox,archive}/mpm/`.
