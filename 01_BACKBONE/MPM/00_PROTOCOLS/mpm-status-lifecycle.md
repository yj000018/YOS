# yOS MPM Status Lifecycle

> **yOS MPM — Mega Prompt Manager** (Inter-LLM Prompt Runtime & Relay System)
> Source: `mpm-frontmatter-schema.json`
> Version: 1.2.0 — Patch: DOCTRINE-PATCH-2026-07-04

---

## 1. Status Definitions

| Status | Folder | Description |
| :--- | :--- | :--- |
| `draft` | `02_MPMs/drafts/` | MPM is being authored. Not yet ready for execution. |
| `ready_for_execution` | `02_MPMs/ready/` | MPM is complete and authorized for execution. |
| `running` | `02_MPMs/running/` | Manus is actively executing this MPM. |
| `blocked` | `02_MPMs/blocked/` | Execution halted due to a blocker. Awaiting resolution. |
| `executed_awaiting_guardian_review` | `02_MPMs/executed/` | Execution complete. Awaiting Architect & Guardian review. |
| `guardian_accepted` | `02_MPMs/reviewed/` | Architect & Guardian accepted the outputs. Ready for archiving. |
| `guardian_rejected` | `02_MPMs/reviewed/` | Architect & Guardian rejected. MPM returns to `draft` for patching. |
| `superseded` | `02_MPMs/superseded/` | This MPM has been replaced by a newer version. |
| `archived` | `02_MPMs/archive/` | Accepted and archived. Immutable historical record. |

---

## 2. Allowed Transitions

```
draft                          → ready_for_execution
ready_for_execution            → running
running                        → executed_awaiting_guardian_review
running                        → blocked
executed_awaiting_guardian_review → guardian_accepted
executed_awaiting_guardian_review → guardian_rejected
guardian_rejected              → draft
guardian_accepted              → archived
any                            → superseded
```

---

## 3. Transition Rules

**draft → ready_for_execution**
Requires: MPM frontmatter complete and valid against `mpm-frontmatter-schema.json`. Architect & Guardian or author explicitly marks it ready.

**ready_for_execution → running**
Triggered by: Manus executing `Run next ready MPM`. Manus moves the file to `running/` and updates the ledger JSON.

**running → executed_awaiting_guardian_review**
Triggered by: Manus completing execution and producing the required outputs and report. Manus updates frontmatter and ledger JSON.

**running → blocked**
Triggered by: Manus encountering an unresolvable blocker. Manus writes a blocker report and updates ledger JSON.

**executed_awaiting_guardian_review → guardian_accepted / guardian_rejected**
Triggered by: Architect & Guardian LLM reviewing the report and issuing a decision. Architect & Guardian updates ledger JSON.

**guardian_rejected → draft**
Triggered by: Architect & Guardian issuing a patch instruction. MPM returns to `drafts/` for revision.

**guardian_accepted → archived**
Triggered by: `Archive accepted MPMs` command. Files moved to `archive/`.

**any → superseded**
Can be triggered at any stage if a newer MPM explicitly supersedes this one.

---

## 4. Enforcement

- Status transitions must always be reflected in `inter_llm_execution_ledger.json` **first**.
- The MD ledger view is regenerated from JSON — never edited directly.
- File location must match the status (e.g., `running` MPMs live in `02_MPMs/running/`).

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

