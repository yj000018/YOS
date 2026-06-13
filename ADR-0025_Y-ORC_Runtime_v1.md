# ADR-0025: Y-ORC Runtime v1 — Real Registry Activation

**Date:** 2026-06-13  
**Status:** Accepted  
**Owner:** Chief Architect (Brahma)  

## Context

Y-ORC Runtime MVP v0 proved the loop with a simulated JSON registry.

Y-ORC Runtime v1 replaces the simulated registry with the live Notion Artifact Registry.

## Decision

Y-OS activates production-grade autonomous execution against the real Notion Artifact Registry.

The trigger condition is: `Status = "Not started"` AND `Consumer = "System"` AND a recognized capability keyword in `Acceptance Notes`.

## Validation Evidence

**ART-DEMO-001** (Execution Plan, Status=Not started, Consumer=System, Capability=generate_report) was created in the Notion Artifact Registry.

Y-ORC Runtime v1 autonomously:
1. Detected the artifact via Notion search polling
2. Resolved capability `generate_report` → worker `Ganesha`
3. Invoked Ganesha worker
4. Created **ART-DEMO-002** in the Notion Registry with full lineage
5. Marked ART-DEMO-001 as `Done` (Consumed)

**ART-DEMO-002 Notion URL:** https://app.notion.com/p/37e35e218cf881c1bbf6e5dafca345c9

## Consequences

Y-OS now executes autonomously against real state. The architectural phase is complete. The operational phase has begun.
