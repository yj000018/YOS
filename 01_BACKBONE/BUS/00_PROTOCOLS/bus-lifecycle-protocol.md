# BUS Lifecycle Protocol

**Version:** 1.0.0
**Status:** active

---

## Universal Flow

```
inbox -> workspace -> outbox -> archive
```

All BUS packets follow this lifecycle regardless of domain or backend.

---

## Stage Semantics

| Stage | Meaning |
|---|---|
| `inbox` | New message/task/artifact awaiting claim by an agent. |
| `workspace` | Claimed and actively being processed. |
| `outbox` | Completed result/report/pointer awaiting consumption by downstream agent. |
| `archive` | Historical/completed/deprecated storage. Final resting state. |
| `dead-letter` | Failed/unprocessable messages. Runtime-dependent support. |
| `ack` | Acknowledgements. Runtime-dependent support. |
| `locks` | Claim locks to prevent double-claiming. Runtime-dependent support. |

---

## Claim Protocol

A packet moves from `inbox` to `workspace` when an agent **claims** it.

Claim rules:
- Claim must be atomic where possible: rename/move `inbox/domain/file` → `workspace/domain/file`.
- Only one agent may claim a packet at a time.
- Claim creates a lock if the runtime supports it.
- If claim fails (race condition), the packet stays in `inbox`.

---

## Completion Protocol

A packet moves from `workspace` to `outbox` when the agent completes processing.

Completion rules:
- Write the result/artifact/pointer to `outbox/domain/`.
- Update the packet status to `outbox`.
- The downstream consumer reads from `outbox`.

---

## Archive Protocol

A packet moves from `outbox` to `archive` when the downstream consumer has consumed it.

Archive rules:
- Move the packet file to `archive/domain/`.
- Update the packet status to `archive`.
- Durable artifacts must be committed to YOS Git before archiving.

---

## Git vs. Runtime Distinction

```
Git-tracked BUS folders define canonical structure and durable records.
Runtime BUS folders may live outside Git and carry ephemeral messages.
```

The `04_DOMAINS/` folder in YOS Git defines the canonical domain structure. The actual runtime inbox/workspace/outbox/archive folders for fast transport live at `$YOS_BUS_RUNTIME_ROOT` (outside Git by default).

---

## Error Handling

If a packet cannot be processed:
1. Move to `dead-letter/` if runtime supports it.
2. Update packet status to `failed`.
3. Log the failure reason in the packet payload.
4. Alert the originating agent if possible.
