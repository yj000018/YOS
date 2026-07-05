# YOS BUS — Report Adapter Protocol

**Version:** 1.0.0
**Status:** active
**Created:** 2026-07-05
**Gate:** MPM-20260705-YOS-BUS-FIRST-LAST-MILE-INTEGRATION-GATE

---

## Abstraction

```
BUS.read_latest_report() -> returns latest MPR path + metadata
```

---

## Fixed Path Doctrine

The canonical last-mile path is **fixed and non-search-based**:

```
01_BACKBONE/MPM/06_REPORTS/indexes/latest-mpr.json
  -> latest_mpr_path
```

No directory search. No glob. No heuristics.

---

## Resolution Order

```
1. latest_mpr_json   — read 01_BACKBONE/MPM/06_REPORTS/indexes/latest-mpr.json
2. bus_outbox_pointer — check BUS outbox/mpm for latest report pointer
3. git_fetch_direct  — git fetch + read path directly
4. manual_paste      — human pastes MPR content (last resort)
```

---

## CLI

```bash
# Read latest MPR pointer (fixed path)
bus.py latest-report

# Emit BUS-friendly domain report pointer
bus.py report-pointer --domain mpm
```

---

## Output Format

`latest-report` emits:
```json
{
  "latest_mp_id": "...",
  "latest_mpr_path": "...",
  "commit": "...",
  "updated_at": "..."
}
```

`report-pointer` emits:
```
MPR_DOMAIN: mpm
MPR_PATH: 01_BACKBONE/MPM/06_REPORTS/awaiting-review/...
MPR_COMMIT: ...
MPR_UPDATED_AT: ...
```

---

## Event Logging

After every report read, update:
```
01_BACKBONE/BUS/06_INDEXES/latest-report-event.json
```
