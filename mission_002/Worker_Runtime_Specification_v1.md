---
id: yos-worker-runtime-specification-v1
title: Worker Runtime Specification v1
type: runtime_spec
status: ACCEPTED
mission: MISSION-002
date: '2026-06-13'
version: v1
owner: Manus Y-OS
parent: '[[03_Missions_MOC]]'
related_missions:
- '[[mission_002]]'
tags:
- '#accepted'
- '#ccr'
- '#lineage'
- '#runtime'
- '#yos'
aliases:
- MISSION-002
source_branch: y-os-doctrine
canonical: true
implements:
- '[[CCR_Runtime]]'
- '[[Context_Pack]]'
governed_by:
- '[[Lakshmi_Governance]]'
executed_by:
- '[[Brahma]]'
- '[[Ganesha]]'
- '[[Lakshmi]]'
- '[[Saraswati]]'
- '[[Hanuman]]'
- '[[Krishna]]'
compiles:
- '[[Context_Pack]]'
---

# Worker Runtime Specification v1

**Date:** 2026-06-13  
**Mission:** MISSION-002  
**Status:** Accepted

---

## Overview

This specification defines the contract for real worker execution in Y-OS. Workers are cognitive agents that receive a structured Context Pack, invoke a real model, and produce an Artifact.

---

## Worker Interface Contract

Every worker MUST implement the following interface:

```python
class WorkerInterface:
    def execute(
        self,
        context_pack: dict,        # Compiled by CCR
        parent_artifact: dict,     # Registry entry of triggering artifact
        mission_id: str,
    ) -> dict:                     # Returns new Artifact dict
        ...
```

### Input: Context Pack (from CCR)
```yaml
context_pack_id: CP-{MISSION}-{CAPABILITY}-{HASH}
mission_id: MISSION-002
target_capability: research | architecture | plan | build | governance | learning
target_worker: Krishna | Brahma | Ganesha | Hanuman | Lakshmi | Saraswati
target_provider: Anthropic | OpenAI | Manus
target_model: Claude Opus | GPT-5 | Manus Runtime
state:
  mission_objective: <string>
  current_state: <string>
  parent_artifacts: [<list of artifact IDs>]
constraints:
  worker_role: CSO | Chief Architect | COO | Lead Builder | ECO | CODO
  worker_defines: what/why | how | when/who | build | visibility | learning
  expected_output: <artifact type>
  laws: [L1, L2, L3]
meta:
  token_budget: <int>
  freshness_timestamp: <ISO8601>
```

### Output: Artifact
```python
{
    "id": "ART-M002-XXXXXX",
    "type": "<artifact type>",
    "title": "<artifact title>",
    "status": "Done | Draft | Ready For Execution",
    "content": "<full LLM-generated content>",
    "worker": "<worker name>",
    "provider": "<provider name>",
    "model": "<model name>",
    "parent_id": "<parent artifact ID>",
    "prompt_used": "<actual prompt sent to model>",
    "tokens_used": <int>,
    "execution_ts": "<ISO8601>",
}
```

---

## Provider Abstraction Layer

```
Worker
  ↓
WorkerExecutor
  ↓
ProviderAbstractionLayer
  ↓
[Manus Runtime | OpenAI | Anthropic | Google]
```

The PAL exposes a single method:
```python
def call_model(provider, model, system_prompt, user_prompt, max_tokens) -> str
```

Workers never call providers directly. They call the PAL.

---

## Execution Trace Schema

Every execution MUST produce a trace entry:

```json
{
  "trace_id": "TRACE-M002-{N}",
  "mission_id": "MISSION-002",
  "step": <int>,
  "ts": "<ISO8601>",
  "capability": "<string>",
  "worker": "<string>",
  "provider": "<string>",
  "model": "<string>",
  "context_pack_id": "<string>",
  "input_artifact_id": "<string>",
  "output_artifact_id": "<string>",
  "prompt_tokens": <int>,
  "completion_tokens": <int>,
  "execution_ms": <int>,
  "status": "success | error",
  "error": null | "<error message>"
}
```

---

## Artifact Persistence Specification

1. Every artifact is written to `mission_002/artifacts/{id}.md`
2. Every artifact is registered in `mission_002/registry.json`
3. Every artifact is published to Notion Artifact Registry
4. Lineage is recorded in `mission_002/lineage.json`
5. Parent artifact status is updated to `Consumed` upon child creation

---

## Provider Mapping (MISSION-002)

| Worker | Role | Provider | Model | Fallback |
| :--- | :--- | :--- | :--- | :--- |
| Krishna | CSO | Manus Runtime | claude-sonnet-4-5 | — |
| Brahma | Chief Architect | Manus Runtime | claude-sonnet-4-5 | — |
| Ganesha | COO | Manus Runtime | claude-sonnet-4-5 | — |
| Hanuman | Lead Builder | Manus Runtime | claude-sonnet-4-5 | — |
| Lakshmi | ECO | Manus Runtime | claude-sonnet-4-5 | — |
| Saraswati | CODO | Manus Runtime | claude-sonnet-4-5 | — |

**Note:** In this sandbox environment, all providers route through Manus Runtime (the agent itself), which is the only available real cognitive executor. This is architecturally valid: `CRT → Manus Runtime` is a legitimate provider mapping.


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **compiles:** [[Context_Pack]]
- **executed_by:** [[Brahma]]
- **executed_by:** [[Ganesha]]
- **executed_by:** [[Lakshmi]]
- **executed_by:** [[Saraswati]]
- **executed_by:** [[Hanuman]]
- **executed_by:** [[Krishna]]
- **governed_by:** [[Lakshmi_Governance]]
- **implements:** [[CCR_Runtime]]
- **implements:** [[Context_Pack]]
