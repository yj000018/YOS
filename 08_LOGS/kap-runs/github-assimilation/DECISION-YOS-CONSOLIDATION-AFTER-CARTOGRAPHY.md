# Decision — Consolidate all YOS-specific assets into YOS after full cartography

**Run:** `KAP-GITHUB-ASSIMILATION-2026-07-23`  
**Status:** ARCHITECT DECISION RECORDED  
**Execution:** DEFERRED UNTIL CARTOGRAPHY IS COMPLETE  
**Development:** FROZEN

## Decision

After the complete Git estate cartography and lineage audit are finished:

> All assets that are genuinely part of YOS must be consolidated into the `yj000018/YOS` repository.

This includes YOS-specific:

- architecture;
- governance;
- protocols;
- backbone modules;
- registries;
- agents and Manus skills;
- automations and scripts;
- interfaces and Shell components;
- memory and continuity mechanisms;
- runtime contracts;
- documentation, decisions and historical lineage required to understand the system.

## Purpose

The consolidation has two primary goals:

1. prevent YOS capabilities from remaining fragmented across many standalone repositories;
2. prevent future agents from rebuilding, remigrating or recopying assets that already exist elsewhere in Git.

## Required sequence

```text
1. Complete estate census
2. Inventory every repository, branch and PR
3. Compare standalone sources with YOS copies
4. Identify unique, newer and deployed variants
5. Decide canonical form and destination
6. Import or reconcile missing YOS content
7. Verify completeness and runtime provenance
8. Archive redundant standalone repositories only after verification
```

No deletion, archival or repository shutdown is authorized before steps 1–7 are complete.

## Consolidation rules

### Rule 1 — YOS owns YOS

If an asset defines or implements YOS itself, its canonical maintained form must live in `yj000018/YOS`.

### Rule 2 — Preserve provenance

Every consolidation must retain:

- original repository;
- source path;
- source commit or branch;
- imported destination;
- transformation notes;
- duplicate/lineage decision;
- deployment source status.

### Rule 3 — Do not flatten blindly

Consolidation does not mean copying every file without review. Exact duplicates, stale snapshots, generated artifacts and superseded drafts must be identified before import.

### Rule 4 — Products may remain standalone

A product or deployable application may remain in its own repository when independent lifecycle, deployment, access control or release management justifies it.

However, its YOS-facing contracts, architectural position, capabilities, interfaces and canonical references must still be represented in YOS.

### Rule 5 — Archive only after proof

A standalone repository may be archived as redundant only when:

- all unique content has been preserved;
- branches and PRs have been audited;
- deployed update URLs have been redirected or intentionally retained;
- Git history has been referenced or preserved;
- the YOS destination has been verified complete;
- an explicit consolidation decision has been recorded.

## Expected final topology

```text
YOS
├── complete YOS architecture and governance
├── complete backbone and protocols
├── complete agent/skill/capability definitions
├── complete automation and interface sources
├── complete lineage and source maps
├── references/contracts for standalone products
└── archive pointers for superseded repositories

Standalone repositories
├── independent products and deployable runtimes where justified
└── archived historical sources after verified consolidation
```

## Completion criterion

The consolidation phase is complete when a new agent can inspect `yj000018/YOS` and determine:

- what YOS is;
- every canonical YOS component;
- what has already been implemented;
- where each component came from;
- which products remain external and why;
- which historical repositories were superseded;
- which repository or path is the maintained source for every YOS capability.
