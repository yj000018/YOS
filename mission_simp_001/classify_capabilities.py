#!/usr/bin/env python3
"""MISSION-SIMP-001 — Capability Classification & Audit Engine."""
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
OUT = ROOT / "mission_simp_001"
OUT.mkdir(exist_ok=True)

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# ── Full module classification ─────────────────────────────────────────────
# Format: module_name → (classification, group, daily_use, loc_estimate, notes)
MODULES = {
    # === LAYER 1: FOUNDATION (FROZEN) ===
    "ccr_runtime_v2":                   ("CORE", "routing",      True,  300, "Context Router — heart of Y-OS"),
    "context_compiler_v2":              ("CORE", "routing",      True,  250, "Context Pack compiler"),
    "provider_router_v2":               ("CORE", "routing",      True,  200, "Multi-provider routing"),
    "provider_registry_v1":             ("CORE", "routing",      True,  150, "Provider registry"),
    "lakshmi_context_review_v1":        ("CORE", "governance",   True,  180, "Constitutional governance hook"),

    # === LAYER 2: EXECUTION ===
    "live_worker_executor_v1":          ("CORE", "execution",    True,  300, "Real LLM API calls"),
    "output_validator_v1":              ("CORE", "execution",    True,  150, "Artifact validation"),
    "artifact_registry_v2":             ("CORE", "memory",       True,  200, "Artifact storage"),
    "execution_trace_logger_v1":        ("CORE", "observability",True,  120, "Execution lineage"),
    "cost_tracker_v1":                  ("CORE", "observability",True,  100, "Cost per call"),

    # === LAYER 3: PIPELINE ===
    "pipeline_state_manager_v1":        ("IMPORTANT", "pipeline", True, 200, "Multi-step pipeline state"),
    "artifact_chaining_engine_v1":      ("IMPORTANT", "pipeline", True, 180, "Artifact → artifact lineage"),
    "checkpoint_rollback_engine_v1":    ("IMPORTANT", "pipeline", False,150, "Rollback — rarely triggered"),
    "validation_queue_v1":              ("IMPORTANT", "pipeline", False,120, "Queue validation — could merge with output_validator"),
    "context_cache_v1":                 ("IMPORTANT", "pipeline", True, 100, "Context caching — performance"),

    # === LAYER 4: MEMORY ===
    "session_delta_engine_v1":          ("CORE", "memory",       True,  200, "Session delta — prevents raw history injection"),
    "living_memory_pipeline_v1":        ("IMPORTANT", "memory",  True,  350, "8-stage LMP — complex, high value"),
    "strategic_memory_engine_v1":       ("OPTIONAL", "memory",   False, 150, "Strategic memory — overlaps with ODT"),
    "simulation_memory_engine_v1":      ("OPTIONAL", "memory",   False, 120, "Simulation memory — niche use"),

    # === LAYER 5: PROVIDER RESILIENCE ===
    "provider_health_monitor_v1":       ("IMPORTANT", "providers",True, 150, "Provider health"),
    "provider_failover_engine_v1":      ("IMPORTANT", "providers",True, 150, "Failover — critical for resilience"),
    "provider_cost_optimizer_v1":       ("OPTIONAL", "providers", False,120, "Cost optimizer — overlaps cost_tracker"),
    "provider_observability_dashboard_v1":("OPTIONAL","providers",False,100, "Dashboard generator — low daily use"),
    "provider_payload_builder_v1":      ("CORE", "providers",    True,  150, "Payload formatting per provider"),
    "gemini_runtime_validation_v1":     ("OPTIONAL", "providers",False, 200, "Gemini-specific validator — merge into provider_router"),
    "gemini_benchmark_runner_v1":       ("OPTIONAL", "providers",False, 180, "Benchmark runner — one-time use"),

    # === LAYER 6: KNOWLEDGE GRAPH ===
    "kg_compiler_v3":                   ("EXPERIMENTAL","graph", False, 400, "KGC v3 — superseded by v4"),
    "kgc_v4_connectivity_engine":       ("IMPORTANT", "graph",   False, 500, "KGC v4 — current graph engine"),

    # === LAYER 7: ODT ===
    "organizational_digital_twin_registry_v1": ("IMPORTANT","odt",False,300,"ODT registry — high value, low daily use"),
    "evolution_tracker_v1":             ("IMPORTANT", "odt",     False, 200, "Evolution tracking"),
    "system_health_monitor_v1":         ("IMPORTANT", "odt",     True,  200, "Health score — daily value"),
    "odt_live_update_engine_v1":        ("OPTIONAL", "odt",      False, 200, "ODT auto-update — rarely triggered"),

    # === LAYER 8: OBSERVABILITY ===
    "organizational_observability_engine_v1":("IMPORTANT","obs", False, 250, "Org observability"),
    "governance_observability_v1":      ("IMPORTANT", "obs",     False, 150, "Governance compliance tracking"),
    "executive_intelligence_score_v1":  ("IMPORTANT", "obs",     True,  150, "EIS score — useful metric"),
    "organizational_alert_engine_v1":   ("OPTIONAL", "obs",      False, 150, "Alert engine — low signal/noise"),
    "weekly_review_generator_v1":       ("OPTIONAL", "obs",      False, 150, "Weekly review — nice-to-have"),

    # === LAYER 9: INTELLIGENCE ===
    "strategic_recommendation_engine_v1":("IMPORTANT","intel",   False, 300, "Strategic recs — high value"),
    "organizational_gap_analysis_v1":   ("IMPORTANT", "intel",   False, 200, "Gap analysis"),
    "evidence_based_reasoning_engine_v1":("IMPORTANT","intel",   False, 200, "Evidence-based reasoning"),
    "mission_proposal_generator_v1":    ("IMPORTANT", "intel",   False, 180, "Mission proposals"),
    "recommendation_prioritization_engine_v1":("OPTIONAL","intel",False,150,"Prioritization — overlaps strategic_rec"),
    "roadmap_generation_engine_v1":     ("OPTIONAL", "intel",    False, 150, "Roadmap gen — low daily use"),
    "executive_advisor_dashboard_v1":   ("OPTIONAL", "intel",    False, 120, "Dashboard gen — low daily use"),

    # === LAYER 10: SIMULATION ===
    "executive_simulation_engine_v1":   ("EXPERIMENTAL","sim",   False, 300, "Simulation — high complexity, low daily use"),
    "scenario_modeling_engine_v1":      ("EXPERIMENTAL","sim",   False, 250, "Scenario modeling"),
    "impact_propagation_engine_v1":     ("EXPERIMENTAL","sim",   False, 200, "Impact propagation"),
    "counterfactual_engine_v1":         ("EXPERIMENTAL","sim",   False, 200, "Counterfactual — interesting but niche"),
    "decision_comparison_engine_v1":    ("EXPERIMENTAL","sim",   False, 150, "Decision comparison"),
    "simulation_governance_v1":         ("EXPERIMENTAL","sim",   False, 120, "Simulation governance"),

    # === LAYER 11: TIME MACHINE ===
    "odt_time_machine_v1":              ("EXPERIMENTAL","time",  False, 300, "Time machine — high complexity"),
    "organizational_snapshot_engine_v1":("EXPERIMENTAL","time",  False, 200, "Snapshot engine"),
    "temporal_reconstruction_engine_v1":("EXPERIMENTAL","time",  False, 200, "Temporal reconstruction"),
    "snapshot_diff_engine_v1":          ("EXPERIMENTAL","time",  False, 150, "Snapshot diff"),
    "organizational_timeline_generator_v1":("OPTIONAL","time",   False, 150, "Timeline generator"),
    "historical_navigation_dashboard_v1":("OPTIONAL","time",     False, 120, "Historical nav dashboard"),
    "evolution_analysis_engine_v1":     ("OPTIONAL", "time",     False, 150, "Evolution analysis"),

    # === LAYER 12: LINEAGE ===
    "legacy_lineage_recovery_engine_v1":("OPTIONAL","lineage",   False, 200, "Legacy lineage — one-time use"),
    "semantic_relationship_inference_v1":("OPTIONAL","lineage",  False, 180, "Semantic inference — part of KGC"),
    "lineage_validation_engine_v1":     ("OPTIONAL","lineage",   False, 150, "Lineage validation — merge with output_validator"),
    "lineage_review_registry_v1":       ("OPTIONAL","lineage",   False, 120, "Lineage registry — merge with artifact_registry"),
    "lineage_dashboard_generator_v1":   ("OPTIONAL","lineage",   False, 100, "Dashboard gen — low daily use"),
    "lineage_canvas_generator_v1":      ("OPTIONAL","lineage",   False, 100, "Canvas gen — low daily use"),

    # === LAYER 13: EVENT BUS ===
    "event_bus_core_v1":                ("IMPORTANT","events",   False, 300, "Event bus — infrastructure"),
    "event_registry_v1":                ("IMPORTANT","events",   False, 150, "Event registry"),
    "event_router_v1":                  ("IMPORTANT","events",   False, 150, "Event router"),
    "event_persistence_v1":             ("IMPORTANT","events",   False, 120, "Event persistence"),
    "event_replay_engine_v1":           ("IMPORTANT","events",   False, 150, "Event replay — for time machine"),
    "event_observability_v1":           ("OPTIONAL","events",    False, 120, "Event observability — low daily use"),
    "event_lineage_tracker_v1":         ("OPTIONAL","events",    False, 100, "Event lineage — overlaps execution_trace"),

    # === LAYER 14: ARTIFACT SUPERSESSION ===
    "artifact_supersession_engine_v1":  ("OPTIONAL","artifacts", False, 150, "Supersession — rarely triggered"),
}

# ── Compute stats ──────────────────────────────────────────────────────────
from collections import Counter

classifications = Counter(v[0] for v in MODULES.values())
groups = Counter(v[1] for v in MODULES.values())
daily_use = sum(1 for v in MODULES.values() if v[2])
total = len(MODULES)

print(f"Total modules: {total}")
print(f"Classifications: {dict(classifications)}")
print(f"Daily use: {daily_use}/{total} ({daily_use/total*100:.0f}%)")

# ── Duplicate / overlap analysis ───────────────────────────────────────────
DUPLICATES = [
    {
        "group": "Cost Tracking",
        "modules": ["cost_tracker_v1", "provider_cost_optimizer_v1"],
        "recommendation": "MERGE → cost_tracker_v2",
        "savings": "1 module"
    },
    {
        "group": "Validation",
        "modules": ["output_validator_v1", "validation_queue_v1", "lineage_validation_engine_v1"],
        "recommendation": "MERGE → validation_engine_v2",
        "savings": "2 modules"
    },
    {
        "group": "Registry",
        "modules": ["artifact_registry_v2", "lineage_review_registry_v1", "provider_registry_v1"],
        "recommendation": "MERGE → unified_registry_v1 (or keep separate — different domains)",
        "savings": "0-1 modules"
    },
    {
        "group": "Dashboard Generators",
        "modules": ["provider_observability_dashboard_v1", "executive_advisor_dashboard_v1",
                    "lineage_dashboard_generator_v1", "historical_navigation_dashboard_v1"],
        "recommendation": "MERGE → dashboard_generator_v1 (single templated generator)",
        "savings": "3 modules"
    },
    {
        "group": "Canvas Generators",
        "modules": ["lineage_canvas_generator_v1"],
        "recommendation": "MERGE into dashboard_generator_v1",
        "savings": "1 module"
    },
    {
        "group": "Memory",
        "modules": ["strategic_memory_engine_v1", "simulation_memory_engine_v1"],
        "recommendation": "MERGE → memory_engine_v2 (or deprecate both — ODT covers this)",
        "savings": "2 modules"
    },
    {
        "group": "Lineage Tracking",
        "modules": ["execution_trace_logger_v1", "event_lineage_tracker_v1", "lineage_validation_engine_v1"],
        "recommendation": "MERGE → lineage_tracker_v2",
        "savings": "2 modules"
    },
    {
        "group": "KGC Versions",
        "modules": ["kg_compiler_v3", "kgc_v4_connectivity_engine"],
        "recommendation": "ARCHIVE kg_compiler_v3 — superseded",
        "savings": "1 module"
    },
    {
        "group": "Gemini-Specific",
        "modules": ["gemini_runtime_validation_v1", "gemini_benchmark_runner_v1"],
        "recommendation": "MERGE into provider_router_v2 + provider_health_monitor_v1",
        "savings": "2 modules"
    },
]

# ── Sunset candidates ──────────────────────────────────────────────────────
SUNSET = [
    {"module": "kg_compiler_v3",                   "reason": "Superseded by kgc_v4", "risk": "LOW"},
    {"module": "gemini_benchmark_runner_v1",        "reason": "One-time validation, done", "risk": "LOW"},
    {"module": "gemini_runtime_validation_v1",      "reason": "Merge into provider_router", "risk": "LOW"},
    {"module": "simulation_memory_engine_v1",       "reason": "ODT covers this", "risk": "LOW"},
    {"module": "strategic_memory_engine_v1",        "reason": "ODT + strategic_rec covers this", "risk": "LOW"},
    {"module": "legacy_lineage_recovery_engine_v1", "reason": "One-time use, mission complete", "risk": "LOW"},
    {"module": "lineage_canvas_generator_v1",       "reason": "Merge into dashboard_generator", "risk": "LOW"},
    {"module": "lineage_dashboard_generator_v1",    "reason": "Merge into dashboard_generator", "risk": "LOW"},
    {"module": "provider_observability_dashboard_v1","reason": "Merge into dashboard_generator", "risk": "LOW"},
    {"module": "executive_advisor_dashboard_v1",    "reason": "Merge into dashboard_generator", "risk": "LOW"},
    {"module": "event_lineage_tracker_v1",          "reason": "Merge into execution_trace_logger", "risk": "LOW"},
    {"module": "lineage_review_registry_v1",        "reason": "Merge into artifact_registry", "risk": "LOW"},
    {"module": "lineage_validation_engine_v1",      "reason": "Merge into output_validator", "risk": "LOW"},
    {"module": "provider_cost_optimizer_v1",        "reason": "Merge into cost_tracker", "risk": "LOW"},
    {"module": "recommendation_prioritization_engine_v1","reason":"Merge into strategic_rec", "risk": "LOW"},
    {"module": "roadmap_generation_engine_v1",      "reason": "Merge into strategic_rec", "risk": "LOW"},
    {"module": "organizational_alert_engine_v1",    "reason": "Low signal/noise, low daily use", "risk": "MEDIUM"},
    {"module": "weekly_review_generator_v1",        "reason": "Nice-to-have, low daily use", "risk": "LOW"},
    {"module": "odt_live_update_engine_v1",         "reason": "Rarely triggered, ODT handles manually", "risk": "MEDIUM"},
]

# ── Rebuild test (7 days) ──────────────────────────────────────────────────
REBUILD = {
    "day_1": {
        "title": "Foundation",
        "modules": ["ccr_runtime_v2", "context_compiler_v2", "provider_router_v2",
                    "provider_registry_v1", "provider_payload_builder_v1"],
        "rationale": "Without routing, nothing works"
    },
    "day_2": {
        "title": "Execution + Governance",
        "modules": ["live_worker_executor_v1", "output_validator_v1",
                    "artifact_registry_v2", "lakshmi_context_review_v1"],
        "rationale": "Without execution + governance, no artifacts"
    },
    "day_3": {
        "title": "Memory + Lineage",
        "modules": ["session_delta_engine_v1", "execution_trace_logger_v1", "cost_tracker_v1"],
        "rationale": "Without memory, no continuity"
    },
    "day_4": {
        "title": "Pipeline + Resilience",
        "modules": ["pipeline_state_manager_v1", "artifact_chaining_engine_v1",
                    "provider_health_monitor_v1", "provider_failover_engine_v1"],
        "rationale": "Multi-step + failover"
    },
    "day_5": {
        "title": "Observability",
        "modules": ["system_health_monitor_v1", "executive_intelligence_score_v1",
                    "organizational_observability_engine_v1"],
        "rationale": "Without observability, no self-awareness"
    },
    "day_6": {
        "title": "Intelligence",
        "modules": ["strategic_recommendation_engine_v1", "organizational_gap_analysis_v1",
                    "evidence_based_reasoning_engine_v1", "mission_proposal_generator_v1"],
        "rationale": "Strategic autonomy"
    },
    "day_7": {
        "title": "Knowledge Graph (minimal)",
        "modules": ["kgc_v4_connectivity_engine", "living_memory_pipeline_v1"],
        "rationale": "Corpus navigation + memory pipeline"
    },
    "NOT_rebuilt": {
        "modules": ["event_bus_core_v1 (and all 6 event_* modules)",
                    "odt_time_machine_v1 (and all 5 time_* modules)",
                    "executive_simulation_engine_v1 (and all 5 sim_* modules)",
                    "counterfactual_engine_v1", "scenario_modeling_engine_v1",
                    "impact_propagation_engine_v1", "organizational_digital_twin_registry_v1",
                    "evolution_tracker_v1", "all dashboard_generator_* modules",
                    "all lineage_* legacy modules"],
        "rationale": "High complexity, low daily value, can be added in month 2"
    }
}

# ── Core Architecture v2 ───────────────────────────────────────────────────
CORE_ARCH_V2 = {
    "layers": {
        "L1_ROUTING": {
            "modules": ["ccr_runtime_v2", "context_compiler_v2", "provider_router_v2",
                        "provider_registry_v1", "provider_payload_builder_v1"],
            "description": "Context routing and provider selection"
        },
        "L2_EXECUTION": {
            "modules": ["live_worker_executor_v1", "output_validator_v1",
                        "artifact_registry_v2", "lakshmi_context_review_v1"],
            "description": "Worker execution, validation, governance"
        },
        "L3_MEMORY": {
            "modules": ["session_delta_engine_v1", "execution_trace_logger_v1",
                        "cost_tracker_v1", "context_cache_v1"],
            "description": "Session memory, lineage, cost"
        },
        "L4_PIPELINE": {
            "modules": ["pipeline_state_manager_v1", "artifact_chaining_engine_v1",
                        "provider_health_monitor_v1", "provider_failover_engine_v1"],
            "description": "Multi-step execution, resilience"
        },
        "L5_OBSERVABILITY": {
            "modules": ["system_health_monitor_v1", "executive_intelligence_score_v1",
                        "governance_observability_v1", "organizational_observability_engine_v1"],
            "description": "Health, EIS, governance compliance"
        },
        "L6_INTELLIGENCE": {
            "modules": ["strategic_recommendation_engine_v1", "organizational_gap_analysis_v1",
                        "evidence_based_reasoning_engine_v1", "mission_proposal_generator_v1"],
            "description": "Strategic autonomy"
        },
        "L7_KNOWLEDGE": {
            "modules": ["kgc_v4_connectivity_engine", "living_memory_pipeline_v1"],
            "description": "Corpus navigation, memory pipeline"
        }
    },
    "total_core_modules": 0,
    "optional_layers": {
        "L8_EVENTS": "Event Bus (7 modules) — add when real-time triggers needed",
        "L9_ODT": "ODT Registry + Evolution (4 modules) — add for organizational awareness",
        "L10_INTELLIGENCE_PLUS": "Simulation + Time Machine (12 modules) — add for predictive capability",
    }
}

core_count = sum(len(v["modules"]) for v in CORE_ARCH_V2["layers"].values())
CORE_ARCH_V2["total_core_modules"] = core_count

# ── Simplification Backlog ─────────────────────────────────────────────────
BACKLOG = [
    {"id": "SIMP-001", "action": "ARCHIVE kg_compiler_v3", "effort": "30min", "roi": "HIGH", "risk": "LOW"},
    {"id": "SIMP-002", "action": "MERGE 4 dashboard generators → dashboard_generator_v1", "effort": "2h", "roi": "HIGH", "risk": "LOW"},
    {"id": "SIMP-003", "action": "MERGE validation_queue + lineage_validation → output_validator_v2", "effort": "2h", "roi": "HIGH", "risk": "LOW"},
    {"id": "SIMP-004", "action": "MERGE cost_tracker + provider_cost_optimizer → cost_tracker_v2", "effort": "1h", "roi": "HIGH", "risk": "LOW"},
    {"id": "SIMP-005", "action": "ARCHIVE legacy_lineage_recovery (one-time use)", "effort": "10min", "roi": "HIGH", "risk": "LOW"},
    {"id": "SIMP-006", "action": "ARCHIVE gemini_benchmark_runner (one-time use)", "effort": "10min", "roi": "MEDIUM", "risk": "LOW"},
    {"id": "SIMP-007", "action": "MERGE gemini_runtime_validation → provider_router_v2", "effort": "2h", "roi": "MEDIUM", "risk": "LOW"},
    {"id": "SIMP-008", "action": "MERGE strategic_memory + simulation_memory → memory_engine_v2", "effort": "2h", "roi": "MEDIUM", "risk": "LOW"},
    {"id": "SIMP-009", "action": "MERGE recommendation_prioritization + roadmap_gen → strategic_rec_v2", "effort": "2h", "roi": "MEDIUM", "risk": "LOW"},
    {"id": "SIMP-010", "action": "MERGE event_lineage_tracker → execution_trace_logger_v2", "effort": "1h", "roi": "MEDIUM", "risk": "LOW"},
    {"id": "SIMP-011", "action": "MERGE lineage_review_registry → artifact_registry_v3", "effort": "1h", "roi": "MEDIUM", "risk": "LOW"},
    {"id": "SIMP-012", "action": "DEPRECATE organizational_alert_engine (low S/N)", "effort": "10min", "roi": "MEDIUM", "risk": "LOW"},
    {"id": "SIMP-013", "action": "DEPRECATE weekly_review_generator (low daily use)", "effort": "10min", "roi": "LOW", "risk": "LOW"},
    {"id": "SIMP-014", "action": "DEPRECATE odt_live_update_engine (rarely triggered)", "effort": "10min", "roi": "LOW", "risk": "MEDIUM"},
    {"id": "SIMP-015", "action": "MOVE simulation layer to /experimental/ folder", "effort": "30min", "roi": "HIGH", "risk": "LOW"},
    {"id": "SIMP-016", "action": "MOVE time_machine layer to /experimental/ folder", "effort": "30min", "roi": "HIGH", "risk": "LOW"},
    {"id": "SIMP-017", "action": "FLATTEN runtime/ → group by layer (routing/, execution/, etc.)", "effort": "2h", "roi": "HIGH", "risk": "LOW"},
    {"id": "SIMP-018", "action": "CONSOLIDATE 26 canvas maps → 8 canonical maps", "effort": "2h", "roi": "HIGH", "risk": "LOW"},
    {"id": "SIMP-019", "action": "CONSOLIDATE 17 dashboards → 6 canonical dashboards", "effort": "2h", "roi": "HIGH", "risk": "LOW"},
    {"id": "SIMP-020", "action": "ARCHIVE mission_001→012 dirs → /archive/ (doctrine preserved in .md)", "effort": "1h", "roi": "MEDIUM", "risk": "LOW"},
]

# ── Save results ───────────────────────────────────────────────────────────
results = {
    "generated": NOW,
    "inventory": {
        "total_modules": total,
        "classifications": dict(classifications),
        "groups": dict(groups),
        "daily_use_modules": daily_use,
        "daily_use_pct": round(daily_use/total*100, 1)
    },
    "modules": {k: {"classification": v[0], "group": v[1], "daily_use": v[2], "notes": v[4]}
                for k, v in MODULES.items()},
    "duplicates": DUPLICATES,
    "sunset_candidates": SUNSET,
    "core_architecture_v2": CORE_ARCH_V2,
    "rebuild_test": REBUILD,
    "simplification_backlog": BACKLOG,
    "complexity_reduction": {
        "current_modules": total,
        "core_modules": core_count,
        "sunset_candidates": len(SUNSET),
        "after_simplification": total - len(SUNSET),
        "reduction_pct": round(len(SUNSET)/total*100, 1)
    }
}

(OUT / "simp001_analysis.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
print(f"✅ simp001_analysis.json")
print(f"\n=== COMPLEXITY REDUCTION SUMMARY ===")
print(f"Current modules: {total}")
print(f"Core modules (L1-L7): {core_count}")
print(f"Sunset candidates: {len(SUNSET)}")
print(f"After simplification: {total - len(SUNSET)}")
print(f"Reduction: {len(SUNSET)/total*100:.0f}%")
print(f"\nClassifications:")
for k, v in sorted(classifications.items()):
    print(f"  {k}: {v} ({v/total*100:.0f}%)")
print(f"\nDaily use: {daily_use}/{total} ({daily_use/total*100:.0f}%)")
print(f"Core daily use: {sum(1 for v in MODULES.values() if v[0]=='CORE' and v[2])}/{sum(1 for v in MODULES.values() if v[0]=='CORE')} CORE modules")
