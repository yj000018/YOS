---
id: yos-dashboard-executive-cockpit
title: Y-OS Executive Cockpit
type: dashboard
subtype: executive_cockpit
mission_id: MISSION-020
eis_score: 87.5
eis_grade: B
health_score: 90.0
governance_compliance: 96.8
generated_at: '2026-06-14'
tags: ['#dashboard', '#executive', '#cockpit', '#yos', '#mission-020']
aliases:
  - Executive Cockpit
  - CEO Dashboard
---

# Y-OS Executive Cockpit

> A CEO should understand the state of Y-OS in under 60 seconds.

---

## System Status

| Indicator | Score | Status |
| :--- | :--- | :--- |
| **Executive Intelligence Score** | **87.5/100 — Grade B** | 🟢 GOOD |
| **Health Score** | **90/100** | 🟢 HEALTHY |
| **Governance Compliance** | **96.8/100** | 🟢 COMPLIANT |
| **Pipeline Success Rate** | **100%** | 🟢 EXCELLENT |
| **Artifact Validity** | **100%** | 🟢 EXCELLENT |
| **Graph Quality** | **47.9/100** | 🟡 FAIR (orphan rate 34.7%) |
| **Observability** | **85/100** | 🟢 GOOD |

---

## Active Alerts

| Alert | Severity | Category |
| :--- | :--- | :--- |
| High Orphan Rate (34.7%) | 🟠 HIGH | GRAPH_INTEGRITY |
| OpenAI Dependence (>70%) | 🟡 WARNING | PROVIDER_DEPENDENCE |
| Idle Workers Detected | 🟡 WARNING | WORKER_FAILURE |

---

## Graph Growth

```dataview
TABLE type, tags
FROM "mission_019"
WHERE file.name = "kg_semantic_graph_v3"
```

| Metric | Value |
| :--- | :--- |
| Graph Nodes | 645 |
| Graph Edges | 4,488 |
| Relationship Types | 29 |
| Concept Nodes | 39 |
| Markdown Files | 483+ |

---

## Artifact Growth

| Mission | Artifacts | Tokens | Cost |
| :--- | :--- | :--- | :--- |
| MISSION-017 | 4 | 4,297 | $0.076 |
| MISSION-018 | 6 | 4,836 | $0.074 |
| **TOTAL** | **10** | **9,133** | **$0.150** |

---

## Pipeline Activity

| Pipeline | Mission | Status | Steps | Artifacts |
| :--- | :--- | :--- | :--- | :--- |
| [[PIPE-5C15BA64]] | MISSION-018 | ✅ COMPLETED | 6 | 6 |

---

## Worker Utilization

| Worker | Capability | Executions | Artifacts | Tokens |
| :--- | :--- | :--- | :--- | :--- |
| Brahma | architecture | 2 | 2 | 1,957 |
| Hanuman | build | 2 | 2 | 1,595 |
| Saraswati | learning | 2 | 2 | 2,601 |
| Lakshmi | governance | 2 | 2 | 1,809 |
| Ganesha | reporting | 1 | 1 | 1,054 |
| CEO | directive | 1 | 1 | 0 |

---

## Provider Usage

| Provider | Calls | Tokens | Cost | Success |
| :--- | :--- | :--- | :--- | :--- |
| OpenAI | 8 (73%) | 6,412 | $0.120 | 100% |
| Anthropic | 2 (18%) | 2,601 | $0.030 | 100% |
| Human (CEO) | 1 (9%) | 0 | $0 | 100% |

---

## Cost Trends

```
M-013–016: $0.000 (no LLM calls)
M-017:     $0.076
M-018:     $0.074
M-019:     $0.000 (no LLM calls)
M-020:     $0.000 (no LLM calls)
CUMULATIVE: $0.150
```

---

## Recent ADRs

| ADR | Title | Status | Score |
| :--- | :--- | :--- | :--- |
| [[ADR-0047]] | Autonomous Organizational Observability | PROPOSED | — |
| [[ADR-0046]] | Organizational Digital Twin Runtime v1 | ACCEPTED | 12 |
| [[ADR-0045]] | Multi-Worker Pipeline Orchestration v1 | ACCEPTED | 10 |
| [[ADR-0044]] | Live Worker Execution v1 | ACCEPTED | 8 |
| [[ADR-0043]] | CCR Runtime v2 Implementation | ACCEPTED | 10 |

---

## Recent Missions

| Mission | Title | Status |
| :--- | :--- | :--- |
| [[MISSION-020]] | Autonomous Organizational Observability | 🔄 RUNNING |
| [[MISSION-019]] | Organizational Digital Twin Runtime v1 | ✅ PASSED |
| [[MISSION-018]] | Multi-Worker Pipeline Orchestration | ✅ PASSED |
| [[MISSION-017]] | Live Worker Execution | ✅ PASSED |
| [[MISSION-016]] | CCR Runtime v2 | ✅ PASSED |

---

## Recent Governance Events

| Event | Verdict | Score |
| :--- | :--- | :--- |
| ADR-0046 Lakshmi Review | APPROVE | 12/100 |
| PIPE-5C15BA64 Post-Review | APPROVE | 3/100 |
| ART-M018-GANESHA Post-Review | APPROVE | 3/100 |
| ART-M018-LAKSHMI Post-Review | APPROVE | 3/100 |

---

## Open Risks

1. **Orphan Rate 34.7%** — KGC v4 body wikilinks pass needed → MISSION-021
2. **OpenAI Dependence 73%** — Provider diversification needed → MISSION-023
3. **ODT Registry Static** — Live update hooks not yet automated → MISSION-020 (in progress)
4. **No Notion Sync** — Memory assets isolated to GitHub → MISSION-022

---

## Top Recommendations

1. **MISSION-021** — KGC v4 body wikilinks pass → reduce orphan rate to <15%
2. **MISSION-022** — Notion ODT Sync → push registry to Notion automatically
3. **MISSION-023** — Provider Diversification → add Gemini/Grok workers
4. Enable **Dataview plugin** in Obsidian vault for live dashboard queries
5. Enable **Breadcrumbs plugin** for hierarchical navigation

---

## Navigation

- [[YOS_Organizational_Digital_Twin]] — Master ODT Canvas
- [[ODT_Self_Observation]] — Self-Observation Canvas
- [[Dashboard_Live_Runtime]] — Runtime details
- [[Dashboard_Workers]] — Worker details
- [[Dashboard_Pipelines]] — Pipeline details
- [[Dashboard_Artifacts]] — Artifact details
- [[Dashboard_Economics]] — Cost details
- [[Dashboard_Governance]] — Governance details

---

*Executive Cockpit v1 — MISSION-020 — Y-OS*
