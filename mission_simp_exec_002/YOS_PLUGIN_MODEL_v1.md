# Y-OS Plugin Model v1

> **Optional capabilities. Activated on demand. Never required for daily operation.**

---

## Plugin 1 — Organizational Digital Twin

| Field | Value |
|---|---|
| Purpose | Represent Y-OS as a living organizational system with state, roles, and metrics |
| Modules | odt_time_machine · organizational_snapshot_engine · temporal_reconstruction · snapshot_diff · organizational_timeline_generator · historical_navigation_dashboard · evolution_analysis_engine |
| Dependencies | artifact_registry · kgc_v4 · session_delta |
| Activation trigger | Monthly organizational review, architecture audit, onboarding |
| Expected value | Full organizational state snapshot, evolution timeline, inflection point analysis |
| Why not core | Not needed for daily execution. Monthly at most. High complexity, low daily ROI. |
| Location | runtime/experimental/ |

---

## Plugin 2 — Strategic Intelligence

| Field | Value |
|---|---|
| Purpose | Analyze gaps, generate mission proposals, prioritize recommendations, produce roadmaps |
| Modules | strategic_recommendation_engine · organizational_gap_analysis · evidence_based_reasoning_engine · mission_proposal_generator · recommendation_prioritization_engine · roadmap_generation_engine |
| Dependencies | artifact_registry · system_health_monitor · EIS |
| Activation trigger | Quarterly planning, architecture review, "what should Y-OS do next?" |
| Expected value | Prioritized recommendation list, next mission proposals, strategic roadmap |
| Why not core | Valuable monthly. Not needed for daily execution. Requires full corpus context. |
| Location | runtime/review/ (move to optional/intelligence/ in Phase 2) |

---

## Plugin 3 — Simulation / Time Machine

| Field | Value |
|---|---|
| Purpose | Replay organizational history, simulate "what if X changes", counterfactual analysis |
| Modules | executive_simulation_engine · scenario_modeling_engine · impact_propagation_engine · counterfactual_engine · decision_comparison_engine · simulation_governance · executive_simulation_dashboard |
| Dependencies | ODT Plugin 1 · artifact_registry · kgc_v4 |
| Activation trigger | Major decision with significant consequences, pre-mission impact analysis |
| Expected value | Scenario comparison, impact propagation, counterfactual insights |
| Why not core | Rare use. Depends on Plugin 1. High compute cost. Not daily. |
| Location | runtime/experimental/ |

---

## Plugin 4 — Advanced Observability

| Field | Value |
|---|---|
| Purpose | Monitor Y-OS health, compute EIS, generate dashboards, track governance compliance |
| Modules | system_health_monitor · executive_intelligence_score · governance_observability · organizational_observability_engine · all dashboards (10_Live_Dashboards/) · all canvas maps (08_Visual_Maps/) |
| Dependencies | artifact_registry · cost_tracker · provider_health_monitor |
| Activation trigger | Weekly health check, performance audit, Obsidian navigation session |
| Expected value | EIS score, health dashboard, governance compliance report, visual graph |
| Why not core | Useful weekly but not existential. Core can run without observability. |
| Location | runtime/review/ + 10_Live_Dashboards/ + 08_Visual_Maps/ |

---

## Plugin Activation Protocol

```
1. Load core (10 modules)
2. Identify need (monthly review / major decision / audit)
3. Activate relevant plugin
4. Run plugin with current artifact_registry context
5. Deactivate — return to core-only mode
```

---

## Plugin Dependency Graph

```
Plugin 3 (Simulation)
    └── requires Plugin 1 (ODT)
            └── requires CORE

Plugin 2 (Strategic)
    └── requires Plugin 4 (Observability)
            └── requires CORE

Plugin 4 (Observability)
    └── requires CORE only
```
