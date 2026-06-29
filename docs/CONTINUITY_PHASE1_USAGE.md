# yOS Continuity Core — Phase 1 Usage Guide

**Status:** CANONICAL  
**Version:** 1.0  
**Date:** 2026-06-29  
**Branch:** phase-iii/yos-continuity-core-consolidation  

---

## Overview

Phase 1 delivers 12 Python scripts implementing the yOS Continuity Core tooling.
These scripts are **operational tools**, not runtime services.
They run on-demand from the command line or from Manus sessions.

**Canonical location:** `YOS/scripts/`  
**Context packs output:** `YOS/core/orchestration/context_packs/`  
**Routing matrix:** `YOS/core/orchestration/registries/LLM_AND_TOOL_ROUTING_MATRIX.md`

---

## Script Inventory

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
| `pack_version_tracker.py` | Version history, rollback, diff | Pack management |

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

### Version Management

```bash
# List all packs
python3 scripts/pack_version_tracker.py list

# Register a pack
python3 scripts/pack_version_tracker.py register --pack my_pack.md --project yos

# Rollback to a previous version
python3 scripts/pack_version_tracker.py rollback --pack-id pack_20260629_120000 --output restored.md

# Diff two versions
python3 scripts/pack_version_tracker.py diff --pack-a pack_v1_id --pack-b pack_v2_id
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
- **Missing CAP** = `hard_stop` before execution
- **Expired CAP** (> 24h) = `blocking`
- **Hash mismatch** = `blocking` (constraints may have changed)

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
| E06: Constraint Acknowledgment | warning |
| E07: Routing Matrix Compliance | blocking |
| E08: Memory Backend Declared | advisory |
| E09: Handoff Completeness | warning |
| E10: Escalation Threshold | advisory |

---

## Memory Backend

All scripts use generic `memory_backend` and `canonical_memory` fields.
No single backend is mandatory. Supported values:

```
memory_backend: notion | mem0 | git | registry | local | other
shared_pack_backend: git | notion | registry | local | other
canonical_memory: Notion + Mem0 | Git | Manual artifact input
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

---

## Files

```
YOS/
├── scripts/                          ← 12 Phase 1 scripts
│   ├── routing_matrix_loader.py
│   ├── continuity_mode_resolver.py
│   ├── context_boundary_detector.py
│   ├── pack_staleness_detector.py
│   ├── context_pack_checksum_verifier.py
│   ├── cap_validator.py
│   ├── context_pack_generator.py
│   ├── pack_command.py
│   ├── handoff_packet_builder.py
│   ├── enforcement_checker.py
│   ├── drift_detector.py
│   ├── pack_preview.py
│   └── pack_version_tracker.py
├── core/orchestration/
│   ├── continuity/                   ← 5 canonical doctrine files
│   ├── registries/
│   │   └── LLM_AND_TOOL_ROUTING_MATRIX.md
│   ├── context_packs/                ← Generated packs + registry
│   │   ├── pack_registry.json
│   │   └── history/
│   └── reports/                      ← Phase reports
└── docs/
    └── CONTINUITY_PHASE1_USAGE.md    ← This file
```
