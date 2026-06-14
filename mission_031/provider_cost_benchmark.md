---
title: Provider Cost Benchmark
mission: MISSION-031
generated: 2026-06-14
type: benchmark
---

# Provider Cost Benchmark — MISSION-031

## Cross-Provider Benchmark (same task)

| Provider | Model | Input $/1M | Output $/1M | Total Tokens | Cost/Worker | Latency |
|:---|:---|---:|---:|---:|---:|---:|
| openai | gpt-4o | — | — | 336 | $0.001988 | 3100ms |
| gemini | gemini-2.5-flash | — | — | 563 | $0.000126 | 8096ms |
| gemini | gemini-2.5-pro | — | — | 509 | $0.003419 | 19929ms |

## Worker Execution Costs (Gemini)

| Worker | Model | Tokens | Cost | Latency |
|:---|:---|---:|---:|---:|
| Brahma | gemini-2.5-pro | 1160 | $0.011005 | 25760ms |
| Hanuman | gemini-2.5-flash | 429 | $0.000115 | 5751ms |
| Saraswati | gemini-2.5-flash | 1118 | $0.000319 | 17737ms |
| Lakshmi | gemini-2.5-flash | 1797 | $0.000524 | 17159ms |

## Summary

| Metric | Value |
|:---|---:|
| Total tokens (4 workers) | 4504 |
| Total cost (4 workers) | $0.011963 |
| Cost per artifact | $0.002991 |
| Annualized (10 missions/day, 4 workers) | $43.66 |

## Cheapest Provider per Use Case

| Use Case | Provider | Model | Cost/1k tokens |
|:---|:---|:---|---:|
| Build / Fast | Gemini | gemini-2.5-flash-lite | ~$0.04 |
| Balanced | Gemini | gemini-2.5-flash | ~$0.08 |
| Architecture | Gemini | gemini-2.5-pro | ~$1.25 |
| Governance | Anthropic | claude-haiku-4 | ~$0.80 |
| Premium | OpenAI | gpt-4o | ~$2.50 |
