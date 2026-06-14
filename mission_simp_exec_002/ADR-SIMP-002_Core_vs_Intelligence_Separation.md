# ADR-SIMP-002 — Core vs Intelligence Separation

**Status:** ACCEPTED  
**Date:** 2026-06-14  
**Mission:** MISSION-SIMP-EXEC-002  
**Supersedes:** ADR-SIMP-001 (extends, does not replace)  
**Lakshmi Risk Score:** 5/100 — APPROVE  

---

## Context

Y-OS has grown from a 5-module concept to a 72-module architecture across 26 missions. The architecture is technically sound but cognitively overwhelming for a single operator. MISSION-SIMP-EXEC-001 reduced active modules from 72 to 41. This ADR defines the permanent separation between core and optional layers.

---

## Decision

**Y-OS Core is frozen as 10 modules across 5 domains.**

```
CORE = {
  capture:   session_delta_engine_v1
  memory:    artifact_registry_v2, context_cache_v1
  context:   context_compiler_v2, ccr_runtime_v2, provider_payload_builder_v1
  execution: live_worker_executor_v1, output_validator_v1, lakshmi_context_review_v1, provider_registry_v1
  review:    (weekly, not daily — no core module required)
}
```

**All ODT, simulation, time-machine, executive intelligence and strategic recommendation layers are optional plugins.**

---

## Consequences

### Positive
- Y-OS can be understood in 10 minutes
- Y-OS can be rebuilt in 3 days
- Daily operation requires only 10 modules
- Optional plugins can evolve independently
- Cognitive load reduced by ~60%

### Negative
- Some modules currently in review/ must be moved to optional/intelligence/
- Plugin activation requires explicit trigger (no auto-load)
- Intelligence layer loses "always-on" status

### Neutral
- All modules preserved in Git — nothing deleted
- Plugin capabilities unchanged
- Constitution compliance unchanged (Lakshmi remains in core)

---

## Promotion Rules

A module may be promoted from OPTIONAL to CORE only if it passes ALL 4 tests:

| Test | Criterion |
|---|---|
| **Weekly use test** | Used at least once per week in normal operation |
| **Workload reduction test** | Demonstrably reduces human effort or cognitive load |
| **7-day rebuild test** | Would be rebuilt in the first 7 days from zero |
| **One-in / one-out test** | Adding it requires removing another core module |

**No future mission may promote a plugin to CORE without passing all 4 tests.**

---

## Plugin Registry

| Plugin | Modules | Activation |
|---|---|---|
| P1: Organizational Digital Twin | 7 | Monthly review |
| P2: Strategic Intelligence | 6 | Quarterly planning |
| P3: Simulation / Time Machine | 7 | Major decisions |
| P4: Advanced Observability | 4+ dashboards | Weekly health check |

---

## Governance Review

**Lakshmi (Constitutional Governance):**

- Article 1 (Artifact Primacy): ✅ All artifacts preserved
- Article 2 (Preservation): ✅ No modules deleted
- Article 3 (Derivation Transparency): ✅ All decisions documented
- Article 4 (Human Override): ✅ Plugin activation is human-triggered
- Article 5 (Governance Before Autonomy): ✅ Lakshmi remains in core

**Risk Score: 5/100 — APPROVE**

---

## CEO Recommendation (Ganesha)

> "This separation is the most important architectural decision since the Constitution. It makes Y-OS maintainable by a single human. ADOPT immediately."

**Verdict: ADOPT**
