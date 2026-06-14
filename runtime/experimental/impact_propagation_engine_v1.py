#!/usr/bin/env python3
"""
Module 3: Impact Propagation Engine v1 — Y-OS MISSION-026
Propagates effects through: missions, ADRs, workers, providers, artifacts, events, dashboards.
Output: impact graph with typed edges.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone


PROPAGATION_RULES = {
    "provider_openai_pct": {
        "affects": ["workers", "artifacts", "cost", "events"],
        "cascade": {"eis_score": -0.5, "monthly_cost_usd": +0.02},
    },
    "provider_gemini_pct": {
        "affects": ["workers", "artifacts", "cost"],
        "cascade": {"monthly_cost_usd": -0.03},
    },
    "active_workers": {
        "affects": ["missions", "artifacts", "events"],
        "cascade": {"total_missions": +2, "eis_score": +0.8},
    },
    "orphan_rate": {
        "affects": ["graph", "dashboards", "navigation"],
        "cascade": {"eis_score": -0.3},
    },
    "graph_quality": {
        "affects": ["dashboards", "navigation", "semantic_search"],
        "cascade": {"eis_score": +0.2},
    },
    "governance_compliance": {
        "affects": ["adrs", "missions", "artifacts"],
        "cascade": {"eis_score": +0.1},
    },
    "monthly_cost_usd": {
        "affects": ["providers", "workers"],
        "cascade": {},
    },
    "notion_sync": {
        "affects": ["memory", "dashboards"],
        "cascade": {"eis_score": +0.5},
    },
    "simulation_layer": {
        "affects": ["decisions", "roadmap", "dashboards"],
        "cascade": {"eis_score": +1.0},
    },
}


@dataclass
class ImpactNode:
    node_id: str
    layer: str
    impact_type: str   # DIRECT / CASCADE
    magnitude: float   # -1.0 to +1.0
    description: str


@dataclass
class ImpactEdge:
    from_node: str
    to_node: str
    relationship: str
    weight: float


@dataclass
class ImpactGraph:
    scenario_id: str
    nodes: list[ImpactNode] = field(default_factory=list)
    edges: list[ImpactEdge] = field(default_factory=list)
    total_impact_score: float = 0.0
    computed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return {
            "scenario_id": self.scenario_id,
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "total_impact_score": self.total_impact_score,
            "nodes": [n.__dict__ for n in self.nodes],
            "edges": [e.__dict__ for e in self.edges],
            "computed_at": self.computed_at,
        }


class ImpactPropagationEngine:
    def propagate(self, scenario_id: str, state_delta: dict) -> ImpactGraph:
        graph = ImpactGraph(scenario_id=scenario_id)
        total = 0.0

        for attr, change in state_delta.items():
            if not isinstance(change, dict):
                continue
            delta = change.get("delta", 0)
            if not isinstance(delta, (int, float)):
                continue

            # Direct impact node
            direct_id = f"direct_{attr}"
            magnitude = max(-1.0, min(1.0, delta / 10.0))
            graph.nodes.append(ImpactNode(
                node_id=direct_id,
                layer="DIRECT",
                impact_type="DIRECT",
                magnitude=magnitude,
                description=f"{attr}: {change['before']} → {change['after']}",
            ))
            total += abs(magnitude)

            # Cascade propagation
            rules = PROPAGATION_RULES.get(attr, {})
            for affected_layer in rules.get("affects", []):
                cascade_id = f"cascade_{attr}_{affected_layer}"
                graph.nodes.append(ImpactNode(
                    node_id=cascade_id,
                    layer=affected_layer.upper(),
                    impact_type="CASCADE",
                    magnitude=magnitude * 0.5,
                    description=f"{attr} change propagates to {affected_layer}",
                ))
                graph.edges.append(ImpactEdge(
                    from_node=direct_id,
                    to_node=cascade_id,
                    relationship="propagates_to",
                    weight=abs(magnitude) * 0.5,
                ))
                total += abs(magnitude) * 0.3

            for cascade_attr, cascade_delta in rules.get("cascade", {}).items():
                cascade_id2 = f"secondary_{attr}_{cascade_attr}"
                graph.nodes.append(ImpactNode(
                    node_id=cascade_id2,
                    layer="SECONDARY",
                    impact_type="CASCADE",
                    magnitude=cascade_delta / 10.0,
                    description=f"Secondary: {cascade_attr} affected by {attr}",
                ))
                graph.edges.append(ImpactEdge(
                    from_node=direct_id,
                    to_node=cascade_id2,
                    relationship="secondary_effect",
                    weight=abs(cascade_delta) / 10.0,
                ))

        graph.total_impact_score = round(total, 3)
        return graph
