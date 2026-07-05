---
mpr_id: MPM-20260705-YOS-MANUS-CONNECTIVITY-CENSUS-GATE-REPORT
mp_id: MPM-20260705-YOS-MANUS-CONNECTIVITY-CENSUS-GATE
title: YOS Manus Connectivity Census Gate — MPR
mode: marathon
status: executed_awaiting_architect_guardian_review
executor: Manus
guardian_required: true
branch: main
commit: pending_patch
executed_at: "2026-07-05T16:00:00Z"
---

# MPR — YOS Manus Connectivity Census Gate

## STATUS BLOCK

```
STATUS:                          EXECUTED_AWAITING_A_G_REVIEW
MODE:                            marathon
COMMIT:                          pending_patch
CONNECTIVITY_MATRIX_CREATED:     yes
MCP_CENSUS_COMPLETE:             yes
API_CENSUS_COMPLETE:             yes
CLI_CENSUS_COMPLETE:             yes
WORKSPACE_CENSUS_COMPLETE:       yes
BEST_BACKEND:                    workspace_filesystem (direct_file) — production_ready
FALLBACK_CHAIN:                  workspace_filesystem → git → manus_api_task → manus_webhook → connector_bridge → mcp_bridge → blob_payload
PROTOCOL_CHANGES_REQUIRED:       yes (6 patches — see below)
READY_FOR_A_G_REVIEW:            yes
```

---

## 1. Census Summary

### Mechanisms Surveyed

| # | Mechanism | Available | Classification |
|---|---|---|---|
| 1 | Workspace Filesystem (`/home/ubuntu/`) | yes | **production_ready** |
| 2 | Git Transport (GitHub yj000018/YOS) | yes | **production_ready** |
| 3 | Manus API — task.create / sendMessage | yes | **production_candidate** |
| 4 | Manus API — Webhooks | yes | **production_candidate** |
| 5 | Manus API — Structured Output | yes | **production_candidate** |
| 6 | Manus API — Connectors (252 available, 0 enabled) | yes | **production_candidate** |
| 7 | MCP Bridge (manus-mcp-cli, 0 servers) | yes | **candidate** |
| 8 | Manus API — file.upload / S3 CDN | yes | **experimental** |
| 9 | Manus API — Projects | yes | **experimental** |
| 10 | Manus Heartbeat (HTTP cron) | yes | **experimental** |
| 11 | Manus Touchpoint Fuse | yes (internal) | **rejected** |

---

## 2. BUS Operations Matrix

| Operation | Filesystem | Git | API task | Webhook | MCP | S3 CDN |
|---|---|---|---|---|---|---|
| BUS.write(packet) | ✅ direct | ✅ commit | ✅ async | ❌ | ⚡ potential | ⚡ partial |
| BUS.claim(domain) | ✅ mv inbox→ws | ✅ mv+commit | ❌ | ❌ | ⚡ potential | ❌ |
| BUS.publish(report) | ✅ mv ws→out | ✅ mv+commit | ✅ async | ✅ push | ⚡ potential | ⚡ url |
| BUS.read_latest_report() | ✅ file read | ✅ file read | ✅ listMessages | ✅ push | ⚡ potential | ⚡ if url known |

Legend: ✅ = supported | ⚡ = potential/partial | ❌ = not supported

---

## 3. Canonical Recommended Backend

```
CANONICAL_BACKEND:     workspace_filesystem (direct_file)
CANONICAL_PATH:        /home/ubuntu/yos-bus-runtime
CANONICAL_ENV_VAR:     YOS_BUS_RUNTIME_ROOT
CLASSIFICATION:        production_ready
LATENCY:               ~1ms
PERSISTENCE:           proven cross-session
LIFECYCLE:             inbox → workspace → outbox → archive (full)
```

**Rationale:** Fastest, most reliable, full lifecycle support, cross-session persistence proven across multiple sessions, zero external dependencies, already operational.

**Gap (critical):** External LLM (ChatGPT) cannot write directly. Requires manual upload bridge (current) or Manus API task relay (recommended upgrade).

---

## 4. Fallback Chain

```
1. workspace_filesystem    → /home/ubuntu/yos-bus-runtime  [production_ready — preferred]
2. git                     → yj000018/YOS main             [production_ready — fallback]
3. manus_api_task          → task.create/sendMessage       [production_candidate — external write]
4. manus_webhook           → last-mile notification only   [production_candidate — report delivery]
5. connector_bridge        → GitHub/GDrive (if enabled)    [production_candidate — optional]
6. mcp_bridge              → if MCP server configured      [candidate — future]
7. blob_payload            → S3 CDN (one-shot only)        [experimental — emergency]
```

---

## 5. External Write Path Analysis

**Critical gap:** ChatGPT cannot write directly to `/home/ubuntu/yos-bus-runtime/`.

| Option | Status | Effort | Impact |
|---|---|---|---|
| A. Manual upload bridge (current) | operational | zero | baseline |
| B. Manus API task.create (recommended) | production_candidate | low | eliminates manual upload |
| C. MCP Server filesystem | candidate | medium | direct write |
| D. GitHub connector | production_candidate | low | alternative |

**Recommended upgrade path:** Option B — ChatGPT calls `POST /v2/task.create` with MP packet as message content → Manus agent places packet in BUS inbox.

---

## 6. Key Discoveries

| Discovery | Impact |
|---|---|
| `/home/ubuntu/` persists cross-session (proven) | Canonical backend confirmed |
| `manus-mcp-cli` installed, 0 servers configured | MCP bridge ready to activate |
| 252 connectors available, 0 enabled | GitHub/GDrive bridge available on demand |
| `task.sendMessage` with `agent-default-main_task` | Fastest external write path |
| Webhooks: `task_created`, `task_stopped` events | Last-mile push notification available |
| Structured output via `structured_output_schema` | MPR as JSON result available |
| `manus-heartbeat` = webdev HTTP cron only | Not a BUS backend |
| `manus-touchpoint-fuse` = internal telemetry | Not a BUS backend |
| No Manus Python/Node SDK | API-only access |
| Rate limit: 10/min task.create | Sufficient for MPM cadence |

---

## 7. Protocol Changes Required

### Patch 1 — Canonical Backend Confirmed
- `workspace_filesystem` → `production_ready` (was: `candidate`)
- `entry-backend-registry.json` updated ✅

### Patch 2 — New Backend IDs Registered
- `manus_api_task`, `manus_webhook`, `connector_bridge`, `mcp_bridge` added to registries ✅

### Patch 3 — External Write Path Documented
- `bus-connectivity-census-protocol-patches.md` created ✅
- Options A/B/C/D documented

### Patch 4 — Fallback Chain Updated
- `entry-backend-registry.json` v1.1.0 ✅
- `report-backend-registry.json` v1.1.0 ✅

### Patch 5 — Rejected Mechanisms Documented
- `manus_touchpoint_fuse`, `manus_heartbeat`, `manus_api_projects` → rejected as BUS backends ✅

### Patch 6 — Migration Roadmap Created
- `bus-migration-roadmap.md` created ✅
- 4 phases defined

---

## 8. Migration Roadmap Summary

| Phase | Gate | Priority | Impact |
|---|---|---|---|
| 0 | Current (operational) | — | baseline |
| 1 | API Task Write Gate | HIGH | eliminates manual upload |
| 2 | Webhook Last-Mile Gate | HIGH | push notification |
| 3 | MCP Server Setup Gate | MEDIUM | direct write |
| 4 | Connector Bridge Gate | LOW | alternative |

---

## 9. Artifacts Delivered

| Artifact | Path |
|---|---|
| Connectivity Matrix (JSON) | `01_BACKBONE/BUS/06_INDEXES/manus-connectivity-matrix.json` |
| Connectivity Matrix (MD) | `01_BACKBONE/BUS/06_INDEXES/manus-connectivity-matrix.md` |
| Protocol Patches | `01_BACKBONE/BUS/00_PROTOCOLS/bus-connectivity-census-protocol-patches.md` |
| Migration Roadmap | `01_BACKBONE/BUS/06_INDEXES/bus-migration-roadmap.md` |
| Entry Backend Registry v1.1.0 | `01_BACKBONE/BUS/05_RUNTIME/entry-backend-registry.json` |
| Report Backend Registry v1.1.0 | `01_BACKBONE/BUS/05_RUNTIME/report-backend-registry.json` |

---

## 10. Suggested Next Gates

1. `MPM-{DATE}-YOS-BUS-MANUS-API-TASK-WRITE-GATE` — validate ChatGPT → task.create → BUS inbox
2. `MPM-{DATE}-YOS-BUS-WEBHOOK-LAST-MILE-GATE` — validate webhook last-mile notification
3. `MPM-{DATE}-YOS-BUS-MCP-SERVER-SETUP-GATE` — configure filesystem MCP server
4. `MPM-{DATE}-YOS-BUS-CONNECTOR-BRIDGE-GATE` — enable GitHub/GDrive connector
