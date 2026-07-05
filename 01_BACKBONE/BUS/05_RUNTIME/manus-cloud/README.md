# BUS Runtime: manus-cloud (manus_workspace)

**Status:** candidate
**Versioned:** no
**Probe Gate:** MPM-20260705-YOS-BUS-MANUS-WORKSPACE-PROBE-GATE
**Probe Date:** 2026-07-05

---

## Overview

The Manus sandbox filesystem (`/home/ubuntu/`) is a persistent, addressable BUS runtime backend.
Cross-session persistence is proven. Lifecycle operations are supported.

Missing proof: external (ChatGPT) direct write without manual upload.
Current operational fallback: `bus.py ingest` (manual upload bridge).

---

## Probe Results Summary

| Question | Answer |
|---|---|
| Stable persistent workspace across sessions? | **yes** — `/home/ubuntu/` persists across hibernation |
| Read/write known inbox path without Git? | **yes** — direct filesystem operations |
| ChatGPT direct write into Manus path? | **no** — manual upload bridge required |
| Same path accessible in future Manus task? | **yes** — persistence proven |
| File latency vs Git? | **substantially faster** — ~43ms vs seconds |
| Reliability/access boundaries? | sandbox-scoped, no external network access required |

---

## Recommended Runtime Path

```bash
export YOS_BUS_RUNTIME_ROOT=/home/ubuntu/yos-bus-runtime
python3 01_BACKBONE/BUS/08_TOOLS/bus.py init-runtime --root /home/ubuntu/yos-bus-runtime
```

---

## Classification

```
candidate
```

Upgrade to `production_candidate` requires: ChatGPT direct write demonstrated (via Manus API task.create + file attachment, or MCP server).

---

## Related

- `02_ADAPTERS/manus-workspace-entry-adapter.md` — full probe details
- `06_INDEXES/manus-workspace-probe-latest.json` — machine-readable probe summary
- `02_ADAPTERS/manual-upload-entry-adapter.md` — current operational fallback
