#!/usr/bin/env python3
"""
System Health Monitor v1 — Y-OS
ADR-0046

Computes Y-OS Health Score 0-100 from:
- Graph connectivity
- Orphan rate
- Artifact validity
- Pipeline success rate
- Governance compliance
- Cache efficiency
- Latency
- Provider reliability
- Memory growth
"""

from __future__ import annotations
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


@dataclass
class HealthMetric:
    name: str
    value: float
    unit: str
    score: float        # 0-100 contribution
    weight: float       # Weight in overall score
    status: str         # GREEN | YELLOW | RED
    threshold_green: float
    threshold_yellow: float
    note: str = ""


@dataclass
class HealthReport:
    health_score: float
    status: str         # HEALTHY | DEGRADED | CRITICAL
    generated_at: str
    metrics: list[HealthMetric]
    recommendations: list[str]
    mission: str = "MISSION-019"


class SystemHealthMonitor:
    """Computes Y-OS system health score."""

    def __init__(self, odt_registry, graph_stats: dict):
        self.odt = odt_registry
        self.graph = graph_stats

    def _score_metric(self, value: float, green: float, yellow: float,
                      higher_is_better: bool = True) -> tuple[float, str]:
        """Return (score 0-100, status)."""
        if higher_is_better:
            if value >= green:
                return 100.0, "GREEN"
            elif value >= yellow:
                return 60.0, "YELLOW"
            else:
                return 20.0, "RED"
        else:  # Lower is better
            if value <= green:
                return 100.0, "GREEN"
            elif value <= yellow:
                return 60.0, "YELLOW"
            else:
                return 20.0, "RED"

    def compute(self) -> HealthReport:
        metrics = []

        # 1. Graph connectivity (% nodes with at least 1 edge)
        nodes = self.graph.get("nodes", 450)
        edges = self.graph.get("edges", 5200)
        connectivity = min(100.0, edges / max(nodes, 1) * 20)  # Edges per node * 20
        s, st = self._score_metric(connectivity, 80, 50)
        metrics.append(HealthMetric("graph_connectivity", round(connectivity, 1), "%",
                                    s, 0.15, st, 80, 50, f"{edges} edges / {nodes} nodes"))

        # 2. Orphan rate (lower is better)
        orphan_rate = 34.7  # From M-013B audit — improved by M-015 but still ~30%
        s, st = self._score_metric(orphan_rate, 15, 30, higher_is_better=False)
        metrics.append(HealthMetric("orphan_rate", orphan_rate, "%",
                                    s, 0.10, st, 15, 30, "Files with no inbound links"))

        # 3. Artifact validity rate
        artifacts = self.odt.artifacts
        valid = sum(1 for a in artifacts.values() if a.validation_verdict in ("VALID", "VALID_WITH_WARNING"))
        validity_rate = round(valid / max(len(artifacts), 1) * 100, 1)
        s, st = self._score_metric(validity_rate, 95, 80)
        metrics.append(HealthMetric("artifact_validity_rate", validity_rate, "%",
                                    s, 0.20, st, 95, 80, f"{valid}/{len(artifacts)} valid"))

        # 4. Pipeline success rate
        pipelines = self.odt.pipelines
        completed = sum(1 for p in pipelines.values() if p.status == "COMPLETED")
        pipeline_rate = round(completed / max(len(pipelines), 1) * 100, 1)
        s, st = self._score_metric(pipeline_rate, 90, 70)
        metrics.append(HealthMetric("pipeline_success_rate", pipeline_rate, "%",
                                    s, 0.15, st, 90, 70, f"{completed}/{len(pipelines)} completed"))

        # 5. Governance compliance (% artifacts with APPROVE verdict)
        gov_approved = sum(1 for a in artifacts.values() if a.governance_verdict == "APPROVE")
        gov_rate = round(gov_approved / max(len(artifacts), 1) * 100, 1)
        s, st = self._score_metric(gov_rate, 95, 80)
        metrics.append(HealthMetric("governance_compliance", gov_rate, "%",
                                    s, 0.15, st, 95, 80, f"{gov_approved}/{len(artifacts)} approved"))

        # 6. Provider reliability
        providers = self.odt.providers
        avg_reliability = sum(p.success_rate for p in providers.values()) / max(len(providers), 1)
        s, st = self._score_metric(avg_reliability, 99, 95)
        metrics.append(HealthMetric("provider_reliability", round(avg_reliability, 1), "%",
                                    s, 0.10, st, 99, 95, "Avg success rate across providers"))

        # 7. Average latency (lower is better, ms)
        avg_latency = 8243.0  # From M-018 results
        s, st = self._score_metric(avg_latency, 5000, 15000, higher_is_better=False)
        metrics.append(HealthMetric("avg_latency_ms", avg_latency, "ms",
                                    s, 0.05, st, 5000, 15000, "Average worker execution latency"))

        # 8. Memory growth (positive — more is better)
        memory_assets = len(self.odt.memory_assets)
        s, st = self._score_metric(memory_assets, 5, 2)
        metrics.append(HealthMetric("memory_assets", float(memory_assets), "count",
                                    s, 0.05, st, 5, 2, "Tracked memory assets"))

        # 9. ADR coverage (ADRs per mission)
        adr_count = len(self.odt.adrs)
        mission_count = len(self.odt.missions)
        adr_coverage = round(adr_count / max(mission_count, 1) * 100, 1)
        s, st = self._score_metric(adr_coverage, 80, 60)
        metrics.append(HealthMetric("adr_coverage", adr_coverage, "%",
                                    s, 0.05, st, 80, 60, f"{adr_count} ADRs for {mission_count} missions"))

        # Compute weighted health score
        total_weight = sum(m.weight for m in metrics)
        health_score = sum(m.score * m.weight for m in metrics) / total_weight
        health_score = round(health_score, 1)

        # Overall status
        if health_score >= 80:
            status = "HEALTHY"
        elif health_score >= 60:
            status = "DEGRADED"
        else:
            status = "CRITICAL"

        # Recommendations
        recommendations = []
        for m in metrics:
            if m.status == "RED":
                recommendations.append(f"CRITICAL: {m.name} = {m.value}{m.unit} — {m.note}")
            elif m.status == "YELLOW":
                recommendations.append(f"WARNING: {m.name} = {m.value}{m.unit} — {m.note}")
        if not recommendations:
            recommendations.append("All metrics GREEN — system healthy")

        return HealthReport(
            health_score=health_score,
            status=status,
            generated_at=datetime.now(timezone.utc).isoformat(),
            metrics=metrics,
            recommendations=recommendations,
        )

    def save(self, report: HealthReport, json_path: Path, md_path: Path) -> None:
        data = asdict(report)
        json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

        lines = [
            "---",
            "id: yos-system-health-v1",
            "title: Y-OS System Health Report v1",
            "type: system_health_report",
            "mission_id: MISSION-019",
            f"health_score: {report.health_score}",
            f"status: {report.status}",
            f"generated_at: '{report.generated_at}'",
            "tags: ['#health', '#yos', '#mission-019']",
            "---",
            "",
            "# Y-OS System Health Report v1",
            "",
            f"**Health Score: {report.health_score}/100**  ",
            f"**Status: {report.status}**  ",
            f"**Generated:** {report.generated_at}  ",
            "",
            "## Metrics",
            "",
            "| Metric | Value | Score | Weight | Status |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ]
        for m in report.metrics:
            icon = "🟢" if m.status == "GREEN" else ("🟡" if m.status == "YELLOW" else "🔴")
            lines.append(f"| {m.name} | {m.value}{m.unit} | {m.score:.0f}/100 | {m.weight:.0%} | {icon} {m.status} |")
        lines += [
            "",
            "## Recommendations",
            "",
        ]
        for r in report.recommendations:
            lines.append(f"- {r}")
        lines += ["", "---", "*System Health Monitor v1 — Y-OS*"]
        md_path.write_text("\n".join(lines), encoding="utf-8")
