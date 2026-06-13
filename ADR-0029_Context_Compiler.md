---
id: yos-adr-0029-context-compiler
title: ADR-0029 Context Compiler
type: adr
status: ACCEPTED
date: '2026-06-13'
owner: Brahma
parent: '[[02_ADR_MOC]]'
tags:
- '#accepted'
- '#adr'
- '#ccr'
- '#memory'
- '#yos'
aliases:
- Context Compiler
source_branch: y-os-doctrine
canonical: true
implements:
- '[[CCR_Runtime]]'
- '[[Context_Pack]]'
governed_by:
- '[[Lakshmi_Governance]]'
executed_by:
- '[[Brahma]]'
- '[[Lakshmi]]'
compiles:
- '[[Context_Pack]]'
injects:
- '[[Mission]]'
---

# ADR-0029: Context Compiler Runtime v1 (CCR-001)

**Date:** 2026-06-13  
**Status:** Accepted  
**Owner:** Chief Architect (Brahma)  
**Mission:** CCR-001

## Context

Y-OS routes capabilities to workers (ART) and workers to models (CRT). However, models require context to execute effectively. Relying on raw conversation history leads to cognitive drift, vendor lock-in, and constraint violation.

## Decision

Y-OS adopts the **Context Compiler Runtime (CCR)** as the canonical layer between the Registry/Memory and model execution.

The Context Compiler transforms scattered organizational memory into an optimal, stateless **Context Pack** for a specific mission, worker, capability, and model.

## Key Rules

1. **Registry stores truth.**
2. **Memory stores accumulated knowledge.**
3. **Context Compiler selects what the model needs now.**

## Validation

A Context Pack must be able to replace raw conversation history for a selected task, preserving enough context without the noise. Lakshmi will score Context Pack quality based on 10 dimensions (Coverage, Relevance, Freshness, etc.).

## Consequences

- All future Y-ORC executions will inject a Context Pack into the LLM prompt.
- Y-OS is fully decoupled from stateful chat threads.
- Token usage becomes predictable and manageable via Token Budgeting.


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **compiles:** [[Context_Pack]]
- **executed_by:** [[Brahma]]
- **executed_by:** [[Lakshmi]]
- **governed_by:** [[Lakshmi_Governance]]
- **implements:** [[CCR_Runtime]]
- **implements:** [[Context_Pack]]
- **injects:** [[Mission]]
