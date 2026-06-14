#!/usr/bin/env python3
"""
Execution Trace Logger v1 — Y-OS
ADR-0044

Records every provider execution as a JSONL trace entry.
Never logs secret values.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import json
import uuid


@dataclass
class ExecutionTrace:
    trace_id: str = field(default_factory=lambda: f"TRACE-{uuid.uuid4().hex[:8].upper()}")
    mission_id: str = ""
    worker: str = ""
    capability: str = ""
    context_pack_id: str = ""
    selected_mode: str = ""
    provider: str = ""
    model: str = ""
    status: str = ""           # SUCCESS | FAILED | SKIPPED_MISSING_SECRET | FALLBACK
    latency_ms: float = 0.0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    estimated_cost_usd: float = 0.0
    artifact_id: str = ""
    error_type: str = ""
    error_message_redacted: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return asdict(self)

    def to_jsonl(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)


class ExecutionTraceLogger:
    """Appends execution traces to a JSONL file."""

    def __init__(self, trace_file: Path):
        self.trace_file = trace_file
        self.trace_file.parent.mkdir(parents=True, exist_ok=True)
        self._traces: list[ExecutionTrace] = []

    def log(self, trace: ExecutionTrace) -> None:
        self._traces.append(trace)
        with open(self.trace_file, "a", encoding="utf-8") as f:
            f.write(trace.to_jsonl() + "\n")

    def get_traces(self) -> list[ExecutionTrace]:
        return list(self._traces)

    def summary(self) -> dict:
        if not self._traces:
            return {"total": 0}
        success = [t for t in self._traces if t.status == "SUCCESS"]
        failed = [t for t in self._traces if t.status == "FAILED"]
        skipped = [t for t in self._traces if t.status == "SKIPPED_MISSING_SECRET"]
        fallback = [t for t in self._traces if t.status == "FALLBACK"]
        total_tokens = sum(t.total_tokens for t in self._traces)
        total_cost = sum(t.estimated_cost_usd for t in self._traces)
        avg_latency = (
            sum(t.latency_ms for t in success) / len(success) if success else 0.0
        )
        return {
            "total": len(self._traces),
            "success": len(success),
            "failed": len(failed),
            "skipped": len(skipped),
            "fallback": len(fallback),
            "total_tokens": total_tokens,
            "estimated_cost_usd": round(total_cost, 6),
            "avg_latency_ms": round(avg_latency, 1),
        }
