# yOS MPM — Generic LLM Adapter (MP)

> **yOS MPM — Mega Prompt Manager** (Inter-LLM Prompt Runtime & Relay System)
> Generic Adapter — Packet type: `MP` — For any LLM (Gemini, Grok, Mistral, etc.)
> Version: 1.2.0 — Patch: DOCTRINE-PATCH-2026-07-04
> Legacy alias: `mpm-generic-llm-adapter.md` (preserved)

---

## 1. Purpose

This adapter allows any LLM to participate in the yOS MPM system without requiring a custom integration. It defines the minimum protocol any LLM must follow.

> **Bootstrap note:** `kap-control-plane` is the current runtime repo. Final home: `yOS Backbone / MPM` (pending Architect & Guardian approval of `MPM-BACKBONE-TOPOLOGY-DECISION-GATE`).

## 2. Minimum Protocol

### To Create an MPM
1. Draft the MPM content following the structure in `mpm-frontmatter-schema.md`.
2. Set `created_by: <LLM name>`, `executor: Manus` (or the intended executor).
3. Output the MPM as a Markdown file or code block.
4. Instruct the user to save it to `02_MPMs/drafts/` in `kap-control-plane`.
5. Instruct the user to add an entry to `inter_llm_execution_ledger.json`.

### To Mark an MPM Ready
1. Verify the MPM frontmatter is complete.
2. Instruct the user to update `status: ready_for_execution` in the ledger JSON.
3. Instruct the user to move the file to `02_MPMs/ready/`.

### To Review an MPM
1. Ask the user to provide the contents of `inter_llm_execution_ledger.json`.
2. Find the latest `executed_awaiting_guardian_review` entry.
3. Ask the user to provide the MPM file and report file.
4. Follow the review steps in `mpm-chatgpt-guardian-review-protocol.md`.
5. Output the decision as a structured Markdown block.
6. Instruct the user to update the ledger JSON.

## 3. Anti-Patterns to Avoid

- Do not re-draft an MPM that already exists in the ledger.
- Do not issue execution commands — only Manus executes.
- Do not modify source corpora directly.
- Do not skip the ledger update step.

## 4. Recommended Commands

**Canonical pattern:**
```
MPM sprint: <mission>
MPM run: <mission>
MPM marathon: <mission>
```

**Other commands:**
```
MPM                              (opens MPM Manager menu)
Show MPM queue
Review latest executed MPM
Create MP sprint <task>
Create MPM run <task>
Route task to best packet type: <task>
```

**Review role:** When acting as Architect & Guardian, follow `mpm-chatgpt-guardian-review-protocol.md`.
