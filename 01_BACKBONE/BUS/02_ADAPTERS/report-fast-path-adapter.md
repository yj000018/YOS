# YOS BUS — Report Fast Path Adapter

**Status:** active
**Backend ID:** latest_mpr_json
**Type:** last-mile report adapter

---

## Role

Canonical last-mile adapter. Reads `latest-mpr.json` to resolve the latest MPR path without search.

---

## Fixed Path

```
01_BACKBONE/MPM/06_REPORTS/indexes/latest-mpr.json
  -> latest_mpr_path
```

This path is **fixed, non-search-based, and non-negotiable**.

---

## Resolution Order

```
1. latest_mpr_json   — primary (this adapter)
2. bus_outbox_pointer — BUS outbox/mpm latest-report pointer
3. git_fetch_direct  — git fetch + direct path
4. manual_paste      — last resort
```

---

## CLI

```bash
bus.py latest-report
# -> reads latest-mpr.json, prints path + metadata

bus.py report-pointer --domain mpm
# -> emits BUS-friendly pointer for A&G consumption
```

---

## ChatGPT/A&G Usage

```
MPR = read 01_BACKBONE/MPM/06_REPORTS/indexes/latest-mpr.json
   -> read latest_mpr_path
   -> A&G review
```

No search. No glob. Fixed path always.
