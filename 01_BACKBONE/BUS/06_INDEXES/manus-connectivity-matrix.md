# YOS BUS — Manus Connectivity Matrix

**Census Gate:** MPM-20260705-YOS-MANUS-CONNECTIVITY-CENSUS-GATE
**Census Date:** 2026-07-05
**Sandbox Version:** 8.0.47

---

## 1. Connectivity Matrix

| Mechanism | Available | BUS.write() | BUS.claim() | BUS.publish() | BUS.read_latest_report() | Cross-Session | Classification |
|---|---|---|---|---|---|---|---|
| Workspace Filesystem (`/home/ubuntu/`) | yes | yes | yes | yes | yes | **proven** | **production_ready** |
| Git Transport (GitHub) | yes | yes | yes | yes | yes | yes (permanent) | **production_ready** |
| Manus API — task.create | yes | yes (async) | no | yes | yes | task-scoped | **production_candidate** |
| Manus API — Webhooks | yes | no | no | yes (push) | yes (push) | yes | **production_candidate** |
| Manus API — Structured Output | yes | no | no | yes | yes | task-scoped | **production_candidate** |
| Manus API — Connectors (GitHub/GDrive) | yes (0 enabled) | yes (if enabled) | yes | yes | yes | connector-dep. | **production_candidate** |
| MCP Bridge (manus-mcp-cli) | yes (no servers) | potential | potential | potential | potential | unknown | **candidate** |
| Manus API — file.upload / S3 CDN | yes | partial | no | partial | partial | no (48h TTL) | **experimental** |
| Manus API — Projects | yes | partial | no | no | no | yes | **experimental** |
| Manus Heartbeat | yes | no | no | no | no | yes (cron) | **experimental** |
| Manus Touchpoint Fuse | yes (internal) | no | no | no | no | no | **rejected** |

---

## 2. Ranked Backend Comparison

### Rank 1 — Workspace Filesystem ⭐ CANONICAL

```
backend_id:    direct_file
path:          /home/ubuntu/yos-bus-runtime
env_var:       YOS_BUS_RUNTIME_ROOT
latency:       ~1ms
persistence:   proven cross-session
lifecycle:     inbox → workspace → outbox → archive (full)
external_write: manual_upload bridge (bus.py ingest)
```

**Why #1:** All four BUS operations supported. Sub-millisecond latency. Cross-session persistence proven across multiple sessions. Zero external dependencies. Already operational.

**Gap:** External LLM (ChatGPT) cannot write directly — requires manual upload bridge or API task relay.

---

### Rank 2 — Git Transport

```
backend_id:    git
repo:          yj000018/YOS (main)
latency:       seconds to minutes
persistence:   permanent (versioned)
lifecycle:     full (via file operations + commits)
external_write: yes (ChatGPT has GitHub access)
```

**Why #2:** Currently operational. External write proven. Versioned and auditable. Slower than filesystem.

---

### Rank 3 — Manus API task.create + task.sendMessage

```
backend_id:    manus_api_task
endpoint:      POST /v2/task.create, POST /v2/task.sendMessage
auth:          x-manus-api-key
latency:       seconds (async)
persistence:   task-scoped
lifecycle:     write=yes, claim=no, publish=yes, read_report=yes
external_write: yes (ChatGPT calls API → Manus agent processes)
```

**Why #3:** Enables ChatGPT → Manus direct write without manual upload. Async. Rate limited (10/min). Requires Manus agent to relay packet into BUS filesystem.

**Key insight:** `task.sendMessage` with `agent-default-main_task` is the fastest external write path. ChatGPT sends packet as message → Manus agent places it in `/home/ubuntu/yos-bus-runtime/inbox/mpm/`.

---

### Rank 4 — Manus API Webhooks

```
backend_id:    manus_webhook
endpoint:      POST /v2/webhook.create
events:        task_created, task_stopped
persistence:   yes (webhook persists)
lifecycle:     publish=yes (push notification), read_report=yes (push)
external_write: no
```

**Why #4:** Excellent for last-mile (MPR delivery notification). When Manus completes an MPR, webhook fires to ChatGPT/external endpoint. Requires public HTTPS endpoint.

---

### Rank 5 — Manus API Connectors (GitHub/Google Drive)

```
backend_id:    connector_bridge
connectors:    252 available, 0 enabled
notable:       GitHub, Google Drive, Notion
lifecycle:     full (if GitHub/GDrive enabled)
external_write: yes (via connector)
```

**Why #5:** If GitHub connector is enabled, provides programmatic Git transport without manual git operations. If Google Drive connector is enabled, provides cloud folder transport. Requires connector auth setup.

---

### Rank 6 — MCP Bridge

```
backend_id:    mcp_bridge
cli:           /usr/local/bin/manus-mcp-cli
servers:       0 configured
lifecycle:     potential (if file-system MCP server configured)
```

**Why #6:** High potential if a filesystem MCP server is configured pointing to `/home/ubuntu/yos-bus-runtime`. Enables external LLM direct write via MCP protocol. Requires server setup.

---

### Rank 7 — S3 CDN Upload (experimental)

```
backend_id:    blob_payload
tool:          manus-upload-file
cdn:           files.manuscdn.com
ttl:           48h
lifecycle:     partial (one-shot delivery only)
```

**Why #7:** Can deliver a packet as a public URL. No lifecycle support. 48h TTL. Not a persistent BUS backend.

---

## 3. Canonical Recommended Backend

```
CANONICAL_BACKEND:     workspace_filesystem (direct_file)
CANONICAL_PATH:        /home/ubuntu/yos-bus-runtime
CANONICAL_ENV_VAR:     YOS_BUS_RUNTIME_ROOT
CANONICAL_INIT:        python3 01_BACKBONE/BUS/08_TOOLS/bus.py init-runtime --root /home/ubuntu/yos-bus-runtime
```

**Rationale:** Fastest, most reliable, full lifecycle support, cross-session persistence proven, zero external dependencies, already operational.

---

## 4. Fallback Chain

```
1. workspace_filesystem    → /home/ubuntu/yos-bus-runtime  [preferred]
2. git                     → yj000018/YOS main             [fallback — external write proven]
3. manus_api_task          → task.sendMessage              [external write path — async]
4. manus_webhook           → last-mile notification only   [report delivery]
5. connector_bridge        → GitHub/GDrive (if enabled)    [optional]
6. mcp_bridge              → if MCP server configured      [future]
7. blob_payload            → S3 CDN (one-shot only)        [emergency]
```

---

## 5. External Write Path (ChatGPT → Manus BUS)

The critical missing link: ChatGPT cannot write directly to `/home/ubuntu/yos-bus-runtime/` without:

**Option A — Manual Upload Bridge (current)**
```
ChatGPT writes MP file → User uploads to Manus → bus.py ingest → BUS inbox
```

**Option B — Manus API task.create (recommended upgrade)**
```
ChatGPT calls POST /v2/task.create with packet as message content
→ Manus agent receives → places packet in /home/ubuntu/yos-bus-runtime/inbox/mpm/
→ bus.py claim → process
```

**Option C — MCP Server (future)**
```
Configure filesystem MCP server → ChatGPT calls MCP tool write_file
→ packet placed in /home/ubuntu/yos-bus-runtime/inbox/mpm/
```

**Option D — GitHub Connector (alternative)**
```
Enable GitHub connector → ChatGPT commits MP to ready queue via connector
→ Manus git pull → process
```

---

## 6. BUS Operations Matrix

| Operation | Filesystem | Git | API task | Webhook | MCP | S3 CDN |
|---|---|---|---|---|---|---|
| BUS.write(packet) | ✅ direct | ✅ commit | ✅ async | ❌ | ⚡ potential | ⚡ partial |
| BUS.claim(domain) | ✅ mv inbox→ws | ✅ mv+commit | ❌ | ❌ | ⚡ potential | ❌ |
| BUS.publish(report) | ✅ mv ws→out | ✅ mv+commit | ✅ async | ✅ push | ⚡ potential | ⚡ url |
| BUS.read_latest_report() | ✅ file read | ✅ file read | ✅ listMessages | ✅ push | ⚡ potential | ⚡ if url known |

Legend: ✅ = supported | ⚡ = potential/partial | ❌ = not supported
