# yOS MPM Output Contract

> **yOS MPM — Mega Prompt Manager** (Inter-LLM Prompt Runtime & Relay System)
> Version: 1.1.0 — Patch: YOS-MPM-NAMING-PATCH-2026-07-04

---

## 1. Principle

Every yOS MPM packet execution must produce a verifiable, durable output set. "Done" means committed to Git with a hash, not just written to disk.

## 2. Mandatory Outputs (All Modes — All Packet Types)

| Output | Description |
| :--- | :--- |
| Gate/Execution Report (`.md`) | Structured report at `report_path` in the MPM frontmatter |
| Updated packet frontmatter | `status`, `completed_at`, `execution_commit`, `control_plane_commit` filled |
| Updated ledger JSON | `inter_llm_execution_ledger.json` entry updated |
| Git commit | All outputs committed to `yos-cognitive-os` and/or `kap-control-plane` |

## 3. Mode-Specific Outputs

### sprint
- Minimal report (can be brief).
- No gate report template required.
- Single commit acceptable.

### run
- Full gate report following the standard template.
- All expected outputs listed in `expected_outputs` must be present.
- Two commits: one for `yos-cognitive-os`, one for `kap-control-plane`.

### marathon
- Full gate report.
- Lane status table in the report.
- All expected outputs per lane.
- Commit hashes inserted into the report.
- Morning Launchpad recommended.

## 4. Report Template (run / marathon)

```markdown
# Gate Report: <GATE-NAME>

## 1. Gate Metadata
- Gate ID:
- Execution Date:
- Mode:
- Status: <STATUS_CODE>

## 2. Objectives

## 3. Outputs Generated

## 4. Key Findings

## 5. Boundary Confirmations

## 6. Next Steps
```

## 5. Commit Convention

```
<REPO>: <MPM_ID> — <short description>
```

Example:
```
yos-cognitive-os: MPM-20260704-RUNTIME-PACK — Runtime pack files created
kap-control-plane: MPM-20260704-RUNTIME-PACK — Ledger and schemas committed
```
