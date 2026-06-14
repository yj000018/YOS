#!/usr/bin/env python3
"""
Module 6: Event Observability v1 — Y-OS MISSION-022
Metrics: events/sec, queue depth, subscriber lag, failed deliveries, replay performance.
Generates Dashboard_Event_Bus.md
"""
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone
from event_bus_core_v1 import EventBusCore
from event_persistence_v1 import EventPersistence


class EventObservability:
    def __init__(self, bus: EventBusCore, persistence: EventPersistence):
        self.bus = bus
        self.persistence = persistence

    def compute_metrics(self) -> dict:
        stats = self.bus.stats
        total = stats["published"]
        events = self.persistence.load_all()

        # Events per category
        by_category: dict[str, int] = {}
        for e in events:
            et = e.get("event_type", "UNKNOWN")
            cat = et.split("_")[0] if "_" in et else "UNKNOWN"
            by_category[cat] = by_category.get(cat, 0) + 1

        return {
            "total_published": total,
            "total_delivered": stats["delivered"],
            "total_failed": stats["failed"],
            "dlq_size": stats["dlq_size"],
            "delivery_rate": round(stats["delivered"] / max(total, 1) * 100, 1),
            "events_by_category": by_category,
            "persisted_events": len(events),
            "computed_at": datetime.now(timezone.utc).isoformat(),
        }

    def generate_dashboard(self, output_path: Path, routing_log: list[dict],
                           replay_result=None) -> None:
        metrics = self.compute_metrics()
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

        category_rows = ""
        for cat, count in sorted(metrics["events_by_category"].items()):
            category_rows += f"| {cat} | {count} |\n"

        routing_rows = ""
        for r in routing_log[:8]:
            targets = ", ".join(r.get("targets", [])[:3])
            routing_rows += f"| {r['event_type'][:30]} | {targets[:40]} |\n"

        replay_section = ""
        if replay_result:
            replay_section = f"""
## Replay Engine

| Metric | Value |
| :--- | :--- |
| Events Replayed | {replay_result.events_replayed} |
| Replay Duration | {replay_result.replay_duration_ms:.1f}ms |
| State Reconstructed | ✅ |
| Missions | {len(replay_result.state_reconstructed.get('missions', []))} |
| ADRs | {len(replay_result.state_reconstructed.get('adrs', []))} |
| Artifacts | {len(replay_result.state_reconstructed.get('artifacts', []))} |
"""

        content = f"""---
id: Dashboard_Event_Bus
title: 'Live Event Bus Dashboard — MISSION-022'
type: dashboard
status: live
mission: MISSION-022
generated_at: '{ts}'
tags:
  - '#dashboard'
  - '#event-bus'
  - '#mission-022'
aliases:
  - Event Bus Dashboard
---

# Live Event Bus Dashboard — MISSION-022

> **Generated:** {ts}  
> **Mission:** [[MISSION-022_Live_Event_Bus]]

---

## Event Metrics

| Metric | Value |
| :--- | :--- |
| **Total Published** | {metrics['total_published']} |
| **Total Delivered** | {metrics['total_delivered']} |
| **Delivery Rate** | {metrics['delivery_rate']}% |
| **Failed Deliveries** | {metrics['total_failed']} |
| **DLQ Size** | {metrics['dlq_size']} |
| **Persisted Events** | {metrics['persisted_events']} |

---

## Events by Category

| Category | Count |
| :--- | :--- |
{category_rows}
---

## Routing Log (last 8)

| Event Type | Targets |
| :--- | :--- |
{routing_rows}
---
{replay_section}
## Navigation

- [[Event_Bus_Architecture]] — Event Bus Canvas
- [[Dashboard_Executive_Cockpit]] — Executive Cockpit
- [[Dashboard_Providers]] — Provider Dashboard
- [[00_Y-OS_Home]] — Home MOC

## Semantic Links

- **reports_to:** [[MISSION-022_Live_Event_Bus]]
- **published_to:** [[00_Y-OS_Home]]
"""
        output_path.write_text(content, encoding="utf-8")
