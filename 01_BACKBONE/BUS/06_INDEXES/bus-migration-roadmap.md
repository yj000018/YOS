# YOS BUS — Backend Migration Roadmap

**Source Gate:** MPM-20260705-YOS-MANUS-CONNECTIVITY-CENSUS-GATE
**Date:** 2026-07-05

---

## Current State (Phase 0 — Operational)

```
CANONICAL_BACKEND:     workspace_filesystem (direct_file)
EXTERNAL_WRITE:        manual_upload bridge (bus.py ingest)
FALLBACK:              git (ChatGPT → commit → Manus git pull)
STATUS:                operational
```

**Operational flow:**
```
ChatGPT writes MP → User uploads → Manus bus.py ingest → /home/ubuntu/yos-bus-runtime/inbox/mpm/
Manus bus.py claim → process → MPR → /home/ubuntu/yos-bus-runtime/outbox/mpm/
Manus git commit + push → ChatGPT reads MPR via GitHub
```

---

## Phase 1 — API Task Write (Near-term)

**Gate:** `MPM-{DATE}-YOS-BUS-MANUS-API-TASK-WRITE-GATE`
**Target:** Eliminate manual upload bridge

**New flow:**
```
ChatGPT POST /v2/task.create { message: { content: "<MP packet>" } }
→ Manus agent receives → places packet in /home/ubuntu/yos-bus-runtime/inbox/mpm/
→ bus.py claim → process → MPR
→ Manus git commit + push OR task.sendMessage with MPR content
→ ChatGPT reads MPR
```

**Requirements:**
- Manus API key in ChatGPT environment
- Manus agent skill/instruction to relay task message → BUS inbox
- Rate limit: 10/min task.create

**Classification upgrade:** `manus_api_task` → `production_ready`

---

## Phase 2 — Webhook Last-Mile (Near-term)

**Gate:** `MPM-{DATE}-YOS-BUS-WEBHOOK-LAST-MILE-GATE`
**Target:** Push notification when MPR is ready

**New flow:**
```
Manus completes MPR → task_stopped webhook fires → ChatGPT endpoint receives
→ ChatGPT reads MPR from task.listMessages or GitHub
```

**Requirements:**
- Public HTTPS endpoint for ChatGPT (or n8n webhook URL)
- webhook.create registration with Manus API key

**Classification upgrade:** `manus_webhook` → `production_ready`

---

## Phase 3 — MCP Server (Medium-term)

**Gate:** `MPM-{DATE}-YOS-BUS-MCP-SERVER-SETUP-GATE`
**Target:** Direct write from external LLM via MCP protocol

**New flow:**
```
ChatGPT MCP tool call: write_file("/home/ubuntu/yos-bus-runtime/inbox/mpm/MP.md", content)
→ MCP server writes file → bus.py claim → process
```

**Requirements:**
- Configure filesystem MCP server in /home/ubuntu/.mcp/servers.json
- MCP server pointing to /home/ubuntu/yos-bus-runtime
- ChatGPT MCP client configuration

**Classification upgrade:** `mcp_bridge` → `production_candidate`

---

## Phase 4 — Connector Bridge (Optional)

**Gate:** `MPM-{DATE}-YOS-BUS-CONNECTOR-BRIDGE-GATE`
**Target:** GitHub/Google Drive connector as BUS transport

**Requirements:**
- Enable GitHub or Google Drive connector in Manus config
- Connector-based write protocol

**Classification upgrade:** `connector_bridge` → `production_ready`

---

## Summary Timeline

| Phase | Gate | Priority | Effort | Impact |
|---|---|---|---|---|
| 0 | Current (operational) | — | done | baseline |
| 1 | API Task Write | HIGH | low | eliminates manual upload |
| 2 | Webhook Last-Mile | HIGH | low | push notification |
| 3 | MCP Server | MEDIUM | medium | direct write |
| 4 | Connector Bridge | LOW | medium | alternative |

---

## Canonical Recommendation

**Short-term (now):** Use `workspace_filesystem` + `manual_upload` bridge + `git` fallback.

**Near-term (Phase 1+2):** Add `manus_api_task` for external write + `manus_webhook` for last-mile.

**Long-term (Phase 3):** MCP server for zero-friction direct write.
