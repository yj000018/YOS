---
id: yos-llm-tool-routing-matrix
title: yOS LLM & Tool Routing Matrix
type: registry
status: CANONICAL yOS CORE REGISTRY
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

**Status:** CANONICAL yOS CORE REGISTRY  
**Date:** 2026-06-29  
**Owner:** Chief Architect (Brahma)  
**Execution Node:** Y-Matrix  

---

## Continuity Integration Note

The yOS LLM & Tool Routing Matrix delegates context/session/handoff mode definitions and enforcement semantics to yOS Continuity Core.

**Reference:** `YOS/core/orchestration/continuity/`

The matrix defines task-class defaults and escalation rules, but does not duplicate Continuity Core doctrine.

---

## Model / Cost Disclaimer

> Model availability, pricing, context windows, and quality indices are **empirical and revisionable**. They must be periodically revalidated and updated through yOS empirical learning logs. These values are routing defaults, not permanent doctrine. Do not treat provider names or cost estimates as immutable truth.

---

## 1. Context & Purpose

The **yOS LLM & Tool Routing Matrix** is the canonical catalog and decision engine for routing tasks to the optimal LLM or tool across the Y-OS ecosystem. It is completely agnostic across all program types and enforces Derivation Transparency by recording which model generated each artifact.

This registry consolidates the former `router.py` logic, the `CRT Model Routing` K-Card principles, and the `Provider Continuity Matrix` into a single authoritative source of truth.

---

## 2. CRT (Cost-Routing-Threshold) Modes

The CRT model is the primary traffic director, dynamically routing prompts to the most cost-efficient LLM that satisfies the required quality threshold.

| Mode | Target LLM (empirical) | Primary Use Case | Approx. Cost / M tokens | Quality Index (empirical) |
| :--- | :--- | :--- | :--- | :--- |
| **Standard** | GPT-4o-mini / Haiku 3 | Simple formatting, syntax checks, short-form editing | ~$0.15 | ~82% |
| **Balanced** | Claude 3.5 Haiku | Clarification, structuring, medium complexity tasks | ~$0.80 | ~89% |
| **Max** | Claude 3.7 Sonnet / GPT-5 | Complex architectural reasoning, multi-file code mods, philosophical synthesis | ~$3.00 | ~98% |

---

## 3. LLM Routing Matrix by Task Class

| Task Class | Primary LLM (empirical) | Fallback LLM | Context Window | Output Window | Latency | Cost Risk | QC Requirement |
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

The matrix defines the following default continuity fields for all task classes unless explicitly overridden by a specific mission or agent.

All values use approved yOS Continuity Core enum values.

| Field | Default Value | Notes |
| :--- | :--- | :--- |
| `default_session_mode` | `stateless_context_pack_only` | Standard stateless execution |
| `default_canonical_memory_mode` | `auto_if_high_risk` | Backend-agnostic — see note below |
| `default_context_pack_depth` | `standard` | Equivalent to T1_standard |
| `default_session_continuity_mode` | `none` | No live session thread by default |
| `default_handoff_mode` | `standard_context_pack` | Full context pack on handoff |
| `default_confirmation_policy` | `inform_only` | Inform unless escalation triggered |
| `default_enforcement_level` | `warning` | Warning mode by default |
| `auto_escalation_allowed` | `true` | — |
| `escalation_triggers` | `api_failure`, `cost_threshold_exceeded`, `context_limit_reached`, `boundary_crossed`, `governance_risk_detected`, `canonical_memory_required`, `session_drift_detected` | — |
| `user_confirmation_required_when` | `destructive_action`, `high_cost_mode`, `full_lineage_context`, `emergency_recovery`, `architecture_change` | — |
| `chief_architect_required_when` | `doctrine_violation`, `canonical_registry_modification`, `gate_critical_fallback`, `continuity_enforcement_override` | — |
| `founder_required_when` | `budget_override`, `new_agent_creation`, `sovereign_override`, `major_scope_expansion` | — |
| `default_context_pack_tier` | `T1_standard` | Maps to `standard` depth |
| `default_staleness_policy` | `standard` | — |
| `cap_required_by_default` | `true` | CAP acknowledgment required |

### Context Pack Tier Mapping

| Tier | context_pack_depth |
| :--- | :--- |
| T0_nano | `minimal` |
| T1_standard | `standard` |
| T2_full_lineage | `full_lineage` |
| T3_emergency_recovery | `emergency_recovery` |

### Canonical Memory Note

> Canonical Memory may be served by available memory backends, including Git, Notion, registry artifacts, Mem0 if available, or manually supplied artifacts. The routing matrix must remain **backend-agnostic**. `auto_if_high_risk` means: activate canonical memory only when the task risk profile warrants it, using whatever backend is available.

---

## 6. Update Policy

The Routing Matrix is a living document. It must be updated based on yOS empirical learning:

- **Monthly Review:** Y-Learn (Sarasvati) analyzes token costs and quality indices.
- **Model Upgrades:** When a new model is released, it must be benchmarked before replacing a Primary LLM.
- **QC Debt:** Legacy skipped files or undocumented workarounds must be reported as QC debt, not silently ignored.

---

## 7. Compatibility Bridge

The legacy path `BOOK/_fcs/registries/LLM_MATRIX.md` is deprecated. A compatibility bridge is maintained at that location pointing to this canonical registry. There must not be two canonical routing matrices.
