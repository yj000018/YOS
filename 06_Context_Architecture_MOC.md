---
id: yos-context-moc
title: Y-OS Context Architecture — Map of Content
type: index
status: ACTIVE
date: 2026-06-13
source_branch: y-os-doctrine
canonical: true
tags:
  - "#yos"
  - "#context"
  - "#ccr"
  - "#artifact"
related_adrs:
  - "[[ADR-0036]]"
  - "[[ADR-0037]]"
  - "[[ADR-0038]]"
aliases:
  - Context Architecture MOC
  - CCR MOC
---

# Y-OS Context Architecture — Map of Content

> Context architecture defines how Y-OS compiles, governs, and injects execution context into each mission cycle.

## Context Modes

| Mode | Name | Tokens | ROI/1k | Use |
| :--- | :--- | :--- | :--- | :--- |
| Mode A | Raw Session History | ~2000 | 45.7 | REJECTED |
| **Mode B** | **Context Pack Only** | **~623** | **140.9** | **PRODUCTION DEFAULT** |
| Mode C | Context Pack + Delta | ~890 | 98.4 | Optional |
| Mode D | Context Pack + Canonical Memory | ~1100 | 83.2 | Constitutional work |
| Mode E | Full Hybrid | ~1800 | 91.3 | Benchmarking only |
| Mode F | Session History Hybrid | ~2400 | 38.1 | REJECTED |

## Key Documents

- [[CCR_Runtime_v2_Architecture]] — ADR-0037
- [[Session_Delta_Engine_v1]] — ADR-0038
- [[Context_Pack_Schema_v1]]
- [[Context_Pack_Standard_v1]]

## Back

[[00_Y-OS_Home]]
