# YARP State Machine

> **Version:** v1.0.0
> **Status:** candidate

---

## States

| State | Description |
|---|---|
| `draft` | MP created, not yet queued |
| `queued` | MP in BUS inbox or MPM ready queue |
| `sent` | EXECUTE_MP message dispatched to executor |
| `acknowledged` | Executor returned ACK |
| `claimed` | Executor moved packet from inbox to workspace (BUS claim) |
| `running` | Executor actively executing MP |
| `waiting_for_info` | Executor sent REQUEST_INFO, awaiting reply |
| `completed` | RESULT returned, MPR written, commit pushed |
| `failed` | ERROR returned, execution unsuccessful |
| `cancelled` | CANCEL accepted by executor |
| `timed_out` | No RESULT within mode timeout |
| `superseded` | A newer EXECUTE_MP for same mp_id received |
| `archived` | FINALIZE complete, session closed |

---

## Allowed Transitions

```
draft          → queued           (MP placed in BUS inbox or MPM ready queue)
queued         → sent             (EXECUTE_MP dispatched)
queued         → cancelled        (CANCEL before dispatch)
sent           → acknowledged     (ACK received)
sent           → timed_out        (no ACK within 60s)
sent           → failed           (NACK received with retry_eligible=false)
acknowledged   → claimed          (BUS claim executed)
acknowledged   → running          (direct execution without BUS claim)
claimed        → running          (execution started)
running        → waiting_for_info (REQUEST_INFO sent)
running        → completed        (RESULT returned)
running        → failed           (ERROR returned)
running        → cancelled        (CANCEL accepted)
running        → timed_out        (no RESULT within mode timeout)
waiting_for_info → running        (info received, execution resumed)
waiting_for_info → timed_out      (no reply within REQUEST_INFO timeout)
completed      → archived         (FINALIZE complete)
failed         → queued           (retry — new attempt_id)
timed_out      → queued           (retry — new attempt_id)
cancelled      → archived         (no retry)
superseded     → archived         (no retry)
```

---

## Invalid Transitions

```
completed   → running     (FORBIDDEN — completed is terminal unless retry)
archived    → any         (FORBIDDEN — archived is terminal)
cancelled   → running     (FORBIDDEN — must re-queue)
failed      → completed   (FORBIDDEN — must re-queue and re-execute)
```

---

## State Diagram (ASCII)

```
draft
  │
  ▼
queued ──────────────────────────────────────────────────────────────► cancelled
  │                                                                          │
  ▼                                                                          │
sent ──────────────────────────────────────────────────────────────────► timed_out
  │                                                                          │
  ▼                                                                          │
acknowledged                                                                 │
  │                                                                          │
  ▼                                                                          │
claimed / running ◄──────────────────────────────────────────────────────────┘
  │
  ├──► waiting_for_info ──► running (resumed)
  │
  ├──► completed ──► archived
  │
  ├──► failed ──► queued (retry)
  │
  ├──► cancelled ──► archived
  │
  ├──► timed_out ──► queued (retry)
  │
  └──► superseded ──► archived
```

---

## Mode Timeouts

| MP Mode | ACK Timeout | RESULT Timeout |
|---|---|---|
| sprint | 60s | 5 min |
| run | 60s | 15 min |
| marathon | 60s | 60 min |

---

## Retry Policy

| Trigger | Max Retries | Backoff |
|---|---|---|
| ACK timeout | 3 | 5s, 15s, 30s |
| RESULT timeout | 2 | 60s, 300s |
| NACK with retry_eligible=true | 2 | 30s, 120s |
| ERROR with retry_eligible=true | 1 | 60s |

---

## Idempotency

EXECUTE_MP messages are idempotent by `mp_id`.

If an executor receives an EXECUTE_MP with an `mp_id` already in `running`, `completed`, or `waiting_for_info` state:
- Return ACK with existing `task_id`
- Do NOT start a new execution
- If `completed`, return existing RESULT

If `mp_id` is in `failed` or `timed_out` state with a new `attempt_id`:
- Accept as a new retry attempt
- Start fresh execution

---

## MPM Ledger Mapping

| YARP State | MPM Ledger Status |
|---|---|
| `draft` | (not in ledger) |
| `queued` | `ready` |
| `sent` / `acknowledged` / `claimed` | `running` |
| `running` / `waiting_for_info` | `running` |
| `completed` | `executed_awaiting_architect_guardian_review` |
| `failed` | `failed` |
| `cancelled` | `cancelled` |
| `timed_out` | `timed_out` |
| `archived` | `archived` |
