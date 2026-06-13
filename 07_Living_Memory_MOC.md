---
id: yos-living-memory-moc
title: Y-OS Living Memory — Map of Content
type: index
status: ACTIVE
date: 2026-06-13
source_branch: y-os-doctrine
canonical: true
tags:
- '#yos'
- '#memory'
- '#living-memory'
- '#session-delta'
- '#artifact'
related_adrs:
- '[[ADR-0038]]'
- '[[ADR-0039]]'
aliases:
- Living Memory MOC
- LMP MOC
implements:
- '[[CCR_Runtime]]'
- '[[Living_Memory]]'
- '[[Session_Delta]]'
governed_by:
- '[[Lakshmi_Governance]]'
executed_by:
- '[[Lakshmi]]'
- '[[Saraswati]]'
references:
- '[[ADR-0039]]'
- '[[ADR-0038]]'
- '[[ADR-0037]]'
---

# Y-OS Living Memory — Map of Content

> The Living Memory Pipeline (LMP) is the canonical 8-stage lifecycle from live interaction to runtime context injection.

## Pipeline Stages

```
Capture → Compress → Delta → Summarize → Archive → Canonicalize → Compile → Inject
```

| Stage | Name | Component |
| :---: | :--- | :--- |
| 1 | Capture | Y-ORC / Session Logger |
| 2 | Compress | CCR |
| 3 | Delta | Session Delta Engine |
| 4 | Summarize | CCR / Saraswati |
| 5 | Archive | Artifact Writer |
| 6 | Canonicalize | Lakshmi |
| 7 | Compile | CCR Runtime v2 |
| 8 | Inject | Context Router |

## Key Documents

- [[Living_Memory_Pipeline_Doctrine_v1]] — ADR-0039
- [[Session_Delta_Engine_v1]] — ADR-0038
- [[CCR_Runtime_v2_Architecture]] — ADR-0037

## Back

[[00_Y-OS_Home]]


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **executed_by:** [[Lakshmi]]
- **executed_by:** [[Saraswati]]
- **governed_by:** [[Lakshmi_Governance]]
- **implements:** [[CCR_Runtime]]
- **implements:** [[Living_Memory]]
- **implements:** [[Session_Delta]]
- **references:** [[ADR-0039]]
- **references:** [[ADR-0038]]
- **references:** [[ADR-0037]]
