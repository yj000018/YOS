# Checkpoint and Finalization Protocol

> **Module:** KAP — Knowledge Absorption Pipeline
> **Gate:** MPM-20260705-YOS-KAP-KNOWLEDGE-ADAPTER-CENSUS-AND-PROBE-GATE
> **Version:** v1.0.0
> **Status:** ACTIVE

---

## Purpose

Define how KAP saves progress (checkpointing) and marks sessions as complete and immutable (finalization).

---

## Part 1 — Checkpointing

### What is a checkpoint?

A checkpoint is a persisted cursor that records the last successfully processed position in a source. It enables resume after interruption without re-processing already-captured records.

### Checkpoint structure

See `kap_checkpoint.schema.json` for the full schema.

```json
{
  "checkpoint_id": "CHK-{adapter_id}-{source_id}-{timestamp}",
  "adapter_id": "string",
  "source_id": "string",
  "cursor": "string",
  "records_processed": 0,
  "created_at": "iso8601",
  "status": "active|superseded|abandoned"
}
```

### When to checkpoint

```
After every 50 records processed (minimum)
After each delta cycle in continuous capture
Before any planned interruption
After detecting a finalization signal
```

### Checkpoint storage

Checkpoints are stored in:
```
01_BACKBONE/KAP/05_RUNS/{adapter_id}/{source_id}/checkpoints/
```

The latest active checkpoint is also referenced in the source's coverage report.

---

## Part 2 — Finalization

### What is finalization?

Finalization marks a session as complete and immutable. A finalized session will not receive new content. KAP can safely generate claims and thought lines from finalized sessions.

**KAP MUST NOT generate claims from non-finalized sessions** (content may change).

### Finalization signals (in order of reliability)

| Signal | Reliability | Notes |
|---|---|---|
| `native_completion_event` | high | Provider signals session is done |
| `SESSION_FINALIZE_event` | high | Explicit KAP finalization event |
| `workspace_marker` | high | Marker file in workspace |
| `task_completion` | high | Manus task completed signal |
| `commit_marker` | high | Git commit marks session boundary |
| `idle_timeout` | medium | Session idle for N minutes (configurable) |
| `full_export_import` | medium | Full export implies completeness |
| `manual_finalize` | low | Human marks session as done |

### Finalization procedure

1. Detect finalization signal
2. Call `detect_finalization(session_id)` → verify confidence
3. If `confidence = high` → auto-finalize
4. If `confidence = medium` → flag for human review within 24h
5. If `confidence = low` → require explicit human MPM to finalize
6. Call `finalize(session_id)` → mark immutable
7. Call `fetch_attachments(session_id)` → capture any remaining attachments
8. Update coverage report

### Finalization by adapter

| Adapter | Best Signal | Confidence |
|---|---|---|
| OpenAI API | API polling (no native event) | medium |
| Manus workspace | task_completion event | high |
| Git repository | commit_marker | high |
| Mem0 | manual_finalize | low |
| Google Drive | workspace_marker | medium |
| Notion | API polling | medium |
| ChatGPT App | manual_finalize (no API) | low |

---

## Part 3 — Resume

After a checkpoint, resume with:

```
result = adapter.resume(cursor)
# Continue from result.resumed_from
```

Resume MUST be idempotent — re-processing an already-processed record MUST be safe (deduplication by `session_id`).
