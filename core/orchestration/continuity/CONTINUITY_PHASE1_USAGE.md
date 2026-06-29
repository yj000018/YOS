# yOS Continuity Core — Phase 1 Usage Guide

**Status:** CANONICAL  
**Version:** 1.1 (Closeout Reconciliation Pass)  
**Date:** 2026-06-29  
**Branch:** phase-iii/yos-continuity-core-consolidation  

---

## Overview

> **Note:** Smoke tests confirm basic script execution and expected minimal behavior. They do not constitute full production validation.

> **Note:** Phase 2 features (semantic diff, prompt caching, pack forking, lineage graph, Sarasvati loop) remain intentionally deferred.

> **Note:** `pack_version_tracker.py` is classified **experimental_non_canonical** — `rollback` and `diff` subcommands are deferred to Phase 2. Only `list` and `register` are Phase 1 approved.

---

Phase 1 delivers **13 Python scripts** implementing the yOS Continuity Core tooling.
These scripts are **operational tools**, not runtime services.
They run on-demand from the command line or from Manus sessions.

**Canonical script location:** `YOS/scripts/`  
**Context packs output:** `YOS/core/orchestration/context_packs/`  
**Routing matrix:** `YOS/core/orchestration/registries/LLM_AND_TOOL_ROUTING_MATRIX.md`

---

## Script Inventory and Classification

| Script | Classification | Phase 2 Risk | Smoke Test |
|---|---|---|---|
| `routing_matrix_loader.py` | canonical_phase1 | None | ✅ rc=0 |
| `continuity_mode_resolver.py` | canonical_phase1 | None | ✅ rc=0 |
| `context_boundary_detector.py` | canonical_phase1 | None | ✅ rc=0 |
| `pack_staleness_detector.py` | canonical_phase1 | None | ✅ rc=0 |
| `context_pack_checksum_verifier.py` | canonical_phase1 | None | ✅ rc=0 |
| `cap_validator.py` | canonical_phase1 | None | ✅ rc=0 |
| `context_pack_generator.py` | canonical_phase1 | None | ✅ rc=0 |
| `pack_command.py` | canonical_phase1 | None | ✅ rc=0 |
| `handoff_packet_builder.py` | canonical_phase1 | Low — lightweight helper | ✅ rc=0 |
| `enforcement_checker.py` | canonical_phase1 | None | ✅ rc=0 |
| `drift_detector.py` | canonical_phase1 | Low — lightweight helper | ✅ rc=0 |
| `pack_preview.py` | canonical_phase1 | None | ✅ rc=0 |
| `pack_version_tracker.py` | **experimental_non_canonical** | **High — rollback/diff** | ✅ rc=0 |

---

## Legacy Script Purpose Table

| Script | Purpose | Primary Use |
|---|---|---|
| `routing_matrix_loader.py` | Load and query the routing matrix | All scripts (dependency) |
| `continuity_mode_resolver.py` | Resolve session mode from task context | Session start |
| `context_boundary_detector.py` | Detect context boundaries requiring new pack | Session monitoring |
| `pack_staleness_detector.py` | Detect stale packs by task_class policy | Before injection |
| `context_pack_checksum_verifier.py` | Verify pack integrity (authoritative) | Before injection |
| `cap_validator.py` | Validate CAP fields (authoritative) | Before execution |
| `context_pack_generator.py` | Generate packs at T0/T1/T2/T3 tiers | Pack creation |
| `pack_command.py` | `/pack` one-click CLI entry point | User-facing |
| `handoff_packet_builder.py` | Build complete Handoff Packets | LLM-to-LLM transfer |
| `enforcement_checker.py` | Run all 10 enforcement rules | Pre-execution gate |
| `drift_detector.py` | Detect context drift between packs | Quality control |
| `pack_preview.py` | Preview pack before injection | Before expensive injection |
| `pack_version_tracker.py` | Pack registry (list/register only — Phase 1) | Pack management |

---

## pack_version_tracker.py — Scope Decision

**Classification: B — experimental_non_canonical**

Reason: Implements real rollback and diff (lines 89–145), explicitly deferred to Phase 2 in the MPM. Present in `scripts/` but **not part of approved Phase 1 canon**. Must not be used in production workflows until Phase 2 is approved.

- Safe Phase 1 use: `list` and `register` subcommands only
- Deferred: `rollback` and `diff` subcommands — Phase 2 only

---

## Quick Start

### Generate a Context Pack

```bash
# T1 Standard pack for a project
python3 scripts/pack_command.py yos-continuity-core --tier T1_standard

# Preview before saving
python3 scripts/pack_command.py yos-continuity-core --tier T2_full_lineage --preview

# From JSON input
python3 scripts/pack_command.py --input-json my_project.json --tier T1_standard
```

### Validate a Pack Before Injection

```bash
# Full enforcement check (all 10 rules)
python3 scripts/enforcement_checker.py --pack core/orchestration/context_packs/my_pack.md

# CAP validation only
python3 scripts/cap_validator.py --pack my_pack.md

# Staleness check
python3 scripts/pack_staleness_detector.py --pack my_pack.md

# Checksum verification
python3 scripts/context_pack_checksum_verifier.py --pack my_pack.md

# Preview summary
python3 scripts/pack_preview.py --pack my_pack.md
```

### Build a Handoff Packet

```bash
# Manus → ChatGPT handoff
python3 scripts/handoff_packet_builder.py \
  --from manus --to chatgpt \
  --project yos-continuity-core \
  --tier T1_standard \
  --task-class architecture
```

### Detect Drift

```bash
# Compare two packs
python3 scripts/drift_detector.py --pack-a pack_v1.md --pack-b pack_v2.md

# Check single pack for staleness drift
python3 scripts/drift_detector.py --pack my_pack.md
```

### Pack Registry (Phase 1 safe operations only)

```bash
# List all registered packs
python3 scripts/pack_version_tracker.py list

# Register a pack (safe — Phase 1 approved)
python3 scripts/pack_version_tracker.py register --pack my_pack.md --project yos

# DEFERRED — do not use until Phase 2 approved:
# python3 scripts/pack_version_tracker.py rollback ...
# python3 scripts/pack_version_tracker.py diff ...
```

---

## Context Pack Tiers

| Tier | Depth | Est. Tokens | Use Case |
|---|---|---|---|
| `T0_nano` | minimal | ~500 | Quick workers, specialized subtasks |
| `T1_standard` | standard | ~2000 | Normal sessions (default) |
| `T2_full_lineage` | full_lineage | ~8000 | Architecture sessions, ADR reviews |
| `T3_emergency_recovery` | emergency_recovery | ~12000+ | Recovery from context loss |

---

## CAP — Constraint Acknowledgment Protocol

CAP is a **handoff validation rule**, not a trust mechanism.

- **LLM acknowledgment** (`cap_acknowledged: true`) = DECLARATIVE only
- **Script/runtime verification** = AUTHORITATIVE
### CAP Severity Rules (Normalized)

| Scenario | Severity |
|---|---|
| Missing CAP — governed handoff | `hard_stop` |
| Missing CAP — gate-critical handoff | `hard_stop` |
| Expired CAP (> 24h) | `blocking` |
| Hash mismatch — gate-critical | `hard_stop` |
| Hash mismatch — governed | `blocking` |
| E02 CAP Validation failure | `hard_stop` or `blocking` (gate criticality) |
| E06 Constraint Acknowledgment — non-governed low-risk | `warning` |
| E06 Constraint Acknowledgment — governed handoff | Escalates to E02 → `blocking` / `hard_stop` |

The receiving LLM must declare:
```
cap_acknowledged: true
cap_acknowledged_by: <llm_id>
cap_acknowledged_at: <ISO8601>
cap_constraints_hash: <sha256>
```

---

## Enforcement Rules Summary

| Rule | Severity if Failed |
|---|---|
| E01: Context Pack Required | hard_stop |
| E02: CAP Validation | hard_stop / blocking |
| E03: Staleness Check | blocking |
| E04: Checksum Integrity | blocking |
| E05: Session Mode Compliance | blocking |
| E06: Constraint Acknowledgment | warning (non-governed) / escalates to E02 (governed) |
| E07: Routing Matrix Compliance | blocking |
| E08: Memory Backend Declared | advisory |
| E09: Handoff Completeness | warning |
| E10: Escalation Threshold | advisory |

---

## Memory Backend

All scripts use generic `canonical_memory_backend` and `shared_pack_backend` fields.

**No backend is mandatory.** Canonical Memory is a policy layer, not a provider dependency.
The system must degrade gracefully when a backend is unavailable.
Context Pack generation must disclose unavailable or missing sources.

```
canonical_memory_backend: git | notion | mem0 | registry | local | manual_artifacts | other | unavailable
shared_pack_backend: git | notion | registry | local | other
```

---

## Phase 2 (Deferred)

The following are **intentionally deferred** to Phase 2:

- Semantic diff between packs
- Prompt caching (Anthropic cache_control / OpenAI)
- Pack forking for multi-agent scenarios
- Lineage graph visualization
- Shared pack with multi-backend sync
- Sarasvati Pack Quality Score loop
- Automatic Notion/Mem0 hydration at session start
- `pack_version_tracker.py` rollback/diff

---

## Files

```
YOS/
├── scripts/                          ← 13 Phase 1 scripts (canonical location)
│   ├── routing_matrix_loader.py          canonical_phase1
│   ├── continuity_mode_resolver.py       canonical_phase1
│   ├── context_boundary_detector.py      canonical_phase1
│   ├── pack_staleness_detector.py        canonical_phase1
│   ├── context_pack_checksum_verifier.py canonical_phase1
│   ├── cap_validator.py                  canonical_phase1
│   ├── context_pack_generator.py         canonical_phase1
│   ├── pack_command.py                   canonical_phase1
│   ├── handoff_packet_builder.py         canonical_phase1
│   ├── enforcement_checker.py            canonical_phase1
│   ├── drift_detector.py                 canonical_phase1
│   ├── pack_preview.py                   canonical_phase1
│   └── pack_version_tracker.py           experimental_non_canonical
├── core/orchestration/
│   ├── continuity/
│   │   ├── YOS_CONTINUITY_CORE.md
│   │   ├── CONTEXT_SESSION_MODE_MATRIX.md
│   │   ├── CONTEXT_PACK_SCHEMA_V2_1_YOS_ADAPTATION.md
│   │   ├── CONTINUITY_ENFORCEMENT_PROTOCOL.md
│   │   ├── CONTINUITY_DECISION_FLOW.md
│   │   └── CONTINUITY_PHASE1_USAGE.md    ← THIS FILE (canonical)
│   ├── registries/
│   │   └── LLM_AND_TOOL_ROUTING_MATRIX.md
│   ├── context_packs/                ← Generated packs + registry
│   │   ├── pack_registry.json
│   │   └── history/
│   └── reports/                      ← Phase reports
└── docs/
    └── CONTINUITY_PHASE1_USAGE.md    ← Stub pointer only (not canonical)
```
