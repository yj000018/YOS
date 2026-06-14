#!/usr/bin/env python3
"""
Organizational Digital Twin Registry v1 — Y-OS
ADR-0046

Maintains current state of Y-OS as a living organizational twin.
Tracks: Workers, Missions, ADRs, Concepts, Pipelines, Artifacts,
Providers, Executions, Validation Reviews, Governance Reviews, Costs,
Memory Assets, Git Commits.
"""

from __future__ import annotations
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


@dataclass
class ODTWorker:
    id: str
    name: str
    capability: str
    provider: str
    model: str
    executions: int = 0
    artifacts_produced: int = 0
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    avg_latency_ms: float = 0.0
    last_active: str = ""


@dataclass
class ODTMission:
    id: str
    title: str
    status: str
    adr: str
    artifacts_produced: int
    date: str
    tokens: int = 0
    cost_usd: float = 0.0


@dataclass
class ODTADR:
    id: str
    title: str
    status: str
    mission: str
    date: str
    supersedes: str = ""


@dataclass
class ODTConcept:
    id: str
    domain: str
    description: str
    source_file: str


@dataclass
class ODTPipeline:
    id: str
    mission_id: str
    status: str
    steps: int
    artifacts: int
    checkpoints: int
    rollbacks: int
    total_tokens: int
    cost_usd: float
    started_at: str
    completed_at: str


@dataclass
class ODTArtifact:
    id: str
    mission_id: str
    artifact_type: str
    worker: str
    provider: str
    model: str
    status: str
    tokens: int
    validation_verdict: str
    governance_verdict: str
    created_at: str


@dataclass
class ODTProvider:
    id: str
    name: str
    calls: int = 0
    tokens: int = 0
    cost_usd: float = 0.0
    avg_latency_ms: float = 0.0
    success_rate: float = 100.0


@dataclass
class ODTCostSummary:
    total_cost_usd: float
    by_provider: dict
    by_worker: dict
    by_mission: dict
    total_tokens: int
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class OrganizationalDigitalTwinRegistry:
    """Living registry of the Y-OS organizational state."""

    def __init__(self):
        self.workers: dict[str, ODTWorker] = {}
        self.missions: dict[str, ODTMission] = {}
        self.adrs: dict[str, ODTADR] = {}
        self.concepts: dict[str, ODTConcept] = {}
        self.pipelines: dict[str, ODTPipeline] = {}
        self.artifacts: dict[str, ODTArtifact] = {}
        self.providers: dict[str, ODTProvider] = {}
        self.git_commits: list[str] = []
        self.memory_assets: list[str] = []
        self.generated_at = datetime.now(timezone.utc).isoformat()

    def populate_from_corpus(self, corpus_root: Path) -> None:
        """Scan corpus and populate registry."""
        # Workers
        worker_defs = [
            ("Brahma", "architecture", "openai", "gpt-4o"),
            ("Hanuman", "build", "openai", "gpt-4o-mini"),
            ("Saraswati", "learning", "anthropic", "claude-opus-4-20250514"),
            ("Lakshmi", "governance", "openai", "gpt-4o"),
            ("Ganesha", "reporting", "openai", "gpt-4o"),
            ("CEO", "directive", "human", "human"),
        ]
        for name, cap, prov, model in worker_defs:
            w = ODTWorker(id=name.lower(), name=name, capability=cap, provider=prov, model=model)
            self.workers[name] = w

        # Missions (from known history)
        mission_data = [
            ("MISSION-013", "Knowledge Graph Compiler v1", "PASSED", "ADR-0040", 2, "2026-06-14"),
            ("MISSION-013B", "Graph Quality Audit", "PASSED", "ADR-0041", 1, "2026-06-14"),
            ("MISSION-014", "Cognitive Graph Architecture v1", "PASSED", "ADR-0041", 12, "2026-06-14"),
            ("MISSION-015", "KGC v2 Visual Drill-Down", "PASSED", "ADR-0042", 45, "2026-06-14"),
            ("MISSION-016", "CCR Runtime v2", "PASSED", "ADR-0043", 6, "2026-06-14"),
            ("MISSION-017", "Live Worker Execution v1", "PASSED", "ADR-0044", 4, "2026-06-14"),
            ("MISSION-018", "Multi-Worker Pipeline Orchestration v1", "PASSED", "ADR-0045", 6, "2026-06-14"),
            ("MISSION-019", "Organizational Digital Twin Runtime v1", "RUNNING", "ADR-0046", 0, "2026-06-14"),
        ]
        for mid, title, status, adr, arts, date in mission_data:
            self.missions[mid] = ODTMission(
                id=mid, title=title, status=status, adr=adr,
                artifacts_produced=arts, date=date,
            )

        # ADRs
        adr_data = [
            ("ADR-0040", "Knowledge Graph Compiler v1", "ACCEPTED", "MISSION-013"),
            ("ADR-0041", "Cognitive Graph Architecture v1", "ACCEPTED", "MISSION-014"),
            ("ADR-0042", "KGC v2 Visual Drill-Down", "ACCEPTED", "MISSION-015"),
            ("ADR-0043", "CCR Runtime v2 Implementation", "ACCEPTED", "MISSION-016"),
            ("ADR-0044", "Live Worker Execution v1", "ACCEPTED", "MISSION-017"),
            ("ADR-0045", "Multi-Worker Pipeline Orchestration v1", "ACCEPTED", "MISSION-018"),
            ("ADR-0046", "Organizational Digital Twin Runtime v1", "PROPOSED", "MISSION-019"),
        ]
        for aid, title, status, mission in adr_data:
            self.adrs[aid] = ODTADR(id=aid, title=title, status=status, mission=mission, date="2026-06-14")

        # Scan concept files
        concepts_dir = corpus_root / "concepts"
        if concepts_dir.exists():
            for f in concepts_dir.glob("*.md"):
                self.concepts[f.stem] = ODTConcept(
                    id=f.stem, domain="Y-OS",
                    description=f"Concept node: {f.stem.replace('_', ' ')}",
                    source_file=str(f.relative_to(corpus_root)),
                )

        # MISSION-018 pipeline
        self.pipelines["PIPE-5C15BA64"] = ODTPipeline(
            id="PIPE-5C15BA64", mission_id="MISSION-018",
            status="COMPLETED", steps=6, artifacts=6,
            checkpoints=6, rollbacks=1, total_tokens=4836,
            cost_usd=0.074135,
            started_at="2026-06-14T00:00:00Z",
            completed_at="2026-06-14T00:41:12Z",
        )

        # MISSION-017 artifacts
        m017_artifacts = [
            ("ART-M017-BRAHMA-ARCHITECTURE", "Architecture Note", "Brahma", "openai", "gpt-4o-2024-08-06", 1117),
            ("ART-M017-HANUMAN-BUILD", "Implementation Plan", "Hanuman", "openai", "gpt-4o-mini-2024-07-18", 829),
            ("ART-M017-SARASWATI-LEARNING", "Learning Report", "Saraswati", "anthropic", "claude-opus-4-20250514", 1358),
            ("ART-M017-LAKSHMI-GOVERNANCE", "Governance Review", "Lakshmi", "openai", "gpt-4o-2024-08-06", 993),
        ]
        for art_id, art_type, worker, prov, model, tokens in m017_artifacts:
            self.artifacts[art_id] = ODTArtifact(
                id=art_id, mission_id="MISSION-017", artifact_type=art_type,
                worker=worker, provider=prov, model=model, status="VALIDATED",
                tokens=tokens, validation_verdict="VALID", governance_verdict="APPROVE",
                created_at="2026-06-14",
            )

        # MISSION-018 artifacts
        m018_artifacts = [
            ("ART-M018-CEO-DIRECTIVE", "CEO Directive", "CEO", "human", "human", 0),
            ("ART-M018-BRAHMA-ARCHITECTURE", "Architecture Note", "Brahma", "openai", "gpt-4o-2024-08-06", 957),
            ("ART-M018-HANUMAN-BUILD", "Implementation Plan", "Hanuman", "openai", "gpt-4o-mini-2024-07-18", 766),
            ("ART-M018-SARASWATI-LEARNING", "Learning Report", "Saraswati", "anthropic", "claude-opus-4-20250514", 1243),
            ("ART-M018-LAKSHMI-GOVERNANCE", "Governance Review", "Lakshmi", "openai", "gpt-4o-2024-08-06", 816),
            ("ART-M018-GANESHA-CEO-BRIEFING", "CEO Briefing", "Ganesha", "openai", "gpt-4o-2024-08-06", 1054),
        ]
        for art_id, art_type, worker, prov, model, tokens in m018_artifacts:
            self.artifacts[art_id] = ODTArtifact(
                id=art_id, mission_id="MISSION-018", artifact_type=art_type,
                worker=worker, provider=prov, model=model, status="VALIDATED",
                tokens=tokens, validation_verdict="VALID", governance_verdict="APPROVE",
                created_at="2026-06-14",
            )

        # Providers
        self.providers["openai"] = ODTProvider(
            id="openai", name="OpenAI", calls=8, tokens=6412,
            cost_usd=0.12, avg_latency_ms=4700, success_rate=100.0,
        )
        self.providers["anthropic"] = ODTProvider(
            id="anthropic", name="Anthropic", calls=2, tokens=2601,
            cost_usd=0.03, avg_latency_ms=22700, success_rate=100.0,
        )
        self.providers["human"] = ODTProvider(
            id="human", name="Human (CEO)", calls=1, tokens=0,
            cost_usd=0.0, avg_latency_ms=0, success_rate=100.0,
        )

        # Git commits
        self.git_commits = [
            "688f374 — MISSION-018",
            "5e1397f — MISSION-017",
            "8faffab — MISSION-016",
            "3d2c350 — MISSION-015",
            "b8f2c29 — MISSION-014",
            "0b09eeb — MISSION-013B",
            "b39af84 — MISSION-013",
        ]

        # Memory assets
        self.memory_assets = [
            "Y-OS_Constitution_v1.md",
            "Cognitive_Graph_Architecture_v1.md",
            "kg_semantic_graph_v2.json",
            "kg_semantic_graph_v3.json",
            "odt_registry.json",
        ]

        # Update worker stats from artifacts
        for art in self.artifacts.values():
            w = self.workers.get(art.worker)
            if w:
                w.executions += 1
                w.artifacts_produced += 1
                w.total_tokens += art.tokens
                w.last_active = "2026-06-14"

    def cost_summary(self) -> ODTCostSummary:
        by_provider = {p.name: round(p.cost_usd, 6) for p in self.providers.values()}
        by_worker = {}
        by_mission = {}
        total_tokens = 0
        for art in self.artifacts.values():
            by_worker[art.worker] = by_worker.get(art.worker, 0) + art.tokens
            by_mission[art.mission_id] = by_mission.get(art.mission_id, 0) + art.tokens
            total_tokens += art.tokens
        return ODTCostSummary(
            total_cost_usd=round(sum(p.cost_usd for p in self.providers.values()), 6),
            by_provider=by_provider,
            by_worker=by_worker,
            by_mission=by_mission,
            total_tokens=total_tokens,
        )

    def to_dict(self) -> dict:
        return {
            "schema_version": "1.0",
            "generated_at": self.generated_at,
            "mission": "MISSION-019",
            "summary": {
                "workers": len(self.workers),
                "missions": len(self.missions),
                "adrs": len(self.adrs),
                "concepts": len(self.concepts),
                "pipelines": len(self.pipelines),
                "artifacts": len(self.artifacts),
                "providers": len(self.providers),
                "git_commits": len(self.git_commits),
                "memory_assets": len(self.memory_assets),
            },
            "workers": {k: asdict(v) for k, v in self.workers.items()},
            "missions": {k: asdict(v) for k, v in self.missions.items()},
            "adrs": {k: asdict(v) for k, v in self.adrs.items()},
            "concepts": {k: asdict(v) for k, v in self.concepts.items()},
            "pipelines": {k: asdict(v) for k, v in self.pipelines.items()},
            "artifacts": {k: asdict(v) for k, v in self.artifacts.items()},
            "providers": {k: asdict(v) for k, v in self.providers.items()},
            "git_commits": self.git_commits,
            "memory_assets": self.memory_assets,
            "cost_summary": asdict(self.cost_summary()),
        }

    def save(self, json_path: Path, md_path: Path) -> None:
        data = self.to_dict()
        json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

        cost = self.cost_summary()
        s = data["summary"]
        lines = [
            "---",
            "id: yos-odt-registry-v1",
            "title: Y-OS Organizational Digital Twin Registry v1",
            "type: odt_registry",
            "mission_id: MISSION-019",
            f"generated_at: '{self.generated_at}'",
            "tags: ['#odt', '#registry', '#yos', '#mission-019']",
            "---",
            "",
            "# Y-OS Organizational Digital Twin Registry v1",
            "",
            f"**Generated:** {self.generated_at}  ",
            f"**Mission:** MISSION-019  ",
            "",
            "## Summary",
            "",
            "| Entity | Count |",
            "| :--- | :--- |",
            f"| Workers | {s['workers']} |",
            f"| Missions | {s['missions']} |",
            f"| ADRs | {s['adrs']} |",
            f"| Concept Nodes | {s['concepts']} |",
            f"| Pipelines | {s['pipelines']} |",
            f"| Artifacts | {s['artifacts']} |",
            f"| Providers | {s['providers']} |",
            f"| Git Commits | {s['git_commits']} |",
            f"| Memory Assets | {s['memory_assets']} |",
            "",
            "## Workers",
            "",
            "| Worker | Capability | Provider | Executions | Artifacts | Tokens |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
        ]
        for w in self.workers.values():
            lines.append(f"| {w.name} | {w.capability} | {w.provider} | {w.executions} | {w.artifacts_produced} | {w.total_tokens:,} |")
        lines += [
            "",
            "## Missions",
            "",
            "| Mission | Status | ADR | Artifacts |",
            "| :--- | :--- | :--- | :--- |",
        ]
        for m in self.missions.values():
            lines.append(f"| [[{m.id}]] | {m.status} | [[{m.adr}]] | {m.artifacts_produced} |")
        lines += [
            "",
            "## Economics",
            "",
            f"**Total Cost:** ${cost.total_cost_usd:.6f} USD  ",
            f"**Total Tokens:** {cost.total_tokens:,}  ",
            "",
            "| Provider | Cost |",
            "| :--- | :--- |",
        ]
        for prov, c in cost.by_provider.items():
            lines.append(f"| {prov} | ${c:.6f} |")
        lines += [
            "",
            "## Pipelines",
            "",
            "| Pipeline | Mission | Status | Steps | Artifacts | Tokens | Cost |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
        ]
        for p in self.pipelines.values():
            lines.append(f"| {p.id} | [[{p.mission_id}]] | {p.status} | {p.steps} | {p.artifacts} | {p.total_tokens:,} | ${p.cost_usd:.6f} |")
        lines += ["", "---", "*Organizational Digital Twin Registry v1 — Y-OS*"]
        md_path.write_text("\n".join(lines), encoding="utf-8")
