# yOS MPM Frontmatter Schema

> **SOURCE OF TRUTH: `mpm-frontmatter-schema.json`**
> This Markdown is a generated view. Never edit it directly.
> Version: 1.1.0 — Patch: YOS-MPM-NAMING-PATCH-2026-07-04

---

Every yOS MPM packet file must begin with a YAML frontmatter block conforming to this schema.

## Required Fields

| Field | Type | Description |
| :--- | :--- | :--- |
| `mpm_id` | `string` | Unique ID. Pattern: `<PACKET_CODE>-YYYYMMDD-SLUG` (e.g., `MPM-20260704-RUNTIME-PACK`, `MPX-20260704-REVIEW`) |
| `title` | `string` | Human-readable title (min 5 chars) |
| `mode` | `enum` | `sprint` \| `run` \| `marathon` |
| `status` | `enum` | See `mpm-status-lifecycle.md` |
| `created_by` | `string` | Authoring LLM or human (e.g., `ChatGPT`, `Claude`, `Yannick`) |
| `created_at` | `date-time` | ISO 8601 creation timestamp |
| `executor` | `string` | Executing agent (e.g., `Manus`, `Claude`) |
| `guardian_required` | `boolean` | Whether Architect & Guardian review is required |

## Optional Fields

| Field | Type | Description |
| :--- | :--- | :--- |
| `packet_type` | `enum` | `MP` \| `MPM` \| `MPC` \| `MPX` \| `MPG` \| `MPP` |
| `target_llm` | `enum` | `Generic` \| `Manus` \| `Claude` \| `ChatGPT` \| `Gemini` \| `Perplexity` |
| `source_scope` | `string` | Which corpora are in scope |
| `forbidden_actions` | `string[]` | Explicit list of forbidden actions |
| `expected_outputs` | `string[]` | Expected output file paths |
| `report_path` | `string` | Path to the gate/execution report |
| `execution_commit` | `string` | Git commit hash in `yos-cognitive-os` |
| `control_plane_commit` | `string` | Git commit hash in `kap-control-plane` |
| `supersedes` | `string` | `mpm_id` of superseded packet |
| `superseded_by` | `string` | `mpm_id` of superseding packet |
| `started_at` | `date-time` | Execution start timestamp |
| `completed_at` | `date-time` | Execution completion timestamp |
| `guardian_decision` | `enum` | `pending` \| `accepted` \| `rejected` \| `patched` |
| `next_gate` | `string` | Recommended next gate |
| `notes` | `string` | Operational notes |

## Packet Type / Target LLM Mapping

| `packet_type` | `target_llm` | Primary Use |
| :--- | :--- | :--- |
| `MP` | `Generic` | Fallback or abstract Mega Prompt |
| `MPM` | `Manus` | Execution, Git/files, long-run, multi-thread |
| `MPC` | `Claude` | Deep critique, writing, long analysis |
| `MPX` | `ChatGPT` | Architecture, Architect & Guardian review, prompt generation |
| `MPG` | `Gemini` | Google/multimodal/large-context work |
| `MPP` | `Perplexity` | Web research and cited external research |

> `MPA` is deprecated. Use `MP` instead.

## Example Frontmatter

```yaml
---
mpm_id: MPM-20260704-EXAMPLE-RUN
packet_type: MPM
target_llm: Manus
title: "Example KAP Run Gate"
mode: run
status: draft
created_by: ChatGPT
created_at: "2026-07-04T09:00:00Z"
executor: Manus
guardian_required: true
source_scope: kap-control-plane only
forbidden_actions:
  - no source mutation
  - no synthesis
expected_outputs:
  - 06_REPORTS/EXAMPLE-RUN-GATE-REPORT.md
report_path: 06_REPORTS/EXAMPLE-RUN-GATE-REPORT.md
guardian_decision: pending
---
```
