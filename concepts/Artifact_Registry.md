---
id: yos-concept-artifact-registry
title: Artifact Registry
type: concept
status: CANONICAL
domain: runtime
date: '2026-06-14'
owner: Brahma
parent: '[[10_Concepts_MOC]]'
constitutional_grounding:
  - 'Article I'
  - 'Article II'
adr_lineage:
  - '[[ADR-0016]]'
  - '[[ADR-0017]]'
mission_evidence:
  - '[[mission_001]]'
  - '[[mission_002]]'
implements: ["[[Artifact_Primacy]]"]
depends_on: ["[[ART]]"]
tags:
  - '#runtime'
  - '#artifact'
  - '#yos'
  - '#accepted'
aliases:
  - Artifact Index
  - Artifact Catalog
source_branch: y-os-doctrine
canonical: true
---

# Artifact Registry

**Type:** Concept  
**Domain:** Runtime  
**Status:** CANONICAL  
**Constitutional Grounding:** Article I, Article II

---

## Definition

The Artifact Registry is the canonical index of all Y-OS artifacts — their IDs, types, versions, owners, and storage locations. It is the operational implementation of Artifact Primacy. Every artifact created by ART is registered here. The Artifact Registry enables discovery, versioning, and retrieval of any Y-OS artifact across sessions. It is the foundation of the Living Memory system.

---

## Constitutional Grounding

- Article I
- Article II

---

## ADR Lineage

- [[ADR-0016]]
- [[ADR-0017]]

---

## Mission Evidence

- [[mission_001]]
- [[mission_002]]

---

## Relationships

**Implements:**
- [[Artifact_Primacy]]

**Depends on:**
- [[ART]]

---

## Current Status

Defined in ADR-0016/0017. Implemented as YAML frontmatter + Git.

---

## Navigation

- [[10_Concepts_MOC]] — All Y-OS Concepts
- [[00_Y-OS_Home]] — Home


## Semantic Links

- **implements:** [[Artifact_Primacy]]