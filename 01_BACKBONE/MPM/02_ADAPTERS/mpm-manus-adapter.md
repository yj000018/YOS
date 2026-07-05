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



---

## Optimized Local Runtime (v2 — 2026-07-05)

**Canonical wording — apply to all executor contexts:**

- `ready/*.md` is the **active queue signal** — physical presence triggers execution eligibility.
- `mp-ledger.json` remains the **JSON-first registry/history/status source of truth**.
- Executors with a local clone **batch all file writes** and push **one commit per MP execution**.
- **GitHub online/API file-by-file mode** is fallback, not preferred.
- `latest-mpr.json` is the **default fast path** for ChatGPT/Architect & Guardian MPR review.
- **ChatGPT GitHub connector calls should be minimized** — Manus/local git is the preferred writer.
- **Ledger backward compatibility:** if `ready/*.md` and ledger disagree, prefer physical `ready/*.md` for queue discovery, then reconcile ledger.

**Local CLI:** `python 01_BACKBONE/MPM/08_TOOLS/mpm.py <command>`

See: `08_TOOLS/README.md`

