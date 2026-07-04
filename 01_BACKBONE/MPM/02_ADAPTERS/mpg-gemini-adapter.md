# yOS MPM — Gemini Adapter (MPG)

> **yOS MPM — Mega Prompt Manager** (Inter-LLM Prompt Runtime & Relay System)
> Canonical adapter file for packet type: `MPG` (Mega Prompt Gemini)
> Version: 1.1.0 — Patch: YOS-MPM-NAMING-PATCH-2026-07-04

---

## 1. Role of Gemini in the yOS MPM System

Gemini is used for:
- Large-context document processing (>200K tokens)
- Google Workspace integrations
- Multimodal tasks (image + text)
- Long-form synthesis requiring massive context windows

## 2. How to Create an MPG Packet

```
Create MPG run <task>
Create MPG sprint <task>
```

Set `packet_type: MPG`, `target_llm: Gemini` in frontmatter.

## 3. Recommended Commands

```
Create MPG run <task>
Route task to best packet type: <task>
```

See also: `yos-mpm-naming-doctrine.md`
