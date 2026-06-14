---
id: yos-concept-obsidian-vault
title: Obsidian Vault
type: concept
status: CANONICAL
domain: technical
date: '2026-06-14'
owner: Brahma
parent: '[[10_Concepts_MOC]]'
constitutional_grounding:
  - 'Article I'
adr_lineage:
  - '[[ADR-0040]]'
  - '[[ADR-0041]]'
  - '[[ADR-0042]]'
mission_evidence:
  - '[[mission_013]]'
  - '[[mission_014]]'
  - '[[mission_015]]'
implements: ["[[Cognitive_Graph]]"]
depends_on: ["[[Git-backed_Memory]]"]
tags:
  - '#technical'
  - '#yos'
  - '#accepted'
aliases:
  - Obsidian
  - Knowledge Vault
  - Y-OS Vault
source_branch: y-os-doctrine
canonical: true
---

# Obsidian Vault

**Type:** Concept  
**Domain:** Technical  
**Status:** CANONICAL  
**Constitutional Grounding:** Article I

---

## Definition

The Obsidian Vault is the primary human-facing interface for the Y-OS knowledge graph. It is a local clone of the y-os-doctrine branch, opened in Obsidian, providing graph view, wikilink navigation, Canvas maps, and Dataview queries. The Obsidian Vault is where the Cognitive Graph becomes navigable by a human. It is not the source of truth (Git is) but the cognitive interface to it.

---

## Constitutional Grounding

- Article I

---

## ADR Lineage

- [[ADR-0040]]
- [[ADR-0041]]
- [[ADR-0042]]

---

## Mission Evidence

- [[mission_013]]
- [[mission_014]]
- [[mission_015]]

---

## Relationships

**Implements:**
- [[Cognitive_Graph]]

**Depends on:**
- [[Git-backed_Memory]]

---

## Current Status

Operational. Clone: git clone https://github.com/yj000018/YOS.git --branch y-os-doctrine

---

## Navigation

- [[10_Concepts_MOC]] — All Y-OS Concepts
- [[00_Y-OS_Home]] — Home


## Semantic Links

- **implements:** [[Cognitive_Graph]]