---
id: yos-concept-replacement-test
title: Replacement Test
type: concept
status: CANONICAL
domain: constitution
date: '2026-06-14'
owner: Brahma
parent: '[[10_Concepts_MOC]]'
constitutional_grounding:
  - 'Article I'
  - 'Article III'
adr_lineage:
  - '[[ADR-0022]]'
mission_evidence:
  - '[[mission_007]]'
implements: ["[[Artifact_Primacy]]"]
depends_on: []
tags:
  - '#constitution'
  - '#governance'
  - '#yos'
  - '#accepted'
aliases:
  - Replaceability Test
  - Agent Independence Test
source_branch: y-os-doctrine
canonical: true
---

# Replacement Test

**Type:** Concept  
**Domain:** Constitution  
**Status:** CANONICAL  
**Constitutional Grounding:** Article I, Article III

---

## Definition

The Replacement Test is a Y-OS constitutional evaluation criterion that asks: if the current agent, worker, or model were replaced by a different one, would the system still produce the same outputs given the same inputs? If yes, the system passes the Replacement Test — its behavior is encoded in artifacts, not in agent memory. If no, the system fails — it has hidden dependencies on specific agent state. The Replacement Test enforces Artifact Primacy and Derivation Transparency.

---

## Constitutional Grounding

- Article I
- Article III

---

## ADR Lineage

- [[ADR-0022]]

---

## Mission Evidence

- [[mission_007]]

---

## Relationships

**Implements:**
- [[Artifact_Primacy]]

**Depends on:**
- (none)

---

## Current Status

Operational. Applied in mission governance reviews.

---

## Navigation

- [[10_Concepts_MOC]] — All Y-OS Concepts
- [[00_Y-OS_Home]] — Home


## Semantic Links

- **implements:** [[Artifact_Primacy]]