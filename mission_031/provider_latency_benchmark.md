---
title: Provider Latency Benchmark
mission: MISSION-031
generated: 2026-06-14
type: benchmark
---

# Provider Latency Benchmark — MISSION-031

## Cross-Provider (same task)

| Provider | Model | Latency (ms) | Tokens | ms/token |
|:---|:---|---:|---:|---:|
| openai | gpt-4o | 3100 | 336 | 9.23 |
| gemini | gemini-2.5-flash | 8096 | 563 | 14.38 |
| gemini | gemini-2.5-pro | 19929 | 509 | 39.15 |

## Multi-Model Availability

| Model | Status | Latency (ms) |
|:---|:---|---:|
| gemini-2.5-pro | AVAILABLE | 9584 |
| gemini-2.5-flash | AVAILABLE | 4447 |
| gemini-2.5-flash-lite | AVAILABLE | 460 |

## Worker Execution Latency (Gemini)

| Worker | Model | Latency (ms) | Tokens |
|:---|:---|---:|---:|
| Brahma | gemini-2.5-pro | 25760 | 1160 |
| Hanuman | gemini-2.5-flash | 5751 | 429 |
| Saraswati | gemini-2.5-flash | 17737 | 1118 |
| Lakshmi | gemini-2.5-flash | 17159 | 1797 |

## Latency Verdict

- **gemini-2.5-flash-lite**: fastest (~460ms) — suitable for low-latency tasks
- **gemini-2.5-flash**: balanced (4–18s) — default worker model
- **gemini-2.5-pro**: slowest (10–26s) — reserved for architecture/reasoning
- **gpt-4o**: fast (3s) — good for structured tasks
