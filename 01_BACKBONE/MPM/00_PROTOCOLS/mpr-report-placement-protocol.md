# MPR Report Placement Protocol

> **System:** yOS MPM — Mega Prompt Manager
> **Version:** 1.0.0
> **Status:** canonical
> **Created:** 2026-07-05

---

## Definitions

**MPR** = Mega Prompt Report — the execution/output artifact produced after an MP packet is executed by a target LLM.

**MP** = Mega Prompt — the generic packet type.
**Packet codes:** `MP` (generic), `MPM` (Manus), `MPC` (Claude), `MPX` (ChatGPT/A&G), `MPG` (Gemini), `MPP` (Perplexity).

---

## Canonical MPR Location

```
01_BACKBONE/MPM/06_REPORTS/
├── awaiting-review/    ← primary drop zone after execution
├── reviewed/           ← after Architect & Guardian review
├── archived/           ← long-term archive
└── indexes/            ← MPR-INDEX.md + mpr-index.json
```

**Rule:** Every MP/MPM/MPC/MPX/MPG/MPP execution MUST produce its primary MPR under:
```
01_BACKBONE/MPM/06_REPORTS/awaiting-review/<MP_ID>-REPORT.md
```

---

## 08_LOGS Role

`08_LOGS/` is the **log and pointer layer only**. It must NOT be the canonical home of any MPR.

`08_LOGS/` may contain:
- Migration logs
- Event logs
- Short pointer files referencing canonical MPRs
- Summaries

**Rule:** If an MPR appears in `08_LOGS/`, it must be a pointer file only, not the canonical copy.

---

## Pointer File Convention

When a log entry references an MPR, create a pointer file at:
```
08_LOGS/<category>/<MP_ID>-REPORT-POINTER.md
```

Pointer file content:
```markdown
# MPR Pointer — <MP_ID>-REPORT

> This file is a log pointer only. It is not the canonical MPR.

Canonical MPR:
01_BACKBONE/MPM/06_REPORTS/awaiting-review/<MP_ID>-REPORT.md
```

---

## MPR Lifecycle

```
Execution → awaiting-review/ → reviewed/ → archived/
```

| Stage | Folder | Who moves it |
| :--- | :--- | :--- |
| After execution | `awaiting-review/` | Target LLM (Manus) |
| After A&G review | `reviewed/` | Manus (on A&G instruction) |
| Long-term | `archived/` | Manus (on A&G instruction) |

---

## MPR Frontmatter (required fields)

Every canonical MPR must include these fields in its header:

```
report_id: <MP_ID>-REPORT
report_type: MPR
mpm_id: <MP_ID>
status: awaiting_architect_guardian_review | architect_guardian_accepted | archived
canonical_mpr_path: 01_BACKBONE/MPM/06_REPORTS/awaiting-review/<MP_ID>-REPORT.md
log_pointer_path: 08_LOGS/<category>/<MP_ID>-REPORT-POINTER.md
branch: <branch>
commit: <commit_hash>
```

---

## Domain-Specific Reports

Domain-specific modules (KAP, ELYSIUM, etc.) may keep secondary reports under their own module path. However:

**Rule:** The canonical MPR pointer MUST still exist under `01_BACKBONE/MPM/06_REPORTS/`.

---

## Enforcement

This protocol is referenced by:
- `mpm-output-contract.md`
- `mpm-manus-fetch-and-run-protocol.md`
- `mpm-sprint-template.md`, `mpm-run-template.md`, `mpm-marathon-template.md`
- `mp-ledger.json` schema (`canonical_mpr_path` field)

---

*mpr-report-placement-protocol.md — yOS MPM v1.0.0 — 2026-07-05*
