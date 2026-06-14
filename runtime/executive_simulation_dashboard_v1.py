#!/usr/bin/env python3
"""
Module 7: Executive Simulation Dashboard v1 — Y-OS MISSION-026
Generates Dashboard_Executive_Simulation.md + Executive_Simulation.canvas
"""
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone


def generate_simulation_dashboard(
    scenarios: list[dict],
    simulations: list[dict],
    counterfactuals: list[dict],
    comparisons: list[dict],
    memory_summary: dict,
    output_path: Path,
) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    scn_rows = ""
    for s in scenarios:
        scn_rows += f"| {s['scenario_id']} | {s['title']} | {s['scenario_type']} | {s['confidence']:.0%} |\n"

    sim_rows = ""
    for s in simulations:
        delta = s.get("state_delta", {})
        eis_d = delta.get("eis_score", {})
        eis_str = f"{eis_d.get('delta', 0):+.1f}" if isinstance(eis_d, dict) else "—"
        sim_rows += f"| {s['simulation_id']} | {s['proposed_change'][:40]} | {s['risk_level']} | {s['confidence']:.0%} | EIS {eis_str} |\n"

    cf_rows = ""
    for c in counterfactuals:
        cf_rows += f"| {c['cf_id']} | {c['question'][:55]} | {c['confidence']:.0%} |\n"

    dc_rows = ""
    for d in comparisons:
        dc_rows += f"| {d['comparison_id']} | {d['question'][:50]} | {d['best_option_id']} |\n"

    content = f"""---
id: Dashboard_Executive_Simulation
title: 'Executive Simulation Dashboard — MISSION-026'
type: dashboard
status: live
mission: MISSION-026
generated_at: '{ts}'
tags: ['#dashboard', '#simulation', '#mission-026']
aliases: [Executive Simulation Dashboard, Simulation Dashboard]
---

# Executive Simulation Dashboard — MISSION-026

> **Generated:** {ts}  
> **Mission:** [[MISSION-026_Executive_Simulation_Layer]]  
> **Scenarios:** {len(scenarios)} | **Simulations:** {len(simulations)} | **Counterfactuals:** {len(counterfactuals)} | **Decision Comparisons:** {len(comparisons)}

---

## Scenarios

| ID | Title | Type | Confidence |
| :--- | :--- | :--- | :--- |
{scn_rows}

---

## Simulation Results

| Simulation | Change | Risk | Confidence | EIS Delta |
| :--- | :--- | :--- | :--- | :--- |
{sim_rows}

---

## Counterfactual Analysis

| ID | Question | Confidence |
| :--- | :--- | :--- |
{cf_rows}

---

## Decision Comparisons

| ID | Question | Best Option |
| :--- | :--- | :--- |
{dc_rows}

---

## Simulation Memory

| Metric | Value |
| :--- | :--- |
| Total Records | {memory_summary.get('total_records', 0)} |
| Calibration Score | {memory_summary.get('calibration_score', 1.0):.3f} |
| By Status | {memory_summary.get('by_status', {})} |

---

## Key Insights

1. **MISSION-013 was the highest-impact mission** (+51 EIS points without it)
2. **Provider diversification (M-023) was the highest-leverage infrastructure decision**
3. **Next best action: MISSION-031** (Live Gemini validation — fastest, lowest risk)
4. **2-parallel execution** is optimal for roadmap acceleration
5. **Claude Opus 4 recommended** for Brahma/architecture worker

---

## Navigation

- [[Dashboard_Strategic_Advisor]] — Strategic Advisor
- [[Dashboard_Executive_Cockpit]] — Executive Cockpit
- [[Dashboard_Time_Machine]] — Time Machine
- [[Strategic_Roadmap]] — Roadmap
- [[00_Y-OS_Home]] — Home MOC

## Semantic Links

- **reports_to:** [[MISSION-026_Executive_Simulation_Layer]]
- **produced_by:** [[executive_simulation_dashboard_v1]]
- **depends_on:** [[MISSION-025_Strategic_Recommendation_Engine]], [[MISSION-024_ODT_Time_Machine]]
"""
    output_path.write_text(content, encoding="utf-8")


def generate_simulation_canvas(scenarios: list[dict], simulations: list[dict], output_path: Path) -> None:
    colors = {"LOW": "#10b981", "MEDIUM": "#f59e0b", "HIGH": "#ef4444"}
    nodes = [
        {"id": "center", "type": "text", "x": 0, "y": 0, "width": 180, "height": 60,
         "text": "**Executive Simulation Layer**\nMISSION-026", "color": "#6366f1"},
    ]
    edges = []
    for i, scn in enumerate(scenarios):
        angle_x = (i % 4) * 280 - 420
        angle_y = (i // 4) * 160 - 80
        node_id = scn["scenario_id"].lower()
        nodes.append({
            "id": node_id, "type": "text",
            "x": angle_x, "y": angle_y,
            "width": 200, "height": 80,
            "text": f"**{scn['scenario_id']}**\n{scn['title']}\n{scn['scenario_type']}",
            "color": "#1e293b",
        })
        edges.append({"id": f"e_{node_id}", "fromNode": "center", "toNode": node_id, "label": f"{scn['confidence']:.0%}"})

    canvas = {"nodes": nodes, "edges": edges}
    output_path.write_text(json.dumps(canvas, indent=2), encoding="utf-8")
