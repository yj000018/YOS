# YOS BUS — First/Last Mile Protocol

**Version:** 1.0.0
**Status:** active
**Created:** 2026-07-05
**Gate:** MPM-20260705-YOS-BUS-FIRST-LAST-MILE-INTEGRATION-GATE

---

## Doctrine

```
BUS.write(packet)          = canonical first-mile abstraction
BUS.read_latest_report()   = canonical last-mile abstraction
```

Backend-specific details are behind adapters. The caller never knows which backend is active.

---

## First Mile

### Problem

Current unwanted workflow:
```
ChatGPT creates file -> user downloads -> user uploads to Manus -> Manus runs MP
```

### Target Workflows

**Preferred future:**
```
ChatGPT/MPM -> BUS entry backend -> BUS inbox/mpm -> Manus MP
```

**Current safe fallback (manual upload bridge):**
```
ChatGPT creates downloadable packet
-> user uploads to Manus
-> Manus: bus.py ingest --domain mpm --file <uploaded_file>
-> packet lands in BUS runtime inbox/mpm
-> MP executes
```

**Git fallback:**
```
ChatGPT writes Git BUS inbox/mpm or MPM/ready
-> Manus MP
```

### Entry Backend Priority

```
1. direct_file     (YOS_BUS_RUNTIME_ROOT — validated)
2. manus_workspace (probe_required)
3. google_drive    (candidate)
4. nas             (optional)
5. git             (fallback — versioned, slow)
6. manual_upload   (fallback — human bridge)
7. blob_payload    (experimental)
```

---

## Last Mile

### Problem

MPR must be readable by ChatGPT/A&G without search.

### Target

```
MPR -> latest-mpr.json fast path -> optional BUS outbox/mpm pointer -> A&G review
```

### Rules

1. Read `01_BACKBONE/MPM/06_REPORTS/indexes/latest-mpr.json` first.
2. Read `latest_mpr_path` from JSON.
3. No search by default.
4. Only search if latest pointer is missing or corrupt.

---

## Environment Variables

| Variable | Purpose |
|---|---|
| `YOS_BUS_RUNTIME_ROOT` | Direct-file runtime root |
| `YOS_BUS_ENTRY_BACKEND` | Override entry backend selection |
| `YOS_BUS_REPORT_BACKEND` | Override report backend selection |

---

## Related Files

| File | Role |
|---|---|
| `00_PROTOCOLS/bus-entry-adapter-protocol.md` | Entry adapter contract |
| `00_PROTOCOLS/bus-report-adapter-protocol.md` | Report adapter contract |
| `05_RUNTIME/entry-backend-registry.json` | Entry backend registry |
| `05_RUNTIME/report-backend-registry.json` | Report backend registry |
| `08_TOOLS/bus.py` | CLI — write, ingest, latest-report, report-pointer |
