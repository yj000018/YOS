# yOS MPM Coordinator-Worker Pattern

> **yOS MPM — Mega Prompt Manager** (Inter-LLM Prompt Runtime & Relay System)
> marathon mode architecture
> Version: 1.1.0 — Patch: YOS-MPM-NAMING-PATCH-2026-07-04

---

## 1. Overview

The Coordinator-Worker pattern is used exclusively in `marathon` mode. It allows a single yOS MPM packet (typically an MPM/Manus packet) to orchestrate multiple parallel lanes of work while maintaining strict boundary compliance and producing a coherent final report.

## 2. Roles

### Coordinator Task
- Reads the MPM and decomposes it into bounded Worker Tasks (lanes).
- Assigns each Worker Task a specific scope and output set.
- Monitors Worker Task completion.
- Performs final consolidation of all Worker outputs.
- Produces the final Architect & Guardian review package.
- **Does not execute Worker-level work directly.**

### Worker Task
- Receives a bounded scope from the Coordinator.
- Executes its lane independently.
- Writes outputs to its designated paths.
- Reports status (PASS / PARTIAL / BLOCKED) to the Coordinator.
- **Does not consolidate or synthesize across lanes.**

## 3. Lane Structure

Each lane in a marathon MPM must define:

| Field | Description |
| :--- | :--- |
| Lane ID | e.g., `A`, `B`, `C` |
| Gate Name | e.g., `YWORLD-GITHUB-CANONICAL-MERGE-PLAN-GATE` |
| Scope | What this lane is allowed to touch |
| Forbidden Actions | Lane-specific prohibitions |
| Expected Outputs | List of file paths |
| Status | `PASS` / `PARTIAL_PASS` / `BLOCKED` / `NOT_STARTED` |

## 4. Consolidation Protocol

After all Workers complete (or safely checkpoint):
1. Coordinator reads all Worker output paths.
2. Coordinator writes the Lane Status Table in the final report.
3. Coordinator inserts commit hashes into the report.
4. Coordinator updates the ledger JSON.
5. Coordinator marks the MPM `executed_awaiting_guardian_review`.

## 5. Blocked Lane Protocol

If a Worker lane is blocked:
1. Worker writes a blocker note to its output path.
2. Worker reports `BLOCKED` to the Coordinator.
3. Coordinator records the blocker in the final report.
4. Coordinator continues with remaining lanes (unless the MPM specifies `stop_on_first_block: true`).
5. Final report status reflects the block (e.g., `PARTIAL_PASS`).
