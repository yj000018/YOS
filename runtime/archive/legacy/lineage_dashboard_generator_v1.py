#!/usr/bin/env python3
"""
Module 5: Lineage Dashboard Generator v1 — Y-OS MISSION-022A
Generates Dashboard_Lineage_Quality.md
"""
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone


def generate_lineage_dashboard(
    registry: dict,
    edges_total: int,
    coverage_before: float,
    coverage_after: float,
    confidence_dist: dict,
    validation_passed: bool,
    output_path: Path,
) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    total = len(registry)
    with_lineage = sum(1 for v in registry.values() if v["lineage_complete"])
    without_lineage = total - with_lineage
    high_conf = confidence_dist.get("HIGH", 0)
    medium_conf = confidence_dist.get("MEDIUM", 0)
    low_conf = confidence_dist.get("LOW", 0)

    content = f"""---
id: Dashboard_Lineage_Quality
title: 'Lineage Quality Dashboard — MISSION-022A'
type: dashboard
status: live
mission: MISSION-022A
generated_at: '{ts}'
tags:
  - '#dashboard'
  - '#lineage'
  - '#mission-022a'
aliases:
  - Lineage Quality Dashboard
---

# Lineage Quality Dashboard — MISSION-022A

> **Generated:** {ts}  
> **Mission:** [[MISSION-022A_Legacy_Mission_Lineage_Recovery]]

---

## Coverage Metrics

| Metric | Before | After | Target | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Mission Lineage Coverage** | {coverage_before:.1f}% | **{coverage_after:.1f}%** | > 95% | {'✅ PASS' if coverage_after >= 95 else '⚠️ PARTIAL'} |
| **Legacy Missions Indexed** | — | **{total}** | 100% | ✅ |
| **Missions with Lineage** | — | **{with_lineage}** | — | — |
| **Remaining Gaps** | — | **{without_lineage}** | 0 | {'✅' if without_lineage == 0 else '⚠️'} |
| **Total Inferred Edges** | — | **{edges_total}** | — | — |
| **Validation Passed** | — | **{'YES' if validation_passed else 'NO'}** | YES | {'✅' if validation_passed else '❌'} |

---

## Confidence Distribution

| Band | Count | % | Review Required |
| :--- | :--- | :--- | :--- |
| **HIGH** (≥ 0.90) | {high_conf} | {high_conf/max(1,edges_total)*100:.1f}% | No |
| **MEDIUM** (0.75–0.90) | {medium_conf} | {medium_conf/max(1,edges_total)*100:.1f}% | Yes |
| **LOW** (< 0.75) | {low_conf} | {low_conf/max(1,edges_total)*100:.1f}% | Yes |

---

## Legacy Mission Status

| Mission | Lineage | ADR Links | Dependencies | Status |
| :--- | :--- | :--- | :--- | :--- |
"""
    for m_id, m_data in sorted(registry.items(), key=lambda x: x[1]["mission_num"]):
        adr_count = len(m_data["adr_links"])
        dep_count = len(m_data["dependencies"])
        status = "✅ Resolved" if m_data["lineage_complete"] else "⚠️ Gap"
        content += f"| {m_id[:30]} | {'Yes' if m_data['lineage_complete'] else 'No'} | {adr_count} | {dep_count} | {status} |\n"

    content += f"""
---

## Navigation

- [[Mission_Lineage_Recovery]] — Recovery Canvas
- [[YOS_Mission_Lineage]] — Mission Lineage Canvas
- [[Dashboard_Graph_Quality]] — Graph Quality Dashboard
- [[Dashboard_Executive_Cockpit]] — Executive Cockpit
- [[00_Y-OS_Home]] — Home MOC

## Semantic Links

- **reports_to:** [[MISSION-022A_Legacy_Mission_Lineage_Recovery]]
- **measured_by:** [[legacy_lineage_recovery_engine_v1]]
- **published_to:** [[00_Y-OS_Home]]
"""
    output_path.write_text(content, encoding="utf-8")
