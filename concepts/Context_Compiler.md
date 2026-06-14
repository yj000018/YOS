---
id: yos-concept-context-compiler
title: Context Compiler
type: concept
status: CANONICAL
domain: context
date: '2026-06-14'
owner: Brahma
parent: '[[10_Concepts_MOC]]'
constitutional_grounding:
  - 'Article I'
adr_lineage:
  - '[[ADR-0029]]'
  - '[[ADR-0030]]'
  - '[[ADR-0037]]'
mission_evidence:
  - '[[mission_005]]'
  - '[[mission_011]]'
implements: ["[[CCR_Runtime]]"]
depends_on: ["[[Context_Pack]]"]
tags:
  - '#context'
  - '#ccr'
  - '#runtime'
  - '#yos'
  - '#accepted'
aliases:
  - CCR Compiler
  - Context Compilation Algorithm
source_branch: y-os-doctrine
canonical: true
---

# Context Compiler

**Type:** Concept  
**Domain:** Context  
**Status:** CANONICAL  
**Constitutional Grounding:** Article I

---

## Definition

The Context Compiler is the core algorithm within CCR Runtime that transforms raw session history, canonical memory, and mission definitions into an optimized context pack. It applies compression, deduplication, and relevance scoring to maximize cognitive ROI per token. The Context Compiler is the computational heart of CCR — it is what makes Mode B (Context Pack Only) achieve 140.9 ROI/1k tokens.

---

## Constitutional Grounding

- Article I

---

## ADR Lineage

- [[ADR-0029]]
- [[ADR-0030]]
- [[ADR-0037]]

---

## Mission Evidence

- [[mission_005]]
- [[mission_011]]

---

## Relationships

**Implements:**
- [[CCR_Runtime]]

**Depends on:**
- [[Context_Pack]]

---

## Current Status

Implemented in context_compiler_v1.py.

---

## Navigation

- [[10_Concepts_MOC]] — All Y-OS Concepts
- [[00_Y-OS_Home]] — Home


## Semantic Links

- **implements:** [[CCR_Runtime]]