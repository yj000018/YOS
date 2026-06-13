---
id: yos-concept-context-router
title: Context Router
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
- '[[ADR-0037]]'
mission_evidence:
- '[[mission_011]]'
implements:
- '[[CCR_Runtime]]'
- '[[Context_Pack]]'
depends_on:
- '[[Context_Pack]]'
- '[[Canonical_Memory]]'
tags:
- '#context'
- '#ccr'
- '#yos'
- '#accepted'
aliases:
- Mode Router
- CCR v2 Router
source_branch: y-os-doctrine
canonical: true
constrained_by:
- '[[Artifact_Primacy]]'
- '[[Derivation_Transparency]]'
references:
- '[[ADR-0037]]'
---

# Context Router

**Type:** Concept  
**Domain:** Context  
**Status:** CANONICAL  
**Constitutional Grounding:** Article I, Article III

---

## Definition

The Context Router is the CCR v2 component that selects the appropriate context mode (A through F) based on mission type, token budget, and constitutional requirements. Mode B (Context Pack Only, 623 tokens) is the production default for standard missions. Mode D (Context Pack + Canonical Memory, 1100 tokens) is used for constitutional work. The Context Router enforces the principle that context selection is a governance decision, not an ad-hoc choice.

---

## Constitutional Grounding

- Article I
- Article III

---

## ADR Lineage

- [[ADR-0037]]

---

## Mission Evidence

- [[mission_011]]

---

## Relationships

**Implements:**
- [[CCR_Runtime]]

**Depends on:**
- [[Context_Pack]]
- [[Canonical_Memory]]

---

## Current Status

Designed (ADR-0037). Mode B in production. Mode D for constitutional work.

---

## Navigation

- [[10_Concepts_MOC]] — All Y-OS Concepts
- [[01_Constitution_MOC]] — Constitutional Layer
- [[00_Y-OS_Home]] — Home


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **constrained_by:** [[Artifact_Primacy]]
- **constrained_by:** [[Derivation_Transparency]]
- **implements:** [[CCR_Runtime]]
- **implements:** [[Context_Pack]]
- **references:** [[ADR-0037]]
