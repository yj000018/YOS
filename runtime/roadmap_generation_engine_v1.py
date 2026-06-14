#!/usr/bin/env python3
"""
Module 8: Roadmap Generation Engine v1 — Y-OS MISSION-025
Generates: 6-month, 12-month, 24-month roadmap + Strategic_Roadmap.canvas
"""
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone
from mission_proposal_generator_v1 import MissionProposal


ROADMAP = {
    "6_months": [
        {"mission": "MISSION-026", "title": "Executive Simulation Layer", "quarter": "Q3 2026", "priority": "CRITICAL"},
        {"mission": "MISSION-031", "title": "Live Gemini + Budget Enforcement", "quarter": "Q3 2026", "priority": "HIGH"},
        {"mission": "MISSION-029", "title": "Notion ODT Sync + Cross-Session Memory", "quarter": "Q3 2026", "priority": "HIGH"},
    ],
    "12_months": [
        {"mission": "MISSION-027", "title": "KGC v5 — Semantic Depth Pass", "quarter": "Q4 2026", "priority": "HIGH"},
        {"mission": "MISSION-028", "title": "n8n Integration — Autonomous Scheduling", "quarter": "Q4 2026", "priority": "HIGH"},
        {"mission": "MISSION-030", "title": "Constitutional Amendment Protocol", "quarter": "Q1 2027", "priority": "MEDIUM"},
    ],
    "24_months": [
        {"mission": "MISSION-032", "title": "Dashboard Exporter + Semantic Search", "quarter": "Q2 2027", "priority": "MEDIUM"},
        {"mission": "MISSION-033", "title": "Autonomous Mission Execution (no human trigger)", "quarter": "Q3 2027", "priority": "HIGH"},
        {"mission": "MISSION-034", "title": "Multi-Agent Y-OS (parallel cognitive workers)", "quarter": "Q4 2027", "priority": "HIGH"},
    ],
}


def generate_roadmap_canvas(proposals: list[MissionProposal], output_path: Path) -> None:
    nodes = [
        {"id": "now", "type": "text", "x": 0, "y": 0, "width": 160, "height": 60,
         "text": "**NOW**\nM-025 Strategic Engine", "color": "#10b981"},
    ]
    edges = []

    colors = {"CRITICAL": "#ef4444", "HIGH": "#f59e0b", "MEDIUM": "#6366f1", "LOW": "#94a3b8"}
    horizons = {"6_months": 300, "12_months": 600, "24_months": 900}
    horizon_labels = {"6_months": "6 Months (Q3 2026)", "12_months": "12 Months (Q4 2026–Q1 2027)", "24_months": "24 Months (2027)"}

    for horizon, x_offset in horizons.items():
        nodes.append({
            "id": f"h_{horizon}", "type": "text",
            "x": x_offset, "y": -120, "width": 200, "height": 50,
            "text": f"**{horizon_labels[horizon]}**", "color": "#1e293b",
        })
        for i, item in enumerate(ROADMAP[horizon]):
            node_id = item["mission"].lower().replace("-", "_")
            nodes.append({
                "id": node_id, "type": "text",
                "x": x_offset, "y": i * 120,
                "width": 200, "height": 80,
                "text": f"**{item['mission']}**\n{item['title']}\n{item['priority']}",
                "color": colors.get(item["priority"], "#94a3b8"),
            })
            edges.append({
                "id": f"e_{node_id}",
                "fromNode": "now" if i == 0 else list(horizons.keys()).index(horizon) > 0 and f"h_{list(horizons.keys())[list(horizons.keys()).index(horizon)-1]}",
                "toNode": node_id,
                "label": item["quarter"],
            })

    canvas = {"nodes": nodes, "edges": [e for e in edges if e.get("fromNode")]}
    output_path.write_text(json.dumps(canvas, indent=2), encoding="utf-8")


def generate_roadmap_md(output_path: Path) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    def rows(horizon: str) -> str:
        result = ""
        for item in ROADMAP[horizon]:
            result += f"| {item['mission']} | {item['title']} | {item['quarter']} | {item['priority']} |\n"
        return result

    content = f"""---
id: Strategic_Roadmap
title: 'Y-OS Strategic Roadmap 2026–2027'
type: roadmap
generated_at: '{ts}'
tags: ['#roadmap', '#strategic', '#mission-025']
aliases: [Strategic Roadmap, Y-OS Roadmap]
---

# Y-OS Strategic Roadmap 2026–2027

> **Generated:** {ts}  
> **Mission:** [[MISSION-025_Strategic_Recommendation_Engine]]

---

## 6-Month Horizon (Q3 2026)

| Mission | Title | Quarter | Priority |
| :--- | :--- | :--- | :--- |
{rows('6_months')}

---

## 12-Month Horizon (Q4 2026 – Q1 2027)

| Mission | Title | Quarter | Priority |
| :--- | :--- | :--- | :--- |
{rows('12_months')}

---

## 24-Month Horizon (2027)

| Mission | Title | Quarter | Priority |
| :--- | :--- | :--- | :--- |
{rows('24_months')}

---

## Semantic Links

- **reports_to:** [[MISSION-025_Strategic_Recommendation_Engine]]
- **produced_by:** [[roadmap_generation_engine_v1]]
- **depends_on:** [[Dashboard_Strategic_Advisor]]
"""
    output_path.write_text(content, encoding="utf-8")
