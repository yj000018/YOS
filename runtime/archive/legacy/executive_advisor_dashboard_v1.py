#!/usr/bin/env python3
"""
Module 7: Executive Advisor Dashboard v1 — Y-OS MISSION-025
Generates Dashboard_Strategic_Advisor.md with:
Top Risks, Top Opportunities, Top Bottlenecks, Top Technical Debt,
Recommended Missions, Roadmap, Strategic Priorities.
"""
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
from strategic_recommendation_engine_v1 import StrategicRecommendation, Category
from organizational_gap_analysis_v1 import GapFinding
from mission_proposal_generator_v1 import MissionProposal
from recommendation_prioritization_engine_v1 import PriorityEntry


def generate_advisor_dashboard(
    recommendations: list[StrategicRecommendation],
    gaps: list[GapFinding],
    proposals: list[MissionProposal],
    priority_queue: list[PriorityEntry],
    output_path: Path,
) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    def recs_by_cat(cat: Category) -> list[StrategicRecommendation]:
        return [r for r in recommendations if r.category == cat]

    risks = recs_by_cat(Category.RISK)
    opps = recs_by_cat(Category.OPPORTUNITY)
    bots = recs_by_cat(Category.BOTTLENECK)
    debts = recs_by_cat(Category.TECHNICAL_DEBT)

    def rec_rows(recs: list[StrategicRecommendation]) -> str:
        rows = ""
        for r in recs[:5]:
            rows += f"| {r.recommendation_id} | {r.title} | {r.impact.value} | {r.urgency.value} | {r.confidence:.0%} |\n"
        return rows or "| — | No findings | — | — | — |\n"

    def gap_rows(cat: str) -> str:
        rows = ""
        for g in [x for x in gaps if x.category == cat][:5]:
            rows += f"| {g.gap_id} | {g.title} | {g.severity} |\n"
        return rows or "| — | No gaps | — |\n"

    priority_rows = ""
    for e in priority_queue[:10]:
        priority_rows += f"| {e.rank} | {e.recommendation_id} | {e.title[:50]} | {e.priority_score} |\n"

    mission_rows = ""
    for p in sorted(proposals, key=lambda x: x.priority_rank)[:7]:
        mission_rows += f"| {p.mission_id} | {p.title} | {p.estimated_effort} | {p.confidence:.0%} | {p.category} |\n"

    content = f"""---
id: Dashboard_Strategic_Advisor
title: 'Strategic Advisor Dashboard — MISSION-025'
type: dashboard
status: live
mission: MISSION-025
generated_at: '{ts}'
tags: ['#dashboard', '#strategic', '#mission-025']
aliases: [Strategic Advisor Dashboard, Strategic Dashboard]
---

# Strategic Advisor Dashboard — MISSION-025

> **Generated:** {ts}  
> **Mission:** [[MISSION-025_Strategic_Recommendation_Engine]]  
> **Total Recommendations:** {len(recommendations)} | **Total Gaps:** {len(gaps)} | **Mission Proposals:** {len(proposals)}

---

## Executive Summary

Y-OS has achieved full organizational self-awareness (EIS 96/100, Graph Quality 100, Mission Lineage 100%).
The strategic gap is now cognitive: Y-OS can observe but not yet simulate.
**Priority 1: MISSION-026 Executive Simulation Layer.**

---

## Top Risks

| ID | Title | Impact | Urgency | Confidence |
| :--- | :--- | :--- | :--- | :--- |
{rec_rows(risks)}

---

## Top Opportunities

| ID | Title | Impact | Urgency | Confidence |
| :--- | :--- | :--- | :--- | :--- |
{rec_rows(opps)}

---

## Top Bottlenecks

| ID | Title | Impact | Urgency | Confidence |
| :--- | :--- | :--- | :--- | :--- |
{rec_rows(bots)}

---

## Top Technical Debt

| Gap ID | Title | Severity |
| :--- | :--- | :--- |
{gap_rows('TECHNICAL_DEBT')}

---

## Strategic Priority Queue (Top 10)

| Rank | ID | Title | Score |
| :--- | :--- | :--- | :--- |
{priority_rows}

---

## Recommended Missions

| Mission | Title | Effort | Confidence | Category |
| :--- | :--- | :--- | :--- | :--- |
{mission_rows}

---

## Navigation

- [[Dashboard_Executive_Cockpit]] — Executive Cockpit
- [[Dashboard_Time_Machine]] — Time Machine
- [[Dashboard_Graph_Quality]] — Graph Quality
- [[Dashboard_Providers]] — Provider Status
- [[Strategic_Roadmap]] — Strategic Roadmap Canvas
- [[00_Y-OS_Home]] — Home MOC

## Semantic Links

- **reports_to:** [[MISSION-025_Strategic_Recommendation_Engine]]
- **produced_by:** [[executive_advisor_dashboard_v1]]
- **depends_on:** [[MISSION-024_ODT_Time_Machine]], [[MISSION-020_Autonomous_Observability]]
"""
    output_path.write_text(content, encoding="utf-8")
