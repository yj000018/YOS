# GitHub Assimilation — Wave 01: Governance and Canonical Topology

**Run:** KAP-GITHUB-ASSIMILATION-2026-07-23  
**Wave date:** 2026-08-06  
**Repository:** `yj000018/YOS`  
**Status:** COMPLETE — evidence-backed first deep audit  
**Doctrine:** Assimilate before building.

## 1. Scope

This wave audited the governance layer that currently defines Git, Obsidian, local/GitHub routing, monorepo structure, and default agent roles.

Sources inspected:

- `yos-governance/Decisions/ADR-001-Git-As-Source-Of-Truth.md`
- `yos-governance/Decisions/ADR-002-Obsidian-As-Human-Interface.md`
- `yos-governance/Decisions/ADR-003-Local-First-Git-Fallback.md`
- `yos-governance/Decisions/ADR-004-Monorepo-As-Initial-YOS-Architecture.md`
- `yos-governance/Decisions/ADR-005-Manus-Primary-Claude-Fallback.md`
- `yos-governance/Manifest/policy-manifest.json`
- `00_META/YOS-CONSTITUTION.md`
- `00_META/YOS-MODULE-REGISTRY.md`
- `00_META/YOS-REPO-MAP.md`
- `00_META/YOS-SOURCE-OF-TRUTH.md`
- `00_META/MIGRATION-INDEX.md`
- current Backbone documents for AGENTS, YARP, BUS, KAP and MPM.

## 2. Confirmed durable decisions

### G-001 — Git is the durable source of truth

The decision remains valid: important YOS content must ultimately be committed and pushed to Git. Git history is the durable conflict-resolution and audit layer.

### G-002 — Obsidian is a human cognitive interface, not the machine canon

The historical ADR establishes Obsidian/Y-WORLD as the human-facing linked-knowledge interface, while agents read structured content from Git. This remains directionally valid, but the timing of Obsidian as the primary human interface is no longer automatic; current consolidation policy places Git first and treats Obsidian attachment as a later integration step.

### G-003 — Local-first / GitHub fallback is an execution policy

The policy remains useful as an adapter/runtime decision, not as a universal architectural identity. Local execution is preferred when available; GitHub API remains a portable fallback.

### G-004 — The monorepo decision remains valid, but its documented topology is stale

ADR-004 describes the original seven-folder monorepo. The implemented repository has since evolved to `00_META`, `01_BACKBONE`, operational layers, source corpus, logs and archive. The ADR should remain as historical rationale and receive a superseding ADR or amendment rather than being silently edited.

### G-005 — Manus-primary / Claude-fallback is historical configuration, not permanent architecture

ADR-005 and `policy-manifest.json` encode a June 2026 execution configuration. The current architecture is orchestrator-agnostic: Manus may be the preferred current human interface and runtime, but routing is configuration owned by YOS via AGENTS/ART/CRT and related modules. This ADR must be marked `SUPERSEDED_IN_PART` or amended.

## 3. High-confidence contradictions and staleness

### C-001 — Old topology versus implemented Backbone

`YOS-MODULE-REGISTRY.md` and `YOS-REPO-MAP.md` omit implemented first-class Backbone modules such as AGENTS and YARP. They also represent ART and CRT as standalone Backbone placeholders, while the newer AGENTS module places them correctly under `01_BACKBONE/AGENTS/04_ROUTING/`.

**Decision:** the implemented AGENTS/YARP architecture is newer and more specific. The older meta maps are stale views and must not govern new development.

### C-002 — Markdown and JSON source-of-truth wording

The Constitution states `JSON = canonical machine source` and `Markdown = generated human-readable view`. Yet many valid architectural decisions exist only as Markdown ADRs and specifications. The current wording is too absolute.

**Required reconciliation:**

- machine registries, ledgers, indexes and runtime state: JSON canonical;
- constitutional doctrine, ADRs, specifications and human-authored architecture: versioned Markdown may be canonical;
- generated Markdown views must be explicitly marked generated;
- source authority is determined by object type and registry metadata, not file extension alone.

### C-003 — Agent role configuration drift

The policy manifest fixes ChatGPT/Manus/Claude roles, while AGENTS/ART/CRT now provide capability-, trust-, quality-, cost- and availability-based routing. Fixed roles are therefore bootstrap defaults, not immutable governance.

### C-004 — Git as durable memory versus fast transport

Historical wording that all agents must read/write Git should not imply Git is the live transport for every step. BUS correctly distinguishes direct runtime transport from durable Git persistence.

## 4. Classification decisions

| Asset | Classification | Decision |
|---|---|---|
| ADR-001 | durable doctrine | KEEP; clarify object-type source authority |
| ADR-002 | durable direction with timing caveat | KEEP; annotate current Git-first consolidation phase |
| ADR-003 | runtime policy | KEEP as policy, not constitutional architecture |
| ADR-004 | historical architecture decision | KEEP + SUPERSEDE with current canonical topology ADR |
| ADR-005 | historical routing configuration | SUPERSEDE_IN_PART |
| policy-manifest.json v1 | bootstrap machine config | KEEP as historical; replace with versioned routing policy sourced from AGENTS/ART/CRT |
| YOS-MODULE-REGISTRY v1 | stale registry view | PATCH/REGENERATE |
| YOS-REPO-MAP v1 | stale topology view | PATCH/REGENERATE |
| YOS-SOURCE-OF-TRUTH v1 | partially valid | PATCH terminology and current bootstrap status |
| MIGRATION-INDEX v1 | incomplete historical log | EXTEND; do not treat as current completion evidence |

## 5. Canonical architecture now evidenced

The current implemented Backbone is at least:

```text
YOS
├── KAP       knowledge assimilation
├── MPM       work orchestration and execution packages
├── YARP      transport-independent inter-agent message semantics
├── AGENTS    identities, capabilities, trust, ART and CRT routing
├── BUS       runtime transport and operational exchange
├── GOVERNANCE
├── MEMORY    still to reconcile deeply
├── SECURITY  still to reconcile deeply
└── additional modules pending complete census
```

This is evidence-based but not yet the final complete module map. ACT, Y-ORC, Y-CTX, CCR, SWARM and other newer concepts must be reconciled against all Git and historical sources before insertion into the canonical map.

## 6. No destructive changes authorized

This wave records findings only. It does not rewrite ADRs, delete legacy paths, move files, or claim final canonization.

## 7. Next wave

Proceed in parallel with:

1. legacy `yos-agents/` and Manus skills census;
2. automations/userscripts/n8n implementation audit;
3. interfaces and YOS Shell lineage;
4. canonical/legacy duplicate comparison;
5. apps/products/prototypes census.

## 8. Wave result

`T07 Governance and ADRs` can move from `PENDING_DEEP_AUDIT` to `DEEP_AUDIT_COMPLETE_PENDING_RECONCILIATION`.

The governance corpus is understood sufficiently to continue assimilation, but not yet sufficiently reconciled to patch the Constitution or regenerate the global module registry.
