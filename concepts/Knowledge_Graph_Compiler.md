---
id: yos-concept-knowledge-graph-compiler
title: Knowledge Graph Compiler
type: concept
status: CANONICAL
domain: memory
date: '2026-06-14'
owner: Brahma
parent: '[[10_Concepts_MOC]]'
constitutional_grounding:
  - 'Article I'
  - 'Article III'
adr_lineage:
  - '[[ADR-0040]]'
  - '[[ADR-0041]]'
  - '[[ADR-0042]]'
mission_evidence:
  - '[[mission_013]]'
  - '[[mission_013b]]'
  - '[[mission_014]]'
  - '[[mission_015]]'
implements: ["[[Cognitive_Graph]]"]
depends_on: ["[[Artifact_Registry]]"]
tags:
  - '#memory'
  - '#artifact'
  - '#yos'
  - '#accepted'
aliases:
  - KGC
  - KGC v1
  - KGC v2
  - Graph Compiler
source_branch: y-os-doctrine
canonical: true
---

# Knowledge Graph Compiler

**Type:** Concept  
**Domain:** Memory  
**Status:** CANONICAL  
**Constitutional Grounding:** Article I, Article III

---

## Definition

The Knowledge Graph Compiler (KGC) is the Y-OS tool that transforms the Markdown artifact corpus into an Obsidian-native knowledge graph. KGC v1 (ADR-0040) added YAML frontmatter, wikilinks, and MOCs. KGC v2 (ADR-0042) adds semantic relationship inference, concept nodes, Canvas visual maps, and Dataview dashboards. The KGC is the operational bridge between the artifact corpus and the cognitive navigation interface.

---

## Constitutional Grounding

- Article I
- Article III

---

## ADR Lineage

- [[ADR-0040]]
- [[ADR-0041]]
- [[ADR-0042]]

---

## Mission Evidence

- [[mission_013]]
- [[mission_013b]]
- [[mission_014]]
- [[mission_015]]

---

## Relationships

**Implements:**
- [[Cognitive_Graph]]

**Depends on:**
- [[Artifact_Registry]]

---

## Current Status

KGC v2 operational (MISSION-015). kg_compiler_v2.py deployed.

---

## Navigation

- [[10_Concepts_MOC]] — All Y-OS Concepts
- [[00_Y-OS_Home]] — Home


## Semantic Links

- **implements:** [[Cognitive_Graph]]