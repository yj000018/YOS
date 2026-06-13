---
id: yos-concept-session-delta
title: Session Delta
type: concept
status: CANONICAL
domain: memory
date: '2026-06-13'
owner: Brahma
parent: '[[10_Concepts_MOC]]'
constitutional_grounding:
- Article I
- Article II
adr_lineage:
- '[[ADR-0038]]'
mission_evidence:
- '[[mission_012]]'
implements:
- '[[Living_Memory]]'
- '[[CCR_Runtime]]'
- '[[Session_Delta]]'
depends_on:
- '[[CCR_Runtime]]'
tags:
- '#memory'
- '#session-delta'
- '#yos'
- '#accepted'
aliases:
- Delta Engine
- Session Delta Engine
source_branch: y-os-doctrine
canonical: true
constrained_by:
- '[[Artifact_Primacy]]'
- '[[Preservation_Principle]]'
references:
- '[[ADR-0038]]'
---

# Session Delta

**Type:** Concept  
**Domain:** Memory  
**Status:** CANONICAL  
**Constitutional Grounding:** Article I, Article II

---

## Definition

Session Delta is the Y-OS mechanism for computing the incremental knowledge contribution of a single session relative to the existing canonical memory. Rather than re-processing full session history, the Session Delta Engine (ADR-0038) identifies what is genuinely new — new decisions, new artifacts, new relationships — and produces a minimal, high-signal delta artifact. This delta is the input to the Living Memory Pipeline's summarize and archive stages.

---

## Constitutional Grounding

- Article I
- Article II

---

## ADR Lineage

- [[ADR-0038]]

---

## Mission Evidence

- [[mission_012]]

---

## Relationships

**Implements:**
- [[Living_Memory]]

**Depends on:**
- [[CCR_Runtime]]

---

## Current Status

Designed (ADR-0038). Implementation pending MISSION-015.

---

## Navigation

- [[10_Concepts_MOC]] — All Y-OS Concepts
- [[01_Constitution_MOC]] — Constitutional Layer
- [[00_Y-OS_Home]] — Home


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **constrained_by:** [[Artifact_Primacy]]
- **constrained_by:** [[Preservation_Principle]]
- **implements:** [[CCR_Runtime]]
- **implements:** [[Living_Memory]]
- **implements:** [[Session_Delta]]
- **references:** [[ADR-0038]]
