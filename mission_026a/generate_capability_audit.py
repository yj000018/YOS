#!/usr/bin/env python3
"""Generate YOS_CAPABILITY_MAP_v1.md, capability_registry_v1.json,
ARCHITECTURAL_REDUNDANCY_REPORT.md, COMPLEXITY_DEBT_REPORT.md for MISSION-026A."""
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
M026A = ROOT / "mission_026a"

# ── CAPABILITY REGISTRY ───────────────────────────────────────────────────────
CAPABILITIES = [
    # CORE
    {"id": "CAP-001", "name": "Constitutional Governance", "mission": "M-001→M-012", "owner": "Lakshmi", "status": "ACTIVE", "classification": "CORE", "strategic_value": 10, "usage_freq": "every_session", "dependencies": [], "notes": "5 Articles, frozen"},
    {"id": "CAP-002", "name": "ADR Decision Registry", "mission": "M-001→M-026A", "owner": "Brahma", "status": "ACTIVE", "classification": "CORE", "strategic_value": 10, "usage_freq": "every_mission", "dependencies": ["CAP-001"], "notes": "51 ADRs"},
    {"id": "CAP-003", "name": "Knowledge Graph Compilation (KGC v4)", "mission": "M-013→M-021", "owner": "Brahma", "status": "ACTIVE", "classification": "CORE", "strategic_value": 9, "usage_freq": "per_mission", "dependencies": ["CAP-002"], "notes": "496 nodes, 4056 edges, 44 rel types"},
    {"id": "CAP-004", "name": "CCR Context Routing (MODE-B/D/E)", "mission": "M-016", "owner": "Brahma", "status": "ACTIVE", "classification": "CORE", "strategic_value": 9, "usage_freq": "every_execution", "dependencies": ["CAP-003"], "notes": "3 modes, worker-specific"},
    {"id": "CAP-005", "name": "Live Worker Execution", "mission": "M-017", "owner": "Hanuman", "status": "ACTIVE", "classification": "CORE", "strategic_value": 9, "usage_freq": "every_execution", "dependencies": ["CAP-004", "CAP-011"], "notes": "Real LLM API calls"},
    {"id": "CAP-006", "name": "Multi-Worker Pipeline Orchestration", "mission": "M-018", "owner": "Brahma", "status": "ACTIVE", "classification": "CORE", "strategic_value": 9, "usage_freq": "per_pipeline", "dependencies": ["CAP-005"], "notes": "Checkpoint, rollback, chaining"},
    {"id": "CAP-007", "name": "Artifact Registry & Lineage", "mission": "M-017", "owner": "Lakshmi", "status": "ACTIVE", "classification": "CORE", "strategic_value": 9, "usage_freq": "every_execution", "dependencies": ["CAP-005"], "notes": "Immutable, typed, lineage-tracked"},
    {"id": "CAP-008", "name": "Governance Review (Lakshmi)", "mission": "M-016", "owner": "Lakshmi", "status": "ACTIVE", "classification": "CORE", "strategic_value": 10, "usage_freq": "every_execution", "dependencies": ["CAP-001"], "notes": "Pre/post execution, score/100"},
    {"id": "CAP-009", "name": "Git Version Control", "mission": "M-013", "owner": "Brahma", "status": "ACTIVE", "classification": "CORE", "strategic_value": 9, "usage_freq": "every_mission", "dependencies": [], "notes": "SSH, y-os-doctrine branch"},
    {"id": "CAP-010", "name": "Obsidian Knowledge Navigation", "mission": "M-013→M-015", "owner": "Saraswati", "status": "ACTIVE", "classification": "CORE", "strategic_value": 8, "usage_freq": "daily", "dependencies": ["CAP-003"], "notes": "531 files, 25 canvas, 14 dashboards"},

    # IMPORTANT
    {"id": "CAP-011", "name": "Provider Diversification & Routing", "mission": "M-023", "owner": "Brahma", "status": "ACTIVE", "classification": "IMPORTANT", "strategic_value": 8, "usage_freq": "every_execution", "dependencies": ["CAP-005"], "notes": "3 providers, 9 models, failover"},
    {"id": "CAP-012", "name": "Event Bus (44 types, 24 rules)", "mission": "M-022", "owner": "Brahma", "status": "ACTIVE", "classification": "IMPORTANT", "strategic_value": 7, "usage_freq": "per_event", "dependencies": ["CAP-006"], "notes": "DLQ, replay, lineage"},
    {"id": "CAP-013", "name": "Organizational Digital Twin", "mission": "M-019", "owner": "Ganesha", "status": "ACTIVE", "classification": "IMPORTANT", "strategic_value": 8, "usage_freq": "per_mission", "dependencies": ["CAP-003", "CAP-007"], "notes": "6 workers, 8 missions, 10 artifacts"},
    {"id": "CAP-014", "name": "System Observability & EIS", "mission": "M-020", "owner": "Lakshmi", "status": "ACTIVE", "classification": "IMPORTANT", "strategic_value": 8, "usage_freq": "continuous", "dependencies": ["CAP-013"], "notes": "EIS 97/100, alerts, weekly review"},
    {"id": "CAP-015", "name": "ODT Time Machine", "mission": "M-024", "owner": "Brahma", "status": "ACTIVE", "classification": "IMPORTANT", "strategic_value": 7, "usage_freq": "on_demand", "dependencies": ["CAP-013", "CAP-012"], "notes": "29 snapshots, 12 phases"},
    {"id": "CAP-016", "name": "Strategic Recommendation Engine", "mission": "M-025", "owner": "Ganesha", "status": "ACTIVE", "classification": "IMPORTANT", "strategic_value": 8, "usage_freq": "per_review", "dependencies": ["CAP-014", "CAP-015"], "notes": "12 recs, 20 gaps, 0 hallucinations"},
    {"id": "CAP-017", "name": "Executive Simulation Layer", "mission": "M-026", "owner": "Ganesha", "status": "ACTIVE", "classification": "IMPORTANT", "strategic_value": 8, "usage_freq": "per_decision", "dependencies": ["CAP-016"], "notes": "7 scenarios, 4 CFs, 3 DCs"},
    {"id": "CAP-018", "name": "Living Memory Pipeline", "mission": "M-016", "owner": "Saraswati", "status": "ACTIVE", "classification": "IMPORTANT", "strategic_value": 7, "usage_freq": "per_session", "dependencies": ["CAP-007"], "notes": "8 stages, session delta"},
    {"id": "CAP-019", "name": "Semantic Connectivity Layer (KGC v4)", "mission": "M-021", "owner": "Brahma", "status": "ACTIVE", "classification": "IMPORTANT", "strategic_value": 7, "usage_freq": "per_mission", "dependencies": ["CAP-003"], "notes": "Orphan rate 7.1%, Digital Thread 92.9%"},
    {"id": "CAP-020", "name": "Legacy Lineage Recovery", "mission": "M-022A", "owner": "Brahma", "status": "ACTIVE", "classification": "IMPORTANT", "strategic_value": 6, "usage_freq": "on_demand", "dependencies": ["CAP-003"], "notes": "100% coverage, 20 edges"},

    # OPTIONAL
    {"id": "CAP-021", "name": "Dataview Dashboards (14)", "mission": "M-015→M-026", "owner": "Saraswati", "status": "ACTIVE", "classification": "OPTIONAL", "strategic_value": 6, "usage_freq": "on_demand", "dependencies": ["CAP-010"], "notes": "Obsidian plugin required"},
    {"id": "CAP-022", "name": "Canvas Visual Maps (25)", "mission": "M-015→M-026", "owner": "Saraswati", "status": "ACTIVE", "classification": "OPTIONAL", "strategic_value": 5, "usage_freq": "on_demand", "dependencies": ["CAP-010"], "notes": "Obsidian native"},
    {"id": "CAP-023", "name": "Concept Nodes (39)", "mission": "M-014→M-015", "owner": "Saraswati", "status": "ACTIVE", "classification": "OPTIONAL", "strategic_value": 6, "usage_freq": "on_demand", "dependencies": ["CAP-003"], "notes": "12 original + 27 expanded"},
    {"id": "CAP-024", "name": "Provider Cost Optimizer", "mission": "M-023", "owner": "Lakshmi", "status": "ACTIVE", "classification": "OPTIONAL", "strategic_value": 6, "usage_freq": "per_execution", "dependencies": ["CAP-011"], "notes": "Budget enforcement pending"},
    {"id": "CAP-025", "name": "Weekly Review Generator", "mission": "M-020", "owner": "Ganesha", "status": "ACTIVE", "classification": "OPTIONAL", "strategic_value": 5, "usage_freq": "weekly", "dependencies": ["CAP-014"], "notes": "Artifact-based"},

    # EXPERIMENTAL
    {"id": "CAP-026", "name": "Excalidraw Visual Maps", "mission": "M-015 (deferred)", "owner": "Saraswati", "status": "DEFERRED", "classification": "EXPERIMENTAL", "strategic_value": 4, "usage_freq": "never", "dependencies": ["CAP-022"], "notes": "Deferred to M-016 (never executed)"},
    {"id": "CAP-027", "name": "Notion ODT Sync", "mission": "M-025 (proposed)", "owner": "Brahma", "status": "PROPOSED", "classification": "EXPERIMENTAL", "strategic_value": 7, "usage_freq": "never", "dependencies": ["CAP-013"], "notes": "REC-004 from M-025"},
    {"id": "CAP-028", "name": "Live Gemini API Validation", "mission": "M-031 (proposed)", "owner": "Brahma", "status": "PROPOSED", "classification": "EXPERIMENTAL", "strategic_value": 7, "usage_freq": "never", "dependencies": ["CAP-011"], "notes": "REC-003 from M-025"},
]

# Save JSON registry
registry = {
    "version": "v1",
    "generated_by": "MISSION-026A",
    "total": len(CAPABILITIES),
    "by_classification": {
        "CORE": sum(1 for c in CAPABILITIES if c["classification"] == "CORE"),
        "IMPORTANT": sum(1 for c in CAPABILITIES if c["classification"] == "IMPORTANT"),
        "OPTIONAL": sum(1 for c in CAPABILITIES if c["classification"] == "OPTIONAL"),
        "EXPERIMENTAL": sum(1 for c in CAPABILITIES if c["classification"] == "EXPERIMENTAL"),
    },
    "capabilities": CAPABILITIES,
    "generated_at": datetime.now(timezone.utc).isoformat(),
}
(M026A / "capability_registry_v1.json").write_text(json.dumps(registry, indent=2), encoding="utf-8")
print(f"Capability registry: {len(CAPABILITIES)} capabilities")

# ── CAPABILITY MAP MD ─────────────────────────────────────────────────────────
cap_md = """---
id: YOS_CAPABILITY_MAP_v1
title: 'Y-OS Capability Map v1'
type: capability_map
status: ACTIVE
date: '2026-06-14'
mission: MISSION-026A
tags:
  - '#capability'
  - '#architecture'
  - '#yos'
---

# Y-OS Capability Map v1

**Generated:** 2026-06-14 | **Mission:** MISSION-026A | **Total:** 28 capabilities

---

## Classification Summary

| Classification | Count | Description |
| :--- | :--- | :--- |
| **CORE** | 10 | Non-negotiable — system fails without these |
| **IMPORTANT** | 10 | High value — significant degradation if absent |
| **OPTIONAL** | 5 | Useful — graceful degradation if absent |
| **EXPERIMENTAL** | 3 | Proposed or deferred — not yet operational |

---

## CORE Capabilities

| ID | Capability | Mission | Owner | Usage | Value |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""
for c in CAPABILITIES:
    if c["classification"] == "CORE":
        cap_md += f"| {c['id']} | {c['name']} | {c['mission']} | {c['owner']} | {c['usage_freq']} | {c['strategic_value']}/10 |\n"

cap_md += "\n## IMPORTANT Capabilities\n\n| ID | Capability | Mission | Owner | Usage | Value |\n| :--- | :--- | :--- | :--- | :--- | :--- |\n"
for c in CAPABILITIES:
    if c["classification"] == "IMPORTANT":
        cap_md += f"| {c['id']} | {c['name']} | {c['mission']} | {c['owner']} | {c['usage_freq']} | {c['strategic_value']}/10 |\n"

cap_md += "\n## OPTIONAL Capabilities\n\n| ID | Capability | Mission | Owner | Usage | Value |\n| :--- | :--- | :--- | :--- | :--- | :--- |\n"
for c in CAPABILITIES:
    if c["classification"] == "OPTIONAL":
        cap_md += f"| {c['id']} | {c['name']} | {c['mission']} | {c['owner']} | {c['usage_freq']} | {c['strategic_value']}/10 |\n"

cap_md += "\n## EXPERIMENTAL Capabilities\n\n| ID | Capability | Mission | Owner | Usage | Value |\n| :--- | :--- | :--- | :--- | :--- | :--- |\n"
for c in CAPABILITIES:
    if c["classification"] == "EXPERIMENTAL":
        cap_md += f"| {c['id']} | {c['name']} | {c['mission']} | {c['owner']} | {c['usage_freq']} | {c['strategic_value']}/10 |\n"

cap_md += "\n---\n\n## Semantic Links\n\n- **governed_by:** [[Y-OS_Constitution_v1]]\n- **produced_by:** [[MISSION-026A_Architecture_Freeze]]\n- **references:** [[YOS_SYSTEM_ARCHITECTURE_v1]]\n"
(ROOT / "YOS_CAPABILITY_MAP_v1.md").write_text(cap_md, encoding="utf-8")
print("Capability map written.")

# ── REDUNDANCY REPORT ─────────────────────────────────────────────────────────
REDUNDANCIES = [
    {"id": "RED-001", "type": "DUPLICATED_COMPILER", "components": ["kg_compiler_v1.py (M-013)", "kg_compiler_v2.py (M-015)", "kg_compiler_v3.py (M-019)", "kgc_v4_connectivity_engine.py (M-021)"], "verdict": "KEEP v4 only", "action": "DEPRECATE v1/v2/v3 (keep as history)", "risk": "LOW", "effort": "LOW"},
    {"id": "RED-002", "type": "DUPLICATED_DASHBOARD_GENERATOR", "components": ["executive_advisor_dashboard_v1.py", "executive_simulation_dashboard_v1.py", "historical_navigation_dashboard_v1.py", "lineage_dashboard_generator_v1.py", "provider_observability_dashboard_v1.py"], "verdict": "MERGE into single DashboardFactory", "action": "MERGE", "risk": "MEDIUM", "effort": "MEDIUM"},
    {"id": "RED-003", "type": "DUPLICATED_LINEAGE_STRUCTURE", "components": ["mission_lineage_registry.json", "candidate_lineage_edges.json", "lineage_review_registry_v1.py", "event_lineage_tracker_v1.py"], "verdict": "Consolidate into single LineageRegistry", "action": "MERGE", "risk": "LOW", "effort": "MEDIUM"},
    {"id": "RED-004", "type": "DUPLICATED_GOVERNANCE_PATH", "components": ["lakshmi_context_review_v1.py", "simulation_governance_v1.py", "lineage_validation_engine_v1.py", "output_validator_v1.py"], "verdict": "Unify under GovernanceEngine v1", "action": "MERGE", "risk": "MEDIUM", "effort": "HIGH"},
    {"id": "RED-005", "type": "DUPLICATED_REGISTRY", "components": ["odt_registry.json", "provider_registry.json", "simulation_registry.json", "event_registry.json", "capability_registry_v1.json"], "verdict": "Keep all — different domains", "action": "KEEP", "risk": "NONE", "effort": "NONE"},
    {"id": "RED-006", "type": "DUPLICATED_CANVAS_GENERATOR", "components": ["generate_canvas_019.py", "generate_visuals_021.py", "lineage_canvas_generator_v1.py", "executive_simulation_dashboard_v1.py (canvas)"], "verdict": "MERGE into CanvasFactory", "action": "MERGE", "risk": "LOW", "effort": "LOW"},
    {"id": "RED-007", "type": "OVERLAPPING_HEALTH_MONITOR", "components": ["system_health_monitor_v1.py", "provider_health_monitor_v1.py", "organizational_observability_engine_v1.py"], "verdict": "Keep all — different scopes (system/provider/org)", "action": "KEEP", "risk": "NONE", "effort": "NONE"},
    {"id": "RED-008", "type": "UNUSED_MODULES", "components": ["art_runtime_v1.py", "crt_runtime_v1.py", "yorc_runtime_v1.py (pre-M013 legacy)"], "verdict": "DEPRECATE — superseded by CCR Runtime v2", "action": "DEPRECATE", "risk": "LOW", "effort": "LOW"},
]

red_md = """---
id: ARCHITECTURAL_REDUNDANCY_REPORT
title: 'Architectural Redundancy Report — MISSION-026A'
type: audit
date: '2026-06-14'
mission: MISSION-026A
---

# Architectural Redundancy Report

**Generated:** 2026-06-14 | **Mission:** MISSION-026A

---

## Summary

| Verdict | Count |
| :--- | :--- |
| KEEP | 2 |
| MERGE | 4 |
| DEPRECATE | 2 |

---

## Redundancies Identified

"""
for r in REDUNDANCIES:
    red_md += f"### {r['id']} — {r['type']}\n\n"
    red_md += f"**Verdict:** {r['verdict']}  \n"
    red_md += f"**Action:** `{r['action']}` | **Risk:** {r['risk']} | **Effort:** {r['effort']}\n\n"
    red_md += "**Components:**\n"
    for c in r["components"]:
        red_md += f"- {c}\n"
    red_md += "\n"

red_md += "---\n\n## Semantic Links\n\n- **produced_by:** [[MISSION-026A_Architecture_Freeze]]\n"
(M026A / "ARCHITECTURAL_REDUNDANCY_REPORT.md").write_text(red_md, encoding="utf-8")
print("Redundancy report written.")

# ── COMPLEXITY DEBT REPORT ────────────────────────────────────────────────────
HOTSPOTS = [
    {"rank": 1, "id": "HOT-001", "component": "runtime/ directory (70 modules)", "score": 95, "issue": "70 flat Python files — no sub-packages, no __init__.py, no module registry", "action": "Reorganize into sub-packages: core/, knowledge/, execution/, memory/, observability/, intelligence/, simulation/"},
    {"rank": 2, "id": "HOT-002", "component": "Governance layer (4 overlapping validators)", "score": 88, "issue": "lakshmi_context_review, simulation_governance, lineage_validation, output_validator — 4 separate governance paths", "action": "Unify into GovernanceEngine v1 with pluggable validators"},
    {"rank": 3, "id": "HOT-003", "component": "Dashboard generators (5 separate modules)", "score": 82, "issue": "Each mission created its own dashboard generator — no shared template", "action": "DashboardFactory v1 with Jinja2 templates"},
    {"rank": 4, "id": "HOT-004", "component": "Canvas generators (4 separate scripts)", "score": 78, "issue": "4 different canvas generation approaches — no shared canvas library", "action": "CanvasFactory v1 with node/edge primitives"},
    {"rank": 5, "id": "HOT-005", "component": "KGC versions (v1/v2/v3/v4 all present)", "score": 75, "issue": "4 compiler versions coexist — v1/v2/v3 are dead code", "action": "Archive v1/v2/v3 to mission_*/legacy/, keep only v4"},
    {"rank": 6, "id": "HOT-006", "component": "JSON registries (131 files)", "score": 70, "issue": "131 JSON files with no schema validation, no versioning, no index", "action": "Registry schema v1 + central registry_index.json"},
    {"rank": 7, "id": "HOT-007", "component": "run_mission_*.py scripts (14 files)", "score": 65, "issue": "14 mission runner scripts with duplicated test harness code", "action": "MissionRunner base class with shared test infrastructure"},
    {"rank": 8, "id": "HOT-008", "component": "Lineage tracking (4 overlapping systems)", "score": 60, "issue": "mission_lineage_registry, event_lineage_tracker, lineage_review_registry, execution_trace_logger — 4 lineage systems", "action": "Consolidate into LineageEngine v1"},
    {"rank": 9, "id": "HOT-009", "component": "Provider payload builder (3 providers, 1 monolithic file)", "score": 55, "issue": "provider_payload_builder_v1.py handles OpenAI/Anthropic/Gemini in one file — no provider plugin pattern", "action": "Provider plugin pattern: ProviderAdapter base class"},
    {"rank": 10, "id": "HOT-010", "component": "ADR-0017 duplicate (2 files with same ID)", "score": 50, "issue": "ADR-0017_Artifact_Registry.md AND ADR-0017_Lakshmi_MVP_Runtime.md — same ID, different content", "action": "Rename one to ADR-0017b or reassign ID"},
]

cplx_md = """---
id: COMPLEXITY_DEBT_REPORT
title: 'Complexity Debt Report — MISSION-026A'
type: audit
date: '2026-06-14'
mission: MISSION-026A
---

# Complexity Debt Report

**Generated:** 2026-06-14 | **Mission:** MISSION-026A

---

## Complexity Metrics

| Dimension | Count | Complexity Score |
| :--- | :--- | :--- |
| Runtime modules | 70 | HIGH |
| JSON registries | 131 | HIGH |
| Canvas maps | 25 | MEDIUM |
| Dashboards | 14 | MEDIUM |
| Relationship types | 44 | MEDIUM |
| ADR files | 51 | LOW |
| Mission runners | 14 | MEDIUM |
| Governance paths | 4 | HIGH |

---

## Top 10 Complexity Hotspots

"""
for h in HOTSPOTS:
    cplx_md += f"### #{h['rank']} — {h['id']}: {h['component']}\n\n"
    cplx_md += f"**Score:** {h['score']}/100  \n"
    cplx_md += f"**Issue:** {h['issue']}  \n"
    cplx_md += f"**Action:** {h['action']}\n\n"

cplx_md += "---\n\n## Semantic Links\n\n- **produced_by:** [[MISSION-026A_Architecture_Freeze]]\n"
(M026A / "COMPLEXITY_DEBT_REPORT.md").write_text(cplx_md, encoding="utf-8")
print("Complexity debt report written.")
print("All Phase 3 artifacts generated.")
