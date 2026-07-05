# YOS BUS — Entry Adapter Protocol

**Version:** 1.0.0
**Status:** active
**Created:** 2026-07-05
**Gate:** MPM-20260705-YOS-BUS-FIRST-LAST-MILE-INTEGRATION-GATE

---

## Abstraction

```
BUS.write(packet, domain, backend?) -> places packet in BUS inbox/domain
```

Every entry adapter must implement this contract regardless of backend.

---

## Adapter Contract

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| `domain` | string | yes | BUS domain (mpm, kap, general, …) |
| `file` | path | yes | Source file to ingest |
| `backend` | string | no | Override backend (default: auto-select from registry) |

### Output

| State | Meaning |
|---|---|
| `placed` | Packet is in `inbox/domain/` of selected backend |
| `error` | Placement failed — fallback triggered |

### Fallback Chain

If selected backend fails:
1. Try next backend in priority order
2. Log fallback event to `06_INDEXES/latest-entry-event.json`
3. Never silently drop packet

---

## Adapters

| Adapter | File | Status |
|---|---|---|
| direct_file | `02_ADAPTERS/direct-file-entry-adapter.md` | validated |
| manus_workspace | `02_ADAPTERS/manus-workspace-entry-adapter.md` | probe_required |
| google_drive | `02_ADAPTERS/google-drive-entry-adapter.md` | candidate |
| git | `02_ADAPTERS/git-entry-adapter.md` | fallback |
| manual_upload | `02_ADAPTERS/manual-upload-entry-adapter.md` | fallback |

---

## CLI

```bash
# Auto-select backend
bus.py ingest --domain mpm --file <path>

# Explicit backend
bus.py write --domain mpm --file <path> --backend direct_file
```

---

## Event Logging

After every ingest/write, update:
```
01_BACKBONE/BUS/06_INDEXES/latest-entry-event.json
```
