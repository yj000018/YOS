---
id: yos-concept-provider-adapter
title: Provider Adapter
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
  - '[[ADR-0027]]'
mission_evidence:
  - '[[mission_005]]'
implements: []
depends_on: ["[[Y-ORC]]"]
tags:
  - '#runtime'
  - '#yos'
  - '#accepted'
aliases:
  - Provider Layer
  - LLM Adapter
  - Model Adapter
source_branch: y-os-doctrine
canonical: true
---

# Provider Adapter

**Type:** Concept  
**Domain:** Runtime  
**Status:** CANONICAL  
**Constitutional Grounding:** Article I, Article III

---

## Definition

The Provider Adapter is the Y-OS abstraction layer that normalizes access to external LLM providers (Anthropic, OpenAI, Gemini, Grok). It translates Y-OS execution requests into provider-specific API calls and normalizes responses back into Y-OS artifact format. The Provider Adapter enforces Derivation Transparency by recording which provider and model generated each artifact. It enables provider-agnostic mission execution.

---

## Constitutional Grounding

- Article I
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
- [[Y-ORC]]

---

## Current Status

Defined in ADR-0027. Implemented in provider registry.

---

## Navigation

- [[10_Concepts_MOC]] — All Y-OS Concepts
- [[00_Y-OS_Home]] — Home
