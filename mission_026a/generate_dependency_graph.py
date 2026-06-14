#!/usr/bin/env python3
"""Generate runtime_dependency_graph.json and Runtime_Dependency_Map.canvas for MISSION-026A."""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
M026A = ROOT / "mission_026a"
CANVAS_DIR = ROOT / "08_Visual_Maps"

# Runtime dependency graph — nodes and typed edges
NODES = [
    # Layer 1 — Foundation
    {"id": "constitution", "label": "Y-OS Constitution", "layer": 1, "type": "doctrine"},
    {"id": "adr_registry", "label": "ADR Registry (51)", "layer": 1, "type": "governance"},
    {"id": "git", "label": "Git / y-os-doctrine", "layer": 1, "type": "infrastructure"},

    # Layer 2 — Knowledge
    {"id": "kgc_v4", "label": "KGC v4 Connectivity", "layer": 2, "type": "compiler"},
    {"id": "semantic_graph", "label": "Semantic Graph v4", "layer": 2, "type": "data"},
    {"id": "concept_nodes", "label": "Concept Nodes (39)", "layer": 2, "type": "knowledge"},
    {"id": "mocs", "label": "MOCs (11)", "layer": 2, "type": "navigation"},
    {"id": "dashboards", "label": "Dashboards (14)", "layer": 2, "type": "visualization"},
    {"id": "canvas_maps", "label": "Canvas Maps (25)", "layer": 2, "type": "visualization"},

    # Layer 3 — Execution
    {"id": "ccr_runtime", "label": "CCR Runtime v2", "layer": 3, "type": "router"},
    {"id": "context_compiler", "label": "Context Compiler v2", "layer": 3, "type": "compiler"},
    {"id": "context_cache", "label": "Context Cache", "layer": 3, "type": "cache"},
    {"id": "lakshmi_review", "label": "Lakshmi Context Review", "layer": 3, "type": "governance"},
    {"id": "provider_router", "label": "Provider Router v2", "layer": 3, "type": "router"},
    {"id": "provider_registry", "label": "Provider Registry", "layer": 3, "type": "registry"},
    {"id": "provider_health", "label": "Provider Health Monitor", "layer": 3, "type": "monitor"},
    {"id": "provider_failover", "label": "Provider Failover", "layer": 3, "type": "resilience"},
    {"id": "live_executor", "label": "Live Worker Executor", "layer": 3, "type": "executor"},
    {"id": "pipeline_orchestrator", "label": "Pipeline Orchestrator", "layer": 3, "type": "orchestrator"},
    {"id": "artifact_chaining", "label": "Artifact Chaining Engine", "layer": 3, "type": "engine"},
    {"id": "checkpoint_rollback", "label": "Checkpoint Rollback", "layer": 3, "type": "recovery"},
    {"id": "artifact_registry", "label": "Artifact Registry v2", "layer": 3, "type": "registry"},
    {"id": "output_validator", "label": "Output Validator", "layer": 3, "type": "validator"},
    {"id": "event_bus", "label": "Event Bus Core", "layer": 3, "type": "bus"},
    {"id": "event_router", "label": "Event Router (24 rules)", "layer": 3, "type": "router"},
    {"id": "event_persistence", "label": "Event Persistence", "layer": 3, "type": "store"},
    {"id": "event_replay", "label": "Event Replay Engine", "layer": 3, "type": "engine"},

    # Layer 4 — Memory
    {"id": "time_machine", "label": "ODT Time Machine", "layer": 4, "type": "engine"},
    {"id": "snapshot_engine", "label": "Snapshot Engine", "layer": 4, "type": "engine"},
    {"id": "temporal_reconstruction", "label": "Temporal Reconstruction", "layer": 4, "type": "engine"},
    {"id": "living_memory", "label": "Living Memory Pipeline", "layer": 4, "type": "pipeline"},
    {"id": "session_delta", "label": "Session Delta Engine", "layer": 4, "type": "engine"},

    # Layer 5 — Observability
    {"id": "odt_registry", "label": "ODT Registry", "layer": 5, "type": "registry"},
    {"id": "odt_live_update", "label": "ODT Live Update Engine", "layer": 5, "type": "engine"},
    {"id": "health_monitor", "label": "System Health Monitor", "layer": 5, "type": "monitor"},
    {"id": "alert_engine", "label": "Alert Engine", "layer": 5, "type": "engine"},
    {"id": "eis", "label": "Executive Intelligence Score", "layer": 5, "type": "scorer"},
    {"id": "governance_obs", "label": "Governance Observability", "layer": 5, "type": "monitor"},

    # Layer 6 — Intelligence
    {"id": "strategic_engine", "label": "Strategic Recommendation Engine", "layer": 6, "type": "engine"},
    {"id": "gap_analysis", "label": "Gap Analysis", "layer": 6, "type": "analyzer"},
    {"id": "evidence_reasoning", "label": "Evidence-Based Reasoning", "layer": 6, "type": "engine"},
    {"id": "mission_proposal", "label": "Mission Proposal Generator", "layer": 6, "type": "generator"},
    {"id": "roadmap_engine", "label": "Roadmap Generation Engine", "layer": 6, "type": "generator"},

    # Layer 7 — Simulation
    {"id": "sim_engine", "label": "Executive Simulation Engine", "layer": 7, "type": "engine"},
    {"id": "scenario_modeling", "label": "Scenario Modeling Engine", "layer": 7, "type": "engine"},
    {"id": "impact_propagation", "label": "Impact Propagation Engine", "layer": 7, "type": "engine"},
    {"id": "counterfactual", "label": "Counterfactual Engine", "layer": 7, "type": "engine"},
    {"id": "decision_comparison", "label": "Decision Comparison Engine", "layer": 7, "type": "engine"},
]

EDGES = [
    # Foundation → Knowledge
    {"from": "constitution", "to": "adr_registry", "type": "governed_by"},
    {"from": "adr_registry", "to": "kgc_v4", "type": "enables"},
    {"from": "kgc_v4", "to": "semantic_graph", "type": "compiles"},
    {"from": "semantic_graph", "to": "concept_nodes", "type": "contains"},
    {"from": "semantic_graph", "to": "mocs", "type": "enables"},
    {"from": "semantic_graph", "to": "dashboards", "type": "enables"},

    # Knowledge → Execution
    {"from": "context_compiler", "to": "ccr_runtime", "type": "feeds"},
    {"from": "ccr_runtime", "to": "provider_router", "type": "routes_to"},
    {"from": "ccr_runtime", "to": "context_cache", "type": "uses"},
    {"from": "ccr_runtime", "to": "lakshmi_review", "type": "governed_by"},
    {"from": "provider_router", "to": "provider_registry", "type": "reads"},
    {"from": "provider_router", "to": "provider_health", "type": "observes"},
    {"from": "provider_router", "to": "provider_failover", "type": "delegates_to"},
    {"from": "live_executor", "to": "ccr_runtime", "type": "uses"},
    {"from": "live_executor", "to": "artifact_registry", "type": "stores"},
    {"from": "live_executor", "to": "output_validator", "type": "validates_via"},
    {"from": "pipeline_orchestrator", "to": "live_executor", "type": "orchestrates"},
    {"from": "pipeline_orchestrator", "to": "artifact_chaining", "type": "uses"},
    {"from": "pipeline_orchestrator", "to": "checkpoint_rollback", "type": "uses"},
    {"from": "event_bus", "to": "event_router", "type": "routes_to"},
    {"from": "event_bus", "to": "event_persistence", "type": "stores"},
    {"from": "event_bus", "to": "event_replay", "type": "enables"},

    # Execution → Memory
    {"from": "artifact_registry", "to": "living_memory", "type": "feeds"},
    {"from": "session_delta", "to": "living_memory", "type": "feeds"},
    {"from": "event_replay", "to": "time_machine", "type": "enables"},
    {"from": "snapshot_engine", "to": "time_machine", "type": "feeds"},
    {"from": "temporal_reconstruction", "to": "time_machine", "type": "feeds"},

    # Memory → Observability
    {"from": "time_machine", "to": "odt_registry", "type": "updates"},
    {"from": "odt_live_update", "to": "odt_registry", "type": "updates"},
    {"from": "health_monitor", "to": "odt_registry", "type": "reads"},
    {"from": "health_monitor", "to": "alert_engine", "type": "triggers"},
    {"from": "odt_registry", "to": "eis", "type": "feeds"},
    {"from": "governance_obs", "to": "eis", "type": "feeds"},

    # Observability → Intelligence
    {"from": "odt_registry", "to": "gap_analysis", "type": "feeds"},
    {"from": "eis", "to": "strategic_engine", "type": "feeds"},
    {"from": "gap_analysis", "to": "strategic_engine", "type": "feeds"},
    {"from": "evidence_reasoning", "to": "strategic_engine", "type": "feeds"},
    {"from": "strategic_engine", "to": "mission_proposal", "type": "generates"},
    {"from": "strategic_engine", "to": "roadmap_engine", "type": "generates"},

    # Intelligence → Simulation
    {"from": "strategic_engine", "to": "sim_engine", "type": "feeds"},
    {"from": "scenario_modeling", "to": "sim_engine", "type": "feeds"},
    {"from": "impact_propagation", "to": "sim_engine", "type": "feeds"},
    {"from": "counterfactual", "to": "sim_engine", "type": "feeds"},
    {"from": "decision_comparison", "to": "sim_engine", "type": "feeds"},
    {"from": "sim_engine", "to": "roadmap_engine", "type": "informs"},

    # Cross-cutting: Governance
    {"from": "constitution", "to": "lakshmi_review", "type": "governed_by"},
    {"from": "constitution", "to": "governance_obs", "type": "governed_by"},
    {"from": "adr_registry", "to": "governance_obs", "type": "governed_by"},
]

# Detect single points of failure (nodes with no failover and high in-degree)
in_degree = {}
for e in EDGES:
    in_degree[e["to"]] = in_degree.get(e["to"], 0) + 1

spof_candidates = [
    n["id"] for n in NODES
    if in_degree.get(n["id"], 0) >= 3
    and n["id"] not in ("provider_failover", "checkpoint_rollback", "event_replay")
]

graph = {
    "version": "v1",
    "generated_by": "MISSION-026A",
    "nodes": NODES,
    "edges": EDGES,
    "stats": {
        "total_nodes": len(NODES),
        "total_edges": len(EDGES),
        "layers": 7,
        "spof_candidates": spof_candidates,
    }
}

(M026A / "runtime_dependency_graph.json").write_text(
    json.dumps(graph, indent=2), encoding="utf-8"
)
print(f"Graph: {len(NODES)} nodes, {len(EDGES)} edges")
print(f"SPOF candidates: {spof_candidates}")

# Canvas
canvas_nodes = []
canvas_edges = []
layer_colors = {
    1: "#e8f5e9", 2: "#e3f2fd", 3: "#fff3e0",
    4: "#fce4ec", 5: "#f3e5f5", 6: "#e8eaf6", 7: "#fff8e1"
}
layer_x = {1: -1200, 2: -800, 3: -200, 4: 400, 5: 900, 6: 1400, 7: 1900}
layer_nodes = {}
for n in NODES:
    layer_nodes.setdefault(n["layer"], []).append(n)

node_positions = {}
for layer, nodes in layer_nodes.items():
    x = layer_x[layer]
    for i, n in enumerate(nodes):
        y = (i - len(nodes) / 2) * 100
        node_positions[n["id"]] = (x, y)
        canvas_nodes.append({
            "id": n["id"],
            "type": "text",
            "x": x, "y": int(y),
            "width": 200, "height": 50,
            "text": f"**{n['label']}**\n_{n['type']}_",
            "color": layer_colors.get(layer, "#ffffff"),
        })

for i, e in enumerate(EDGES):
    if e["from"] in node_positions and e["to"] in node_positions:
        canvas_edges.append({
            "id": f"edge_{i}",
            "fromNode": e["from"], "fromSide": "right",
            "toNode": e["to"], "toSide": "left",
            "label": e["type"],
        })

canvas = {"nodes": canvas_nodes, "edges": canvas_edges}
(CANVAS_DIR / "Runtime_Dependency_Map.canvas").write_text(
    json.dumps(canvas, indent=2), encoding="utf-8"
)
print(f"Canvas: {len(canvas_nodes)} nodes, {len(canvas_edges)} edges")
print("Done.")
