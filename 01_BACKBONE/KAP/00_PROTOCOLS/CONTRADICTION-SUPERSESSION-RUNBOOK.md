# CONTRADICTION-SUPERSESSION-RUNBOOK

> Y-OS / KAP Cognitive Architecture
> Gate: PROCESS-DOCS-RUNBOOK-GATE
> Last Updated: 2026-07-03

## 1. Core Philosophy

In a complex, evolving cognitive architecture, contradictions are not errors—they are evidence of learning, pivoting, or refining. Supersession is the natural lifecycle of an active doctrine becoming historical context. We do not delete the past; we contextualize it.

## 2. Identifying Contradictions

A contradiction exists when two Claims assert mutually exclusive facts or architectural decisions.
- **Example:** Claim A states "Notion is the primary database." Claim B states "Git is the primary database."
- **Action:** Both Claims must be marked with `truth_status: contradicted`. A new entry must be created in `CONTRADICTION-SUPERSESSION-REGISTRY.md` linking the two claims.

## 3. Identifying Supersession

Supersession occurs when a newer, validated Claim or Decision Thread explicitly replaces an older one.
- **Example:** Decision Thread DT-002 explicitly states "We are moving from Notion to Git for all architecture documents."
- **Action:** The older Claim/Thread is marked `truth_status: superseded`. The newer Claim/Thread is marked `truth_status: validated`. An entry is created in `CONTRADICTION-SUPERSESSION-REGISTRY.md` documenting the transition.

## 4. Required Fields for Registry Entries

When logging a contradiction or supersession in `CONTRADICTION-SUPERSESSION-REGISTRY.md`, include:
- `entry_id`: Unique identifier (e.g., `CS-001`).
- `type`: `contradiction` or `supersession`.
- `entities_involved`: Array of `claim_id`, `thought_line_id`, or `decision_thread_id`.
- `resolution_status`: `unresolved`, `resolved_by_supersession`, `resolved_by_synthesis`.
- `rationale`: Brief explanation of the conflict or the reason for supersession.

## 5. Avoiding "Newer = Better" Errors

Do not automatically assume a newer document supersedes an older one unless the newer document explicitly addresses the change. A newer document might simply be a draft or an unvalidated thought experiment. When in doubt, flag as a `contradiction` and trigger human review.

## 6. Review Triggers

All unresolved contradictions involving `active_doctrine` Claims must trigger a Guardian Architect review before any further synthesis can occur in that domain.
