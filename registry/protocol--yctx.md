---
id: protocol--yctx
title: protocol--yctx
type: protocol
status: active
date: '2026-06-13'
version: '1.0'
owner: Manus Y-OS
tags:
- core
- context
- deterministic
- backend
source_branch: y-os-doctrine
canonical: true
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
