#!/usr/bin/env python3
"""
Module 3: Provider Health Monitor v1 — Y-OS MISSION-023
Tracks availability, latency, success rate, cost anomalies.
"""
from __future__ import annotations
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from provider_registry_v1 import ProviderRegistry


@dataclass
class HealthMetrics:
    provider_id: str
    health_state: str
    availability: float
    avg_latency_ms: float
    success_rate: float
    cost_anomaly: bool
    score: float  # 0-100
    checked_at: str = ""

    def __post_init__(self):
        if not self.checked_at:
            self.checked_at = datetime.now(timezone.utc).isoformat()


class ProviderHealthMonitor:
    def __init__(self, registry: ProviderRegistry):
        self.registry = registry
        self.metrics: dict[str, HealthMetrics] = {}

    def check_all(self) -> dict[str, HealthMetrics]:
        """Simulate health check for all providers."""
        for pid, provider in self.registry.providers.items():
            # Compute health score
            avail_score = provider.availability * 40
            latency_score = max(0, (2000 - provider.avg_latency_ms) / 2000 * 30)
            success_score = provider.success_rate * 30
            score = avail_score + latency_score + success_score

            # Determine state
            if score >= 85:
                state = "HEALTHY"
            elif score >= 60:
                state = "DEGRADED"
            else:
                state = "FAILED"

            # Cost anomaly: if any model costs > 10x the cheapest
            costs = [m.input_cost_per_1k for m in provider.models]
            cost_anomaly = (max(costs) / min(costs) > 10) if costs else False

            self.metrics[pid] = HealthMetrics(
                provider_id=pid,
                health_state=state,
                availability=provider.availability,
                avg_latency_ms=provider.avg_latency_ms,
                success_rate=provider.success_rate,
                cost_anomaly=cost_anomaly,
                score=round(score, 1),
            )
            # Update registry
            self.registry.set_health(pid, state)

        return self.metrics

    def to_json(self) -> dict:
        return {
            pid: {
                "health_state": m.health_state,
                "availability": m.availability,
                "avg_latency_ms": m.avg_latency_ms,
                "success_rate": m.success_rate,
                "cost_anomaly": m.cost_anomaly,
                "score": m.score,
                "checked_at": m.checked_at,
            }
            for pid, m in self.metrics.items()
        }
