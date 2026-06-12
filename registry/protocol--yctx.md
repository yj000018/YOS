---
id: protocol--yctx
type: protocol
name: Y-CTX
slug: yctx
status: active
visibility: public
version: "1.0"
description: Context extraction and assembly module. Reads Y-MEM and produces Context Packs consumed by Y-ORC.
question: What context is relevant?
produces: Context Pack
consumes: Y-MEM output
equivalent_role: Analyst, Briefing Officer
tags: [core, context, deterministic, backend]
module_owner: Y-CTX
created_at: "2026-06-12"
---

# Y-CTX — Context Module

Y-CTX is a system module (deterministic). It does not orchestrate. It assembles context.

## Responsibilities
- Extract relevant context from Y-MEM for a given situation
- Assemble Context Pack (structured object passed to Y-ORC)
- Filter and rank context by relevance

## Non-Responsibilities
- Does not orchestrate actions (Y-ORC)
- Does not store memory (Y-MEM)
- Does not exercise judgment (agents)

## Interface
- Input: situation description, intent, session state
- Output: Context Pack { memory_snippets, active_projects, relevant_objects, constraints }
