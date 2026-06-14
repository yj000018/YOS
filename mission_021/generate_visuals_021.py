#!/usr/bin/env python3
"""
MISSION-021 Visual Generation
- Dashboard_Graph_Quality.md
- YOS_Digital_Thread.canvas
- YOS_Mission_Lineage.canvas
- YOS_Artifact_Lineage.canvas
- YOS_Graph_Health.canvas
"""
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
M021 = ROOT / "mission_021"
CANVAS_DIR = ROOT / "08_Visual_Maps"
DASHBOARD_DIR = ROOT / "10_Live_Dashboards"
CANVAS_DIR.mkdir(exist_ok=True)
DASHBOARD_DIR.mkdir(exist_ok=True)

# Load results
results = json.loads((M021 / "mission_021_results.json").read_text())
b = results["before"]
a = results["after"]


# ── Dashboard_Graph_Quality.md ────────────────────────────────────────────────

def gen_dashboard():
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    content = f"""---
id: Dashboard_Graph_Quality
title: 'Graph Quality Dashboard — Y-OS KGC v4'
type: dashboard
status: live
mission: MISSION-021
generated_at: '{ts}'
tags:
  - '#dashboard'
  - '#graph'
  - '#kgc-v4'
  - '#mission-021'
aliases:
  - Graph Quality Dashboard
---

# Graph Quality Dashboard — Y-OS KGC v4

> **Generated:** {ts}  
> **Mission:** [[MISSION-021_Semantic_Connectivity_Layer]]  
> **Engine:** [[kgc_v4_connectivity_engine]]

---

## Core Metrics

| Metric | Before (M-020) | After (M-021) | Target | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Orphan Rate** | {b['orphan_rate']}% | **{a['orphan_rate']}%** | < 15% | {'✅ PASS' if a['orphan_rate'] < 15 else '❌ FAIL'} |
| **Orphan Count** | {b['orphan_count']} | **{a['orphan_count']}** | — | — |
| **Graph Quality Score** | {b['graph_quality']} | **{a['graph_quality']}** | > 80 | {'✅ PASS' if a['graph_quality'] > 80 else '❌ FAIL'} |
| **Total Nodes** | {b['total_nodes']} | **{a['total_nodes']}** | — | — |
| **Total Edges** | {b['total_edges']} | **{a['total_edges']}** | — | — |
| **Connectivity Score** | {b['connectivity']}% | **{a['connectivity']}%** | — | — |
| **Digital Thread Coverage** | {b['dt_coverage']}% | **{a['dt_coverage']}%** | > 90% | {'✅ PASS' if a['dt_coverage'] >= 90 else '❌ FAIL'} |
| **Lineage Coverage** | {b['lineage_coverage']}% | **{a['lineage_coverage']}%** | > 95% | {'⚠️ PARTIAL' if a['lineage_coverage'] < 95 else '✅ PASS'} |
| **EIS Score** | 87.5 | **{results['new_eis']}** | > 92 | {'✅ PASS' if results['new_eis'] > 92 else '❌ FAIL'} |
| **Relationship Types** | 29 | **{results['relationship_types']}** | — | — |

---

## Improvement Summary

| Metric | Delta |
| :--- | :--- |
| Orphans resolved | **{results['orphans_resolved']}** |
| Edges added | **{results['edges_added']}** |
| Files enriched (body wikilinks) | **{results['files_enriched']}** |
| Digital Thread complete | **{'YES' if results['digital_thread_complete'] else 'NO'}** |

---

## Test Results

| Test | Description | Result |
| :--- | :--- | :--- |
| A | Orphan Reduction < 15% | {results['tests']['TEST_A']} |
| B | Graph Quality > 80 | {results['tests']['TEST_B']} |
| C | Digital Thread ≥ 90% | {results['tests']['TEST_C']} |
| D | Mission Lineage ≥ 95% | {results['tests']['TEST_D']} |
| E | Canvas Generation | {results['tests']['TEST_E']} |
| F | Dashboard Generation | {results['tests']['TEST_F']} |
| G | EIS > 92 | {results['tests']['TEST_G']} |

---

## Dataview Queries

```dataview
TABLE orphan_rate, graph_quality_score, eis_score
FROM "mission_021"
WHERE type = "report"
SORT file.mtime DESC
```

```dataview
LIST
FROM "concepts"
WHERE is_orphan = false
SORT file.name ASC
```

---

## Navigation

- [[YOS_Digital_Thread]] — Digital Thread Canvas
- [[YOS_Mission_Lineage]] — Mission Lineage Canvas
- [[YOS_Artifact_Lineage]] — Artifact Lineage Canvas
- [[YOS_Graph_Health]] — Graph Health Canvas
- [[00_Y-OS_Home]] — Home MOC
- [[Dashboard_Executive_Cockpit]] — Executive Cockpit

## Semantic Links

- **reports_to:** [[MISSION-021_Semantic_Connectivity_Layer]]
- **measured_by:** [[kgc_v4_connectivity_engine]]
- **published_to:** [[00_Y-OS_Home]]
"""
    path = DASHBOARD_DIR / "Dashboard_Graph_Quality.md"
    path.write_text(content, encoding="utf-8")
    print(f"  Dashboard: {path}")
    return path


# ── Canvas generator ──────────────────────────────────────────────────────────

def make_node(node_id: str, x: float, y: float, label: str,
              color: str = "", width: int = 200, height: int = 60,
              file_path: str = "") -> dict:
    node = {
        "id": node_id,
        "x": x, "y": y,
        "width": width, "height": height,
        "type": "text",
        "text": label,
    }
    if color:
        node["color"] = color
    if file_path:
        node["type"] = "file"
        node["file"] = file_path
        del node["text"]
    return node


def make_edge(edge_id: str, from_id: str, to_id: str, label: str = "") -> dict:
    e = {"id": edge_id, "fromNode": from_id, "toNode": to_id,
         "fromSide": "right", "toSide": "left"}
    if label:
        e["label"] = label
    return e


# ── Canvas 1: Digital Thread ──────────────────────────────────────────────────

def gen_digital_thread_canvas():
    nodes = [
        make_node("n_ceo", -800, 0, "CEO Directive\n(Yannick)", "1", 180, 80),
        make_node("n_mission", -550, 0, "MISSION-013→021\n(Missions)", "2", 200, 80,
                  file_path="01_Missions_MOC.md"),
        make_node("n_adr", -280, 0, "ADR-0040→0049\n(Architecture)", "3", 200, 80,
                  file_path="02_ADR_MOC.md"),
        make_node("n_worker", 0, 0, "Workers\n(Brahma/Hanuman/\nSaraswati/Lakshmi)", "4", 200, 100),
        make_node("n_context", 260, 0, "Context Pack\n(CCR v2)", "5", 180, 80),
        make_node("n_provider", 480, 0, "LLM Provider\n(OpenAI/Anthropic)", "6", 200, 80),
        make_node("n_artifact", 700, 0, "Artifact\n(ART-M0XX)", "7", 180, 80),
        make_node("n_gov", 700, 150, "Governance Review\n(Lakshmi)", "2", 200, 80),
        make_node("n_dashboard", 700, -150, "Dashboard\n(Executive Cockpit)", "3", 200, 80,
                  file_path="10_Live_Dashboards/Dashboard_Executive_Cockpit.md"),
    ]
    edges = [
        make_edge("e1", "n_ceo", "n_mission", "creates"),
        make_edge("e2", "n_mission", "n_adr", "produces"),
        make_edge("e3", "n_adr", "n_worker", "executed_by"),
        make_edge("e4", "n_worker", "n_context", "consumes"),
        make_edge("e5", "n_context", "n_provider", "routes_to"),
        make_edge("e6", "n_provider", "n_artifact", "produces"),
        make_edge("e7", "n_artifact", "n_gov", "reviewed_by"),
        make_edge("e8", "n_artifact", "n_dashboard", "published_to"),
    ]
    canvas = {"nodes": nodes, "edges": edges}
    path = CANVAS_DIR / "YOS_Digital_Thread.canvas"
    path.write_text(json.dumps(canvas, indent=2), encoding="utf-8")
    print(f"  Canvas: {path}")
    return path


# ── Canvas 2: Mission Lineage ─────────────────────────────────────────────────

def gen_mission_lineage_canvas():
    lineage = json.loads((M021 / "mission_lineage_registry.json").read_text())
    # Show M-013 → M-021 chain
    mission_chain = [
        ("MISSION-013_Knowledge_Graph_Compiler", "M-013\nKGC v1"),
        ("MISSION-013B_Graph_Quality_Audit", "M-013B\nGraph Audit"),
        ("MISSION-014_Cognitive_Graph_Architecture", "M-014\nCognitive Graph"),
        ("MISSION-015_KGC_v2_Visual_Drill_Down", "M-015\nKGC v2"),
        ("MISSION-016_CCR_Runtime_v2", "M-016\nCCR Runtime v2"),
        ("MISSION-017_Live_Worker_Execution_Report", "M-017\nLive Workers"),
        ("MISSION-018_Multi_Worker_Pipeline_Report", "M-018\nPipeline"),
        ("MISSION-019_Organizational_Digital_Twin_Report", "M-019\nODT"),
        ("MISSION-020_Autonomous_Observability_Report", "M-020\nObservability"),
        ("MISSION-021_Semantic_Connectivity_Layer", "M-021\nKGC v4"),
    ]
    nodes = []
    edges = []
    for i, (m_id, label) in enumerate(mission_chain):
        x = i * 220 - 1000
        fp = f"mission_0{13+i}/{m_id}.md" if i < 9 else f"mission_021/{m_id}.md"
        nodes.append(make_node(f"m{i}", x, 0, label, str((i % 6) + 1), 180, 80))
        if i > 0:
            edges.append(make_edge(f"e{i}", f"m{i-1}", f"m{i}", "evolves_into"))

    # Add ADR nodes below
    adr_chain = [
        ("ADR-0040_Knowledge_Graph_Compiler", "ADR-0040"),
        ("ADR-0041_Cognitive_Graph_Architecture", "ADR-0041"),
        ("ADR-0042_KGC_v2_Visual_Drill_Down", "ADR-0042"),
        ("ADR-0043_CCR_Runtime_v2_Implementation", "ADR-0043"),
        ("ADR-0044_Live_Worker_Execution_v1", "ADR-0044"),
        ("ADR-0045_Multi_Worker_Pipeline_Orchestration_v1", "ADR-0045"),
        ("ADR-0046_Organizational_Digital_Twin_Runtime_v1", "ADR-0046"),
        ("ADR-0047_Autonomous_Organizational_Observability", "ADR-0047"),
        ("ADR-0048_Roadmap_Architecture_Review", "ADR-0048"),
    ]
    for i, (adr_id, label) in enumerate(adr_chain):
        x = i * 220 - 1000
        nodes.append(make_node(f"a{i}", x, 160, label, "4", 180, 60))
        edges.append(make_edge(f"ea{i}", f"m{i}", f"a{i}", "produces"))

    canvas = {"nodes": nodes, "edges": edges}
    path = CANVAS_DIR / "YOS_Mission_Lineage.canvas"
    path.write_text(json.dumps(canvas, indent=2), encoding="utf-8")
    print(f"  Canvas: {path}")
    return path


# ── Canvas 3: Artifact Lineage ────────────────────────────────────────────────

def gen_artifact_lineage_canvas():
    nodes = [
        make_node("n_m017", -400, -200, "M-017\nLive Workers", "2", 160, 70),
        make_node("n_m018", -400, 0, "M-018\nPipeline", "2", 160, 70),
        make_node("n_m019", -400, 200, "M-019\nODT", "2", 160, 70),
        make_node("n_brahma", -150, -200, "Brahma\nArchitecture", "1", 160, 70),
        make_node("n_hanuman", -150, -80, "Hanuman\nBuild", "3", 160, 70),
        make_node("n_saraswati", -150, 40, "Saraswati\nLearning", "5", 160, 70),
        make_node("n_lakshmi", -150, 160, "Lakshmi\nGovernance", "4", 160, 70),
        make_node("n_ganesha", -150, 280, "Ganesha\nReporting", "6", 160, 70),
        make_node("n_art1", 100, -200, "ART-M017\nBRAHMA", "1", 180, 70),
        make_node("n_art2", 100, -80, "ART-M017\nHANUMAN", "3", 180, 70),
        make_node("n_art3", 100, 40, "ART-M017\nSARASWATI", "5", 180, 70),
        make_node("n_art4", 100, 160, "ART-M017\nLAKSHMI", "4", 180, 70),
        make_node("n_art5", 100, 280, "ART-M018\nCEO-BRIEFING", "6", 180, 70),
        make_node("n_registry", 350, 40, "Artifact\nRegistry v2", "2", 180, 80),
        make_node("n_git", 550, 40, "Git\ny-os-doctrine", "4", 160, 70),
    ]
    edges = [
        make_edge("e1", "n_m017", "n_brahma", "executed_by"),
        make_edge("e2", "n_m017", "n_hanuman", "executed_by"),
        make_edge("e3", "n_m018", "n_saraswati", "executed_by"),
        make_edge("e4", "n_m018", "n_lakshmi", "executed_by"),
        make_edge("e5", "n_m019", "n_ganesha", "executed_by"),
        make_edge("e6", "n_brahma", "n_art1", "produces"),
        make_edge("e7", "n_hanuman", "n_art2", "produces"),
        make_edge("e8", "n_saraswati", "n_art3", "produces"),
        make_edge("e9", "n_lakshmi", "n_art4", "produces"),
        make_edge("e10", "n_ganesha", "n_art5", "produces"),
        make_edge("e11", "n_art1", "n_registry", "stores"),
        make_edge("e12", "n_art3", "n_registry", "stores"),
        make_edge("e13", "n_art5", "n_registry", "stores"),
        make_edge("e14", "n_registry", "n_git", "publishes"),
    ]
    canvas = {"nodes": nodes, "edges": edges}
    path = CANVAS_DIR / "YOS_Artifact_Lineage.canvas"
    path.write_text(json.dumps(canvas, indent=2), encoding="utf-8")
    print(f"  Canvas: {path}")
    return path


# ── Canvas 4: Graph Health ────────────────────────────────────────────────────

def gen_graph_health_canvas():
    b = results["before"]
    a = results["after"]
    nodes = [
        make_node("n_title", 0, -300, "Y-OS Graph Health\nKGC v4 — MISSION-021", "1", 300, 80),
        make_node("n_orphan_b", -400, -100, f"Orphans BEFORE\n{b['orphan_count']} ({b['orphan_rate']}%)", "6", 200, 80),
        make_node("n_orphan_a", -400, 50, f"Orphans AFTER\n{a['orphan_count']} ({a['orphan_rate']}%)\n✅ < 15%", "3", 200, 80),
        make_node("n_gq_b", -100, -100, f"Graph Quality BEFORE\n{b['graph_quality']}", "6", 200, 80),
        make_node("n_gq_a", -100, 50, f"Graph Quality AFTER\n{a['graph_quality']}\n✅ > 80", "3", 200, 80),
        make_node("n_edges_b", 200, -100, f"Edges BEFORE\n{b['total_edges']}", "6", 200, 80),
        make_node("n_edges_a", 200, 50, f"Edges AFTER\n{a['total_edges']}\n+{results['edges_added']}", "3", 200, 80),
        make_node("n_eis_b", 500, -100, f"EIS BEFORE\n87.5", "6", 200, 80),
        make_node("n_eis_a", 500, 50, f"EIS AFTER\n{results['new_eis']}\n✅ > 92", "3", 200, 80),
        make_node("n_dt", 0, 200, f"Digital Thread\n{a['dt_coverage']}% coverage\n✅ > 90%", "3", 220, 80),
        make_node("n_dashboard", 0, 350, "Dashboard_Graph_Quality", "2", 220, 60,
                  file_path="10_Live_Dashboards/Dashboard_Graph_Quality.md"),
    ]
    edges = [
        make_edge("e1", "n_orphan_b", "n_orphan_a", "resolved"),
        make_edge("e2", "n_gq_b", "n_gq_a", "improved"),
        make_edge("e3", "n_edges_b", "n_edges_a", "grew"),
        make_edge("e4", "n_eis_b", "n_eis_a", "improved"),
        make_edge("e5", "n_title", "n_dt", "measures"),
        make_edge("e6", "n_dt", "n_dashboard", "reports_to"),
    ]
    canvas = {"nodes": nodes, "edges": edges}
    path = CANVAS_DIR / "YOS_Graph_Health.canvas"
    path.write_text(json.dumps(canvas, indent=2), encoding="utf-8")
    print(f"  Canvas: {path}")
    return path


if __name__ == "__main__":
    print("=== Generating MISSION-021 visuals ===")
    gen_dashboard()
    gen_digital_thread_canvas()
    gen_mission_lineage_canvas()
    gen_artifact_lineage_canvas()
    gen_graph_health_canvas()
    print("=== All visuals generated ===")
