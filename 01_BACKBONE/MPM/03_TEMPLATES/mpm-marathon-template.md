---
mpm_id: MPM-YYYYMMDD-MARATHON-SLUG
title: "<Big objective title>"
mode: marathon
status: draft
created_by: "<ChatGPT | Claude | Yannick>"
created_at: "YYYY-MM-DDTHH:MM:SSZ"
executor: Manus
guardian_required: true
source_scope: "<kap-control-plane | yos-cognitive-os | none>"
forbidden_actions:
  - no source mutation
  - no synthesis
  - no merge
  - no canonicalization
expected_outputs:
  - "<Lane A output path>"
  - "<Lane B output path>"
  - "06_REPORTS/<MARATHON-NAME>-BATCH-REPORT.md"
  - "06_Reports/Gates/KAP-MORNING-LAUNCHPAD-AFTER-<MARATHON-NAME>.md"
expected_mpr_path: "01_BACKBONE/MPM/06_REPORTS/awaiting-review/<MP_ID>-REPORT.md"
log_pointer_path: "08_LOGS/<category>/<MP_ID>-REPORT-POINTER.md"
report_path: "01_BACKBONE/MPM/06_REPORTS/awaiting-review/<MP_ID>-REPORT.md"
execution_commit: null
control_plane_commit: null
guardian_decision: pending
---

# MPM Marathon: <Big objective title>

## 0. Mission
<2-3 sentences describing the overall objective.>

## 1. Core Doctrine
<Relevant doctrine, constraints, and principles.>

## 2. Coordinator-Worker Pattern
Use Coordinator Task + parallel bounded Worker Tasks. Workers write separate outputs. Coordinator consolidates. See `mpm-coordinator-worker-pattern.md`.

---

## 3. Lane A — <LANE-A-GATE-NAME>

**Scope:** <What Lane A is allowed to touch.>

**Required outputs:**
```text
<path/to/lane-a-output1.md>
<path/to/lane-a-output2.json>
```

**Forbidden:**
- <Lane A specific restrictions.>

---

## 4. Lane B — <LANE-B-GATE-NAME>

**Scope:** <What Lane B is allowed to touch.>

**Required outputs:**
```text
<path/to/lane-b-output1.md>
```

**Forbidden:**
- <Lane B specific restrictions.>

---

## 5. Final Batch Report

Create:
```text
06_REPORTS/<MARATHON-NAME>-BATCH-REPORT.md
```

Include:
1. Final batch status.
2. Lane status table: `| Lane | Gate | Status | Outputs | Commit | Next Step |`
3. Files created/updated.
4. Commits.
5. Key findings.
6. Blockers.
7. Boundary confirmations (explicit list).
8. Recommended next gates.
9. Architect & Guardian review checklist.

## 6. Status Options

```text
<MARATHON-NAME>_BATCH_COMPLETED_SUCCESSFULLY_AWAITING_GUARDIAN_REVIEW
<MARATHON-NAME>_BATCH_PARTIAL_PASS_AWAITING_GUARDIAN_REVIEW
<MARATHON-NAME>_BATCH_BLOCKED_AWAITING_GUARDIAN_REVIEW
```

## 7. Stop Condition
After producing the final batch report and morning launchpad, stop. Wait for Architect & Guardian review.


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

