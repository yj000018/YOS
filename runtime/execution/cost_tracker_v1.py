#!/usr/bin/env python3
"""
Cost Tracker v1 — Y-OS
ADR-0044

Estimates cost per provider/model and produces a cost report.
All prices are estimates — mark clearly.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Prices per 1M tokens (USD) — estimates, may be outdated
MODEL_PRICING: dict[str, dict[str, float]] = {
    "gpt-4o":          {"input": 2.50,  "output": 10.00},
    "gpt-4o-mini":     {"input": 0.15,  "output": 0.60},
    "gpt-4-turbo":     {"input": 10.00, "output": 30.00},
    "claude-opus-4-5": {"input": 15.00, "output": 75.00},
    "claude-sonnet-4-5":{"input": 3.00, "output": 15.00},
    "claude-haiku-3-5":{"input": 0.80,  "output": 4.00},
    "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
    "claude-3-5-haiku-20241022":  {"input": 0.80, "output": 4.00},
    "claude-opus-4-20250514":     {"input": 15.00, "output": 75.00},
    "claude-sonnet-4-20250514":   {"input": 3.00,  "output": 15.00},
}


@dataclass
class CostEntry:
    trace_id: str
    worker: str
    provider: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost_usd: float
    pricing_source: str = "estimated"


class CostTracker:
    """Tracks token usage and estimates costs."""

    def __init__(self):
        self._entries: list[CostEntry] = []

    def estimate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Estimate cost in USD."""
        pricing = MODEL_PRICING.get(model)
        if not pricing:
            # Unknown model — use gpt-4o as fallback estimate
            pricing = MODEL_PRICING["gpt-4o"]
        input_cost = (prompt_tokens / 1_000_000) * pricing["input"]
        output_cost = (completion_tokens / 1_000_000) * pricing["output"]
        return round(input_cost + output_cost, 8)

    def record(
        self,
        trace_id: str,
        worker: str,
        provider: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
    ) -> CostEntry:
        total = prompt_tokens + completion_tokens
        cost = self.estimate_cost(model, prompt_tokens, completion_tokens)
        entry = CostEntry(
            trace_id=trace_id,
            worker=worker,
            provider=provider,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total,
            estimated_cost_usd=cost,
        )
        self._entries.append(entry)
        return entry

    def total_cost(self) -> float:
        return round(sum(e.estimated_cost_usd for e in self._entries), 6)

    def total_tokens(self) -> int:
        return sum(e.total_tokens for e in self._entries)

    def produce_report(self, output_path: Path) -> str:
        lines = [
            "---",
            "id: yos-cost-report-mission-017",
            "title: Cost Report — MISSION-017",
            "type: cost_report",
            "mission_id: MISSION-017",
            f"generated: '{datetime.now(timezone.utc).isoformat()}'",
            "tags: ['#cost', '#yos', '#mission-017']",
            "---",
            "",
            "# Cost Report — MISSION-017",
            "",
            "> **DISCLAIMER:** All costs are estimates based on public pricing. Actual costs may differ.",
            "",
            f"**Generated:** {datetime.now(timezone.utc).isoformat()}",
            f"**Total Estimated Cost:** ${self.total_cost():.6f} USD",
            f"**Total Tokens:** {self.total_tokens():,}",
            "",
            "---",
            "",
            "## Per-Execution Breakdown",
            "",
            "| Trace ID | Worker | Provider | Model | Prompt | Completion | Total | Cost (USD) |",
            "| :--- | :--- | :--- | :--- | ---: | ---: | ---: | ---: |",
        ]
        for e in self._entries:
            lines.append(
                f"| {e.trace_id} | {e.worker} | {e.provider} | {e.model} | "
                f"{e.prompt_tokens:,} | {e.completion_tokens:,} | {e.total_tokens:,} | "
                f"${e.estimated_cost_usd:.6f} |"
            )
        lines += [
            "",
            "---",
            "",
            "## Summary",
            "",
            f"| Metric | Value |",
            f"| :--- | :--- |",
            f"| Total executions | {len(self._entries)} |",
            f"| Total prompt tokens | {sum(e.prompt_tokens for e in self._entries):,} |",
            f"| Total completion tokens | {sum(e.completion_tokens for e in self._entries):,} |",
            f"| Total tokens | {self.total_tokens():,} |",
            f"| Total estimated cost | ${self.total_cost():.6f} USD |",
            "",
            "---",
            "*Cost Tracker v1 — Y-OS — prices are estimates*",
        ]
        report = "\n".join(lines)
        output_path.write_text(report, encoding="utf-8")
        return report
