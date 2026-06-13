---
id: yos-adr-0028-crt-runtime-v1
title: ADR-0028 CRT Runtime v1
type: adr
status: ACCEPTED
date: '2026-06-13'
version: v1
owner: Brahma
parent: '[[02_ADR_MOC]]'
tags:
- '#accepted'
- '#adr'
- '#lineage'
- '#memory'
- '#yos'
aliases:
- CRT Runtime v1
source_branch: y-os-doctrine
canonical: true
---

# ADR-0028: CRT Runtime v1

**Date:** 2026-06-13  
**Status:** Accepted  
**Owner:** Chief Architect (Brahma)  
**Mission:** CRT-001

## Purpose

CRT (Capability Routing Table) is the final layer of the Y-OS routing stack. It resolves a **Worker** to a specific **Provider** and **Model**. It is the only component in Y-OS that knows about LLMs.

## Architecture

```
Capability → ART → Worker → CRT → { provider, model, fallback }
```

CRT is a pure resolver. It has no state, no memory, no reasoning. It reads `model_registry.json` and returns a routing decision.

## Strict Separation of Concerns

| Component | Knows | Does NOT Know |
| :--- | :--- | :--- |
| Y-ORC | Capabilities | Workers, Models |
| ART | Workers | Models, Providers |
| **CRT** | **Models, Providers** | **Capabilities, Business Logic** |

## Responsibilities

- Read `model_registry.json`.
- Accept a `worker` name as input.
- Return `{ provider, model, fallback }`.
- Log every resolution to `crt_execution_log.jsonl`.

## Non-Responsibilities

CRT is explicitly NOT responsible for:
- Cost optimization
- Benchmarking or scoring
- Autonomous model tuning
- RL or model voting
- Swarm coordination
- Any orchestration logic

## Data Structures

**Input:** `worker: str`

**Output:**
```json
{
  "worker": "Krishna",
  "provider": "Anthropic",
  "model": "Claude Opus",
  "fallback": "GPT-5",
  "reason": "default"
}
```

## Validation Criteria

1. Y-ORC is unchanged when `model_registry.json` is modified.
2. ART is unchanged when `model_registry.json` is modified.
3. Only `model_registry.json` needs to change to swap providers.
4. Lineage is preserved across all provider swaps.
5. Execution log captures every resolution.

## Future Roadmap

- CRT v2: Add `cost_tier` field for budget-aware routing.
- CRT v3: Add `context_window` field for task-size routing.
- CRT v4: Add `fallback_chain` for multi-provider resilience.
