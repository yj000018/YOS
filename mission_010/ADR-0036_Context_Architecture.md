---
id: yos-adr-0036-context-architecture
title: ADR-0036 Context Architecture
type: adr
status: ACCEPTED
mission: MISSION-010
date: '2026-06-13'
owner: Brahma
parent: '[[03_Missions_MOC]]'
related_adrs:
- '[[ADR-0029]]'
- '[[ADR-0033]]'
- '[[ADR-0035]]'
related_missions:
- '[[mission_010]]'
constitutional_articles:
- 'Article V: Governance Before Autonomy'
tags:
- '#accepted'
- '#adr'
- '#ccr'
- '#memory'
- '#yos'
aliases:
- Context Architecture
- MISSION-010
source_branch: y-os-doctrine
canonical: true
implements:
- '[[CCR_Runtime]]'
- '[[Context_Pack]]'
governed_by:
- '[[Governance_Determinism]]'
- '[[Lakshmi_Governance]]'
executed_by:
- '[[Brahma]]'
- '[[Lakshmi]]'
compiles:
- '[[Context_Pack]]'
---

# ADR-0036 — Y-OS Canonical Context Architecture

**Status:** ACCEPTED
**Date:** 2026-06-13
**Mission:** MISSION-010
**Related:** ADR-0029 (CCR Runtime), ADR-0033 (Governance Determinism), ADR-0035 (Executable Governance)

---

## Context

MISSION-010 validated 5 context architecture modes against an identical task using real LLM calls, scored across 8 dimensions by Lakshmi.

**Task:** Evaluate whether Article VI should be adopted as Amendment-001.
**Worker:** Brahma (identical across all modes).
**Providers:** OpenAI gpt-4o (Modes A/B/C) + Anthropic claude-opus-4-5 (Modes D/E).

---

## Benchmark Results

| Mode | Architecture | Exec Quality | Efficiency | Org Memory | **Final Score** | Tokens |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| E | Canonical Memory + Context Pack + Session | 94.8 | 84.0 | 90 | **91.3** | 1,595 |
| D | Canonical Memory + Context Pack | 88.8 | 81.0 | 85 | **86.2** | 1,439 |
| A | Conversation Only | 87.8 | 81.0 | 80 | **85.0** | 511 |
| B | Context Pack Only | 86.3 | 81.0 | 80 | **84.1** | 805 |
| C | Conversation + Context Pack | 86.2 | 80.0 | 80 | **83.8** | 959 |

**Lakshmi Governance Score:** 20/100 — APPROVE (Pristine range)

---

## Decision

Y-OS adopts the following canonical context architecture classification:

```
Session Memory    = Execution Context   (ephemeral, session-scoped)
Context Packs     = Organizational Context (compiled, artifact-backed)
Canonical Memory  = Organizational Truth  (Constitution + ADRs + Registry)
```

**Canonical Y-OS Runtime Context = Canonical Memory + Context Pack + Session Context (Mode E)**

---

## Hypotheses Validated

| Hypothesis | Result |
| :--- | :--- |
| H1: Context Packs > raw conversation | **PARTIALLY VALIDATED** — Mode B (84.1) < Mode A (85.0). Context Packs alone are not superior; they require Canonical Memory to shine. |
| H2: Canonical Memory + Context Pack + Session = highest quality | **VALIDATED** — Mode E (91.3) is the clear winner. |
| H3: Session Memory ≠ Organizational Memory | **VALIDATED** — Mode D (86.2) without session still outperforms A/B/C. Canonical Memory is the differentiator. |

---

## Key Insight

Context Packs alone (Mode B) do not outperform raw conversation (Mode A). The value of Context Packs emerges **only when combined with Canonical Memory**. The differentiator is not the Context Pack format — it is the presence of organizational truth (Constitution + ADRs).

---

## Canonical Context Substrate

```
Y-OS Execution = Canonical Memory (truth)
              + Context Pack (compiled organizational state)
              + Session Context (execution thread)
```

Each layer has a distinct role:
- **Canonical Memory** — what Y-OS is and what it decided
- **Context Pack** — what this mission knows and needs
- **Session Context** — what just happened in this execution

---

## Consequences

**Positive:**
- Context architecture is now deterministic and measurable
- CCR Runtime v1.1 is validated as the correct compilation layer
- Organizational memory is formally separated from execution memory

**Constraints:**
- Mode E requires higher token budget (~1,595 vs ~511 for Mode A)
- Canonical Memory must be kept current (ADR updates, Constitution amendments)
- Context Packs must be compiled fresh per mission (not reused across missions)

---

## Status

**ACCEPTED** — Mode E is the canonical Y-OS context architecture.


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **compiles:** [[Context_Pack]]
- **executed_by:** [[Brahma]]
- **executed_by:** [[Lakshmi]]
- **governed_by:** [[Governance_Determinism]]
- **governed_by:** [[Lakshmi_Governance]]
- **implements:** [[CCR_Runtime]]
- **implements:** [[Context_Pack]]
