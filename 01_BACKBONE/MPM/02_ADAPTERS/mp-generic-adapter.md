# yOS MPM — Generic Adapter (MP)

> **yOS MPM — Mega Prompt Manager** (Inter-LLM Prompt Runtime & Relay System)
> Canonical adapter file for packet type: `MP` (Mega Prompt generic)
> Version: 1.1.0 — Patch: YOS-MPM-NAMING-PATCH-2026-07-04
> Replaces: ~~MPA (Mega Prompt Any)~~ — DEPRECATED

---

## 1. Purpose

`MP` is the fallback or abstract packet type for tasks that do not have a specific target LLM, or for routing decisions that have not yet been made.

## 2. How to Create an MP Packet

```
Create MP sprint <task>
Create MP run <task>
```

Set `packet_type: MP`, `target_llm: Generic` in frontmatter.

## 3. Routing

When an `MP` packet is ready for execution, the executor should either:
- Route it to the best available LLM based on the task description.
- Or use `Route task to best packet type: <task>` to get a recommendation.

## 4. Deprecated: MPA

`MPA` (Mega Prompt Any) is deprecated. All new generic packets must use `MP`.

See also: `yos-mpm-naming-doctrine.md`
