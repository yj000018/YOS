---
id: yos-concept-context-pack
title: Context Pack
type: concept
status: CANONICAL
domain: context
date: '2026-06-13'
owner: Brahma
parent: '[[10_Concepts_MOC]]'
constitutional_grounding:
- Article I
adr_lineage:
- '[[ADR-0036]]'
- '[[ADR-0037]]'
mission_evidence:
- '[[mission_010]]'
- '[[mission_011]]'
implements:
- '[[CCR_Runtime]]'
- '[[Session_Delta]]'
- '[[Context_Pack]]'
depends_on:
- '[[CCR_Runtime]]'
tags:
- '#context'
- '#ccr'
- '#yos'
- '#accepted'
aliases:
- Context Pack v1
- Mode B Context
source_branch: y-os-doctrine
canonical: true
constrained_by:
- '[[Artifact_Primacy]]'
compiles:
- '[[Context_Pack]]'
injects:
- '[[Mission]]'
references:
- '[[ADR-0036]]'
- '[[ADR-0037]]'
---

# Context Pack

**Type:** Concept  
**Domain:** Context  
**Status:** CANONICAL  
**Constitutional Grounding:** Article I

---

## Definition

A Context Pack is a structured, pre-compiled artifact that contains the minimal sufficient context for executing a Y-OS mission. It replaces raw session history as the primary context injection mechanism. A Context Pack contains: current mission definition, relevant ADR summaries, active worker registry, constitutional constraints, and session delta from previous missions. Mode B (Context Pack Only) achieves 140.9 ROI/1k tokens — the highest efficiency of all context modes.

---

## Constitutional Grounding

- Article I

---

## ADR Lineage

- [[ADR-0036]]
- [[ADR-0037]]

---

## Mission Evidence

- [[mission_010]]
- [[mission_011]]

---

## Relationships

**Implements:**
- (none)

**Depends on:**
- [[CCR_Runtime]]

---

## Current Status

Production default (Mode B). Schema defined in Context_Pack_Schema_v1.

---

## Navigation

- [[10_Concepts_MOC]] — All Y-OS Concepts
- [[01_Constitution_MOC]] — Constitutional Layer
- [[00_Y-OS_Home]] — Home


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **compiles:** [[Context_Pack]]
- **constrained_by:** [[Artifact_Primacy]]
- **implements:** [[CCR_Runtime]]
- **implements:** [[Session_Delta]]
- **implements:** [[Context_Pack]]
- **injects:** [[Mission]]
- **references:** [[ADR-0036]]
- **references:** [[ADR-0037]]
