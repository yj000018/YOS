---
id: yos-concept-human-override
title: Human Override
type: concept
status: CANONICAL
domain: constitution
date: '2026-06-13'
owner: Brahma
parent: '[[10_Concepts_MOC]]'
constitutional_grounding:
- Article IV
adr_lineage:
- '[[ADR-0024]]'
- '[[ADR-0034]]'
mission_evidence:
- '[[mission_006]]'
- '[[mission_009]]'
implements: []
depends_on:
- '[[Governance_Before_Autonomy]]'
tags:
- '#constitution'
- '#yos'
- '#accepted'
aliases:
- Human Authority
- Article IV
- Human-in-the-Loop
source_branch: y-os-doctrine
canonical: true
constrained_by:
- '[[Human_Override]]'
references:
- '[[ADR-0024]]'
- '[[ADR-0034]]'
---

# Human Override

**Type:** Concept  
**Domain:** Constitution  
**Status:** CANONICAL  
**Constitutional Grounding:** Article IV

---

## Definition

Human Override is the constitutional principle that no Y-OS agent, runtime, or automated process may take irreversible action without explicit human authorization. All destructive operations (deletion, force-push, financial transactions, external API writes) require prior human confirmation. This principle ensures that Y-OS remains a human-directed system — agents are operators, not principals. The human architect retains final authority over all organizational decisions.

---

## Constitutional Grounding

- Article IV

---

## ADR Lineage

- [[ADR-0024]]
- [[ADR-0034]]

---

## Mission Evidence

- [[mission_006]]
- [[mission_009]]

---

## Relationships

**Implements:**
- (none)

**Depends on:**
- [[Governance_Before_Autonomy]]

---

## Current Status

FROZEN — Constitutional Article IV. Enforced by K7 rule (financial) and K2 rule (spending).

---

## Navigation

- [[10_Concepts_MOC]] — All Y-OS Concepts
- [[01_Constitution_MOC]] — Constitutional Layer
- [[00_Y-OS_Home]] — Home


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **constrained_by:** [[Human_Override]]
- **references:** [[ADR-0024]]
- **references:** [[ADR-0034]]
