---
id: yos-concept-worker-registry
title: Worker Registry
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
depends_on: ["[[Y-ORC]]"]
tags:
  - '#runtime'
  - '#yos'
  - '#accepted'
aliases:
  - Worker Catalog
  - Agent Registry
source_branch: y-os-doctrine
canonical: true
---

# Worker Registry

**Type:** Concept  
**Domain:** Runtime  
**Status:** CANONICAL  
**Constitutional Grounding:** Article I, Article III

---

## Definition

The Worker Registry is the canonical catalog of all Y-OS workers — their names, roles, capabilities, and current status. Workers include: CEO, Krishna, Brahma, Ganesha, Hanuman, Lakshmi, Saraswati. The Worker Registry enforces Derivation Transparency by ensuring that every artifact records which worker produced it. It also enables Y-ORC to route tasks to the correct worker based on capability matching.

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
- [[Y-ORC]]

---

## Current Status

Defined in worker_registry.json.

---

## Navigation

- [[10_Concepts_MOC]] — All Y-OS Concepts
- [[00_Y-OS_Home]] — Home
