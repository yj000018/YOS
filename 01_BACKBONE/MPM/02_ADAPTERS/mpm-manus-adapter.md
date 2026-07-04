# yOS MPM — Manus Adapter (MPM)

> **yOS MPM — Mega Prompt Manager** (Inter-LLM Prompt Runtime & Relay System)
> Canonical adapter file for packet type: `MPM` (Mega Prompt Manus)
> Version: 1.1.0 — Patch: YOS-MPM-NAMING-PATCH-2026-07-04

---

This is the canonical adapter file for `MPM` (Mega Prompt Manus) packets.

The full fetch-and-run protocol is defined in: `mpm-manus-fetch-and-run-protocol.md`

See also: `yos-mpm-naming-doctrine.md` for packet type definitions.

---

## MPR Canonical Path

After execution, the target LLM writes the canonical Mega Prompt Report (MPR) to:
```
01_BACKBONE/MPM/06_REPORTS/awaiting-review/
```
The source LLM retrieves the MPR from that canonical path for review.
See: `00_PROTOCOLS/mpr-report-placement-protocol.md`

