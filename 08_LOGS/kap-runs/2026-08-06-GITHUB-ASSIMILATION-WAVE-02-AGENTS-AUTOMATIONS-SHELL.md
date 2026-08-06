# GitHub Assimilation — Wave 02: Legacy Agents, Automations and YOS Shell

**Run:** KAP-GITHUB-ASSIMILATION-2026-07-23  
**Wave date:** 2026-08-06  
**Repository:** `yj000018/YOS`  
**Status:** FIRST PASS COMPLETE — deep audit still required  
**Doctrine:** Assimilate before building.

## 1. Scope

This wave established the first evidence-backed inventory and lineage for three parallel tracks:

1. legacy `yos-agents/` assets and Manus skills;
2. `yos-automations/`, including scripts, userscripts, cockpit and LLM pipeline;
3. the YOS visual Shell layered over Manus.

No code was rewritten and no legacy asset was deleted or moved.

## 2. Legacy Manus agent assets

The current legacy Manus subtree contains three major families:

```text
yos-agents/manus/
├── manus-enhancer/
├── yos-manus-client/
└── yos-skills/
```

### 2.1 Manus skills registry

The `.skill_versions.json` registry records 35 named Manus skills with provider/version identifiers. The set includes memory, session continuity, project hydration, routing, development, artifact generation, file organization and task management capabilities.

Confirmed examples:

- `memoriser`
- `hydrater`
- `memory-manager`
- `memory-pipeline`
- `session-synthesis`
- `session-synthesizer`
- `session-navigator`
- `project-hydration`
- `project-synthesis`
- `llm-router`
- `yos-mmm`
- `manus-api`
- `dev`
- `task-manager`
- `status`
- `summary`

### 2.2 Registry inconsistency

The skills README documents only seven skills, while the machine registry contains 35. Therefore the README is a stale partial view, not a complete inventory.

### 2.3 Classification

| Asset family | Current meaning | Preliminary decision |
|---|---|---|
| Manus-specific skill instructions | Provider adapter / executable skill definitions | KEEP as source evidence; later map to provider-neutral capabilities and workflows |
| `.skill_versions.json` | Deployed Manus skill-instance registry | KEEP; classify as provider-specific deployment registry, not universal YOS registry |
| Skills README | Partial human view | REGENERATE after full census |
| Duplicate skill names (`session-synthesis` / `session-synthesizer`, memory variants) | Possible generations or overlapping roles | RECONCILE lineage before merge |

## 3. Automations

The legacy automation tree currently exposes:

```text
yos-automations/
├── n8n/
├── playbooks/
└── scripts/
    ├── yos-cockpit/
    ├── yos-llm-pipeline/
    ├── yos-scripts/
    └── yos-userscripts/
```

The top-level `n8n/` and `playbooks/` directories currently resolve to empty-tree hashes in the directory listing, while the meaningful implementation corpus is concentrated under `scripts/`.

### 3.1 Preliminary semantic roles

| Folder | Role |
|---|---|
| `yos-cockpit` | Browser extension, mobile userscript and shared cockpit logic |
| `yos-userscripts` | Tampermonkey/Gear userscript collection |
| `yos-scripts` | Operational YOS scripts and service utilities |
| `yos-llm-pipeline` | Historical LLM knowledge-distillation / knowledge-OS pipeline |

### 3.2 Preliminary findings

- The automation layer contains both runtime code and architectural experiments.
- Several assets overlap with `yos-agents/manus/manus-enhancer` and `yos-manus-client`.
- `yos-cockpit` is not merely an automation; it is also a human interface implementation and should ultimately be represented in the Shell lineage, with executable helpers remaining under Automations.
- Empty or placeholder canonical directories must not be mistaken for completed migration.

## 4. YOS Shell lineage

### 4.1 Implemented branches

`yos-manus-client` already implements:

- Manus UI cleanup;
- YOS branding;
- project colors;
- project/session navigator;
- prompt injection;
- message toolbars;
- Markdown export;
- keyboard shortcuts;
- local cache and fetch interception.

`manus-enhancer` / `yos-cockpit` defines a larger two-client architecture:

- desktop browser extension;
- Chrome/Brave Side Panel;
- shared core;
- mobile Tampermonkey client;
- Smart, Actions, Navigation and Settings panels;
- n8n webhook integration.

### 4.2 Architectural synthesis

The evidence supports this lineage:

```text
YOS Manus client
  → UI cleanup, branding and navigation
  → Manus enhancer
  → shared core + desktop Side Panel + mobile userscript
  → YOS Cockpit
  → future unified YOS Shell
```

Y-Menu, Command Center and Navigator are not separate replacement applications. They are semantic/routing/view capabilities that should later be integrated into the unified Shell after source reconciliation.

### 4.3 Correct target boundary

```text
YOS Shell
  displays · launches · injects · opens · reports state

YOS Core
  owns registries · workflows · routing · memory · context · policies · provenance

Manus
  supplies current human interface and execution substrate
```

No business logic should be embedded permanently in DOM selectors or Tampermonkey code.

## 5. Confirmed issues

### AAS-001 — Multiple overlapping client implementations

At least `yos-manus-client`, `manus-enhancer`, and `yos-cockpit` overlap. They require a file-level comparison and lineage map before any rewrite.

### AAS-002 — Provider-specific skill corpus is richer than documentation

The deployed-skill registry contains five times more skills than the README documents. A complete skill fact sheet census is required.

### AAS-003 — Universal versus Manus-specific logic is mixed

Some skills encode universal YOS workflows; others are purely Manus adapters. They must be separated conceptually before migration.

### AAS-004 — Canonical path migration remains incomplete

Legacy folders remain the substantive implementation locations, while several canonical destinations are placeholders or partial copies.

### AAS-005 — Empty n8n/playbook roots do not prove absence

The current monorepo locations appear empty, but related workflow logic may remain in scripts, bootstrap repos, Notion, Manus filesystems or exports. Mark as `NOT_RECOVERED_HERE`, not `NEVER_EXISTED`.

## 6. Required next probes

1. Enumerate every Manus skill and produce one row per skill: purpose, inputs, outputs, dependencies, universal/provider-specific classification, overlap and status.
2. Compare file trees and hashes across `yos-manus-client`, `manus-enhancer` and `yos-cockpit`.
3. Inventory every userscript and operational script.
4. Deep-read `yos-llm-pipeline` and map it against current KAP, MPM, MCE and context-continuity concepts.
5. Search bootstrap repositories and archives for missing n8n workflows and playbooks.
6. Locate voice, dashboard and Light Client implementations across Apps, Automations and Y-WORLD.

## 7. Track status

- `T08 Legacy agents and Manus skills` → `FIRST_PASS_COMPLETE`
- `T09 Automations, scripts, n8n and userscripts` → `FIRST_PASS_COMPLETE`
- `T10 Interfaces and YOS Shell lineage` → `FIRST_PASS_COMPLETE`

These tracks are understood at family level but are not yet deeply assimilated file by file.
