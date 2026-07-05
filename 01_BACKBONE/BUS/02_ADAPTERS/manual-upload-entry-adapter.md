# YOS BUS — Manual Upload Entry Adapter

**Status:** fallback
**Backend ID:** manual_upload
**Versioned:** no
**Transport commit required:** no

---

## Role

Human bridge: user uploads MP file to Manus, then Manus ingests it into BUS.

This is the **current operational fallback** until a direct write backend is available.

---

## Workflow

```
1. ChatGPT generates MP packet
2. User downloads packet from ChatGPT
3. User uploads packet to Manus (attachment)
4. Manus runs:
   bus.py ingest --domain mpm --file <uploaded_file_path>
5. Packet lands in BUS runtime inbox/mpm (direct_file) or Git fallback
6. MP executes via BUS-first resolution
```

---

## bus.py ingest semantics

```bash
bus.py ingest --domain mpm --file /home/ubuntu/upload/MPM-XXXX.md
```

- Copies file into `$YOS_BUS_RUNTIME_ROOT/inbox/mpm/` if runtime root is set
- Falls back to `01_BACKBONE/BUS/04_DOMAINS/mpm/inbox/` (Git domain)
- Logs event to `latest-entry-event.json`

---

## Notes

- This adapter requires no configuration beyond Manus file access
- No API keys, no cloud credentials
- Latency: human-dependent (seconds to minutes)
- Reliability: high (human-verified delivery)
