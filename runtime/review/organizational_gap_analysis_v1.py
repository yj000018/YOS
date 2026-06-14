#!/usr/bin/env python3
"""
Module 2: Organizational Gap Analysis v1 — Y-OS MISSION-025
Detects: capability gaps, technical debt, provider risks, governance risks,
graph weaknesses, execution bottlenecks, observability gaps, memory gaps.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class GapFinding:
    gap_id: str
    category: str
    title: str
    description: str
    severity: str   # CRITICAL / HIGH / MEDIUM / LOW
    evidence: list[str]
    remediation: str
    target_mission: str

    def to_dict(self) -> dict:
        return {
            "gap_id": self.gap_id,
            "category": self.category,
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "evidence": self.evidence,
            "remediation": self.remediation,
            "target_mission": self.target_mission,
        }


GAPS: list[GapFinding] = [
    # Capability Gaps
    GapFinding("GAP-001", "CAPABILITY", "No Executive Simulation Layer",
               "Y-OS cannot model causal impact of decisions. What-if analysis is impossible.",
               "CRITICAL", ["ADR-0048 M-026 pending", "EIS=96 plateau"],
               "Implement MISSION-026 Executive Simulation Layer", "MISSION-026"),
    GapFinding("GAP-002", "CAPABILITY", "No Semantic Search over Corpus",
               "4,056 semantic edges exist but are not queryable via natural language.",
               "HIGH", ["kg_semantic_graph_v4.json", "Exa in routing playbook"],
               "Implement vector index + semantic search API", "MISSION-027"),
    GapFinding("GAP-003", "CAPABILITY", "No External Trigger for Event Bus",
               "Event Bus operational but requires manual trigger. No n8n/webhook integration.",
               "HIGH", ["M-022 Event Bus", "44 event types", "n8n in playbook"],
               "Implement n8n webhook → Event Bus bridge", "MISSION-028"),
    # Technical Debt
    GapFinding("GAP-004", "TECHNICAL_DEBT", "Orphan Rate 7.1% (34 files)",
               "34 Markdown files remain unlinked despite KGC v4. Body wikilinks pass incomplete.",
               "HIGH", ["M-021 audit", "ADR-0049 partial pass"],
               "KGC v5 body wikilinks pass targeting orphan files", "MISSION-027"),
    GapFinding("GAP-005", "TECHNICAL_DEBT", "Python __pycache__ committed to Git",
               "Runtime __pycache__ directories are committed to y-os-doctrine. Adds noise.",
               "LOW", ["git log --name-only shows .pyc files"],
               "Add .gitignore for __pycache__ and remove committed .pyc files", "MISSION-025"),
    GapFinding("GAP-006", "TECHNICAL_DEBT", "No Git auto-push hook",
               "Every mission requires manual git commit + push. 82 manual operations.",
               "MEDIUM", ["82 commits", "M-022 Event Bus MISSION_COMPLETED event"],
               "Implement Event Bus → git push hook", "MISSION-026"),
    GapFinding("GAP-007", "TECHNICAL_DEBT", "Mission lineage 9 LOW-confidence edges",
               "9 of 20 lineage edges are LOW confidence (human_review_required=true).",
               "MEDIUM", ["M-022A candidate_lineage_edges.json", "lineage_review_registry"],
               "Human review + confirmation of 9 LOW-confidence edges", "MISSION-025"),
    # Provider Risks
    GapFinding("GAP-008", "PROVIDER_RISK", "Gemini not live-tested",
               "Gemini registered in provider registry but no live API key validated.",
               "HIGH", ["M-023 provider_registry.json", "failover tests used mock"],
               "Add GEMINI_API_KEY to Manus Secrets, run live validation", "MISSION-025"),
    GapFinding("GAP-009", "PROVIDER_RISK", "No cost budget enforcement",
               "Cost tracking exists but no hard budget limits. Runaway cost possible.",
               "HIGH", ["M-023 cost_tracker_v1", "K2 rule", "M-017 cost_report"],
               "Implement budget_enforcer_v1 with configurable limits", "MISSION-026"),
    # Governance Risks
    GapFinding("GAP-010", "GOVERNANCE", "No Constitutional Amendment Protocol",
               "Constitution v1 FROZEN but no formal amendment process defined.",
               "MEDIUM", ["Y-OS_Constitution_v1 FROZEN", "ADR-0034"],
               "Define amendment protocol in new ADR", "MISSION-029"),
    GapFinding("GAP-011", "GOVERNANCE", "Lakshmi review is code-only, not LLM-based",
               "Lakshmi governance is rule-based scoring, not semantic reasoning.",
               "MEDIUM", ["lakshmi_context_review_v1.py", "ADR-0043"],
               "Implement LLM-based Lakshmi review using Anthropic API", "MISSION-027"),
    # Graph Weaknesses
    GapFinding("GAP-012", "GRAPH", "ADR supersession chain not traversable",
               "ADRs that supersede others lack machine-readable supersedes edges.",
               "MEDIUM", ["ADR-0041 supersedes pattern", "kg_semantic_graph_v4.json"],
               "Add supersedes edges in KGC v5", "MISSION-027"),
    GapFinding("GAP-013", "GRAPH", "No concept-to-concept edges",
               "12→39 concept nodes exist but have no inter-concept edges.",
               "MEDIUM", ["M-014 concept nodes", "10_Concepts_MOC.md"],
               "Add concept-to-concept typed edges in KGC v5", "MISSION-027"),
    # Execution Bottlenecks
    GapFinding("GAP-014", "EXECUTION", "Pipeline orchestrator has no retry logic",
               "Failed worker calls have no automatic retry. Failover is provider-level only.",
               "MEDIUM", ["M-018 pipeline_orchestrator", "M-023 failover_engine"],
               "Add retry_policy to pipeline_orchestrator_v2", "MISSION-026"),
    GapFinding("GAP-015", "EXECUTION", "No parallel worker execution",
               "Pipeline executes workers sequentially. Parallel execution would reduce latency.",
               "MEDIUM", ["M-018 pipeline_state_manager", "ADR-0045"],
               "Implement parallel worker lanes in pipeline_orchestrator_v2", "MISSION-028"),
    # Observability Gaps
    GapFinding("GAP-016", "OBSERVABILITY", "No real-time alerting to external channel",
               "Alert engine generates alerts but does not push to Slack/email/webhook.",
               "MEDIUM", ["M-020 organizational_alert_engine_v1", "n8n in playbook"],
               "Implement alert_publisher_v1 with n8n/webhook output", "MISSION-028"),
    GapFinding("GAP-017", "OBSERVABILITY", "Dashboards not accessible outside Obsidian",
               "All dashboards are Dataview-dependent. No static HTML export.",
               "MEDIUM", ["M-015 dashboards", "M-019 dashboards", "M-020 dashboards"],
               "Implement dashboard_exporter_v1 generating static HTML", "MISSION-027"),
    # Memory Gaps
    GapFinding("GAP-018", "MEMORY", "No Notion sync for ODT Registry",
               "ODT Registry is JSON-only. Not accessible cross-session without file read.",
               "HIGH", ["M-019 odt_registry.json", "Notion MCP available"],
               "Implement notion_odt_sync_v1", "MISSION-026"),
    GapFinding("GAP-019", "MEMORY", "No cross-session memory for strategic decisions",
               "Strategic recommendations generated per-session. No persistent memory.",
               "HIGH", ["M-025 strategic_memory_engine", "Mem0 in routing playbook"],
               "Implement Mem0 sync for strategic decisions", "MISSION-026"),
    GapFinding("GAP-020", "MEMORY", "y-os-doctrine not archived to Notion Memory",
               "82 commits represent significant knowledge not yet in Notion Memory.",
               "MEDIUM", ["82 commits on y-os-doctrine", "memory-manager skill"],
               "Run session-synthesizer + memoriser skills on y-os-doctrine", "MISSION-025"),
]


class OrganizationalGapAnalysis:
    def __init__(self):
        self.gaps = GAPS

    def analyze(self) -> dict:
        by_severity = {}
        by_category = {}
        for g in self.gaps:
            by_severity.setdefault(g.severity, []).append(g.gap_id)
            by_category.setdefault(g.category, []).append(g.gap_id)
        return {
            "total_gaps": len(self.gaps),
            "by_severity": {k: len(v) for k, v in by_severity.items()},
            "by_category": {k: len(v) for k, v in by_category.items()},
            "critical_gaps": [g.gap_id for g in self.gaps if g.severity == "CRITICAL"],
            "high_gaps": [g.gap_id for g in self.gaps if g.severity == "HIGH"],
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    def to_registry(self) -> list[dict]:
        return [g.to_dict() for g in self.gaps]
