# BUS Reflex Architecture

**Version:** 1.0.0
**Status:** defined — NOT YET ACTIVATED
**Integrated from:** `yj000018/yos-bus` github-actions-reflex-architecture.md

---

## Status Warning

> **GitHub Actions integration is NOT yet activated.**
> This document defines the architecture for future activation.
> Do not implement GitHub Actions workflows until an explicit MPM gate approves activation.

---

## Concept

A BUS reflex is an automated reaction triggered by a BUS event, file change, or condition threshold. Reflexes allow the BUS to respond to events without human intervention, subject to safety rules.

---

## Reflex Types

| Type | Trigger | Example |
|---|---|---|
| `inbox_arrival` | New file in `inbox/domain/` | Notify Manus that a new MP is ready |
| `threshold` | Count or size threshold | Alert if inbox/mpm has >3 unclaimed packets |
| `schedule` | Time-based | Daily BUS health check |
| `failure` | Packet moved to dead-letter | Alert on failed MPM execution |
| `outbox_ready` | New file in `outbox/domain/` | Notify A&G that MPR is ready for review |

---

## GitHub Actions Integration (Future)

When activated, GitHub Actions workflows will:

1. Watch for new files in `04_DOMAINS/*/inbox/` (Git-backed BUS).
2. Trigger a reflex packet creation.
3. Route the reflex to the appropriate agent via BUS.

```yaml
# FUTURE — not yet active
on:
  push:
    paths:
      - '01_BACKBONE/BUS/04_DOMAINS/mpm/inbox/**'
```

---

## Safety Rules

1. **No arbitrary code execution from BUS packets.** Reflexes may only route, notify, or create new BUS packets.
2. **All reflexes with `auto_execute: false` require human approval.**
3. **Reflex schema must be validated before execution.**
4. **GitHub Actions must be explicitly approved in a dedicated MPM gate.**

---

## Activation Gate

To activate GitHub Actions reflexes, create and execute:

```
MPM-{DATE}-YOS-BUS-REFLEX-ACTIVATION-GATE
```

This gate must:
- Define specific reflex workflows.
- Validate safety boundaries.
- Get A&G approval before push.

---

## Legacy Note

This architecture integrates and supersedes `github-actions-reflex-architecture.md` from `yj000018/yos-bus`. The core concept is preserved. Activation is deferred pending explicit gate.
