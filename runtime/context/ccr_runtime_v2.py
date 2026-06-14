#!/usr/bin/env python3
"""
CCR Runtime v2 — Context Router
ADR-0037 / ADR-0043 — Y-OS

Selects context compilation mode (B/D/E) based on routing inputs.
No raw session history is ever injected.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional
import json


# ─── Routing Inputs ──────────────────────────────────────────────────────────

@dataclass
class RoutingRequest:
    mission_id: str
    worker: str                          # Brahma, Hanuman, Saraswati, Ganesha, etc.
    capability: str                      # architecture, build, learning, governance, etc.
    task_type: str = "standard"          # standard | strategic | constitutional | complex
    governance_risk: int = 0             # 0–100
    token_budget: int = 8000             # max tokens for context pack
    recent_delta_required: bool = False  # True if unresolved session delta needed
    constitutional_scope: bool = False   # True if ADR/doctrine/constitution work


# ─── Routing Output ───────────────────────────────────────────────────────────

@dataclass
class RoutingDecision:
    selected_mode: str                   # MODE-B | MODE-D | MODE-E
    reason: str
    context_sources: list[str]
    token_budget: int
    governance_required: bool
    worker: str
    capability: str
    mission_id: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


# ─── Mode Definitions ─────────────────────────────────────────────────────────

MODES = {
    "MODE-B": {
        "name": "Context Pack Only",
        "description": "Default for normal execution. Minimal, focused context.",
        "sources": ["context_pack"],
        "roi": 140.9,
        "token_multiplier": 1.0,
    },
    "MODE-D": {
        "name": "Context Pack + Canonical Memory",
        "description": "For strategy, architecture, governance, ADR, constitutional work.",
        "sources": ["context_pack", "canonical_memory"],
        "roi": 89.2,
        "token_multiplier": 1.6,
    },
    "MODE-E": {
        "name": "Context Pack + Canonical Memory + Session Delta",
        "description": "For complex multi-step reasoning or unresolved recent decisions.",
        "sources": ["context_pack", "canonical_memory", "session_delta"],
        "roi": 67.8,
        "token_multiplier": 2.1,
    },
}

# Workers and their default modes
WORKER_DEFAULT_MODES = {
    "Brahma":    "MODE-D",   # CTO — architecture always needs canonical memory
    "Ganesha":   "MODE-D",   # CEO — strategy
    "Lakshmi":   "MODE-D",   # CLO — governance/risk
    "Hanuman":   "MODE-B",   # COO — build/execute
    "Saraswati": "MODE-B",   # CLO (Learn) — default B, escalates to E
    "Krishna":   "MODE-B",   # CPO — product
}

# Capabilities that force MODE-D
MODE_D_CAPABILITIES = {
    "architecture", "governance", "constitutional", "adr", "doctrine",
    "strategy", "risk", "review", "audit", "design",
}

# Capabilities that force MODE-B
MODE_B_CAPABILITIES = {
    "build", "execute", "deploy", "test", "implement", "code", "fix",
}


# ─── Router ──────────────────────────────────────────────────────────────────

class CCRRouter:
    """Context Router — selects MODE-B, MODE-D, or MODE-E."""

    def route(self, req: RoutingRequest) -> RoutingDecision:
        mode, reason = self._select_mode(req)
        sources = MODES[mode]["sources"]
        effective_budget = int(req.token_budget * MODES[mode]["token_multiplier"])
        governance_required = (
            req.governance_risk > 35
            or req.constitutional_scope
            or mode in ("MODE-D", "MODE-E")
        )

        return RoutingDecision(
            selected_mode=mode,
            reason=reason,
            context_sources=sources,
            token_budget=effective_budget,
            governance_required=governance_required,
            worker=req.worker,
            capability=req.capability,
            mission_id=req.mission_id,
        )

    def _select_mode(self, req: RoutingRequest) -> tuple[str, str]:
        # MODE-E: complex + recent delta required
        if req.recent_delta_required and req.task_type in ("complex", "strategic"):
            return "MODE-E", (
                f"MODE-E selected: recent_delta_required=True + task_type={req.task_type}. "
                f"Unresolved session state must be included."
            )

        # MODE-E: high governance risk + delta required
        if req.recent_delta_required and req.governance_risk > 55:
            return "MODE-E", (
                f"MODE-E selected: governance_risk={req.governance_risk} > 55 + "
                f"recent_delta_required=True."
            )

        # MODE-D: constitutional scope
        if req.constitutional_scope:
            return "MODE-D", (
                f"MODE-D selected: constitutional_scope=True. "
                f"Canonical memory required for doctrine consistency."
            )

        # MODE-D: strategic/architectural task type
        if req.task_type in ("strategic", "constitutional", "governance"):
            return "MODE-D", (
                f"MODE-D selected: task_type={req.task_type}. "
                f"Canonical memory required."
            )

        # MODE-D: capability in architecture/governance set
        if req.capability.lower() in MODE_D_CAPABILITIES:
            return "MODE-D", (
                f"MODE-D selected: capability={req.capability} requires canonical memory."
            )

        # MODE-D: worker default is D and no explicit B override
        worker_default = WORKER_DEFAULT_MODES.get(req.worker, "MODE-B")
        if worker_default == "MODE-D" and req.capability.lower() not in MODE_B_CAPABILITIES:
            return "MODE-D", (
                f"MODE-D selected: worker={req.worker} default mode is D. "
                f"Capability {req.capability} does not override to B."
            )

        # MODE-B: default
        return "MODE-B", (
            f"MODE-B selected: standard execution. "
            f"worker={req.worker}, capability={req.capability}. "
            f"Context Pack only — no raw session history."
        )


# ─── CLI / Module Interface ───────────────────────────────────────────────────

def route(
    mission_id: str,
    worker: str,
    capability: str,
    task_type: str = "standard",
    governance_risk: int = 0,
    token_budget: int = 8000,
    recent_delta_required: bool = False,
    constitutional_scope: bool = False,
) -> RoutingDecision:
    """Public interface for CCR Router."""
    req = RoutingRequest(
        mission_id=mission_id,
        worker=worker,
        capability=capability,
        task_type=task_type,
        governance_risk=governance_risk,
        token_budget=token_budget,
        recent_delta_required=recent_delta_required,
        constitutional_scope=constitutional_scope,
    )
    return CCRRouter().route(req)


if __name__ == "__main__":
    # Quick self-test
    tests = [
        dict(mission_id="MISSION-016-A", worker="Brahma", capability="architecture"),
        dict(mission_id="MISSION-016-B", worker="Hanuman", capability="build"),
        dict(mission_id="MISSION-016-C", worker="Saraswati", capability="learning",
             recent_delta_required=True, task_type="complex"),
    ]
    for t in tests:
        d = route(**t)
        print(f"[{d.worker}/{d.capability}] → {d.selected_mode} | {d.reason[:60]}...")
