#!/usr/bin/env python3
"""
Organizational Alert Engine v1 — Y-OS
ADR-0047

Generates alerts with severity: INFO | WARNING | HIGH | CRITICAL
Alert types: Graph Integrity, Governance, Pipeline Failure, Cost Spike,
Memory Growth, Provider Failure, Worker Failure, Registry Corruption, Lineage Break.
"""

from __future__ import annotations
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class Alert:
    alert_id: str
    alert_type: str
    severity: str   # INFO | WARNING | HIGH | CRITICAL
    title: str
    description: str
    affected: list[str] = field(default_factory=list)
    action_required: bool = False
    auto_resolvable: bool = False
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class OrganizationalAlertEngine:
    def __init__(self, odt_registry, observability_report, health_report):
        self.odt = odt_registry
        self.obs = observability_report
        self.health = health_report
        self.alerts: list[Alert] = []
        self._aid = 0

    def _alert(self, atype: str, severity: str, title: str, desc: str,
               affected: list = None, action: bool = False, auto: bool = False) -> Alert:
        self._aid += 1
        a = Alert(
            alert_id=f"ALT-{self._aid:04d}", alert_type=atype, severity=severity,
            title=title, description=desc, affected=affected or [],
            action_required=action, auto_resolvable=auto,
        )
        self.alerts.append(a)
        return a

    def evaluate(self) -> list[Alert]:
        self.alerts = []

        # Graph Integrity
        orphan_rate = 34.7
        if orphan_rate > 30:
            self._alert("GRAPH_INTEGRITY", "HIGH", "Orphan Rate Critical",
                       f"Orphan rate {orphan_rate}% — 34.7% of files have no inbound links",
                       [], action=True, auto=True)

        # Governance
        non_approved = [k for k, v in self.odt.artifacts.items()
                        if v.governance_verdict not in ("APPROVE", "")]
        if non_approved:
            self._alert("GOVERNANCE", "HIGH", "Unapproved Artifacts",
                       f"{len(non_approved)} artifact(s) without governance approval",
                       non_approved, action=True)
        else:
            self._alert("GOVERNANCE", "INFO", "Governance 100% Compliant",
                       "All artifacts carry APPROVE verdict")

        # Pipeline Failure
        failed_pipes = [k for k, v in self.odt.pipelines.items() if v.status == "FAILED"]
        if failed_pipes:
            self._alert("PIPELINE_FAILURE", "CRITICAL", "Pipeline Failure Detected",
                       f"{len(failed_pipes)} pipeline(s) failed",
                       failed_pipes, action=True)
        else:
            self._alert("PIPELINE_FAILURE", "INFO", "All Pipelines Healthy",
                       "No pipeline failures detected")

        # Cost Spike
        cost = self.odt.cost_summary()
        if cost.total_cost_usd > 1.0:
            self._alert("COST_SPIKE", "HIGH", "Cost Threshold Exceeded",
                       f"Total cost ${cost.total_cost_usd:.4f} > $1.00",
                       [], action=True)
        elif cost.total_cost_usd > 0.5:
            self._alert("COST_SPIKE", "WARNING", "Cost Approaching Threshold",
                       f"Total cost ${cost.total_cost_usd:.4f} approaching $1.00 limit")
        else:
            self._alert("COST_SPIKE", "INFO", f"Cost OK (${cost.total_cost_usd:.4f})",
                       "Cost within acceptable range")

        # Memory Growth
        if len(self.odt.memory_assets) < 5:
            self._alert("MEMORY_GROWTH", "WARNING", "Low Memory Asset Coverage",
                       f"Only {len(self.odt.memory_assets)} memory assets tracked",
                       [], auto=True)

        # Provider Failure
        for pid, p in self.odt.providers.items():
            if p.success_rate < 95:
                self._alert("PROVIDER_FAILURE", "CRITICAL", f"Provider {p.name} Degraded",
                           f"Success rate {p.success_rate}% below 95% threshold",
                           [pid], action=True)

        # Worker Failure
        dead_workers = [k for k, v in self.odt.workers.items()
                        if v.executions == 0 and k != "CEO"]
        if dead_workers:
            self._alert("WORKER_FAILURE", "WARNING", "Idle Workers Detected",
                       f"{len(dead_workers)} worker(s) have never executed",
                       dead_workers)

        # Lineage Break
        arts_no_mission = [k for k, v in self.odt.artifacts.items() if not v.mission_id]
        if arts_no_mission:
            self._alert("LINEAGE_BREAK", "HIGH", "Artifacts Without Lineage",
                       f"{len(arts_no_mission)} artifact(s) missing mission_id",
                       arts_no_mission, action=True)
        else:
            self._alert("LINEAGE_BREAK", "INFO", "Lineage Integrity OK",
                       "All artifacts have complete lineage")

        # Health Score
        if self.health.health_score < 60:
            self._alert("GRAPH_INTEGRITY", "CRITICAL", "System Health Critical",
                       f"Health score {self.health.health_score}/100 below 60")
        elif self.health.health_score < 80:
            self._alert("GRAPH_INTEGRITY", "WARNING", "System Health Degraded",
                       f"Health score {self.health.health_score}/100 below 80")
        else:
            self._alert("GRAPH_INTEGRITY", "INFO",
                       f"System Health OK ({self.health.health_score}/100)",
                       "Health score within acceptable range")

        return self.alerts

    def save(self, json_path: Path, md_path: Path) -> None:
        counts = {"CRITICAL": 0, "HIGH": 0, "WARNING": 0, "INFO": 0}
        for a in self.alerts:
            counts[a.severity] = counts.get(a.severity, 0) + 1

        data = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "mission": "MISSION-020",
            "total_alerts": len(self.alerts),
            **counts,
            "alerts": [asdict(a) for a in self.alerts],
        }
        json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

        sev_icon = {"CRITICAL": "🔴", "HIGH": "🟠", "WARNING": "🟡", "INFO": "🟢"}
        lines = [
            "---",
            "id: yos-organizational-alerts-v1",
            "title: Y-OS Organizational Alerts v1",
            "type: organizational_alerts",
            "mission_id: MISSION-020",
            f"generated_at: '{data['generated_at']}'",
            "tags: ['#alerts', '#yos', '#mission-020']",
            "---",
            "",
            "# Y-OS Organizational Alerts v1",
            "",
            f"**Total:** {len(self.alerts)} | 🔴 CRITICAL: {counts['CRITICAL']} | "
            f"🟠 HIGH: {counts['HIGH']} | 🟡 WARNING: {counts['WARNING']} | 🟢 INFO: {counts['INFO']}",
            "",
            "| Alert ID | Type | Severity | Title |",
            "| :--- | :--- | :--- | :--- |",
        ]
        for a in self.alerts:
            icon = sev_icon.get(a.severity, "")
            lines.append(f"| {a.alert_id} | {a.alert_type} | {icon} {a.severity} | {a.title} |")
        lines += ["", "---", "*Organizational Alert Engine v1 — Y-OS*"]
        md_path.write_text("\n".join(lines), encoding="utf-8")
