#!/usr/bin/env python3
"""
Module 2: Provider Registry v1 — Y-OS MISSION-023
Tracks providers, models, pricing, capabilities, limits, health state.
"""
from __future__ import annotations
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional


@dataclass
class ModelSpec:
    model_id: str
    provider: str
    context_window: int
    input_cost_per_1k: float   # USD per 1K tokens
    output_cost_per_1k: float
    capabilities: list[str]    # architecture, build, governance, learning, vision
    max_output_tokens: int
    supports_system_prompt: bool = True
    tier: str = "standard"     # standard / premium / economy


@dataclass
class ProviderSpec:
    provider_id: str
    display_name: str
    api_base: str
    health_state: str = "HEALTHY"   # HEALTHY / DEGRADED / FAILED
    availability: float = 1.0       # 0.0–1.0
    avg_latency_ms: float = 800.0
    success_rate: float = 1.0
    models: list[ModelSpec] = field(default_factory=list)
    last_checked: str = ""

    def __post_init__(self):
        if not self.last_checked:
            self.last_checked = datetime.now(timezone.utc).isoformat()


# ── Provider Definitions ──────────────────────────────────────────────────────

PROVIDER_REGISTRY: dict[str, ProviderSpec] = {
    "openai": ProviderSpec(
        provider_id="openai",
        display_name="OpenAI",
        api_base="https://api.openai.com/v1",
        health_state="HEALTHY",
        availability=0.999,
        avg_latency_ms=650,
        success_rate=0.997,
        models=[
            ModelSpec(
                model_id="gpt-4o-2024-08-06",
                provider="openai",
                context_window=128000,
                input_cost_per_1k=0.0025,
                output_cost_per_1k=0.010,
                capabilities=["architecture", "governance", "build", "vision"],
                max_output_tokens=16384,
                tier="premium",
            ),
            ModelSpec(
                model_id="gpt-4o-mini-2024-07-18",
                provider="openai",
                context_window=128000,
                input_cost_per_1k=0.00015,
                output_cost_per_1k=0.0006,
                capabilities=["build", "learning"],
                max_output_tokens=16384,
                tier="economy",
            ),
            ModelSpec(
                model_id="o1-mini",
                provider="openai",
                context_window=128000,
                input_cost_per_1k=0.003,
                output_cost_per_1k=0.012,
                capabilities=["architecture", "reasoning"],
                max_output_tokens=65536,
                tier="premium",
            ),
        ],
    ),
    "anthropic": ProviderSpec(
        provider_id="anthropic",
        display_name="Anthropic",
        api_base="https://api.anthropic.com/v1",
        health_state="HEALTHY",
        availability=0.997,
        avg_latency_ms=900,
        success_rate=0.995,
        models=[
            ModelSpec(
                model_id="claude-opus-4-20250514",
                provider="anthropic",
                context_window=200000,
                input_cost_per_1k=0.015,
                output_cost_per_1k=0.075,
                capabilities=["learning", "governance", "architecture", "long_context"],
                max_output_tokens=32000,
                tier="premium",
            ),
            ModelSpec(
                model_id="claude-sonnet-4-20250514",
                provider="anthropic",
                context_window=200000,
                input_cost_per_1k=0.003,
                output_cost_per_1k=0.015,
                capabilities=["learning", "build", "governance"],
                max_output_tokens=16000,
                tier="standard",
            ),
            ModelSpec(
                model_id="claude-haiku-3-5",
                provider="anthropic",
                context_window=200000,
                input_cost_per_1k=0.00025,
                output_cost_per_1k=0.00125,
                capabilities=["build", "learning"],
                max_output_tokens=8192,
                tier="economy",
            ),
        ],
    ),
    "gemini": ProviderSpec(
        provider_id="gemini",
        display_name="Google Gemini",
        api_base="https://generativelanguage.googleapis.com/v1beta",
        health_state="HEALTHY",
        availability=0.995,
        avg_latency_ms=750,
        success_rate=0.993,
        models=[
            ModelSpec(
                model_id="gemini-2.0-flash-exp",
                provider="gemini",
                context_window=1000000,
                input_cost_per_1k=0.00010,
                output_cost_per_1k=0.00040,
                capabilities=["architecture", "learning", "long_context", "vision"],
                max_output_tokens=8192,
                tier="economy",
            ),
            ModelSpec(
                model_id="gemini-1.5-pro",
                provider="gemini",
                context_window=2000000,
                input_cost_per_1k=0.00125,
                output_cost_per_1k=0.005,
                capabilities=["architecture", "learning", "long_context", "governance"],
                max_output_tokens=8192,
                tier="standard",
            ),
            ModelSpec(
                model_id="gemini-1.5-flash",
                provider="gemini",
                context_window=1000000,
                input_cost_per_1k=0.000075,
                output_cost_per_1k=0.0003,
                capabilities=["build", "learning"],
                max_output_tokens=8192,
                tier="economy",
            ),
        ],
    ),
}


class ProviderRegistry:
    def __init__(self):
        self.providers = PROVIDER_REGISTRY

    def get_provider(self, provider_id: str) -> Optional[ProviderSpec]:
        return self.providers.get(provider_id)

    def get_healthy_providers(self) -> list[str]:
        return [pid for pid, p in self.providers.items()
                if p.health_state != "FAILED"]

    def get_models_for_capability(self, capability: str) -> list[ModelSpec]:
        models = []
        for p in self.providers.values():
            if p.health_state == "FAILED":
                continue
            for m in p.models:
                if capability in m.capabilities:
                    models.append(m)
        return sorted(models, key=lambda m: m.input_cost_per_1k)

    def set_health(self, provider_id: str, state: str) -> None:
        if provider_id in self.providers:
            self.providers[provider_id].health_state = state
            self.providers[provider_id].last_checked = datetime.now(timezone.utc).isoformat()

    def to_json(self) -> dict:
        result = {}
        for pid, p in self.providers.items():
            result[pid] = {
                "provider_id": p.provider_id,
                "display_name": p.display_name,
                "health_state": p.health_state,
                "availability": p.availability,
                "avg_latency_ms": p.avg_latency_ms,
                "success_rate": p.success_rate,
                "model_count": len(p.models),
                "models": [
                    {
                        "model_id": m.model_id,
                        "tier": m.tier,
                        "capabilities": m.capabilities,
                        "input_cost_per_1k": m.input_cost_per_1k,
                        "output_cost_per_1k": m.output_cost_per_1k,
                        "context_window": m.context_window,
                    }
                    for m in p.models
                ],
            }
        return result
