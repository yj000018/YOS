# BUS Canonical Doctrine

**Version:** 1.0.0
**Status:** active
**Source:** MPM-20260705-YOS-BUS-MPM-FUSION-AND-DIRECT-RUNTIME-GATE

---

## Core Definitions

| Module | Role |
|---|---|
| **BUS** | Universal transport, operational memory, and inter-agent exchange layer. |
| **MPM** | Specialized orchestration layer for Mega Prompts. A BUS domain/stream. |
| **KAP** | Knowledge Assimilation Pipeline. A BUS domain. |
| **Git** | Durable/auditable memory and versioning backend. Not the fast transport. |
| **Direct file runtime** | Preferred fast non-versioned transport backend. |

---

## Mandatory Principles

1. **BUS is universal.** All inter-agent transport, regardless of content type, flows through BUS.
2. **MPM is a BUS domain/stream, not a separate transport architecture.** MPM execution logic is internal to MPM; BUS handles transport only.
3. **GitHub/Git may be a backend, but Git is not required for fast handoff.** Git commits are too slow for real-time agent exchange.
4. **Direct file transport must support non-versioned message passing.** Files written to `$YOS_BUS_RUNTIME_ROOT` do not require a Git commit.
5. **All accepted/executed durable outputs eventually land in canonical YOS Git.** Ephemeral BUS messages may be temporary; final artifacts must be committed.
6. **Runtime messages may be temporary and non-versioned.** Not every BUS event needs a commit.
7. **Source of truth depends on lifecycle phase:**

| Phase | Source of Truth |
|---|---|
| Transport phase | Runtime BUS (direct_file, manus_cloud, etc.) |
| Execution phase | MPM / KAP / domain runtime |
| Durable phase | YOS Git canonical artifacts |

---

## Topology

```
yj000018/YOS @ main
└── 01_BACKBONE/
    ├── BUS/          ← universal transport layer
    ├── MPM/          ← mega prompt orchestration (BUS domain: mpm)
    ├── KAP/          ← knowledge assimilation (BUS domain: kap)
    ├── ART/
    ├── CRT/
    ├── MEMORY/
    ├── ROUTING/
    ├── GOVERNANCE/
    └── SECURITY/
```

---

## What BUS Is NOT

- BUS is not a task executor. It transports packets; execution is the responsibility of the target module (MPM, KAP, etc.).
- BUS is not a source corpus. It does not store knowledge content.
- BUS is not a replacement for MPM ledger or reports. MPM canonical paths remain in `01_BACKBONE/MPM/`.
- BUS is not GitHub Actions. Reflex architecture is defined but not yet activated.

---

## Versioning Policy

- BUS structure changes require a new MPM gate.
- Schema changes increment the schema version field.
- Runtime registry changes update `05_RUNTIME/runtime-registry.json`.
- Domain additions require a new domain folder and README.
