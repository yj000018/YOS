# yOS MPM — Claude Adapter (MPC)

> **yOS MPM — Mega Prompt Manager** (Inter-LLM Prompt Runtime & Relay System)
> Claude Adapter — Packet type: `MPC`
> Version: 1.1.0 — Patch: YOS-MPM-NAMING-PATCH-2026-07-04
> Legacy alias: `mpm-claude-adapter.md` (preserved)

---

## 1. Role of Claude in the yOS MPM System

Claude can act as:
- **MPC Author:** Draft MPC packets for complex architecture, critique, or long-analysis tasks.
- **Architect & Guardian Reviewer:** Review executed packets and issue decisions.
- **Executor (via API):** Execute sprint or run packets directly if integrated.

## 2. How to Create a Packet (Claude)

```
Create MPC run <gate/task description>
Create MPM run <gate/task description>
```

Claude will:
1. Draft the packet with valid YAML frontmatter (see `mpm-frontmatter-schema.md`), including `packet_type: MPC` and `target_llm: Claude`.
2. Set `created_by: Claude`, `executor: Manus` (or `Claude` if self-executing).
3. Output the packet as a Markdown code block for copy-paste into Git, or write it directly if Git access is available.
4. Instruct the user to save it to `02_MPMs/drafts/` and add it to the ledger JSON.

## 3. How to Review a Packet (Claude)

Follow the same protocol as `mpm-chatgpt-guardian-review-protocol.md`. Claude must:
1. Read the ledger JSON.
2. Read the packet and report.
3. Check boundary compliance.
4. Issue a decision.
5. Update the ledger JSON.

## 4. How to Avoid Copy-Paste Loops

Claude must never re-paste the full packet content into a new conversation without first checking the ledger. Claude must always reference `mpm_id` when discussing a packet, and always check `status` before acting on it.

## 5. Claude-Specific Commands

```
Review latest executed packet
Review latest executed MPM
Review MPM <mpm_id>
Create MPC run <task>
Create MPM run <task>
Create MPC sprint <task>
```

## 6. Claude Project Integration

If Claude has a Project with the yOS MPM runtime files attached:
- The Project instructions should reference `mpm-frontmatter-schema.md`, `mpm-status-lifecycle.md`, and `yos-mpm-naming-doctrine.md`.
- Claude should always check the ledger JSON before creating or reviewing packets.
- The Project should not store packet content directly — it should reference Git paths.
