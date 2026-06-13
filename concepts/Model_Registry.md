---
id: yos-concept-model-registry
title: Model Registry
type: concept
status: CANONICAL
domain: runtime
date: '2026-06-14'
owner: Brahma
parent: '[[10_Concepts_MOC]]'
constitutional_grounding:
  - 'Article III'
adr_lineage:
  - '[[ADR-0027]]'
mission_evidence:
  - '[[mission_005]]'
implements: []
depends_on: ["[[Provider_Adapter]]"]
tags:
  - '#runtime'
  - '#yos'
  - '#accepted'
aliases:
  - LLM Registry
  - Model Catalog
source_branch: y-os-doctrine
canonical: true
---

# Model Registry

**Type:** Concept  
**Domain:** Runtime  
**Status:** CANONICAL  
**Constitutional Grounding:** Article III

---

## Definition

The Model Registry is the canonical catalog of all LLM models available to Y-OS workers — their provider, version, capabilities, cost, and routing rules. It enables the Provider Adapter to select the optimal model for each task based on type (reasoning, coding, vision, long-context) and budget constraints. The Model Registry enforces Derivation Transparency by recording which model generated each artifact.

---

## Constitutional Grounding

- Article III

---

## ADR Lineage

- [[ADR-0027]]

---

## Mission Evidence

- [[mission_005]]

---

## Relationships

**Implements:**
- (none)

**Depends on:**
- [[Provider_Adapter]]

---

## Current Status

Defined in model_registry.json.

---

## Navigation

- [[10_Concepts_MOC]] — All Y-OS Concepts
- [[00_Y-OS_Home]] — Home
