---
id: yos-concept-art
title: ART
type: concept
status: CANONICAL
domain: runtime
date: '2026-06-14'
owner: Brahma
parent: '[[10_Concepts_MOC]]'
constitutional_grounding:
  - 'Article I'
adr_lineage:
  - '[[ADR-0026]]'
mission_evidence:
  - '[[mission_005]]'
implements: ["[[Artifact_Primacy]]"]
depends_on: ["[[Y-ORC]]"]
tags:
  - '#runtime'
  - '#yos'
  - '#accepted'
aliases:
  - Artifact Runtime
  - Artifact Worker
source_branch: y-os-doctrine
canonical: true
---

# ART

**Type:** Concept  
**Domain:** Runtime  
**Status:** CANONICAL  
**Constitutional Grounding:** Article I

---

## Definition

ART (Artifact Runtime) is the Y-OS worker responsible for creating, versioning, and storing artifacts. Every time a Y-OS process produces an output — a document, a report, a code file, a schema — ART captures it, assigns a canonical ID, and stores it in the Artifact Registry. ART is the operational implementation of Artifact Primacy. Without ART, knowledge would remain in agent memory rather than in durable, versioned artifacts.

---

## Constitutional Grounding

- Article I

---

## ADR Lineage

- [[ADR-0026]]

---

## Mission Evidence

- [[mission_005]]

---

## Relationships

**Implements:**
- [[Artifact_Primacy]]

**Depends on:**
- [[Y-ORC]]

---

## Current Status

Implemented in art_runtime_v1.py.

---

## Navigation

- [[10_Concepts_MOC]] — All Y-OS Concepts
- [[00_Y-OS_Home]] — Home


## Semantic Links

- **implements:** [[Artifact_Primacy]]