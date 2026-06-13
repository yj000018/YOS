---
id: yos-adr-0019-lakshmi-runtime-v2.1
title: ADR-0019 Lakshmi Runtime v2.1
type: adr
status: ACCEPTED
date: '2026-06-13'
version: v2.1
owner: Lakshmi
parent: '[[02_ADR_MOC]]'
tags:
- '#accepted'
- '#adr'
- '#lineage'
- '#yos'
aliases:
- Lakshmi Runtime v2.1
source_branch: y-os-doctrine
canonical: true
---

# ADR-0019: Lakshmi Runtime v2.1 — Deterministic Fallback & Graph Engine

**Status:** Accepted  
**Date:** 2026-06-13  
**Owner:** Chief Architect (Brahma)  

## Context
Lakshmi Runtime v2.0 successfully demonstrated the ability to read the Artifact Registry and generate a CEO Briefing via an LLM. However, it suffered from two critical architectural flaws:
1.  **Single Point of Failure:** If the LLM failed, the entire visibility layer failed, violating Law #11 ("Visibility must survive replacement or failure of any capability").
2.  **Mocked Lineage:** It relied on hardcoded artifact relationships rather than reconstructing the true mission graph from the Notion Registry.

## Decision
We will upgrade Lakshmi Runtime to v2.1 with the following architectural changes:

1.  **Deterministic Fallback:** Implement a hardcoded, deterministic briefing generator that is automatically invoked if the LLM fails, times out, or returns an empty response.
2.  **Mission Graph Engine:** Implement an engine that dynamically reconstructs the Directed Acyclic Graph (DAG) of each mission by parsing `parent_id` and `child_ids` from the Registry.
3.  **Dynamic Open Loop Engine:** The Open Loop Engine will evaluate rules against the dynamically generated Mission Graph rather than a flat list.

## Consequences
*   **Positive:** Lakshmi is now operationally autonomous and highly resilient. The CEO is guaranteed to receive a briefing regardless of API status.
*   **Positive:** The system truly consumes the Artifact Lineage Model introduced in v1.1.
*   **Negative:** The deterministic briefing is less nuanced than the LLM synthesis, serving purely as a data readout. This is an acceptable tradeoff for guaranteed uptime.
