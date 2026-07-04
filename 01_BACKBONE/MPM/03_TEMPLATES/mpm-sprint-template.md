---
mpm_id: MPM-YYYYMMDD-SPRINT-SLUG
title: "<Short task title>"
mode: sprint
status: draft
created_by: "<ChatGPT | Claude | Yannick>"
created_at: "YYYY-MM-DDTHH:MM:SSZ"
executor: Manus
guardian_required: false
source_scope: "kap-control-plane only"
forbidden_actions:
  - no source mutation
expected_outputs:
  - "06_REPORTS/<OUTPUT-FILE>.md"
expected_mpr_path: "01_BACKBONE/MPM/06_REPORTS/awaiting-review/<MP_ID>-REPORT.md"
log_pointer_path: "08_LOGS/<category>/<MP_ID>-REPORT-POINTER.md"
report_path: "01_BACKBONE/MPM/06_REPORTS/awaiting-review/<MP_ID>-REPORT.md"
guardian_decision: pending
---

# MPM Sprint: <Short task title>

## 1. Objective
<One sentence: what needs to be done.>

## 2. Scope
<What is in scope. Be specific.>

## 3. Forbidden Actions
- No source mutation.
- <Any sprint-specific restrictions.>

## 4. Expected Output
- `06_REPORTS/<OUTPUT-FILE>.md`

## 5. Stop Condition
After producing the output, stop.
