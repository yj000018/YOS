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



---

## MP Runtime Resolution

All MP/MPM runtime resolution occurs inside repo `yj000018/YOS`.

| Command | Runtime |
| :--- | :--- |
| `MP` / `MP next` / `MP queue` | `yj000018/YOS @ main / 01_BACKBONE/MPM/` |
| `MP branch=<name>` | `yj000018/YOS @ <name> / 01_BACKBONE/MPM/` |
| `MP queue branch=<name>` | `yj000018/YOS @ <name> / 01_BACKBONE/MPM/` |

**Default runtime:** `YOS/main/01_BACKBONE/MPM/`
**Explicit branch runtime:** `YOS/<branch>/01_BACKBONE/MPM/`
**Legacy bootstrap:** `kap-control-plane` is fallback only — never default runtime.

See: `07_BRANCHES/BRANCH-RUNTIME-POLICY.md`

