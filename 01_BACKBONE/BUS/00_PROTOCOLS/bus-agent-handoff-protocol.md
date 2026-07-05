# BUS Agent Handoff Protocol

**Version:** 1.0.0
**Status:** active
**Integrated from:** `yj000018/yos-bus` protocols

---

## Purpose

Defines how agents hand off work, results, and context through the BUS layer.

---

## Handoff Types

| Type | Description |
|---|---|
| **Task handoff** | Agent A creates a task packet in `inbox/domain/` for Agent B to claim. |
| **Artifact handoff** | Agent A produces an artifact and places it in `outbox/domain/` for Agent B to consume. |
| **Decision handoff** | Agent A creates a decision packet requiring review by Agent B or human. |
| **MPM handoff** | ChatGPT A&G creates an MP packet in BUS `inbox/mpm/`; Manus claims and executes. |

---

## Handoff Rules

1. **Producer writes, consumer reads.** The producing agent writes to `inbox/` or `outbox/`. The consuming agent reads and claims.
2. **Claim is atomic.** Move `inbox/domain/file` → `workspace/domain/file` in a single operation.
3. **No double-claiming.** If a lock file exists, do not claim.
4. **Context must be self-contained.** A BUS packet must carry enough context for the consumer to act without querying the producer.
5. **Risk flags require human review.** If `risk_flags` is non-empty, do not auto-execute — present micro-menu.
6. **Durable outputs go to Git.** After execution, canonical artifacts must be committed to YOS Git.

---

## MPM-Specific Handoff

```
ChatGPT A&G (producer)
  -> writes MP packet to BUS inbox/mpm/ (or MPM/04_QUEUE/ready/ as Git fallback)

Manus (consumer)
  -> reads BUS inbox/mpm/ (preferred)
  -> claims: moves to workspace/mpm/
  -> executes MP
  -> writes MPR to MPM/06_REPORTS/awaiting-review/
  -> writes pointer to BUS outbox/mpm/
  -> moves MP to archive/mpm/

ChatGPT A&G (downstream consumer)
  -> reads BUS outbox/mpm/ or latest-mpr.json fast path
  -> reviews MPR
  -> approves/rejects
```

---

## Failure Handling

If an agent cannot complete a claimed task:
1. Move the packet from `workspace/domain/` to `dead-letter/`.
2. Update packet status to `failed`.
3. Include failure reason in packet payload.
4. Notify the originating agent if possible.

---

## Legacy Note

This protocol integrates and supersedes the agent handoff rules from `yj000018/yos-bus` (HEAD: 245818d). The core inbox/workspace/outbox/archive model is preserved. Domain routing and multi-backend support are new additions.
