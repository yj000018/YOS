---
type: k-card
domain: Y-OS
tags: [ai, model-routing, crt, cost-efficiency, yos]
created: 2026-05-29
status: active
---

# CRT Model Routing

The **CRT (Cost-Routing-Threshold)** model is the primary traffic director of the [[Y-OS]] cognitive layer. It intercepts every incoming prompt and routes it dynamically to the most cost-efficient LLM that satisfies the required quality threshold.

## Core Principles

- **Standard Routing**: Simple tasks (formatting, short-form editing, syntax checks) are routed to lighter models like Claude 3.5 Haiku or GPT-4o-mini.
- **Max Routing**: Complex architectural reasoning, multi-file code modifications, or philosophical synthesis are routed to Claude 3.5 Sonnet or GPT-5.
- **Dynamic Context Hygiene**: Cleans the context window by stripping redundant system prompts and compressing historical turns before sending to expensive endpoints [[Obsidian — Mermaid + Wikilinks incompatibility]].

## Integration

The CRT router connects directly to [[Manus Operations]] and is orchestrated by [[n8n Cognitive Automation]].

## Performance Metrics

| Mode | Target LLM | Avg Token Cost | Quality Index |
| :--- | :--- | :--- | :--- |
| **Standard** | GPT-4o-mini | $0.15 / M | 82% |
| **Balanced** | Claude 3.5 Haiku | $0.80 / M | 89% |
| **Max** | Claude 3.5 Sonnet | $3.00 / M | 98% |\n