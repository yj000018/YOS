#!/usr/bin/env python3
"""
Module 1: Provider Router v2 — Y-OS MISSION-023
Dynamic provider selection based on worker, capability, mode, cost, latency, health.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from provider_registry_v1 import ProviderRegistry, ModelSpec


# ── Routing Strategy Map ──────────────────────────────────────────────────────
# worker_type → [(provider, model_tier, priority)]
ROUTING_STRATEGY = {
    "architecture": [
        ("openai",    "premium",  1),
        ("gemini",    "standard", 2),
        ("anthropic", "premium",  3),
    ],
    "build": [
        ("gemini",    "economy",  1),
        ("openai",    "economy",  2),
        ("anthropic", "economy",  3),
    ],
    "governance": [
        ("anthropic", "premium",  1),
        ("openai",    "premium",  2),
        ("gemini",    "standard", 3),
    ],
    "learning": [
        ("anthropic", "standard", 1),
        ("gemini",    "standard", 2),
        ("openai",    "economy",  3),
    ],
    "reporting": [
        ("openai",    "premium",  1),
        ("anthropic", "standard", 2),
        ("gemini",    "economy",  3),
    ],
}

# MODE overrides
MODE_PROVIDER_PREFERENCE = {
    "MODE-D": ["openai", "gemini", "anthropic"],   # Deep architecture
    "MODE-B": ["gemini", "openai", "anthropic"],   # Build (cost-first)
    "MODE-E": ["anthropic", "gemini", "openai"],   # Epistemic/learning
}


@dataclass
class RoutingDecision:
    worker: str
    capability: str
    mode: str
    selected_provider: str
    selected_model: str
    routing_reason: str
    fallback_chain: list[str]
    estimated_cost_per_1k: float
    confidence: float


class ProviderRouterV2:
    def __init__(self, registry: ProviderRegistry):
        self.registry = registry
        self.routing_log: list[RoutingDecision] = []

    def route(
        self,
        worker: str,
        capability: str,
        mode: str = "MODE-D",
        cost_budget: Optional[float] = None,
        latency_target_ms: Optional[float] = None,
    ) -> RoutingDecision:
        """Select optimal provider+model for given worker/capability/mode."""

        # Get mode preference order
        mode_prefs = MODE_PROVIDER_PREFERENCE.get(mode, ["openai", "anthropic", "gemini"])

        # Get capability strategy
        cap_strategy = ROUTING_STRATEGY.get(capability, ROUTING_STRATEGY["build"])

        # Build candidate list: mode preference × capability strategy
        candidates: list[tuple[str, str, int]] = []
        for provider_id in mode_prefs:
            for (strat_provider, tier, priority) in cap_strategy:
                if strat_provider == provider_id:
                    candidates.append((provider_id, tier, priority))
                    break

        # Add any missing providers from strategy
        for (strat_provider, tier, priority) in cap_strategy:
            if not any(c[0] == strat_provider for c in candidates):
                candidates.append((strat_provider, tier, priority))

        # Filter by health and find best model
        selected_provider = None
        selected_model = None
        routing_reason = ""
        fallback_chain = []

        for provider_id, tier, priority in candidates:
            provider = self.registry.get_provider(provider_id)
            if not provider or provider.health_state == "FAILED":
                fallback_chain.append(f"{provider_id}:FAILED")
                continue

            # Find matching model
            model = self._select_model(provider, capability, tier, cost_budget)
            if model:
                if selected_provider is None:
                    selected_provider = provider_id
                    selected_model = model.model_id
                    routing_reason = (
                        f"Mode={mode}, capability={capability}, "
                        f"provider={provider_id} (health={provider.health_state}, "
                        f"tier={tier}, priority={priority})"
                    )
                else:
                    fallback_chain.append(f"{provider_id}:{model.model_id}")

        # Ultimate fallback
        if not selected_provider:
            selected_provider = "openai"
            selected_model = "gpt-4o-mini-2024-07-18"
            routing_reason = "Ultimate fallback — all preferred providers unavailable"

        # Get cost
        cost = 0.0
        provider = self.registry.get_provider(selected_provider)
        if provider:
            for m in provider.models:
                if m.model_id == selected_model:
                    cost = m.input_cost_per_1k
                    break

        decision = RoutingDecision(
            worker=worker,
            capability=capability,
            mode=mode,
            selected_provider=selected_provider,
            selected_model=selected_model,
            routing_reason=routing_reason,
            fallback_chain=fallback_chain[:3],
            estimated_cost_per_1k=cost,
            confidence=0.95 if selected_provider != "openai" or mode == "MODE-D" else 0.85,
        )
        self.routing_log.append(decision)
        return decision

    def _select_model(self, provider, capability: str, tier: str,
                      cost_budget: Optional[float]) -> Optional[ModelSpec]:
        """Select best model from provider matching capability and tier."""
        candidates = [m for m in provider.models if capability in m.capabilities]
        if not candidates:
            candidates = provider.models  # fallback to any model

        # Filter by tier preference
        tier_candidates = [m for m in candidates if m.tier == tier]
        if not tier_candidates:
            tier_candidates = candidates

        # Filter by cost budget
        if cost_budget:
            budget_candidates = [m for m in tier_candidates
                                  if m.input_cost_per_1k <= cost_budget]
            if budget_candidates:
                tier_candidates = budget_candidates

        # Return cheapest qualifying model
        return min(tier_candidates, key=lambda m: m.input_cost_per_1k) if tier_candidates else None

    def compute_provider_share(self) -> dict[str, float]:
        """Compute provider share from routing log."""
        if not self.routing_log:
            return {}
        counts: dict[str, int] = {}
        for d in self.routing_log:
            counts[d.selected_provider] = counts.get(d.selected_provider, 0) + 1
        total = len(self.routing_log)
        return {p: round(c / total * 100, 1) for p, c in counts.items()}
