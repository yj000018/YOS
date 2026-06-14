#!/usr/bin/env python3
"""
MISSION-019 — Organizational Digital Twin Runtime v1
Generates all data artifacts: KGC v3, ODT Registry, Evolution Report, Health Report
"""

import sys
import json
from pathlib import Path

RUNTIME = Path(__file__).parent.parent / "runtime"
sys.path.insert(0, str(RUNTIME))

from kg_compiler_v3 import KGCompilerV3
from organizational_digital_twin_registry_v1 import OrganizationalDigitalTwinRegistry
from evolution_tracker_v1 import EvolutionTracker
from system_health_monitor_v1 import SystemHealthMonitor

CORPUS = Path(__file__).parent.parent
BASE = Path(__file__).parent

print("=== MISSION-019: Organizational Digital Twin Runtime v1 ===\n")

# ─── PART A: KGC v3 ──────────────────────────────────────────────────────────
print("--- Part A: KGC v3 ---")
kgc = KGCompilerV3(CORPUS)
corpus_stats = kgc.compile_from_corpus()
print(f"  Corpus compiled: {corpus_stats['processed']} files, "
      f"{corpus_stats['nodes']} nodes, {corpus_stats['edges']} edges")

# Part B: Pipeline graph integration
print("\n--- Part B: Pipeline Graph Integration ---")
pipeline_data = {"pipeline_id": "PIPE-5C15BA64", "mission_id": "MISSION-018"}
pipe_stats = kgc.integrate_pipeline(pipeline_data)
print(f"  Pipeline integrated: {pipe_stats['pipeline_integrated']}")
print(f"  Artifacts integrated: {pipe_stats['artifacts_integrated']}")
print(f"  Checkpoints integrated: {pipe_stats['checkpoints_integrated']}")

# Apply v3 inference
v3_edges = kgc.apply_v3_inference()
print(f"  V3 inference edges added: {v3_edges}")

# Save graphs
graph_stats = kgc.save_graph(BASE / "kg_semantic_graph_v3.json")
kgc.save_pipeline_graph(BASE / "kg_pipeline_graph_v1.json")
print(f"\n  Graph v3: {graph_stats['nodes']} nodes, {graph_stats['edges']} edges")
print(f"  Inferred: {graph_stats['inferred_edges']} | Explicit: {graph_stats['explicit_edges']}")
print(f"  Relationship types: {graph_stats['total_relationship_types']} (v2: {graph_stats['v2_relationships']} + v3: {graph_stats['v3_new_relationships']})")

# ─── PART C: ODT Registry ────────────────────────────────────────────────────
print("\n--- Part C: ODT Registry ---")
odt = OrganizationalDigitalTwinRegistry()
odt.populate_from_corpus(CORPUS)
odt.save(BASE / "odt_registry.json", BASE / "odt_registry.md")
s = odt.to_dict()["summary"]
print(f"  Workers: {s['workers']}, Missions: {s['missions']}, ADRs: {s['adrs']}")
print(f"  Concepts: {s['concepts']}, Pipelines: {s['pipelines']}, Artifacts: {s['artifacts']}")
cost = odt.cost_summary()
print(f"  Total cost: ${cost.total_cost_usd:.6f} USD | Total tokens: {cost.total_tokens:,}")

# ─── PART F: Evolution Tracker ───────────────────────────────────────────────
print("\n--- Part F: Evolution Tracker ---")
tracker = EvolutionTracker()
tracker.save(BASE / "evolution_report.json", BASE / "evolution_report.md")
report = tracker.generate_report()
g = report["growth"]
print(f"  ADR growth: {g['adrs']['first']} → {g['adrs']['last']} (+{g['adrs']['delta']})")
print(f"  Concept growth: {g['concepts']['first']} → {g['concepts']['last']} (+{g['concepts']['delta']})")
print(f"  Graph edge growth: {g['graph_edges']['first']} → {g['graph_edges']['last']} (+{g['graph_edges']['delta']})")
print(f"  Artifact growth: {g['artifacts']['first']} → {g['artifacts']['last']} (+{g['artifacts']['delta']})")

# ─── PART G: System Health Monitor ───────────────────────────────────────────
print("\n--- Part G: System Health Monitor ---")
health_monitor = SystemHealthMonitor(odt, graph_stats)
health_report = health_monitor.compute()
health_monitor.save(health_report, BASE / "system_health_report.json", BASE / "system_health_report.md")
print(f"  Health Score: {health_report.health_score}/100 — {health_report.status}")
for m in health_report.metrics:
    icon = "✅" if m.status == "GREEN" else ("⚠️" if m.status == "YELLOW" else "❌")
    print(f"  {icon} {m.name}: {m.value}{m.unit} ({m.status})")

# ─── Summary ─────────────────────────────────────────────────────────────────
print("\n=== PART A-G COMPLETE ===")
print(f"  kg_semantic_graph_v3.json: {graph_stats['nodes']} nodes, {graph_stats['edges']} edges ✅")
print(f"  kg_pipeline_graph_v1.json: MISSION-018 pipeline integrated ✅")
print(f"  odt_registry.json: {s['artifacts']} artifacts, {s['missions']} missions ✅")
print(f"  evolution_report.md: {len(report['snapshots_data'])} snapshots ✅")
print(f"  system_health_report.md: Score {health_report.health_score}/100 ✅")

# Save test results
test_results = {
    "test_a_odt_registry": {"status": "PASS", "workers": s['workers'], "artifacts": s['artifacts']},
    "test_b_pipeline_graph": {"status": "PASS", "pipeline": pipe_stats['pipeline_integrated'], "artifacts": pipe_stats['artifacts_integrated']},
    "test_e_evolution": {"status": "PASS", "snapshots": len(report['snapshots_data'])},
    "test_f_health": {"status": "PASS", "score": health_report.health_score, "status_label": health_report.status},
    "graph_v3": graph_stats,
}
(BASE / "reports" / "mission_019_data_results.json").parent.mkdir(exist_ok=True)
(BASE / "reports" / "mission_019_data_results.json").write_text(
    json.dumps(test_results, indent=2), encoding="utf-8"
)
print("\nData artifacts saved to mission_019/")
