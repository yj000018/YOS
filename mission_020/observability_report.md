---
id: yos-observability-report-v1
title: Y-OS Organizational Observability Report v1
type: observability_report
mission_id: MISSION-020
overall_status: HEALTHY
generated_at: '2026-06-14T03:55:17.482345+00:00'
tags: ['#observability', '#yos', '#mission-020']
---

# Y-OS Organizational Observability Report v1

**Status: HEALTHY**  
**Findings: 11** (CRITICAL: 0 | HIGH: 1 | WARNING: 4 | INFO: 6)  
**Generated:** 2026-06-14T03:55:17.482345+00:00  

## Findings

| ID | Category | Severity | Title |
| :--- | :--- | :--- | :--- |
| OBS-0001 | ADR_DRIFT | 🟡 WARNING | Proposed ADRs Pending Acceptance |
| OBS-0002 | MISSION_DRIFT | 🟡 WARNING | Missions in RUNNING State |
| OBS-0003 | GRAPH_ANOMALY | 🟠 HIGH | High Orphan Rate |
| OBS-0004 | GOVERNANCE_RISK | 🟢 INFO | Governance Compliance 100% |
| OBS-0005 | PIPELINE_FAILURE | 🟢 INFO | All Pipelines Completed |
| OBS-0006 | UNUSED_CONCEPTS | 🟢 INFO | Concept Coverage OK (39 nodes) |
| OBS-0007 | COST_ANOMALY | 🟢 INFO | Cost Within Budget ($0.1502) |
| OBS-0008 | PROVIDER_DEPENDENCE | 🟡 WARNING | High OpenAI Dependence |
| OBS-0009 | MEMORY_GROWTH | 🟢 INFO | Memory Assets Tracked (5) |
| OBS-0010 | LINEAGE_INTEGRITY | 🟢 INFO | Lineage Integrity 100% |
| OBS-0011 | EXECUTION_BOTTLENECK | 🟡 WARNING | Elevated Latency |

## Details

### OBS-0001 — Proposed ADRs Pending Acceptance
**Severity:** WARNING  
**Category:** ADR_DRIFT  
**Description:** 1 ADR(s) in PROPOSED state — not yet ACCEPTED  
**Affected:** ADR-0047  
**Recommendation:** Review and accept or reject pending ADRs  

### OBS-0002 — Missions in RUNNING State
**Severity:** WARNING  
**Category:** MISSION_DRIFT  
**Description:** 1 mission(s) not yet completed  
**Affected:** MISSION-020  
**Recommendation:** Complete or cancel running missions  

### OBS-0003 — High Orphan Rate
**Severity:** HIGH  
**Category:** GRAPH_ANOMALY  
**Description:** Orphan rate 34.7% exceeds threshold (30%). Files with no inbound links are invisible in graph navigation.  
**Recommendation:** Run KGC v3 body wikilinks pass to reduce orphans  

### OBS-0008 — High OpenAI Dependence
**Severity:** WARNING  
**Category:** PROVIDER_DEPENDENCE  
**Description:** OpenAI handles 72.7% of all calls — single-provider risk  
**Affected:** openai  
**Recommendation:** Diversify provider usage across Anthropic, Gemini  

### OBS-0011 — Elevated Latency
**Severity:** WARNING  
**Category:** EXECUTION_BOTTLENECK  
**Description:** Average latency 8243ms above 5s target  
**Recommendation:** Consider async execution for non-blocking workers  

---
*Organizational Observability Engine v1 — Y-OS*