# YOS BUS — Connectivity Census Protocol Patches

**Source Gate:** MPM-20260705-YOS-MANUS-CONNECTIVITY-CENSUS-GATE
**Date:** 2026-07-05
**Status:** applied

---

## Patch 1 — Canonical Backend Confirmed

**Target:** `bus-canonical-doctrine.md`, `runtime-registry.json`, `entry-backend-registry.json`

**Change:** Confirm `workspace_filesystem` (direct_file) as canonical production-ready backend.

```
CANONICAL_BACKEND: workspace_filesystem
CANONICAL_PATH:    /home/ubuntu/yos-bus-runtime
CANONICAL_ENV_VAR: YOS_BUS_RUNTIME_ROOT
STATUS:            production_ready (was: candidate)
```

**Rationale:** Census confirms full lifecycle support, sub-ms latency, cross-session persistence proven.

---

## Patch 2 — New Backend IDs Registered

**Target:** `entry-backend-registry.json`, `runtime-registry.json`

**New backends identified:**
- `manus_api_task` — task.create/sendMessage external write path
- `manus_webhook` — last-mile push notification
- `connector_bridge` — GitHub/GDrive connector transport
- `mcp_bridge` — MCP server file transport (future)

---

## Patch 3 — External Write Path Documented

**Target:** `bus-first-last-mile-protocol.md`, `bus-mpm-bridge-protocol.md`

**Change:** Add Option B (Manus API task.create) as recommended external write path.

```
EXTERNAL_WRITE_OPTIONS:
  A. manual_upload (current — operational)
  B. manus_api_task (recommended upgrade — ChatGPT → task.create → Manus agent → BUS)
  C. mcp_bridge (future — requires MCP server setup)
  D. connector_bridge (alternative — requires GitHub connector)
```

---

## Patch 4 — Fallback Chain Updated

**Target:** `runtime-registry.json`, `bus-runtime-backend-protocol.md`

**New fallback chain:**
```
1. workspace_filesystem    [production_ready — preferred]
2. git                     [production_ready — fallback]
3. manus_api_task          [production_candidate — external write]
4. manus_webhook           [production_candidate — last-mile only]
5. connector_bridge        [production_candidate — if enabled]
6. mcp_bridge              [candidate — if configured]
7. blob_payload            [experimental — emergency only]
```

---

## Patch 5 — Rejected Mechanisms

**Target:** `bus-canonical-doctrine.md`

**Rejected as BUS backends:**
- `manus_touchpoint_fuse` — internal telemetry only
- `manus_heartbeat` — webdev cron only
- `manus_api_projects` — instructions only, no packet transport
- `manus_api_file_upload` (standalone) — 48h TTL, no lifecycle

---

## Patch 6 — Next Gates Required

**Target:** `bus-domain-index.md`, `latest-bus-event.md`

**Required probe gates:**
1. `MPM-{DATE}-YOS-BUS-MANUS-API-TASK-WRITE-GATE` — validate ChatGPT → task.create → BUS inbox
2. `MPM-{DATE}-YOS-BUS-MCP-SERVER-SETUP-GATE` — configure filesystem MCP server
3. `MPM-{DATE}-YOS-BUS-WEBHOOK-LAST-MILE-GATE` — validate webhook last-mile notification
4. `MPM-{DATE}-YOS-BUS-CONNECTOR-BRIDGE-GATE` — enable GitHub/GDrive connector
