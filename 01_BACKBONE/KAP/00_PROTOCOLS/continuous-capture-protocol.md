# Continuous Capture Protocol

> **Module:** KAP — Knowledge Absorption Pipeline
> **Gate:** MPM-20260705-YOS-KAP-KNOWLEDGE-ADAPTER-CENSUS-AND-PROBE-GATE
> **Version:** v1.0.0
> **Status:** ACTIVE

---

## Purpose

Define the protocol for continuously capturing new sessions and deltas from a source as they occur. Continuous capture is the steady-state operation after historical backfill is complete.

---

## Signal Priority

Prefer signals in this order (per doctrine Article VII):

```
1. native message event (webhook/push)      ← most reliable, lowest latency
2. native completion/archive event          ← reliable for finalization
3. API polling cursor                       ← reliable, higher latency
4. filesystem watcher                       ← reliable for workspace adapters
5. scheduled delta import                   ← fallback, configurable interval
6. manual finalize marker                   ← always available
```

**Best available signal wins.**

---

## Protocol Steps

### Step 1 — Signal Registration

For each source, determine the best available signal:
- Check if adapter supports webhooks → register webhook endpoint
- Check if adapter supports native events → subscribe
- Otherwise → configure polling interval (default: 15 minutes)

### Step 2 — Delta Capture Loop

```
cursor = last_checkpoint_cursor (or None for initial run)

on_signal():
  result = adapter.retrieve_delta(cursor)
  for record in result.records:
    if is_new(record):
      store_as_source_fragment(record)
    elif is_updated(record):
      update_source_fragment(record)
  cursor = result.new_cursor
  checkpoint(cursor)
  if result.has_more:
    continue loop immediately
```

### Step 3 — Finalization Detection

For each active session, periodically call `detect_finalization()`:
- If `is_finalized = true` → call `finalize()` → mark session as immutable
- If `confidence = low` → flag for human review

### Step 4 — Attachment Capture

When a session is finalized, call `fetch_attachments()` to capture any associated files.

### Step 5 — Coverage Update

After each delta cycle, update the coverage report for the source.

---

## Polling Intervals by Adapter Class

| Class | Default Interval | Notes |
|---|---|---|
| Class A — API Runtime | 15 minutes | Respect rate limits |
| Class B — Workspace Runtime | 5 minutes | Filesystem watchers preferred |
| Class C — Consumer UI | N/A | Not supported for continuous capture |

---

## Current State (2026-07-05)

**Continuous capture is NOT yet deployed.** This protocol defines the target architecture. Current state: manual relay (human uploads MP to Manus). See `bus-migration-roadmap.md` for rollout phases.

---

## Constraints

```
MUST respect adapter rate limits.
MUST NOT poll more frequently than adapter allows.
MUST checkpoint after every delta cycle.
MUST NOT run continuous capture without Guardian authorization.
```
