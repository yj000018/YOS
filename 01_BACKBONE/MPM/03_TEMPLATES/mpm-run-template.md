---
mpm_id: MPM-YYYYMMDD-RUN-SLUG
title: "<Gate or task title>"
mode: run
status: draft
created_by: "<ChatGPT | Claude | Yannick>"
created_at: "YYYY-MM-DDTHH:MM:SSZ"
executor: Manus
guardian_required: true
source_scope: "<kap-control-plane only | yos-cognitive-os | none>"
forbidden_actions:
  - no source mutation
  - no synthesis
  - no merge
expected_outputs:
  - "<path/to/output1.md>"
  - "<path/to/output2.json>"
  - "06_REPORTS/<GATE-NAME>-GATE-REPORT.md"
expected_mpr_path: "01_BACKBONE/MPM/06_REPORTS/awaiting-review/<MP_ID>-REPORT.md"
log_pointer_path: "08_LOGS/<category>/<MP_ID>-REPORT-POINTER.md"
report_path: "01_BACKBONE/MPM/06_REPORTS/awaiting-review/<MP_ID>-REPORT.md"
execution_commit: null
control_plane_commit: null
guardian_decision: pending
next_gate: "<NEXT-GATE-NAME>"
---

# MPM Run: <Gate or task title>

## 1. Role
You are Manus acting as KAP Executor under ChatGPT Architect & Guardian supervision.

## 2. Objective
<2-3 sentences describing the goal of this gate.>

## 3. Core Doctrine
<Any relevant doctrine or constraints specific to this gate.>

## 4. Required Outputs

```text
<path/to/output1.md>
<path/to/output2.json>
06_REPORTS/<GATE-NAME>-GATE-REPORT.md
```

## 5. Forbidden Actions
- No source mutation.
- No synthesis.
- No merge.
- <Gate-specific restrictions.>

## 6. Status Options

```text
<GATE-NAME>_GATE_PASS
<GATE-NAME>_GATE_PASS_WITH_MINOR_GAPS
<GATE-NAME>_GATE_PARTIAL_REQUIRES_PATCH
<GATE-NAME>_GATE_FAIL_BOUNDARY_BREACHED
```

## 7. Stop Condition
After producing the gate report, stop. Wait for Architect & Guardian review.


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

