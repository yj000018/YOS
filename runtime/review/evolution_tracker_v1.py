#!/usr/bin/env python3
"""
Evolution Tracker v1 — Y-OS
ADR-0046

Tracks growth of ADRs, Missions, Concepts, Pipelines, Artifacts, Workers, Costs, Graph.
Generates evolution_report.json + evolution_report.md
"""

from __future__ import annotations
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class EvolutionSnapshot:
    date: str
    mission: str
    adrs: int
    missions: int
    concepts: int
    pipelines: int
    artifacts: int
    graph_nodes: int
    graph_edges: int
    total_tokens: int
    total_cost_usd: float
    markdown_files: int


EVOLUTION_HISTORY = [
    EvolutionSnapshot("2026-06-14-M013", "MISSION-013", 20, 12, 0, 0, 0, 301, 565, 0, 0.0, 301),
    EvolutionSnapshot("2026-06-14-M014", "MISSION-014", 21, 13, 12, 0, 0, 330, 600, 0, 0.0, 330),
    EvolutionSnapshot("2026-06-14-M015", "MISSION-015", 22, 14, 39, 0, 0, 375, 4498, 0, 0.0, 375),
    EvolutionSnapshot("2026-06-14-M016", "MISSION-016", 23, 15, 39, 0, 0, 381, 4520, 0, 0.0, 381),
    EvolutionSnapshot("2026-06-14-M017", "MISSION-017", 24, 16, 39, 0, 4, 395, 4600, 4297, 0.076055, 395),
    EvolutionSnapshot("2026-06-14-M018", "MISSION-018", 25, 17, 39, 1, 10, 420, 4800, 9133, 0.150190, 420),
    EvolutionSnapshot("2026-06-14-M019", "MISSION-019", 26, 18, 39, 1, 10, 450, 5200, 9133, 0.150190, 450),
]


class EvolutionTracker:
    """Tracks Y-OS organizational evolution over missions."""

    def __init__(self):
        self.snapshots = EVOLUTION_HISTORY

    def growth_rate(self, field_name: str) -> dict:
        """Calculate growth from first to last snapshot."""
        first = getattr(self.snapshots[0], field_name, 0)
        last = getattr(self.snapshots[-1], field_name, 0)
        delta = last - first
        pct = round(delta / first * 100, 1) if first > 0 else 0.0
        return {"first": first, "last": last, "delta": delta, "growth_pct": pct}

    def generate_report(self) -> dict:
        fields = ["adrs", "missions", "concepts", "pipelines", "artifacts",
                  "graph_nodes", "graph_edges", "total_tokens", "total_cost_usd", "markdown_files"]
        return {
            "schema_version": "1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "mission": "MISSION-019",
            "snapshots": len(self.snapshots),
            "growth": {f: self.growth_rate(f) for f in fields},
            "snapshots_data": [asdict(s) for s in self.snapshots],
        }

    def save(self, json_path: Path, md_path: Path) -> None:
        report = self.generate_report()
        json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

        lines = [
            "---",
            "id: yos-evolution-report-v1",
            "title: Y-OS Evolution Report v1",
            "type: evolution_report",
            "mission_id: MISSION-019",
            f"generated_at: '{report['generated_at']}'",
            "tags: ['#evolution', '#yos', '#mission-019']",
            "---",
            "",
            "# Y-OS Evolution Report v1",
            "",
            f"**Snapshots:** {report['snapshots']}  ",
            f"**Generated:** {report['generated_at']}  ",
            "",
            "## Growth Summary",
            "",
            "| Metric | Start | Current | Delta | Growth |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ]
        for metric, g in report["growth"].items():
            lines.append(f"| {metric} | {g['first']} | {g['last']} | +{g['delta']} | {g['growth_pct']}% |")
        lines += [
            "",
            "## Mission Timeline",
            "",
            "| Mission | ADRs | Concepts | Artifacts | Graph Nodes | Graph Edges | Cost |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
        ]
        for s in self.snapshots:
            lines.append(
                f"| [[{s.mission}]] | {s.adrs} | {s.concepts} | {s.artifacts} | "
                f"{s.graph_nodes} | {s.graph_edges} | ${s.total_cost_usd:.4f} |"
            )
        lines += ["", "---", "*Evolution Tracker v1 — Y-OS*"]
        md_path.write_text("\n".join(lines), encoding="utf-8")
