---
id: yos-system-health-v1
title: Y-OS System Health Report v1
type: system_health_report
mission_id: MISSION-019
health_score: 90.0
status: HEALTHY
generated_at: '2026-06-14T03:42:14.452992+00:00'
tags: ['#health', '#yos', '#mission-019']
---

# Y-OS System Health Report v1

**Health Score: 90.0/100**  
**Status: HEALTHY**  
**Generated:** 2026-06-14T03:42:14.452992+00:00  

## Metrics

| Metric | Value | Score | Weight | Status |
| :--- | :--- | :--- | :--- | :--- |
| graph_connectivity | 100.0% | 100/100 | 15% | 🟢 GREEN |
| orphan_rate | 34.7% | 20/100 | 10% | 🔴 RED |
| artifact_validity_rate | 100.0% | 100/100 | 20% | 🟢 GREEN |
| pipeline_success_rate | 100.0% | 100/100 | 15% | 🟢 GREEN |
| governance_compliance | 100.0% | 100/100 | 15% | 🟢 GREEN |
| provider_reliability | 100.0% | 100/100 | 10% | 🟢 GREEN |
| avg_latency_ms | 8243.0ms | 60/100 | 5% | 🟡 YELLOW |
| memory_assets | 5.0count | 100/100 | 5% | 🟢 GREEN |
| adr_coverage | 87.5% | 100/100 | 5% | 🟢 GREEN |

## Recommendations

- CRITICAL: orphan_rate = 34.7% — Files with no inbound links
- WARNING: avg_latency_ms = 8243.0ms — Average worker execution latency

---
*System Health Monitor v1 — Y-OS*