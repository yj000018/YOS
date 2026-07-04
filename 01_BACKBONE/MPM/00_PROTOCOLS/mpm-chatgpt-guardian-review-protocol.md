# yOS MPM — ChatGPT Architect & Guardian Review Protocol (MPX Adapter)

> **yOS MPM — Mega Prompt Manager** (Inter-LLM Prompt Runtime & Relay System)
> ChatGPT Adapter — Packet type: `MPX` — Architect & Guardian Role
> Version: 1.2.0 — Patch: TRANSPORT-COLLISION-PATCH-2026-07-04

---

## 1. Purpose

This protocol allows ChatGPT (or any Architect & Guardian LLM) to review executed MPMs without copy-paste. The Guardian issues a single command; the protocol defines exactly what to read, how to evaluate, and what to output.

## 2. Trigger Command

```
Review latest executed packet
Review latest executed MPM
```

Or for a specific packet:

```
Review MPM <mpm_id>
```

## 3. Review Steps

### Step 1 — Open the Ledger
Read `kap-control-plane/00_META/inter_llm_execution_ledger.json`.

### Step 2 — Find the MPM to Review
Find the latest entry with `status: executed_awaiting_guardian_review`.

### Step 3 — Read the MPM and Report
- Read the MPM file at `mpm_path`.
- Read the execution report at `report_path`.

### Step 4 — Check Boundary Compliance
Verify the report's **Boundary Confirmations** section. All 10 permanent boundaries must be explicitly confirmed.

### Step 5 — Evaluate Outputs
Verify that all files listed in `expected_outputs` exist and are non-empty.

### Step 6 — Issue Decision

**Accept:**
- Update ledger JSON: `guardian_decision → accepted`, `status → guardian_accepted`.
- Write a brief acceptance note to `06_REPORTS/GUARDIAN-DECISION-<MPM_ID>.md`.
- Recommend the next MPM.

**Reject:**
- Update ledger JSON: `guardian_decision → rejected`, `status → guardian_rejected`.
- Write a patch instruction to `06_REPORTS/GUARDIAN-DECISION-<MPM_ID>.md`.
- Move MPM back to `02_MPMs/drafts/`.
- Update ledger JSON: `status → draft`.

**Patch (minor fix, re-run not required):**
- Apply the patch directly to the relevant files.
- Update ledger JSON: `guardian_decision → patched`, `status → guardian_accepted`.

### Step 7 — Update the Ledger JSON
Regenerate the MD ledger view from JSON. Commit.

### Step 8 — Recommend Next MPM
State the recommended next gate or MPM. Never approve execution gates if only a plan review is appropriate.

---

## 4. How to Create a Packet (ChatGPT)

```
Create MPX run <gate/task description>
Create MPM run <gate/task description>
```

ChatGPT will:
1. Draft the packet content (mission, objectives, outputs, forbidden actions).
2. Format it with valid YAML frontmatter including `packet_type: MPX` (or `MPM` if targeting Manus) and `target_llm`.
3. Provide it as a downloadable Markdown file or paste it into the conversation.
4. Instruct Manus to save it to `02_MPMs/drafts/` and add it to the ledger JSON.
5. Mark it `ready_for_execution` when satisfied.

---

## 5. GGG Export Rules — Collision Prevention

> **Critical:** These rules prevent ready/running state collisions. See `mpm-transport-collision-rules.md` for full details.

| Rule | Description |
| :--- | :--- |
| **Write to `ready/` only** | GGG may only commit MPM files to `02_MPMs/ready/` (or `02_MPMs/drafts/`). Never to `running/`, `executed/`, `blocked/`, or `superseded/`. |
| **Never update the JSON ledger** | Only Manus updates `inter_llm_execution_ledger.json`. GGG reads it; never writes it. |
| **Never write to `running/`** | Once Manus claims an MPM (moves it to `running/`), GGG must not touch that file. |
| **One MPM per commit** | When exporting via GitHub connector, commit one MPM file at a time to minimize collision surface. |
| **Check ledger before export** | Before committing a new MPM to `ready/`, read the ledger to confirm the `mpm_id` does not already exist. |
| **Architect & Guardian decision → tell Manus** | Architect & Guardian decisions (accept/reject) are communicated to Manus verbally or via a new MPX packet. Manus updates the JSON ledger. GGG does not update the ledger directly. |
