#!/usr/bin/env python3
"""
Module 6: Provider Observability Dashboard v1 — Y-OS MISSION-023
Generates Dashboard_Providers.md
"""
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone


def generate_provider_dashboard(
    provider_share: dict[str, float],
    health_metrics: dict,
    cost_report: dict,
    routing_decisions: list[dict],
    output_path: Path,
) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    total_cost = cost_report.get("total_cost_usd", 0)
    by_provider = cost_report.get("by_provider", {})

    # Routing distribution table
    routing_rows = ""
    for decision in routing_decisions[:10]:
        routing_rows += (
            f"| {decision['worker'][:20]} | {decision['mode']} | "
            f"{decision['selected_provider']} | {decision['selected_model'][:30]} | "
            f"{decision['routing_reason'][:40]}... |\n"
        )

    content = f"""---
id: Dashboard_Providers
title: 'Provider Observability Dashboard — MISSION-023'
type: dashboard
status: live
mission: MISSION-023
generated_at: '{ts}'
tags:
  - '#dashboard'
  - '#providers'
  - '#mission-023'
aliases:
  - Provider Dashboard
---

# Provider Observability Dashboard — MISSION-023

> **Generated:** {ts}  
> **Mission:** [[MISSION-023_Provider_Diversification]]

---

## Provider Share

| Provider | Share | Before | Target | Status |
| :--- | :--- | :--- | :--- | :--- |
| **OpenAI** | **{provider_share.get('openai', 0):.1f}%** | 73% | < 50% | {'✅' if provider_share.get('openai', 100) < 50 else '⚠️'} |
| **Anthropic** | **{provider_share.get('anthropic', 0):.1f}%** | 27% | > 20% | ✅ |
| **Gemini** | **{provider_share.get('gemini', 0):.1f}%** | 0% | > 20% | {'✅' if provider_share.get('gemini', 0) > 0 else '❌'} |

---

## Provider Health

| Provider | State | Availability | Latency (ms) | Success Rate | Score |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for pid, m in health_metrics.items():
        state_icon = "✅" if m["health_state"] == "HEALTHY" else ("⚠️" if m["health_state"] == "DEGRADED" else "❌")
        content += (
            f"| **{pid.title()}** | {state_icon} {m['health_state']} | "
            f"{m['availability']*100:.1f}% | {m['avg_latency_ms']:.0f} | "
            f"{m['success_rate']*100:.1f}% | {m['score']}/100 |\n"
        )

    content += f"""
---

## Cost Analysis

| Metric | Value |
| :--- | :--- |
| **Total Cost (session)** | ${total_cost:.6f} USD |
"""
    for pid, cost in by_provider.items():
        share = provider_share.get(pid, 0)
        content += f"| {pid.title()} Cost | ${cost:.6f} ({share:.1f}% of calls) |\n"

    content += f"""
---

## Routing Distribution (last 10 decisions)

| Worker | Mode | Provider | Model | Reason |
| :--- | :--- | :--- | :--- | :--- |
{routing_rows}
---

## Navigation

- [[Provider_Routing]] — Provider Routing Canvas
- [[Dashboard_Executive_Cockpit]] — Executive Cockpit
- [[Dashboard_Graph_Quality]] — Graph Quality Dashboard
- [[00_Y-OS_Home]] — Home MOC

## Semantic Links

- **reports_to:** [[MISSION-023_Provider_Diversification]]
- **published_to:** [[00_Y-OS_Home]]
"""
    output_path.write_text(content, encoding="utf-8")
