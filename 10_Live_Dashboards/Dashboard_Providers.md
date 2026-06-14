---
id: Dashboard_Providers
title: 'Provider Observability Dashboard — MISSION-023'
type: dashboard
status: live
mission: MISSION-023
generated_at: '2026-06-14 04:48 UTC'
tags:
  - '#dashboard'
  - '#providers'
  - '#mission-023'
aliases:
  - Provider Dashboard
---

# Provider Observability Dashboard — MISSION-023

> **Generated:** 2026-06-14 04:48 UTC  
> **Mission:** [[MISSION-023_Provider_Diversification]]

---

## Provider Share

| Provider | Share | Before | Target | Status |
| :--- | :--- | :--- | :--- | :--- |
| **OpenAI** | **42.9%** | 73% | < 50% | ✅ |
| **Anthropic** | **28.6%** | 27% | > 20% | ✅ |
| **Gemini** | **28.6%** | 0% | > 20% | ✅ |

---

## Provider Health

| Provider | State | Availability | Latency (ms) | Success Rate | Score |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Openai** | ✅ HEALTHY | 99.9% | 650 | 99.7% | 90.1/100 |
| **Anthropic** | ✅ HEALTHY | 99.7% | 900 | 99.5% | 86.2/100 |
| **Gemini** | ✅ HEALTHY | 99.5% | 750 | 99.3% | 88.3/100 |

---

## Cost Analysis

| Metric | Value |
| :--- | :--- |
| **Total Cost (session)** | $0.085950 USD |
| Openai Cost | $0.022500 (42.9% of calls) |
| Gemini Cost | $0.000450 (28.6% of calls) |
| Anthropic Cost | $0.063000 (28.6% of calls) |

---

## Routing Distribution (last 10 decisions)

| Worker | Mode | Provider | Model | Reason |
| :--- | :--- | :--- | :--- | :--- |
| Brahma | MODE-D | openai | gpt-4o-2024-08-06 | Mode=MODE-D, capability=architecture, pr... |
| Hanuman | MODE-B | gemini | gemini-1.5-flash | Mode=MODE-B, capability=build, provider=... |
| Saraswati | MODE-E | anthropic | claude-sonnet-4-20250514 | Mode=MODE-E, capability=learning, provid... |
| Lakshmi | MODE-D | openai | gpt-4o-2024-08-06 | Mode=MODE-D, capability=governance, prov... |
| Ganesha | MODE-D | openai | gpt-4o-2024-08-06 | Mode=MODE-D, capability=reporting, provi... |
| Vishnu | MODE-E | anthropic | claude-opus-4-20250514 | Mode=MODE-E, capability=architecture, pr... |
| Indra | MODE-B | gemini | gemini-1.5-flash | Mode=MODE-B, capability=build, provider=... |

---

## Navigation

- [[Provider_Routing]] — Provider Routing Canvas
- [[Dashboard_Executive_Cockpit]] — Executive Cockpit
- [[Dashboard_Graph_Quality]] — Graph Quality Dashboard
- [[00_Y-OS_Home]] — Home MOC

## Semantic Links

- **reports_to:** [[MISSION-023_Provider_Diversification]]
- **published_to:** [[00_Y-OS_Home]]
