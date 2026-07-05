# Latest BUS Event

> **Source of truth:** `06_INDEXES/latest-bus-event.json`

| Field | Value |
|---|---|
| Event ID | BUS-20260705-MANUS-API-CAPABILITY-VERIFICATION |
| Event Type | api_capability_verification |
| Domain | mpm |
| Status | executed |
| MP ID | MPM-20260705-YOS-MANUS-API-CAPABILITY-VERIFICATION-GATE |
| Capabilities Verified | 9 |
| Proven | task_create, send_message, file_upload, task_attachment, conversation_continuation, auth_model, structured_output |
| Supported | webhooks |
| Unsupported Direct / Supported Indirect | workspace_write, workspace_read |
| Critical Blockers | BL-01 (no direct workspace write), BL-02 (no direct workspace read) |
| Recommended Pattern | Async Task Relay Pattern |
| Best Auth | x-manus-api-key |
| Updated At | 2026-07-05T17:00:00Z |
