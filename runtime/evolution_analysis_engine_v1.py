#!/usr/bin/env python3
"""
Module 7: Evolution Analysis Engine v1 — Y-OS MISSION-024
Analyzes: growth, acceleration, bottlenecks, structural changes, organizational phases.
"""
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone
from odt_time_machine_v1 import ODTSnapshot


PHASE_DEFINITIONS = {
    "Foundation":  "M-001→M-004: Constitution, workers, governance framework",
    "Runtime":     "M-005→M-011: CCR Runtime, context architecture, execution engine",
    "Memory":      "M-012→M-012B: Session delta, living memory pipeline",
    "Graph":       "M-013→M-022A: Knowledge graph, cognitive architecture, semantic connectivity",
    "Execution":   "M-017→M-018: Live worker execution, multi-worker pipeline",
    "ODT":         "M-019→M-020: Organizational Digital Twin, autonomous observability",
    "Planning":    "M-021A: Roadmap architecture review",
    "Providers":   "M-023: Provider diversification (3 providers)",
    "Events":      "M-022: Live Event Bus, event-driven runtime",
}


class EvolutionAnalysisEngine:
    def __init__(self, snapshots: list[ODTSnapshot]):
        self.snapshots = snapshots

    def analyze(self) -> dict:
        phases: dict[str, list[ODTSnapshot]] = {}
        for s in self.snapshots:
            phases.setdefault(s.phase, []).append(s)

        # Growth rates
        first = self.snapshots[0]
        last = self.snapshots[-1]
        total_missions = last.missions_count - first.missions_count
        total_adrs = last.adrs_count - first.adrs_count

        # Acceleration: missions per phase
        phase_velocity = {
            phase: len(snaps) for phase, snaps in phases.items()
        }
        fastest_phase = max(phase_velocity, key=phase_velocity.get)

        # Bottlenecks: phases with only 1 mission
        bottlenecks = [p for p, v in phase_velocity.items() if v == 1]

        # Structural changes: phase transitions
        transitions = []
        prev_phase = None
        for s in self.snapshots:
            if s.phase != prev_phase:
                transitions.append({"phase": s.phase, "started_at": s.mission_id})
                prev_phase = s.phase

        # EIS acceleration
        eis_snapshots = [(s.mission_id, s.eis_score) for s in self.snapshots if s.eis_score > 0]
        eis_acceleration = []
        for i in range(1, len(eis_snapshots)):
            delta = eis_snapshots[i][1] - eis_snapshots[i - 1][1]
            if delta > 5:
                eis_acceleration.append({
                    "from": eis_snapshots[i - 1][0],
                    "to": eis_snapshots[i][0],
                    "delta": round(delta, 1),
                })

        return {
            "total_missions": total_missions,
            "total_adrs": total_adrs,
            "total_phases": len(phases),
            "phase_definitions": PHASE_DEFINITIONS,
            "phase_velocity": phase_velocity,
            "fastest_phase": fastest_phase,
            "bottlenecks": bottlenecks,
            "phase_transitions": transitions,
            "eis_acceleration_events": eis_acceleration,
            "graph_quality_journey": "0 → 65 → 82 → 100 (M-013 → M-015 → M-021)",
            "provider_evolution": "Mono-OpenAI → 3-provider (M-023)",
            "key_inflection_points": [
                "M-013: Graph compiler — corpus becomes navigable",
                "M-016: CCR Runtime v2 — execution engine live",
                "M-019: ODT — organizational self-awareness",
                "M-021: Graph Quality 100 — full connectivity",
                "M-023: Provider diversification — resilience",
                "M-022: Event Bus — event-driven runtime",
            ],
        }

    def generate_report(self, output_path: Path) -> None:
        analysis = self.analyze()
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

        phase_rows = ""
        for phase, count in analysis["phase_velocity"].items():
            defn = PHASE_DEFINITIONS.get(phase, "")
            phase_rows += f"| {phase} | {count} | {defn} |\n"

        inflection_rows = ""
        for point in analysis["key_inflection_points"]:
            inflection_rows += f"- {point}\n"

        accel_rows = ""
        for a in analysis["eis_acceleration_events"]:
            accel_rows += f"| {a['from']} → {a['to']} | +{a['delta']} |\n"

        content = f"""---
id: evolution_report
title: 'Y-OS Evolution Analysis Report — MISSION-024'
type: report
generated_at: '{ts}'
tags: ['#report', '#evolution', '#mission-024']
aliases: [Evolution Report]
---

# Y-OS Evolution Analysis Report

> **Generated:** {ts}  
> **Mission:** [[MISSION-024_ODT_Time_Machine]]

---

## Summary

| Metric | Value |
| :--- | :--- |
| Total Missions | {analysis['total_missions']} |
| Total ADRs | {analysis['total_adrs']} |
| Organizational Phases | {analysis['total_phases']} |
| Fastest Phase | {analysis['fastest_phase']} |
| Graph Quality Journey | {analysis['graph_quality_journey']} |
| Provider Evolution | {analysis['provider_evolution']} |

---

## Phase Analysis

| Phase | Missions | Description |
| :--- | :--- | :--- |
{phase_rows}
---

## EIS Acceleration Events

| Period | EIS Delta |
| :--- | :--- |
{accel_rows if accel_rows else "| No major acceleration events detected | — |\n"}

---

## Key Inflection Points

{inflection_rows}

---

## Semantic Links

- **reports_to:** [[MISSION-024_ODT_Time_Machine]]
- **produced_by:** [[evolution_analysis_engine_v1]]
"""
        output_path.write_text(content, encoding="utf-8")
