# YOS BUS — MPR Report Pointer Template

**Usage:** Use this template when emitting a last-mile report pointer for A&G consumption.

---

## Pointer Format (plain text)

```
MPR_DOMAIN: mpm
MPR_MP_ID: {MP_ID}
MPR_PATH: {canonical_mpr_path}
MPR_COMMIT: {commit_hash}
MPR_STATUS: {executed_awaiting_architect_guardian_review}
MPR_UPDATED_AT: {ISO8601}
MPR_FAST_PATH: 01_BACKBONE/MPM/06_REPORTS/indexes/latest-mpr.json
```

---

## Pointer Format (JSON)

```json
{
  "mpr_domain": "mpm",
  "mpr_mp_id": "{MP_ID}",
  "mpr_path": "{canonical_mpr_path}",
  "mpr_commit": "{commit_hash}",
  "mpr_status": "executed_awaiting_architect_guardian_review",
  "mpr_updated_at": "{ISO8601}",
  "mpr_fast_path": "01_BACKBONE/MPM/06_REPORTS/indexes/latest-mpr.json"
}
```

---

## Notes

- Always read `latest-mpr.json` first — do not search
- This pointer is for A&G review routing only
- Do not commit runtime pointer files to Git
