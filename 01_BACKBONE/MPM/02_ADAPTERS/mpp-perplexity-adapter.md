# yOS MPM — Perplexity Adapter (MPP)

> **yOS MPM — Mega Prompt Manager** (Inter-LLM Prompt Runtime & Relay System)
> Canonical adapter file for packet type: `MPP` (Mega Prompt Perplexity)
> Version: 1.1.0 — Patch: YOS-MPM-NAMING-PATCH-2026-07-04

---

## 1. Role of Perplexity in the yOS MPM System

Perplexity is used for:
- Web research with cited sources
- Real-time information retrieval
- Fact-checking against live web content
- Competitive intelligence and market research

## 2. How to Create an MPP Packet

```
Create MPP run <task>
Create MPP sprint <task>
```

Set `packet_type: MPP`, `target_llm: Perplexity` in frontmatter.

## 3. Recommended Commands

```
Create MPP sprint <research task>
Route task to best packet type: <task>
```

See also: `yos-mpm-naming-doctrine.md`
