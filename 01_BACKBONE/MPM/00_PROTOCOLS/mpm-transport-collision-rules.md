# yOS MPM — Transport Collision Rules

> **System:** yOS MPM — Mega Prompt Manager
> **Version:** 1.0.0
> **Status:** canonical
> **Source:** Architect & Guardian decision 2026-07-04 — TRANSPORT-TEST deviation patch

---

## Context

A **transport collision** occurs when both GGG (ChatGPT Architect & Guardian) and Manus independently write to the same MPM file path in the same Git repository. This was observed in `MPM-20260704-GGG-MANUS-TRANSPORT-TEST`:

- GGG committed the MPM to `02_MPMs/ready/` via GitHub connector
- Manus simultaneously moved it to `02_MPMs/running/` locally
- Result: duplicate file in both `ready/` and `running/` after merge

---

## Rule 1 — Source of Truth for GGG-Authored MPMs

**The JSON ledger is always the source of truth for MPM status.**

- GGG is the **author** of MPMs.
- Manus is the **executor** and **state manager**.
- GGG writes MPM files to `02_MPMs/ready/` via GitHub connector.
- Manus owns all status transitions: `ready → running → executed_awaiting_guardian_review`.
- GGG must **never** write directly to `running/`, `executed/`, `blocked/`, or `superseded/`.
- GGG must **never** update the JSON ledger directly — only Manus updates the ledger.

---

## Rule 2 — Import / Claim Semantics

When Manus picks up an MPM from `ready/`:

1. **Read** `inter_llm_execution_ledger.json` — confirm the MPM is registered with `status: ready_for_execution` or `status: ready`.
2. **If not registered:** add entry to JSON ledger with `status: running` before moving the file.
3. **Claim** the MPM by moving it from `ready/` to `running/` atomically (single `git mv`).
4. **Update** JSON ledger: `status → running`, `started_at → now`, `mpm_path → 02_MPMs/running/...`.
5. **Regenerate** MD ledger view.
6. **Commit** both the file move and the ledger update in a single commit.
7. **Push** immediately — do not defer.

The single-commit claim prevents GGG from committing a conflicting state between Manus's move and push.

---

## Rule 3 — Ready/Running File Move Rules

| Action | Who | When | File location |
| :--- | :--- | :--- | :--- |
| Create MPM | GGG | Authoring | `02_MPMs/drafts/` |
| Mark ready | GGG | Authorized for execution | `02_MPMs/ready/` |
| Claim (move to running) | **Manus only** | Before execution starts | `02_MPMs/running/` |
| Mark executed | **Manus only** | After execution | `02_MPMs/executed/` |
| Mark blocked | **Manus only** | On blocker | `02_MPMs/blocked/` |
| Architect & Guardian review | GGG | After execution | reads from `executed/` |
| Mark accepted/rejected | GGG → Manus | Architect & Guardian decision | Manus updates JSON ledger |

**GGG must never write to `running/`, `executed/`, `blocked/`, or `superseded/`.**

---

## Rule 4 — Duplicate Detection

Before claiming an MPM, Manus must check:

```python
# Pseudocode
if mpm_id in ledger and ledger[mpm_id]['status'] in ['running', 'executed_awaiting_guardian_review', 'guardian_accepted']:
    # Already claimed — do not re-claim
    raise CollisionError(f"{mpm_id} already in status {ledger[mpm_id]['status']}")

if file_exists('02_MPMs/running/' + mpm_filename):
    # File already in running — check ledger consistency
    if ledger[mpm_id]['status'] != 'running':
        # Ledger out of sync — update ledger to match file reality
        ledger[mpm_id]['status'] = 'running'
        # Log deviation
```

If a duplicate is found in both `ready/` and `running/`:
1. Keep the `running/` copy (Manus claimed it).
2. Delete the `ready/` copy.
3. Log the collision in the execution report.
4. Do not delete without logging.

---

## Rule 5 — Merge Conflict Handling

If a `git push` fails due to divergent branches:

1. **Pull with `--no-rebase -X ours`** — Manus's local state (JSON ledger, file moves) takes precedence.
2. **Verify** the JSON ledger is intact after merge: `python3 -c "import json; json.load(open('00_META/inter_llm_execution_ledger.json'))"`.
3. **If JSON is corrupted** by merge: restore from the last known good commit (`git show HEAD~1:00_META/inter_llm_execution_ledger.json`), re-apply the update, recommit.
4. **Remove duplicates** created by the merge (e.g., file in both `ready/` and `running/`).
5. **Log all deviations** in the execution report under "Deviation Log".
6. **Push** the resolved state.

**Never use `git push --force` on `master`.** Use merge with `-X ours` only.

---

## Rule 6 — Ledger-First Recovery Procedure

If the ledger and filesystem are out of sync (e.g., after a failed push, a partial merge, or a session interruption):

1. **Read** `inter_llm_execution_ledger.json` — this is the source of truth.
2. **For each entry**, verify the file exists at `mpm_path`.
3. **If file is missing**: log as `file_missing` deviation; do not recreate without authorization.
4. **If file is in wrong folder**: move to match `mpm_path` in ledger; commit.
5. **If status in ledger says `running` but file is in `executed/`**: update ledger status to `executed_awaiting_guardian_review`; commit.
6. **Regenerate MD view** after any recovery.
7. **Commit recovery** with message: `recovery: ledger-filesystem sync — [mpm_id]`.

---

## Summary Table

| Scenario | Detection | Resolution |
| :--- | :--- | :--- |
| GGG commits to `ready/` while Manus is claiming | Push rejection | Pull `--no-rebase -X ours`; remove `ready/` duplicate |
| Duplicate in `ready/` + `running/` | Pre-claim check | Keep `running/`, delete `ready/`, log deviation |
| JSON ledger corrupted by merge | JSON parse error | Restore from `git show HEAD~1`, re-apply, recommit |
| Ledger says `running`, file in `executed/` | Recovery scan | Update ledger status, regenerate MD, commit |
| GGG writes to `running/` directly | File in wrong folder | Move to `ready/` or `executed/` per ledger; log |
| Status transition skipped | Ledger audit | Reconstruct from git log; update ledger; log |

---

## Patch Applied To

- `mpm-manus-fetch-and-run-protocol.md` — Step 2 now includes "claim" semantics (single-commit move + ledger update)
- `mpm-chatgpt-guardian-review-protocol.md` — GGG export rules: write to `ready/` only, never to `running/`/`executed/`

---

*Generated by Manus — MPM-20260704-TRANSPORT-COLLISION-PATCH — 2026-07-04*
