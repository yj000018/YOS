#!/usr/bin/env python3
"""
Module 6: Historical Navigation Dashboard v1 — Y-OS MISSION-024
Generates Dashboard_Time_Machine.md with mission, ADR, worker, provider, graph, EIS evolution views.
"""
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
from odt_time_machine_v1 import ODTSnapshot


def generate_time_machine_dashboard(
    snapshots: list[ODTSnapshot],
    phase_transitions: list[dict],
    output_path: Path,
) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    first = snapshots[0]
    last = snapshots[-1]

    transition_rows = ""
    for t in phase_transitions:
        transition_rows += f"| {t['from_phase']} | {t['to_phase']} | {t['at_mission']} | {t['timestamp'][:10]} |\n"

    snapshot_rows = ""
    for s in snapshots[-8:]:  # Last 8 snapshots
        snapshot_rows += f"| {s.mission_id} | {s.phase} | {s.missions_count} | {s.adrs_count} | {s.graph_quality} | {s.eis_score} |\n"

    content = f"""---
id: Dashboard_Time_Machine
title: 'ODT Time Machine Dashboard — MISSION-024'
type: dashboard
status: live
mission: MISSION-024
generated_at: '{ts}'
tags: ['#dashboard', '#time-machine', '#mission-024']
aliases: [Time Machine Dashboard]
---

# ODT Time Machine Dashboard — MISSION-024

> **Generated:** {ts}  
> **Mission:** [[MISSION-024_ODT_Time_Machine]]

---

## Y-OS Organizational Summary

| Metric | First State (M-001) | Current State (M-024) | Delta |
| :--- | :--- | :--- | :--- |
| **Missions** | {first.missions_count} | {last.missions_count} | +{last.missions_count - first.missions_count} |
| **ADRs** | {first.adrs_count} | {last.adrs_count} | +{last.adrs_count - first.adrs_count} |
| **Artifacts** | {first.artifacts_count} | {last.artifacts_count} | +{last.artifacts_count - first.artifacts_count} |
| **Workers** | {first.workers_count} | {last.workers_count} | +{last.workers_count - first.workers_count} |
| **Graph Quality** | {first.graph_quality} | {last.graph_quality} | +{round(last.graph_quality - first.graph_quality, 1)} |
| **EIS Score** | {first.eis_score} | {last.eis_score} | +{round(last.eis_score - first.eis_score, 1)} |

---

## Phase Transitions

| From Phase | To Phase | At Mission | Date |
| :--- | :--- | :--- | :--- |
{transition_rows}
---

## Recent Snapshots (Last 8)

| Mission | Phase | Missions | ADRs | Graph Quality | EIS |
| :--- | :--- | :--- | :--- | :--- | :--- |
{snapshot_rows}
---

## Navigation

- [[Timeline_Missions]] — Mission Timeline
- [[Timeline_ADRs]] — ADR Timeline
- [[Timeline_Providers]] — Provider Timeline
- [[Timeline_Evolution]] — Evolution Timeline
- [[ODT_Time_Machine]] — Time Machine Canvas
- [[Dashboard_Executive_Cockpit]] — Executive Cockpit
- [[00_Y-OS_Home]] — Home MOC

## Semantic Links

- **reports_to:** [[MISSION-024_ODT_Time_Machine]]
- **produced_by:** [[historical_navigation_dashboard_v1]]
"""
    output_path.write_text(content, encoding="utf-8")
