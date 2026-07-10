# Historical Backfill Protocol

> **Module:** KAP — Knowledge Absorption Pipeline
> **Gate:** MPM-20260705-YOS-KAP-KNOWLEDGE-ADAPTER-CENSUS-AND-PROBE-GATE
> **Version:** v1.0.0
> **Status:** ACTIVE

---

## Purpose

Define the protocol for retrieving historical sessions and records from a source via a Knowledge Adapter. Historical backfill is a one-time or periodic operation to capture past knowledge that predates continuous capture.

---

## Preconditions

Before starting a historical backfill:

1. Adapter `health_check()` returns `healthy`
2. Source is registered in `knowledge-adapters.json` with status ≥ `candidate`
3. A Guardian-authorized MPM gate has been issued for this source
4. Coverage report baseline has been established via `report_coverage()`

---

## Protocol Steps

### Step 1 — Scope Definition

Define the backfill scope:
- `source_id` — which source to backfill
- `since` — earliest date (null = all available history)
- `until` — latest date (null = up to current)
- `max_records` — hard cap to prevent runaway enumeration (default: 500)

**Rule:** Never enumerate full history without a `max_records` cap on the first run.

### Step 2 — Metadata Probe

Call `list_sessions(source_id, limit=50)` to understand:
- Total known record count
- Date range available
- Cursor structure

Record findings in the gate report before proceeding.

### Step 3 — Paginated Retrieval

```
cursor = None
records_retrieved = 0

loop:
  result = adapter.list_sessions(source_id, cursor=cursor, limit=50)
  for session_summary in result.sessions:
    record = adapter.retrieve_session(session_summary.session_id)
    store_as_source_fragment(record)
    records_retrieved += 1
    if records_retrieved >= max_records:
      checkpoint(cursor)
      HALT — request new MPM gate to continue
  cursor = result.next_cursor
  if cursor is None:
    COMPLETE
```

### Step 4 — Checkpointing

After every 50 records (or at natural boundaries), call `checkpoint(session_id, cursor)` and persist the cursor. This enables resume after interruption.

### Step 5 — Coverage Report

After backfill completes (or is halted), call `report_coverage(source_id)` and include in gate report.

### Step 6 — Human Review Gate

Halt and produce a gate report. The Guardian Architect reviews:
- Records retrieved
- Coverage level achieved
- Known gaps
- Recommended next action (continue backfill, proceed to claim extraction, or defer)

---

## Constraints

```
MUST NOT enumerate thousands of records blindly.
MUST NOT import full historical corpora without Guardian authorization.
MUST NOT mutate source corpus.
MUST checkpoint every 50 records minimum.
MUST produce a coverage report at the end of each run.
```

---

## Adapter Suitability

| Adapter Type | Backfill Support | Notes |
|---|---|---|
| Conversation Adapter (API) | `candidate` | API may not expose consumer app history |
| Workspace Adapter | `proven` | Filesystem history always accessible |
| Repository Adapter | `proven` | Git log is complete and immutable |
| Memory Adapter | `candidate` | Depends on Mem0 API capabilities |
| File Adapter | `proven` | Export corpus is complete |
| Research Adapter | `unsupported` | Research results are not session-based |
| Evidence Adapter | `unsupported` | Evidence is retrieved on demand, not historical |
