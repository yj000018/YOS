# Knowledge Adapter Contract

> **Module:** KAP — Knowledge Absorption Pipeline
> **Gate:** MPM-20260705-YOS-KAP-KNOWLEDGE-ADAPTER-CENSUS-AND-PROBE-GATE
> **Version:** v1.0.0
> **Status:** ACTIVE

---

## Overview

The Knowledge Adapter Contract defines the normalized interface that every KAP adapter MUST implement. KAP calls only these methods — never provider-specific APIs directly.

---

## Method Definitions

### `discover_sources() → list[SourceDescriptor]`

Enumerate all available sources accessible through this adapter.

| Field | Type | Description |
|---|---|---|
| `source_id` | string | Unique identifier for the source |
| `source_type` | string | Type: `conversation`, `workspace`, `repository`, `memory`, `file`, `research` |
| `display_name` | string | Human-readable name |
| `accessible` | bool | Whether the source is currently accessible |
| `estimated_record_count` | int\|null | Estimated number of records (null if unknown) |

---

### `list_sessions(source_id, cursor=None, limit=50) → SessionList`

List sessions/records from a source, with optional cursor for pagination.

| Field | Type | Description |
|---|---|---|
| `sessions` | list[SessionSummary] | List of session summaries |
| `next_cursor` | string\|null | Cursor for next page (null if exhausted) |
| `total_known` | int\|null | Total known count (null if unknown) |

---

### `retrieve_session(session_id) → KAPSessionRecord`

Retrieve the full content of a single session. Returns a normalized `KAPSessionRecord` (see schema).

---

### `retrieve_history(source_id, since=None, until=None) → list[KAPSessionRecord]`

Retrieve all sessions within a time range. Use `since`/`until` as ISO8601 strings or null for unbounded.

**Constraint:** MUST NOT enumerate thousands of sessions blindly. Implementations MUST support pagination.

---

### `retrieve_delta(cursor) → DeltaResult`

Retrieve only new/updated sessions since the given cursor.

| Field | Type | Description |
|---|---|---|
| `records` | list[KAPSessionRecord] | New or updated records |
| `new_cursor` | string | Updated cursor for next delta call |
| `has_more` | bool | Whether more records are available |

---

### `fetch_attachments(session_id) → list[Attachment]`

Retrieve attachments (files, images, documents) for a session.

| Field | Type | Description |
|---|---|---|
| `attachment_id` | string | Unique ID |
| `filename` | string | Original filename |
| `mime_type` | string | MIME type |
| `size_bytes` | int\|null | Size in bytes |
| `content_url` | string\|null | URL or path to content |

---

### `checkpoint(session_id, cursor) → CheckpointRecord`

Save a progress checkpoint for a session. Returns a `KAPCheckpoint` (see schema).

---

### `detect_finalization(session_id) → FinalizationStatus`

Detect whether a session has been finalized (completed, archived, immutable).

| Field | Type | Description |
|---|---|---|
| `is_finalized` | bool | Whether the session is finalized |
| `signal_type` | string | Signal used: `native_event`, `idle_timeout`, `manual`, `unknown` |
| `confidence` | string | `high`, `medium`, `low` |
| `finalized_at` | string\|null | ISO8601 timestamp if known |

---

### `finalize(session_id) → bool`

Mark a session as finalized in the adapter's internal state. Returns `true` on success.

---

### `resume(cursor) → ResumeResult`

Resume processing from a saved checkpoint cursor.

| Field | Type | Description |
|---|---|---|
| `resumed_from` | string | The cursor used to resume |
| `records_available` | int\|null | Estimated records available from this cursor |

---

### `report_coverage(source_id) → CoverageReport`

Generate a coverage report for a source. Returns a `KAPCoverageReport` (see schema).

---

### `health_check() → HealthStatus`

Check adapter health and connectivity.

| Field | Type | Description |
|---|---|---|
| `status` | string | `healthy`, `degraded`, `unavailable` |
| `latency_ms` | int\|null | Response latency in milliseconds |
| `auth_valid` | bool | Whether authentication is valid |
| `message` | string\|null | Human-readable status message |

---

## Method Status Values

Each method implementation MUST declare a status:

| Status | Meaning |
|---|---|
| `proven` | Tested and working in production |
| `candidate` | Implemented but not yet fully tested |
| `unsupported` | Not available for this adapter |
| `unknown` | Not yet probed |
| `not_applicable` | Not relevant for this adapter type |

---

## Normalized Events

Adapters SHOULD emit these normalized events when possible:

```
source_discovered          — a new source was found
session_created            — a new session was created
session_delta_available    — new content is available for an existing session
checkpoint_due             — a checkpoint should be saved
session_idle               — session has been idle for a threshold period
session_finalized          — session is complete and immutable
historical_batch_ready     — a batch of historical records is ready for processing
attachment_available       — an attachment is available for a session
adapter_error              — an error occurred in the adapter
```
