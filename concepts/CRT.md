---
id: yos-concept-crt
title: CRT
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
  - '[[ADR-0028]]'
mission_evidence:
  - '[[mission_005]]'
implements: ["[[Context_Pack]]"]
depends_on: ["[[CCR_Runtime]]", "[[Y-ORC]]"]
tags:
  - '#runtime'
  - '#yos'
  - '#accepted'
aliases:
  - Context Runtime
  - Context Worker
source_branch: y-os-doctrine
canonical: true
---

# CRT

**Type:** Concept  
**Domain:** Runtime  
**Status:** CANONICAL  
**Constitutional Grounding:** Article I, Article III

---

## Definition

CRT (Context Runtime) is the Y-OS worker responsible for managing execution context. CRT reads the current context pack, injects it into the active mission, and updates the context state after each execution cycle. CRT works in conjunction with CCR (Context Compiler Runtime) — CCR compiles the context pack, CRT injects it. CRT ensures that every mission execution has access to the right context at the right time.

---

## Constitutional Grounding

- Article I
- Article III

---

## ADR Lineage

- [[ADR-0028]]

---

## Mission Evidence

- [[mission_005]]

---

## Relationships

**Implements:**
- [[Context_Pack]]

**Depends on:**
- [[CCR_Runtime]]
- [[Y-ORC]]

---

## Current Status

Implemented in crt_runtime_v1.py.

---

## Navigation

- [[10_Concepts_MOC]] — All Y-OS Concepts
- [[00_Y-OS_Home]] — Home


## Semantic Links

- **implements:** [[Context_Pack]]