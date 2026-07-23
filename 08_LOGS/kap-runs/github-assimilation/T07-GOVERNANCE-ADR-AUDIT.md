# T07 — Governance and ADR Deep Audit

**Run:** `KAP-GITHUB-ASSIMILATION-2026-07-23`  
**Track:** T07  
**Status:** FIRST DEEP PASS COMPLETE — MANUS ROLE CLARIFIED  
**Scope:** `00_META/`, `01_BACKBONE/GOVERNANCE/`, legacy `yos-governance/`, and Architecture Baseline v0.5 PR

## Executive conclusion

The governance layer contains a valid historical foundation, but it is not currently synchronized with the implemented backbone or the operator's current execution policy.

The five original ADRs must be preserved as historical accepted decisions. They must not be silently rewritten. Several require clarification or amendment through new ADRs.

A key clarification from the Architect:

> Manus remains the essential and primary YOS engine: the principal dialog interface, augmented by the YOS Shell, and the general orchestration environment.

This architectural role must be distinguished from a temporary credit-conservation policy during source assimilation. ChatGPT and direct connectors should perform work that can be completed efficiently here, while Manus credits are reserved for work that benefits from Manus execution capabilities. This is an operational optimization, not a demotion of Manus in the YOS architecture.

## Evidence reviewed

- `00_META/YOS-CONSTITUTION.md`
- `00_META/YOS-MODULE-REGISTRY.md`
- `00_META/YOS-REPO-MAP.md`
- `00_META/YOS-SOURCE-OF-TRUTH.md`
- `01_BACKBONE/GOVERNANCE/Decisions/ADR-001..005`
- `01_BACKBONE/GOVERNANCE/Manifest/policy-manifest.json`
- `01_BACKBONE/AGENTS/`
- `01_BACKBONE/BUS/`
- `01_BACKBONE/YARP/`
- PR #2: `agent/yos-baseline-v0.5`
- Architect clarification, 2026-07-23: Manus is the primary dialog and general orchestration engine

## ADR disposition

| ADR | Historical decision | Current assessment | Disposition |
|---|---|---|---|
| ADR-001 | Git as source of truth | Valid for durable code, architecture, ADRs and artifacts; too broad if interpreted as the only authority for runtime state, raw evidence or canonical semantic knowledge | KEEP + AMEND BY DOMAIN-SPECIFIC SOT ADR |
| ADR-002 | Obsidian as human cognitive interface | Valid as designated local Markdown/knowledge interface; does not make Obsidian the primary dialog or orchestration UI | KEEP + CLARIFY |
| ADR-003 | Local-first, GitHub API fallback | Still valid as an execution-path principle when a local runtime exists | KEEP |
| ADR-004 | Monorepo as initial architecture | Valid and substantially executed; the topology shown inside the ADR is the legacy pre-canonical topology | KEEP + MARK TOPOLOGY HISTORICAL |
| ADR-005 | Manus primary, Claude fallback | The central premise remains valid: Manus is the primary YOS dialog and general orchestration environment. The fallback and credit-use rules need refinement, not supersession | KEEP + CLARIFY RESOURCE-AWARE EXECUTION |

## Critical governance drift

### G-001 — Canonical module registry is stale

`00_META/YOS-MODULE-REGISTRY.md` still describes:

- BUS as a placeholder although an active BUS implementation exists;
- ART and CRT as standalone placeholder backbone folders;
- legacy ROUTING as a first-class module;
- no AGENTS module;
- no YARP module.

Implemented evidence now supports the peer backbone set:

```text
KAP · MPM · YARP · AGENTS · BUS · GOVERNANCE
```

ART and CRT are currently implemented/documented as routing domains under `01_BACKBONE/AGENTS/04_ROUTING/`, pending final reconciliation with the broader Baseline v0.5 control-plane model.

**Severity:** CRITICAL  
**Action:** Replace registry only after the archaeology and boundary reconciliation tracks complete. Do not patch prematurely.

### G-002 — Repo map contains incorrect semantics

The current map expands:

- ART as “Autonomous Reasoning Threads”;
- CRT as “Continuity & Recovery Threads”.

Current Y-OS architecture evidence instead uses:

- ART — Agent & Resource Routing Table;
- CRT — Cognitive Routing Table.

It also lists BUS as a placeholder and omits YARP and AGENTS.

**Severity:** CRITICAL  
**Action:** Treat `00_META/YOS-REPO-MAP.md` v1.0.0 as historical migration-era documentation until regenerated from the final JSON registry.

### G-003 — Constitution ownership table predates AGENTS and YARP

The Constitution names MPM and KAP as backbone modules but assigns agents only to `02_AGENTS/`. This predates the creation of the first-class `01_BACKBONE/AGENTS/` identity/capability/trust/routing module and `01_BACKBONE/YARP/`.

**Severity:** HIGH  
**Action:** Constitutional amendment required after module-boundary review.

### G-004 — Manus role needs two-layer clarification

`policy-manifest.json` assigns Manus “primary execution and orchestration”. The architectural direction remains correct but must be expressed more precisely:

```text
Manus = primary YOS experience environment
      + primary augmented dialog interface
      + general orchestration engine

YOS Shell = augmentation layer around Manus

YOS Core / Y-Nexus / Y-ORC / MPM / ART / CRT / KAP / BUS / YARP
          = sovereign system services and protocols used through or beyond Manus
```

Operational resource selection is a separate concern. During the GitHub assimilation wave:

- direct GitHub/Notion/file work should be executed from ChatGPT when equivalent;
- Manus credits should be conserved for Manus-specific execution or when its orchestration environment adds material value;
- this does not change Manus's primary architectural position.

**Severity:** HIGH  
**Action:** Preserve ADR-005. Add a clarification ADR separating architectural primacy from task-level resource selection.

### G-005 — Source-of-truth doctrine needs domain separation

The old absolute rule “all content must ultimately live in Git” conflicts with the newer and stronger domain model:

- Git: durable implementation and versioned artifact truth;
- ARCH: immutable raw evidence;
- KAP: provenance-backed canonical structured knowledge;
- Obsidian: local human knowledge interface;
- Notion: operational workspace/staging until deliberately migrated;
- runtime DB/state store: ephemeral job/runtime state;
- dedicated secret manager: secrets.

**Severity:** HIGH  
**Action:** Promote a domain-specific Source-of-Truth Matrix via ADR; do not erase ADR-001.

## Baseline v0.5 status

PR #2 is a useful top-down investigation framework, not yet merge-ready canon.

Positive:

- explicit status vocabulary;
- no-invention rule;
- module boundaries and lineage hypotheses;
- implementation evidence matrix;
- source-wave roadmap;
- domain-specific source-of-truth matrix;
- recognition of Manus as the current preferred human cockpit and program-direction environment.

Required before promotion:

1. complete repository archaeology;
2. reconcile Y-Nexus/Y-ORC/ART/CRT with implemented AGENTS/YARP/BUS/MPM structures;
3. verify implementation claims against code and logs;
4. resolve overlap with current constitutional files;
5. decide whether Baseline documents remain under legacy `yos-governance/` or move to canonical governance paths;
6. encode the Manus/YOS Shell/YOS Core relationship without reducing Manus to a replaceable adapter.

## Proposed ADR queue — not yet adopted

| Candidate | Purpose |
|---|---|
| ADR-006 | Domain-specific sources of truth |
| ADR-007 | Manus as primary augmented dialog and general orchestration engine; resource-aware task execution |
| ADR-008 | Canonical peer backbone modules and module-boundary model |
| ADR-009 | YOS Shell as the augmentation layer around Manus native experience |
| ADR-010 | Legacy-to-canonical path lifecycle and deletion criteria |

## Keep / merge / archive recommendation

| Object | Recommendation |
|---|---|
| Original ADR-001..005 | KEEP immutable as historical decisions |
| `policy-manifest.json` v1.0.0 | KEEP; clarify rather than invalidate Manus primacy |
| `00_META` v1.0 docs | KEEP as migration-era versions; regenerate rather than hand-edit piecemeal |
| PR #2 Baseline v0.5 | KEEP OPEN/DRAFT during archaeology; do not merge yet |
| duplicate legacy `yos-governance/` copies | MERGE lineage, then archive only after hash/provenance verification |

## Track completion state

This track is not globally complete until:

- every governance file is hash-compared between legacy and canonical paths;
- PR #2 claims are mapped to implementation evidence;
- proposed ADRs are approved or rejected;
- JSON registry and generated Markdown views are regenerated consistently;
- Manus architectural primacy and resource-aware execution are formally separated in governance.
