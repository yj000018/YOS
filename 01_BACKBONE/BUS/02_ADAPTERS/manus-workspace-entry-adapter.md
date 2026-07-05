# YOS BUS — Manus Workspace Entry Adapter

**Status:** probe_required
**Backend ID:** manus_workspace
**Versioned:** no
**Transport commit required:** no

---

## Role

Potential online Manus server/workspace transport. If Manus exposes a persistent workspace path accessible across sessions, this adapter enables direct packet placement without Git.

---

## Status

Not yet probed. Candidate for future gate: `MPM-{DATE}-YOS-BUS-MANUS-WORKSPACE-PROBE-GATE`.

---

## Requirements (when probed)

- Manus persistent workspace path (e.g., `/home/ubuntu/yos-bus-runtime/` on sandbox)
- Cross-session accessibility confirmed
- `YOS_BUS_RUNTIME_ROOT` pointing to persistent path

---

## Notes

The direct-file adapter with a persistent path (`/home/ubuntu/yos-bus-runtime/`) may already satisfy this use case.
See: `06_INDEXES/direct-file-runtime-probe-latest.json` — recommended persistent alternative.

Do not claim cross-session Manus cloud persistence unless actually tested.
