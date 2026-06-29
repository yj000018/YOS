---
id: yos-llm-tool-routing-matrix
title: yOS LLM & Tool Routing Matrix
type: registry
status: CANONICAL yOS CORE MODULE
date: '2026-06-29'
owner: Chief Architect (Brahma)
tags:
- '#routing'
- '#llm'
- '#tools'
- '#yos-core'
source_branch: phase-iii/yos-continuity-core-consolidation
canonical: true
---

# yOS LLM & Tool Routing Matrix

**Status:** CANONICAL yOS CORE MODULE  
**Date:** 2026-06-29  
**Owner:** Chief Architect (Brahma)  
**Execution Node:** Y-Matrix  

## 1. Context & Purpose

The **yOS LLM & Tool Routing Matrix** is the canonical catalog and decision engine for routing tasks to the optimal LLM or tool across the Y-OS ecosystem. It is completely agnostic across all program types and enforces Derivation Transparency by recording which model generated each artifact.

This registry consolidates the former `router.py` logic, the `CRT Model Routing` K-Card principles, and the `Provider Continuity Matrix` into a single authoritative source of truth.

> **Continuity Integration Note:**  
> The yOS LLM & Tool Routing Matrix delegates context/session/handoff mode defaults to yOS Continuity Core and must include continuity-related fields where applicable.  
> **Reference:** `YOS/core/orchestration/continuity/`

---

## 2. CRT (Cost-Routing-Threshold) Modes

The CRT model is the primary traffic director, dynamically routing prompts to the most cost-efficient LLM that satisfies the required quality threshold.

| Mode | Target LLM | Primary Use Case | Avg Token Cost | Quality Index |
| :--- | :--- | :--- | :--- | :--- |
| **Standard** | GPT-4o-mini / Haiku 3 | Simple formatting, syntax checks, short-form editing | $0.15 / M | 82% |
| **Balanced** | Claude 3.5 Haiku | Clarification, structuring, medium complexity tasks | $0.80 / M | 89% |
| **Max** | Claude 3.7 Sonnet / GPT-5 | Complex architectural reasoning, multi-file code mods, philosophical synthesis | $3.00 / M | 98% |

---

## 3. LLM Routing Matrix by Task Class

| Task Class | Primary LLM | Fallback LLM | Context Window | Output Window | Latency | Cost Risk | QC Requirement |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `book_prose` | Claude 3 Opus | Claude 3.7 Sonnet | 200k | 4k | High | High | Tone/Style Check |
| `architecture` | Claude 3.7 Sonnet | GPT-5 | 200k | 8k | Medium | High | Structural Consistency |
| `code_generation` | GPT-5 | Claude 3.7 Sonnet | 128k | 8k | Medium | High | Syntax/Logic Validation |
| `research` | Perplexity sonar-pro | GPT-4o | 128k | 4k | Low | Medium | Citation Verification |
| `data_analysis` | GPT-5 | Claude 3.5 Haiku | 128k | 8k | Medium | High | Calculation Accuracy |
| `vision_image` | Gemini 2.5 Flash | GPT-4o | 1M | N/A | Low | Medium | Visual Fidelity |
| `translation` | Mistral Large | Claude 3.5 Haiku | 32k | 8k | Low | Low | Nuance Preservation |
| `conversation` | Grok 4 | GPT-4o-mini | 128k | 4k | Low | Low | Context Adherence |
| `default` | Claude 3.7 Sonnet | GPT-4o | 200k | 8k | Medium | Medium | General Sanity Check |

---

## 4. Fallback Rules

1. **Auto-Fallback:** If the primary LLM fails due to rate limits or transient API errors, Y-Matrix automatically routes to the Fallback LLM.
2. **Approval-Required Fallback:** If both Primary and Fallback fail, or if falling back implies a >3x cost increase, execution pauses and requests explicit approval from the Founder or Chief Architect.

---

## 5. Continuity Core Default Fields

The matrix defines the following default continuity fields for all task classes unless explicitly overridden by a specific mission or agent:

- `default_session_mode`: MODE_B_FRESH_PACK
- `default_canonical_memory_mode`: MEM0_AND_NOTION
- `default_context_pack_depth`: T1_STANDARD
- `default_session_continuity_mode`: STATELESS
- `default_handoff_mode`: EXPLICIT_ACK
- `default_confirmation_policy`: REQUIRE_ON_DESTRUCTIVE
- `default_enforcement_level`: STRICT
- `auto_escalation_allowed`: TRUE
- `escalation_triggers`: [API_FAILURE, COST_THRESHOLD_EXCEEDED, CONTEXT_LIMIT_REACHED]
- `user_confirmation_required_when`: [COST > $5, DESTRUCTIVE_ACTION, ARCHITECTURE_CHANGE]
- `chief_architect_required_when`: [DOCTRINE_VIOLATION, CANONICAL_REGISTRY_MODIFICATION]
- `founder_required_when`: [BUDGET_OVERRIDE, NEW_AGENT_CREATION]
- `default_context_pack_tier`: T1_STANDARD
- `default_staleness_policy`: REJECT_IF_OLDER_THAN_24H
- `cap_required_by_default`: TRUE

---

## 6. Update Policy

The Routing Matrix is a living document. It must be updated based on yOS empirical learning:
- **Monthly Review:** Y-Learn (Sarasvati) analyzes token costs and quality indices.
- **Model Upgrades:** When a new model is released (e.g., GPT-5.5), it must be benchmarked before replacing a Primary LLM.
- **QC Debt:** Legacy skipped files or undocumented workarounds must be reported as QC debt, not silently ignored.

---

## 7. Compatibility Bridge

The legacy path `BOOK/_fcs/registries/LLM_MATRIX.md` is deprecated. A compatibility bridge must be maintained at that location pointing to this canonical registry to prevent duplicate or competing matrix files.
