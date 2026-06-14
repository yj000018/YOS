---
title: Dashboard — Providers
mission: MISSION-031
updated: 2026-06-14
type: dashboard
---

# Provider Dashboard — Y-OS Runtime

> Updated by MISSION-031 — Gemini promoted to Tier-1

## Provider Registry v2

| Provider | Tier | Status | Models | Share Target | Validated |
|:---|:---|:---|:---|:---|:---|
| OpenAI | Tier-1 | ACTIVE | gpt-4o, gpt-4o-mini | 35% | ✅ |
| Anthropic | Tier-1 | ACTIVE | claude-opus-4, claude-haiku-4 | 30% | ✅ |
| **Gemini** | **Tier-1** | **ACTIVE** | gemini-2.5-pro, gemini-2.5-flash, gemini-2.5-flash-lite | **35%** | **✅ NEW** |

## Quality Ranking (MISSION-031 benchmark)

| Rank | Provider | Model | Score |
|:---|:---|:---|---:|
| #1 | gemini | gemini-2.5-flash | 88.3/100 |
| #2 | gemini | gemini-2.5-pro | 88.3/100 |
| #3 | openai | gpt-4o | 83.8/100 |

## Failover Matrix

| Primary Fails | Fallback | Status |
|:---|:---|:---|
| OpenAI | Gemini | ✅ VALIDATED |
| Anthropic | Gemini | ✅ VALIDATED |
| Gemini | OpenAI | ✅ VALIDATED |

## Cost Efficiency

| Model | Cost/1k tokens | Best For |
|:---|---:|:---|
| gemini-2.5-flash-lite | ~$0.04 | Fast/cheap tasks |
| gemini-2.5-flash | ~$0.08 | Default workers |
| gpt-4o-mini | ~$0.08 | Structured output |
| gemini-2.5-pro | ~$1.25 | Architecture |
| gpt-4o | ~$2.50 | Premium reasoning |
| claude-opus-4 | ~$15.00 | Long-context governance |
