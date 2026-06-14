---
title: Provider Routing Validation
mission: MISSION-031
generated: 2026-06-14
type: validation
---

# Provider Routing Validation — MISSION-031

## Routing Decisions

| Worker | Task Type | Expected Model | Actual Model | Verdict |
|:---|:---|:---|:---|:---|
| Brahma | N/A | gemini-2.5-pro | gemini-2.5-pro | ✅ CORRECT |
| Hanuman | N/A | gemini-2.5-flash | gemini-2.5-flash | ✅ CORRECT |
| Saraswati | N/A | gemini-2.5-flash | gemini-2.5-flash | ✅ CORRECT |
| Lakshmi | N/A | gemini-2.5-flash | gemini-2.5-flash | ✅ CORRECT |

**Routing accuracy: 4/4 (100%)**

## Routing Rules Applied

| Rule | Provider | Rationale |
|:---|:---|:---|
| architecture → best reasoning | gemini-2.5-pro | Highest quality for complex analysis |
| build → cheapest valid | gemini-2.5-flash | 16x cheaper than Pro, sufficient quality |
| learning → large context | gemini-2.5-flash | 1M token context window |
| governance → safest | gemini-2.5-flash | Consistent, predictable output |

## Failover Routing

| Scenario | Primary | Fallback | Status |
|:---|:---|:---|:---|
| OPENAI_FAILED | openai | gemini/gemini-2.5-flash | FAILOVER_SUCCESS |
| ANTHROPIC_FAILED | anthropic | gemini/gemini-2.5-flash | FAILOVER_SUCCESS |
| GEMINI_FAILED | gemini | openai/gpt-4o-mini | FAILOVER_SUCCESS |
