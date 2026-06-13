---
id: yos-adr-0026-art-runtime-v1
title: ADR-0026 ART Runtime v1
type: adr
status: ACCEPTED
date: '2026-06-13'
version: v1
owner: Brahma
parent: '[[02_ADR_MOC]]'
related_adrs:
- '[[ADR-0027]]'
tags:
- '#accepted'
- '#adr'
- '#lineage'
- '#yos'
aliases:
- ART Runtime v1
source_branch: y-os-doctrine
canonical: true
---

# ADR-0026: ART Runtime v1 — Agent Routing Table

**Date:** 2026-06-13  
**Status:** Accepted  
**Owner:** Chief Architect (Brahma)

## Context

Y-ORC Runtime v1 proved autonomous execution against the real Notion Registry.

Its limitation: capability → worker mapping was fixed inside Y-ORC.

This violates the Y-OS organizational principle: *organizational behavior must live in artifacts, not in agents or orchestrators.*

## Decision

Y-OS introduces the **Agent Routing Table (ART)** as a dedicated routing layer between Y-ORC and workers.

**Stack:**
```
Artifact → Y-ORC → Capability → ART → Worker → Artifact
```

**Separation of concerns:**
- Y-ORC knows: capabilities
- ART knows: workers
- Workers know: execution

Y-ORC never references agent names. ART is the only component that maps capability → worker. The mapping lives in `worker_registry.json` — a configurable artifact, not code.

## Validation Evidence

**ART-RESEARCH-001** (Strategy Brief, Status=Not started, Consumer=System, Capability=research) was created in the Notion Artifact Registry.

ART Runtime v1 autonomously:
1. Y-ORC detected the artifact (Status=Not started, Consumer=System)
2. Y-ORC identified capability: `research`
3. Y-ORC called `ART.resolve('research')` — never touched worker names
4. ART resolved: `research` → `Krishna` (from `worker_registry.json`)
5. Y-ORC invoked Krishna
6. Krishna produced **Research Output — ART-RESEARCH-001**
7. Artifact written to Notion Registry with lineage
8. ART-RESEARCH-001 marked Done (Consumed)

**Output artifact Notion URL:** https://app.notion.com/p/37e35e218cf88176a5c5da464ad5ef43

**Worker replacement proof:** `demo_worker_replacement()` shows `research → NewResearchAgent` without any Y-ORC code change.

## Consequences

Workers are now fully replaceable without modifying Y-ORC.

The path to CRT Runtime v1 (Capability → Worker → Model) is open:
ART resolves capability → worker.
CRT will resolve worker → model.

**ADR-0027 (CRT Runtime v1) is the natural next step.**
