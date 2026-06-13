---
id: yos-adr-0018-lakshmi-runtime-mvp
title: ADR-0018 Lakshmi Runtime MVP
type: adr
status: ACCEPTED
date: '2026-06-13'
owner: Lakshmi
parent: '[[02_ADR_MOC]]'
related_adrs:
- '[[ADR-0013]]'
- '[[ADR-0017]]'
tags:
- '#accepted'
- '#adr'
- '#lineage'
- '#yos'
aliases:
- Lakshmi Runtime MVP
source_branch: y-os-doctrine
canonical: true
validates:
- '[[ADR-0018]]'
- '[[ADR-0013]]'
- '[[ADR-0017]]'
governed_by:
- '[[Lakshmi_Governance]]'
executed_by:
- '[[Brahma]]'
- '[[Lakshmi]]'
---

# ADR-0018: Lakshmi Runtime MVP v2

**Date:** 2026-06-13  
**Status:** Accepted  
**Owner:** Chief Architect (Brahma)  

## 1. Context

Lakshmi (ECO) was defined as a role in ADR-0013 to provide executive visibility. The Artifact Registry was upgraded to v1.1 (ADR-0017) to support lineage. 

We now need to implement the first operational runtime for Lakshmi. This runtime must read the registry, reconstruct missions, detect open loops, and generate a CEO Briefing.

## 2. Decision

We will implement the **Lakshmi Runtime MVP v2** as a standalone Python script (`lakshmi_runtime.py`).

*   **Data Source:** Live Notion Artifact Registry via MCP `notion-search` and `notion-fetch`.
*   **Processing:** Local Python logic to build the DAG and apply Open Loop rules.
*   **Synthesis:** Cloud Opus (Anthropic) via Manus proxy to generate the final CEO Briefing.
*   **Output:** Markdown files and JSON state files. No UI will be built in this phase.

## 3. Rationale

1.  **Decoupling Visibility from Orchestration:** By building Lakshmi as a read-only script before building Y-ORC, we ensure that visibility is independent of execution mechanics.
2.  **Simplicity:** A Python script is easily triggered via cron or manually by the CEO, avoiding the need for a persistent server at this stage.
3.  **LLM Choice:** Cloud Opus is selected for text synthesis per Y-OS text processing guidelines, ensuring high-quality executive summaries.

## 4. Consequences

*   The script will need to handle Notion API rate limits and pagination if the registry grows large.
*   The output is static (Markdown/JSON). A future iteration will need to push this data back into a Notion Dashboard page for live viewing.


---

## Semantic Links

*Inferred by KGC v2 — MISSION-015*

- **executed_by:** [[Brahma]]
- **executed_by:** [[Lakshmi]]
- **governed_by:** [[Lakshmi_Governance]]
- **validates:** [[ADR-0018]]
- **validates:** [[ADR-0013]]
- **validates:** [[ADR-0017]]
