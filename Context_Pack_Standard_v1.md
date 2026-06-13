---
id: yos-context-pack-standard-v1
title: Context Pack Standard v1
type: context_pack
status: DRAFT
date: '2026-06-13'
version: v1
owner: Manus Y-OS
parent: '[[06_Context_Architecture_MOC]]'
related_adrs:
- '[[ADR-0026]]'
- '[[ADR-0027]]'
tags:
- '#context'
- '#proposed'
- '#yos'
source_branch: y-os-doctrine
canonical: true
---

# Context Pack Standard v1

**Mission:** CCV-001  
**Date:** 2026-06-13  
**Status:** Draft

## Definition
The Canonical Y-OS Context Pack is the structured payload injected into every fresh LLM session to ensure cognitive continuity. It replaces hidden conversation history with explicit, declarative state.

## Structure

```json
{
  "context_pack_id": "CP-102938",
  "mission_id": "MISS-YORC-V1",
  "routing": {
    "target_worker": "Brahma",
    "target_capability": "architecture",
    "target_model": "claude-3-5-sonnet"
  },
  "state": {
    "current_mission_state": "Designing CRT Runtime v1",
    "open_loops": ["Define Worker to Model routing"],
    "known_risks": ["Model hallucinating non-existent capabilities"],
    "missing_context": ["Provider API key limits"]
  },
  "artifact": {
    "parent_artifact_id": "ART-CRT-REQ-001",
    "parent_artifact_content": "...",
    "artifact_chain": ["ART-INIT-001", "ART-CRT-REQ-001"],
    "required_output_artifact": "Architecture Package"
  },
  "doctrine": {
    "relevant_adrs": ["ADR-0026"],
    "relevant_laws": ["Law #3: Artifacts are the source of truth"],
    "relevant_doctrine": ["Theory of Organization v1"],
    "constraints": ["Do not automate model routing yet"]
  },
  "execution": {
    "success_criteria": ["Architecture supports dynamic model selection"],
    "expected_output_format": "Markdown document with ADR-0027"
  }
}
```

## Injection Rules
1. **Statelessness:** The Context Pack MUST be the first message (or system prompt) in a fresh session.
2. **Completeness:** It MUST contain all information necessary to complete the task without requiring the worker to ask clarifying questions.
3. **Format:** It SHOULD be formatted as structured JSON or clearly delineated Markdown to facilitate parsing by the LLM.
