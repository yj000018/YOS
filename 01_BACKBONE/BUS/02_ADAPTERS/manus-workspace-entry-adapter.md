# YOS BUS — Manus Workspace Entry Adapter

**Status:** candidate
**Backend ID:** manus_workspace
**Versioned:** no
**Transport commit required:** no
**Probe Gate:** MPM-20260705-YOS-BUS-MANUS-WORKSPACE-PROBE-GATE
**Probe Date:** 2026-07-05

---

## Role

Manus sandbox filesystem (`/home/ubuntu/`) as a persistent, addressable BUS runtime backend.
Enables direct packet placement without Git transport.

---

## Probe Results (2026-07-05)

### Probe A — Manus Workspace Filesystem

| Check | Result |
|---|---|
| FS available | yes |
| Stable path | `/home/ubuntu/` |
| Same-session read/write | yes |
| Lifecycle move (inbox→workspace→outbox) | yes |
| Cross-session persistence | **proven** |

**Evidence of cross-session persistence:**
- `/home/ubuntu/yos-monorepo/` — created in prior sessions, persists across hibernation cycles
- `/home/ubuntu/.gitconfig` — modified 2026-07-02, persists
- `/home/ubuntu/.env` — modified 2026-07-01, persists
- `/home/ubuntu/.manus/` — persists
- Disk: 40GB root, 30GB free — stable storage

**Recommended persistent runtime path:**
```
/home/ubuntu/yos-bus-runtime/
```
This path was initialized and validated in this probe gate.

### Probe B — MCP Bridge

| Check | Result |
|---|---|
| manus-mcp-cli available | yes (`/usr/local/bin/manus-mcp-cli`) |
| MCP servers configured | no (empty `servers.json`) |
| File write via MCP | unknown — no servers configured |
| Stable MCP addressing | unknown |
| MCP backend status | probe_required |

**Note:** `manus-mcp-cli` is installed and functional. No MCP servers are currently configured in this sandbox session. File write via MCP is architecturally possible but not demonstrated.

### Probe C — Manus API / Upload / Storage

| Check | Result |
|---|---|
| `manus-upload-file` available | yes |
| S3/CDN upload | yes — public URL returned (`files.manuscdn.com`) |
| CDN URL accessible | yes (HTTP 200, no auth required) |
| CDN URL pattern | `session_file/<session_id>/<random_id>.ext` |
| CDN URL persistence | unknown — likely session-scoped |
| Manus API docs found | yes (`open.manus.im`) |
| `file.upload` endpoint | yes — POST `/v2/file.upload` |
| File expiration | 48 hours after upload |
| Workspace write via API | no — API files are task-attached, not workspace-persistent |
| Workspace read via API | no |
| Stable task context | no — file IDs are ephemeral |
| API backend status | probe_required |

**Key finding:** `manus-upload-file` uploads to S3 CDN and returns a public URL. This URL is publicly readable but not workspace-persistent. The Manus API `file.upload` endpoint attaches files to tasks (48h TTL), not to a persistent workspace. This does not satisfy BUS inbox/workspace/outbox lifecycle requirements.

---

## Classification

```
MANUS_WORKSPACE_BACKEND_CLASSIFICATION: candidate
```

**Rationale:**
- Probe A (filesystem): cross-session persistence PROVEN, lifecycle SUPPORTED → strong evidence
- Missing proof: ChatGPT/external LLM direct write into `/home/ubuntu/yos-bus-runtime/` without manual upload
- The manual upload bridge (`bus.py ingest`) currently fills this gap
- Upgrade path to `production_candidate`: demonstrate programmatic write from ChatGPT side (API or MCP)

---

## Current Operational Configuration

```bash
export YOS_BUS_RUNTIME_ROOT=/home/ubuntu/yos-bus-runtime
```

This is the recommended persistent runtime root. Initialize with:
```bash
python3 01_BACKBONE/BUS/08_TOOLS/bus.py init-runtime --root /home/ubuntu/yos-bus-runtime
```

---

## Upgrade Path to `production_candidate`

One of the following must be demonstrated:
1. ChatGPT writes directly to `/home/ubuntu/yos-bus-runtime/inbox/mpm/` via Manus API `task.create` + file attachment
2. An MCP server is configured that exposes a file-write resource
3. A Manus API endpoint is found that writes to persistent workspace path

---

## Notes

- `manus-upload-file` (S3/CDN) is NOT a BUS backend — it provides public URLs, not persistent workspace paths
- `manus-mcp-cli` is available but no servers configured — future MCP probe gate may unlock this
- The direct-file adapter at `/home/ubuntu/yos-bus-runtime/` is the current validated operational backend
- See: `06_INDEXES/manus-workspace-probe-latest.json` for machine-readable probe summary
