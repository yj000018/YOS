# Lakshmi Runtime Architecture v2.1

**Owner:** Chief Architect (Brahma)  
**Status:** Accepted  
**Date:** 2026-06-13  

## 1. Overview

Lakshmi Runtime v2.1 transforms the MVP into a resilient, deterministic executive visibility engine. It guarantees that visibility survives the failure of any single capability (specifically LLMs) by implementing a deterministic fallback mechanism. It also replaces mocked data with a true Mission Graph Engine that reconstructs lineage directly from the Notion Artifact Registry.

## 2. Core Components

1.  **Registry Parser:** Reads raw `notion-fetch` data (handling pagination and full properties) and normalizes it into internal `Artifact` objects.
2.  **Mission Graph Engine:** Builds a Directed Acyclic Graph (DAG) for each mission using `Parent Artifact ID` and `Child Artifact IDs`.
3.  **Open Loop Engine:** Evaluates the DAG against strict rules (L-01 to M-02) to detect anomalies.
4.  **Briefing Generator (LLM):** Attempts to synthesize the CEO Briefing using Claude Opus (via Manus proxy).
5.  **Briefing Generator (Deterministic Fallback):** If the LLM fails, times out, or returns empty, this engine generates a strictly formatted text briefing based on the Mission Graph and Open Loops data.
6.  **Output Engine:** Writes JSON state and Markdown briefings.

## 3. Resilience Principle (Law #11)

> "Visibility must survive replacement or failure of any capability."

If the LLM capability fails, Lakshmi must still produce:
*   `lakshmi_dashboard_state.json`
*   `lakshmi_open_loops.json`
*   `lakshmi_ceo_briefing.md` (using the deterministic template)

This ensures the CEO always receives the pulse of the organization, regardless of external API status.
