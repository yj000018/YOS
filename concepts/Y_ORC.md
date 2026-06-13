---
id: yos-concept-y-orc
title: Y-ORC
type: concept
status: CANONICAL
domain: runtime
date: '2026-06-14'
owner: Brahma
parent: '[[10_Concepts_MOC]]'
constitutional_grounding:
  - 'Article I'
  - 'Article III'
adr_lineage:
  - '[[ADR-0025]]'
mission_evidence:
  - '[[mission_005]]'
implements: []
depends_on: ["[[ART]]", "[[CRT]]", "[[CCR_Runtime]]"]
tags:
  - '#runtime'
  - '#yos'
  - '#accepted'
aliases:
  - Y-OS Orchestration Runtime Core
  - Orchestrator
source_branch: y-os-doctrine
canonical: true
---

# Y-ORC

**Type:** Concept  
**Domain:** Runtime  
**Status:** CANONICAL  
**Constitutional Grounding:** Article I, Article III

---

## Definition

Y-ORC (Y-OS Orchestration Runtime Core) is the central orchestration engine of Y-OS. It receives mission definitions, routes tasks to appropriate workers (ART, CRT, CCR), manages execution state, and ensures that all outputs are materialized as artifacts. Y-ORC is the operational heart of the Y-OS runtime — it does not execute tasks directly but coordinates the workers that do. Y-ORC enforces Artifact Primacy by ensuring every worker output is captured.

---

## Constitutional Grounding

- Article I
- Article III

---

## ADR Lineage

- [[ADR-0025]]

---

## Mission Evidence

- [[mission_005]]

---

## Relationships

**Implements:**
- (none)

**Depends on:**
- [[ART]]
- [[CRT]]
- [[CCR_Runtime]]

---

## Current Status

Implemented in yorc_runtime_v1.py.

---

## Navigation

- [[10_Concepts_MOC]] — All Y-OS Concepts
- [[00_Y-OS_Home]] — Home
