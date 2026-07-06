# DISC-009 — Async Task Relay Pattern

**ID:** DISC-009
**Title:** ChatGPT cannot write directly to Manus workspace
**Status:** candidate
**First seen:** MPM-20260705-YOS-MANUS-API-CAPABILITY-VERIFICATION-GATE-REPORT.md

---

## The Discovery

No Manus API endpoint allows direct workspace write from ChatGPT.
file.upload → S3 CDN (not workspace).
task.create → creates task, does not write files.

## Canonical Pattern

```
ChatGPT POST task.sendMessage
  + structured_output_schema
→ Manus agent receives
→ Manus agent writes to /home/ubuntu/yos-bus-runtime/inbox/mpm/
→ bus.py claim → process → MPR
→ Manus git push OR task.sendMessage with MPR
→ ChatGPT reads MPR
```

## Sources

- MPM-20260705-YOS-MANUS-API-CAPABILITY-VERIFICATION-GATE-REPORT.md
- manus-api-capability-matrix.md
- bus-migration-roadmap.md (Phase 1)
