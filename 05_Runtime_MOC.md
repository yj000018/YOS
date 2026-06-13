---
id: yos-runtime-moc
title: Y-OS Runtime — Map of Content
type: index
status: ACTIVE
date: 2026-06-13
source_branch: y-os-doctrine
canonical: true
tags:
- '#yos'
- '#runtime'
- '#artifact'
related_adrs:
- '[[ADR-0025]]'
- '[[ADR-0026]]'
- '[[ADR-0028]]'
aliases:
- Runtime MOC
implements:
- '[[CCR_Runtime]]'
- '[[Context_Pack]]'
compiles:
- '[[Context_Pack]]'
references:
- '[[ADR-0025]]'
- '[[ADR-0026]]'
- '[[ADR-0028]]'
- '[[ADR-0029]]'
- '[[ADR-0030]]'
- '[[ADR-0037]]'
---

# Y-OS Runtime — Map of Content

> The Y-OS runtime is the operational layer that executes organizational intelligence. It consists of Y-ORC, ART, CRT, and CCR.

## Runtime Components

| Component | File | ADR | Description |
| :--- | :--- | :--- | :--- |
| Y-ORC v1 | [[yorc_runtime_v1]] | [[ADR-0025]] | Orchestrator + Notion Registry |
| ART v1 | [[art_runtime_v1]] | [[ADR-0026]] | Agent Routing Table |
| CRT v1 | [[crt_runtime_v1]] | [[ADR-0028]] | Worker-to-Model resolver |
| CCR v1 | [[context_compiler_v1]] | [[ADR-0029]] | Context Pack compiler |
| CCR v1.1 | [[CCR_Runtime_v1.1_Governance_Patch]] | [[ADR-0030]] | Governance patch |
| CCR v2 | [[CCR_Runtime_v2_Architecture]] | [[ADR-0037]] | Mode B/D context router |

## Worker Registry

- [[worker_registry]] — Capability → Worker mapping
- [[model_registry]] — Worker → Model/Provider mapping

## Back

[[00_Y-OS_Home]]


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **compiles:** [[Context_Pack]]
- **implements:** [[CCR_Runtime]]
- **implements:** [[Context_Pack]]
- **references:** [[ADR-0025]]
- **references:** [[ADR-0026]]
- **references:** [[ADR-0028]]
- **references:** [[ADR-0029]]
- **references:** [[ADR-0030]]
- **references:** [[ADR-0037]]
