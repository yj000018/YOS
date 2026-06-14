---
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

### #1 — HOT-001: runtime/ directory (70 modules)

**Score:** 95/100  
**Issue:** 70 flat Python files — no sub-packages, no __init__.py, no module registry  
**Action:** Reorganize into sub-packages: core/, knowledge/, execution/, memory/, observability/, intelligence/, simulation/

### #2 — HOT-002: Governance layer (4 overlapping validators)

**Score:** 88/100  
**Issue:** lakshmi_context_review, simulation_governance, lineage_validation, output_validator — 4 separate governance paths  
**Action:** Unify into GovernanceEngine v1 with pluggable validators

### #3 — HOT-003: Dashboard generators (5 separate modules)

**Score:** 82/100  
**Issue:** Each mission created its own dashboard generator — no shared template  
**Action:** DashboardFactory v1 with Jinja2 templates

### #4 — HOT-004: Canvas generators (4 separate scripts)

**Score:** 78/100  
**Issue:** 4 different canvas generation approaches — no shared canvas library  
**Action:** CanvasFactory v1 with node/edge primitives

### #5 — HOT-005: KGC versions (v1/v2/v3/v4 all present)

**Score:** 75/100  
**Issue:** 4 compiler versions coexist — v1/v2/v3 are dead code  
**Action:** Archive v1/v2/v3 to mission_*/legacy/, keep only v4

### #6 — HOT-006: JSON registries (131 files)

**Score:** 70/100  
**Issue:** 131 JSON files with no schema validation, no versioning, no index  
**Action:** Registry schema v1 + central registry_index.json

### #7 — HOT-007: run_mission_*.py scripts (14 files)

**Score:** 65/100  
**Issue:** 14 mission runner scripts with duplicated test harness code  
**Action:** MissionRunner base class with shared test infrastructure

### #8 — HOT-008: Lineage tracking (4 overlapping systems)

**Score:** 60/100  
**Issue:** mission_lineage_registry, event_lineage_tracker, lineage_review_registry, execution_trace_logger — 4 lineage systems  
**Action:** Consolidate into LineageEngine v1

### #9 — HOT-009: Provider payload builder (3 providers, 1 monolithic file)

**Score:** 55/100  
**Issue:** provider_payload_builder_v1.py handles OpenAI/Anthropic/Gemini in one file — no provider plugin pattern  
**Action:** Provider plugin pattern: ProviderAdapter base class

### #10 — HOT-010: ADR-0017 duplicate (2 files with same ID)

**Score:** 50/100  
**Issue:** ADR-0017_Artifact_Registry.md AND ADR-0017_Lakshmi_MVP_Runtime.md — same ID, different content  
**Action:** Rename one to ADR-0017b or reassign ID

---

## Semantic Links

- **produced_by:** [[MISSION-026A_Architecture_Freeze]]
