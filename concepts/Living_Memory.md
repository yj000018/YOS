---
id: yos-concept-living-memory
title: Living Memory
type: concept
status: CANONICAL
domain: memory
date: '2026-06-13'
owner: Brahma
parent: '[[10_Concepts_MOC]]'
constitutional_grounding:
- Article I
- Article II
- Article III
adr_lineage:
- '[[ADR-0039]]'
mission_evidence:
- '[[mission_012b]]'
implements:
- '[[CCR_Runtime]]'
- '[[Living_Memory]]'
depends_on:
- '[[Session_Delta]]'
- '[[CCR_Runtime]]'
- '[[Canonical_Memory]]'
tags:
- '#memory'
- '#living-memory'
- '#yos'
- '#accepted'
aliases:
- LMP
- Living Memory Pipeline
- Organizational Memory
source_branch: y-os-doctrine
canonical: true
constrained_by:
- '[[Artifact_Primacy]]'
- '[[Preservation_Principle]]'
- '[[Derivation_Transparency]]'
references:
- '[[ADR-0039]]'
---

# Living Memory

**Type:** Concept  
**Domain:** Memory  
**Status:** CANONICAL  
**Constitutional Grounding:** Article I, Article II, Article III

---

## Definition

Living Memory is the Y-OS concept of organizational memory as a continuously evolving, self-compacting knowledge graph rather than a static archive. Unlike traditional document storage, Living Memory is alive — it grows with each session, compresses redundancy, surfaces canonical knowledge, and feeds directly into execution context. The Living Memory Pipeline (ADR-0039) defines the 8-stage lifecycle: Capture → Compress → Delta → Summarize → Archive → Canonicalize → Compile → Inject.

---

## Constitutional Grounding

- Article I
- Article II
- Article III

---

## ADR Lineage

- [[ADR-0039]]

---

## Mission Evidence

- [[mission_012b]]

---

## Relationships

**Implements:**
- (none)

**Depends on:**
- [[Session_Delta]]
- [[CCR_Runtime]]
- [[Canonical_Memory]]

---

## Current Status

Doctrine defined (ADR-0039). Pipeline implementation pending MISSION-015.

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
- **constrained_by:** [[Derivation_Transparency]]
- **implements:** [[CCR_Runtime]]
- **implements:** [[Living_Memory]]
- **references:** [[ADR-0039]]
