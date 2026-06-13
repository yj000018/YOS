---
id: yos-concept-ccr-runtime
title: CCR Runtime
type: concept
status: CANONICAL
domain: context
date: '2026-06-13'
owner: Brahma
parent: '[[10_Concepts_MOC]]'
constitutional_grounding:
- Article I
- Article III
adr_lineage:
- '[[ADR-0029]]'
- '[[ADR-0030]]'
- '[[ADR-0037]]'
mission_evidence:
- '[[mission_005]]'
- '[[mission_005b]]'
- '[[mission_011]]'
implements:
- '[[Context_Pack]]'
- '[[Context_Router]]'
- '[[CCR_Runtime]]'
depends_on:
- '[[Session_Delta]]'
- '[[Canonical_Memory]]'
tags:
- '#context'
- '#ccr'
- '#runtime'
- '#yos'
- '#accepted'
aliases:
- Context Compiler Runtime
- CCR
- Context Compiler
source_branch: y-os-doctrine
canonical: true
constrained_by:
- '[[Artifact_Primacy]]'
- '[[Derivation_Transparency]]'
compiles:
- '[[Context_Pack]]'
injects:
- '[[Mission]]'
references:
- '[[ADR-0029]]'
- '[[ADR-0030]]'
- '[[ADR-0037]]'
---

# CCR Runtime

**Type:** Concept  
**Domain:** Context  
**Status:** CANONICAL  
**Constitutional Grounding:** Article I, Article III

---

## Definition

The CCR Runtime (Context Compiler Runtime) is the Y-OS component responsible for compiling, routing, and injecting execution context into mission cycles. It transforms raw session history and canonical memory into optimized context packs that maximize cognitive ROI per token. CCR v1 (ADR-0029) established the baseline compiler. CCR v1.1 (ADR-0030) added governance patch. CCR v2 (ADR-0037) introduced Mode B/D context routing with 140.9 ROI/1k tokens for Mode B (production default).

---

## Constitutional Grounding

- Article I
- Article III

---

## ADR Lineage

- [[ADR-0029]]
- [[ADR-0030]]
- [[ADR-0037]]

---

## Mission Evidence

- [[mission_005]]
- [[mission_005b]]
- [[mission_011]]

---

## Relationships

**Implements:**
- [[Context_Pack]]
- [[Context_Router]]

**Depends on:**
- [[Session_Delta]]
- [[Canonical_Memory]]

---

## Current Status

CCR v2 is the production default. Mode B = 623 tokens, ROI 140.9/1k.

---

## Navigation

- [[10_Concepts_MOC]] — All Y-OS Concepts
- [[01_Constitution_MOC]] — Constitutional Layer
- [[00_Y-OS_Home]] — Home


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **compiles:** [[Context_Pack]]
- **constrained_by:** [[Artifact_Primacy]]
- **constrained_by:** [[Derivation_Transparency]]
- **implements:** [[CCR_Runtime]]
- **implements:** [[Context_Pack]]
- **injects:** [[Mission]]
- **references:** [[ADR-0029]]
- **references:** [[ADR-0030]]
- **references:** [[ADR-0037]]
