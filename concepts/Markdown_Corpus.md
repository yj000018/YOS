---
id: yos-concept-markdown-corpus
title: Markdown Corpus
type: concept
status: CANONICAL
domain: technical
date: '2026-06-14'
owner: Brahma
parent: '[[10_Concepts_MOC]]'
constitutional_grounding:
  - 'Article I'
  - 'Article II'
adr_lineage:
  - '[[ADR-0040]]'
mission_evidence:
  - '[[mission_013]]'
implements: []
depends_on: ["[[Artifact_Registry]]"]
tags:
  - '#technical'
  - '#yos'
  - '#accepted'
aliases:
  - Markdown Archive
  - Y-OS Corpus
  - Document Corpus
source_branch: y-os-doctrine
canonical: true
---

# Markdown Corpus

**Type:** Concept  
**Domain:** Technical  
**Status:** CANONICAL  
**Constitutional Grounding:** Article I, Article II

---

## Definition

The Markdown Corpus is the complete collection of Y-OS Markdown artifacts — currently 330+ files — that form the document layer of the Cognitive Graph. Each file is a Y-OS artifact with YAML frontmatter, typed relationships, and wikilinks. The Markdown Corpus is the raw material that KGC transforms into a knowledge graph. It is stored in Git and navigated through Obsidian.

---

## Constitutional Grounding

- Article I
- Article II

---

## ADR Lineage

- [[ADR-0040]]

---

## Mission Evidence

- [[mission_013]]

---

## Relationships

**Implements:**
- (none)

**Depends on:**
- [[Artifact_Registry]]

---

## Current Status

330+ files, 100% frontmatter, 1620+ semantic edges (KGC v2).

---

## Navigation

- [[10_Concepts_MOC]] — All Y-OS Concepts
- [[00_Y-OS_Home]] — Home
