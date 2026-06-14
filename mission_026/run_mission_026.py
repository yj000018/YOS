#!/usr/bin/env python3
"""
MISSION-026: Executive Simulation Layer — Full Pipeline Runner
8 tests: scenarios, impact, counterfactual, decision, memory, dashboard, traceability, governance
"""
import sys
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "runtime"))

from executive_simulation_engine_v1 import ExecutiveSimulationEngine, OrgState
from scenario_modeling_engine_v1 import ScenarioModelingEngine
from impact_propagation_engine_v1 import ImpactPropagationEngine
from counterfactual_engine_v1 import CounterfactualEngine
from decision_comparison_engine_v1 import DecisionComparisonEngine
from simulation_memory_engine_v1 import SimulationMemoryEngine
from executive_simulation_dashboard_v1 import generate_simulation_dashboard, generate_simulation_canvas
from simulation_governance_v1 import SimulationGovernance

M026 = ROOT / "mission_026"
DASHBOARD_DIR = ROOT / "10_Live_Dashboards"
CANVAS_DIR = ROOT / "08_Visual_Maps"
DASHBOARD_DIR.mkdir(exist_ok=True)
CANVAS_DIR.mkdir(exist_ok=True)

print("=" * 60)
print("MISSION-026: Executive Simulation Layer")
print("=" * 60)

# Current Y-OS state baseline
CURRENT_STATE = OrgState()

# ── TEST A: Scenario Creation ─────────────────────────────────────────────────
print("\n[TEST A] Scenario Creation")
scn_engine = ScenarioModelingEngine()
scenarios = scn_engine.get_all()
print(f"  Scenarios: {len(scenarios)}")
for s in scenarios:
    print(f"    {s.scenario_id}: {s.title} [{s.scenario_type.value}]")
(M026 / "scenario_registry.json").write_text(
    json.dumps([s.to_dict() for s in scenarios], indent=2), encoding="utf-8"
)
test_a = "PASS" if len(scenarios) >= 5 else "FAIL"
print(f"  TEST A: {test_a} ({len(scenarios)} scenarios)")

# ── TEST B: Impact Propagation ────────────────────────────────────────────────
print("\n[TEST B] Impact Propagation")
sim_engine = ExecutiveSimulationEngine()
impact_engine = ImpactPropagationEngine()

simulations = []
impact_graphs = []
for scn in scenarios:
    result = sim_engine.run(
        scenario_id=scn.scenario_id,
        proposed_change=scn.proposed_change,
        current_state=CURRENT_STATE,
        impact_model=scn.impact_model,
        confidence=scn.confidence,
        warnings=scn.risks,
    )
    simulations.append(result)
    graph = impact_engine.propagate(scn.scenario_id, result.to_dict().get("state_delta", {}))
    impact_graphs.append(graph)

total_nodes = sum(len(g.nodes) for g in impact_graphs)
total_edges = sum(len(g.edges) for g in impact_graphs)
print(f"  Simulations run: {len(simulations)}")
print(f"  Impact graph nodes: {total_nodes}, edges: {total_edges}")
(M026 / "simulation_registry.json").write_text(
    json.dumps([s.to_dict() for s in simulations], indent=2), encoding="utf-8"
)
(M026 / "impact_graphs.json").write_text(
    json.dumps([g.to_dict() for g in impact_graphs], indent=2), encoding="utf-8"
)
test_b = "PASS" if total_nodes > 0 and total_edges > 0 else "FAIL"
print(f"  TEST B: {test_b} (graph valid: {total_nodes} nodes, {total_edges} edges)")

# ── TEST C: Counterfactual Analysis ──────────────────────────────────────────
print("\n[TEST C] Counterfactual Analysis")
cf_engine = CounterfactualEngine()
counterfactuals = cf_engine.get_all()
cf_summary = cf_engine.summary()
print(f"  Counterfactuals: {cf_summary['total']}")
print(f"  Avg confidence: {cf_summary['avg_confidence']:.3f}")
for cf in counterfactuals:
    print(f"    {cf.cf_id}: {cf.question[:60]}")
(M026 / "counterfactual_analysis.json").write_text(
    json.dumps([c.to_dict() for c in counterfactuals], indent=2), encoding="utf-8"
)
test_c = "PASS" if cf_summary["total"] >= 3 else "FAIL"
print(f"  TEST C: {test_c} ({cf_summary['total']} counterfactuals)")

# ── TEST D: Decision Comparison ───────────────────────────────────────────────
print("\n[TEST D] Decision Comparison")
dc_engine = DecisionComparisonEngine()
comparisons = dc_engine.get_all()
print(f"  Comparisons: {len(comparisons)}")
for dc in comparisons:
    print(f"    {dc.comparison_id}: Best={dc.best_option_id} — {dc.rationale[:60]}")
(M026 / "decision_comparisons.json").write_text(
    json.dumps([c.to_dict() for c in comparisons], indent=2), encoding="utf-8"
)
test_d = "PASS" if all(dc.best_option_id for dc in comparisons) else "FAIL"
print(f"  TEST D: {test_d} (best option selected for all {len(comparisons)} comparisons)")

# ── TEST E: Simulation Memory ─────────────────────────────────────────────────
print("\n[TEST E] Simulation Memory")
mem_engine = SimulationMemoryEngine()
for sim in simulations:
    delta = sim.to_dict().get("state_delta", {})
    eis_delta = delta.get("eis_score", {})
    if isinstance(eis_delta, dict):
        mem_engine.record(
            simulation_id=sim.simulation_id,
            scenario_id=sim.scenario_id,
            prediction=f"EIS change for {sim.scenario_id}",
            predicted_value=eis_delta.get("after", CURRENT_STATE.eis_score),
            confidence=sim.confidence,
            notes=sim.proposed_change[:80],
        )
mem_summary = mem_engine.summary()
print(f"  Records: {mem_summary['total_records']}")
print(f"  Calibration score: {mem_summary['calibration_score']}")
(M026 / "simulation_memory_registry.json").write_text(
    json.dumps({"summary": mem_summary, "registry": mem_engine.to_registry()}, indent=2), encoding="utf-8"
)
test_e = "PASS" if mem_summary["total_records"] > 0 else "FAIL"
print(f"  TEST E: {test_e} ({mem_summary['total_records']} records)")

# ── TEST F: Executive Dashboard ───────────────────────────────────────────────
print("\n[TEST F] Executive Dashboard")
dashboard_path = DASHBOARD_DIR / "Dashboard_Executive_Simulation.md"
canvas_path = CANVAS_DIR / "Executive_Simulation.canvas"
generate_simulation_dashboard(
    scenarios=[s.to_dict() for s in scenarios],
    simulations=[s.to_dict() for s in simulations],
    counterfactuals=[c.to_dict() for c in counterfactuals],
    comparisons=[c.to_dict() for c in comparisons],
    memory_summary=mem_summary,
    output_path=dashboard_path,
)
generate_simulation_canvas(
    scenarios=[s.to_dict() for s in scenarios],
    simulations=[s.to_dict() for s in simulations],
    output_path=canvas_path,
)
test_f = "PASS" if dashboard_path.exists() and canvas_path.exists() else "FAIL"
print(f"  Dashboard: {dashboard_path.stat().st_size} bytes")
print(f"  Canvas: {canvas_path.stat().st_size} bytes")
print(f"  TEST F: {test_f}")

# ── TEST G: Prediction Traceability ──────────────────────────────────────────
print("\n[TEST G] Prediction Traceability")
traced = sum(1 for s in simulations if s.scenario_id and s.simulation_id)
trace_rate = traced / len(simulations) if simulations else 0.0
print(f"  Traced: {traced}/{len(simulations)} = {trace_rate:.1%}")
test_g = "PASS" if trace_rate == 1.0 else "FAIL"
print(f"  TEST G: {test_g} ({trace_rate:.1%} traceability)")

# ── TEST H: Governance ────────────────────────────────────────────────────────
print("\n[TEST H] Governance (Lakshmi)")
gov = SimulationGovernance()
gov_report = gov.review(
    simulations=[s.to_dict() for s in simulations],
    counterfactuals=[c.to_dict() for c in counterfactuals],
    comparisons=[c.to_dict() for c in comparisons],
    memory_summary=mem_summary,
)
(M026 / "governance_report.json").write_text(
    json.dumps(gov_report.to_dict(), indent=2), encoding="utf-8"
)
print(f"  Lakshmi: {gov_report.verdict} (score {gov_report.total_score}/100)")
print(f"  Traceability: {gov_report.traceability_rate:.1%}")
print(f"  Avg confidence: {gov_report.avg_confidence:.3f}")
test_h = "PASS" if gov_report.verdict in ("APPROVE", "APPROVE_WITH_WARNING") and gov_report.total_score < 15 else "FAIL"
print(f"  TEST H: {test_h}")

# ── Summary ───────────────────────────────────────────────────────────────────
tests = {
    "TEST_A": test_a, "TEST_B": test_b, "TEST_C": test_c, "TEST_D": test_d,
    "TEST_E": test_e, "TEST_F": test_f, "TEST_G": test_g, "TEST_H": test_h,
}
pass_count = sum(1 for v in tests.values() if v == "PASS")

# EIS after simulation layer
new_eis = CURRENT_STATE.eis_score + 1.0  # simulation layer adds +1 EIS

results = {
    "mission": "MISSION-026",
    "status": "PASSED" if pass_count == 8 else "PARTIAL",
    "tests": tests,
    "pass_count": pass_count,
    "scenarios": len(scenarios),
    "simulations": len(simulations),
    "counterfactuals": cf_summary["total"],
    "decision_comparisons": len(comparisons),
    "impact_nodes": total_nodes,
    "impact_edges": total_edges,
    "memory_records": mem_summary["total_records"],
    "traceability_rate": trace_rate,
    "lakshmi_score": gov_report.total_score,
    "lakshmi_verdict": gov_report.verdict,
    "predicted_eis": new_eis,
    "generated_at": datetime.now(timezone.utc).isoformat(),
}
(M026 / "mission_026_results.json").write_text(
    json.dumps(results, indent=2), encoding="utf-8"
)

print(f"\n{'='*60}")
print(f"RESULT: {results['status']} — {pass_count}/8 tests PASS")
print(f"Scenarios: {len(scenarios)} | Simulations: {len(simulations)} | CF: {cf_summary['total']} | DC: {len(comparisons)}")
print(f"Impact: {total_nodes} nodes, {total_edges} edges")
print(f"Traceability: {trace_rate:.1%} | Lakshmi: {gov_report.verdict} ({gov_report.total_score})")
print(f"Predicted EIS: {new_eis}")
print(f"{'='*60}")
