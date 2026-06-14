#!/usr/bin/env python3
"""
Module 5: Provider Cost Optimizer v1 — Y-OS MISSION-023
Tracks cost by provider/worker/mission and recommends lowest-cost valid route.
"""
from __future__ import annotations
import json
from dataclasses import dataclass, field
from provider_registry_v1 import ProviderRegistry
from provider_router_v2 import RoutingDecision


@dataclass
class CostRecord:
    provider: str
    worker: str
    mission: str
    tokens_in: int
    tokens_out: int
    cost_usd: float
    model: str


class ProviderCostOptimizer:
    def __init__(self, registry: ProviderRegistry):
        self.registry = registry
        self.records: list[CostRecord] = []

    def record(self, decision: RoutingDecision, mission: str,
               tokens_in: int = 1000, tokens_out: int = 500) -> float:
        """Record a cost event and return actual cost."""
        provider = self.registry.get_provider(decision.selected_provider)
        cost = 0.0
        if provider:
            for m in provider.models:
                if m.model_id == decision.selected_model:
                    cost = (tokens_in / 1000 * m.input_cost_per_1k +
                            tokens_out / 1000 * m.output_cost_per_1k)
                    break
        self.records.append(CostRecord(
            provider=decision.selected_provider,
            worker=decision.worker,
            mission=mission,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            cost_usd=round(cost, 6),
            model=decision.selected_model,
        ))
        return cost

    def recommend_cheapest(self, capability: str) -> dict:
        """Return lowest-cost valid provider+model for a capability."""
        models = self.registry.get_models_for_capability(capability)
        if not models:
            return {}
        cheapest = models[0]
        return {
            "capability": capability,
            "recommended_provider": cheapest.provider,
            "recommended_model": cheapest.model_id,
            "input_cost_per_1k": cheapest.input_cost_per_1k,
            "output_cost_per_1k": cheapest.output_cost_per_1k,
            "tier": cheapest.tier,
        }

    def cost_by_provider(self) -> dict[str, float]:
        result: dict[str, float] = {}
        for r in self.records:
            result[r.provider] = round(result.get(r.provider, 0) + r.cost_usd, 6)
        return result

    def cost_by_worker(self) -> dict[str, float]:
        result: dict[str, float] = {}
        for r in self.records:
            result[r.worker] = round(result.get(r.worker, 0) + r.cost_usd, 6)
        return result

    def cost_by_mission(self) -> dict[str, float]:
        result: dict[str, float] = {}
        for r in self.records:
            result[r.mission] = round(result.get(r.mission, 0) + r.cost_usd, 6)
        return result

    def total_cost(self) -> float:
        return round(sum(r.cost_usd for r in self.records), 6)

    def to_json(self) -> dict:
        return {
            "total_cost_usd": self.total_cost(),
            "by_provider": self.cost_by_provider(),
            "by_worker": self.cost_by_worker(),
            "by_mission": self.cost_by_mission(),
            "records": [
                {"provider": r.provider, "worker": r.worker, "model": r.model,
                 "tokens_in": r.tokens_in, "tokens_out": r.tokens_out,
                 "cost_usd": r.cost_usd, "mission": r.mission}
                for r in self.records
            ],
        }
