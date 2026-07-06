# DISC-007 — Workspace Filesystem is Canonical BUS Runtime

**ID:** DISC-007
**Title:** /home/ubuntu/ persists cross-session — canonical BUS runtime
**Status:** canonical
**First seen:** MPM-20260705-YOS-BUS-MANUS-WORKSPACE-PROBE-GATE-REPORT.md

---

## The Discovery

Empirical test confirmed: /home/ubuntu/ persists across Manus sandbox sessions.
/tmp does NOT persist (discovered in DIRECT-FILE-PROBE-GATE).

## Canonical Consequence

`/home/ubuntu/yos-bus-runtime` = canonical persistent BUS runtime.

## Rule

Never use /tmp for BUS runtime.

## Sources

- MPM-20260705-YOS-BUS-MANUS-WORKSPACE-PROBE-GATE-REPORT.md
- MPM-20260705-YOS-BUS-DIRECT-FILE-RUNTIME-PROBE-GATE-REPORT.md
- direct-file-runtime-probe-latest.json
