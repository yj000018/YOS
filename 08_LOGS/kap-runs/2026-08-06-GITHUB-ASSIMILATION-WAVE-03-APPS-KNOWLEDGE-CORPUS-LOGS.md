# GitHub Assimilation — Wave 03: Apps, Knowledge Domains, Source Corpus and Logs

**Run:** `KAP-GITHUB-ASSIMILATION-2026-07-23`  
**Wave date:** 2026-08-06  
**Repository:** `yj000018/YOS`  
**Status:** FIRST PASS COMPLETE — deep semantic assimilation remains open  
**Doctrine:** Assimilate before building.

## 1. Scope

This wave inspected the current top-level structure of:

- `06_APPS_PRODUCTS/`
- `05_KNOWLEDGE_DOMAINS/`
- `07_SOURCE_CORPUS/`
- `08_LOGS/`
- the current recursive repository tree and root topology.

The goal was to determine whether the canonical destinations contain substantive migrated assets, placeholders, or mixed states. No file was moved, deleted, canonicalized or rewritten.

## 2. Repository-level finding

The current root is not the simple topology described by the older June/July README and meta maps. It now contains both canonical layers and additional roots, including:

```text
00_META
01_BACKBONE
02_AGENTS
03_AUTOMATIONS
04_INTERFACES
05_AUTOMATION
05_KNOWLEDGE_DOMAINS
06_APPS_PRODUCTS
07_SOURCE_CORPUS
08_LOGS
99_ARCHIVE
CANON
AGENTS.md
```

This proves that the repository is in a mixed migration state. The singular `05_AUTOMATION` root coexists with `03_AUTOMATIONS`; `CANON` coexists with the meta/governance architecture; and multiple canonical destinations contain placeholders while implementations remain elsewhere.

## 3. Apps and products

The canonical `06_APPS_PRODUCTS/` root currently exposes:

- `chroniques/`
- `daylog/`
- `prototypes/`
- `tool_registry/`
- `y-family/`
- `yos-client/`
- `youniverse/`
- `yos-bootstrap-skill.md`

Several directories share the same empty-tree hash, indicating placeholder directories rather than migrated implementations. `chroniques`, `tool_registry` and `yos-client` have distinct trees and require deep inspection. Therefore:

- canonical path existence is not evidence of completed app migration;
- the legacy `yos-apps/` and `yos-related/experiments/` corpus remains necessary source evidence;
- each application needs a Project/App Fact Sheet with lineage, implementation location and current runtime status.

**Track T11:** `FIRST_PASS_COMPLETE_PENDING_DEEP_APP_CENSUS`.

## 4. Knowledge domains

The canonical `05_KNOWLEDGE_DOMAINS/` root contains named domain directories for CasaTAO, ELYSIUM, KOSMOS, Works, Y-WORLD and YOUniverse, but all inspected domain directories resolve to the same empty-tree hash.

This is strong evidence that the intended semantic topology was scaffolded but that the substantive Y-WORLD corpus was not migrated into these canonical destinations. The actual knowledge content remains primarily in legacy `yos-vault/knowledge/Y-WORLD/`, archived repositories, Notion and external/local vaults.

Consequences:

- do not treat `05_KNOWLEDGE_DOMAINS/*` as populated knowledge bases;
- retain the existing Y-WORLD metadata census and legacy vault as source evidence;
- perform a note-level semantic assimilation before any migration or deletion;
- distinguish `CANON`, knowledge domains, source corpus and generated views explicitly.

**Track T12:** `FIRST_PASS_COMPLETE_PENDING_NOTE_LEVEL_ASSIMILATION`.

## 5. Source corpus

`07_SOURCE_CORPUS/` is partly operational and partly scaffolded.

Substantive roots observed:

- `RAINDROP/`
- `chatgpt/`

Placeholder or empty roots observed:

- `fingerprints/`
- `imports/`
- `inventories/`
- `quarantine/`
- `source-maps/`

This means the source-corpus architecture exists, but its expected KAP support directories are not consistently populated. Existing source registries under `01_BACKBONE/KAP/04_REGISTRIES/` contain more historical metadata than these top-level folders.

Required reconciliation:

1. register the current YOS monorepo as a source instance;
2. map `07_SOURCE_CORPUS/chatgpt` and `RAINDROP` to source-channel/instance/object registries;
3. determine whether fingerprints, inventories and source maps exist elsewhere before declaring absence;
4. preserve raw exports separately from synthesized knowledge.

## 6. Logs

`08_LOGS/` is also mixed.

Substantive roots observed:

- `kap-runs/`
- `migrations/`
- `mpm-reports/`
- `raindrop-bookmarks/`
- `session-ledger/`

Placeholder roots observed:

- `agent-runs/`
- `decisions/`
- `errors/`
- `execution/`

The current KAP assimilation tracker and wave reports are durable and remotely available in `kap-runs`. However, empty operational log directories show that the proposed logging ontology has not been uniformly adopted.

Required reconciliation:

- define which ledgers are canonical by object type;
- map MPM, BUS, KAP, session and execution evidence without duplication;
- avoid inferring that an empty canonical directory means no historical evidence exists;
- identify reports stored inside module-local folders versus global logs.

**Track T13:** `FIRST_PASS_COMPLETE_PENDING_LEDGER_RECONCILIATION`.

## 7. Confirmed cross-cutting findings

### AKCL-001 — Canonical topology is scaffolded unevenly

The repository contains a mixture of substantive canonical modules, empty intended destinations and legacy implementation roots.

### AKCL-002 — Path presence is not migration proof

Multiple named app and knowledge directories are empty placeholders. Migration status must be evidence-backed at file level.

### AKCL-003 — Knowledge content remains outside canonical domain roots

The actual Y-WORLD content remains in the legacy vault and external sources; canonical knowledge-domain directories are not populated.

### AKCL-004 — Source and log registries are more mature than their folder projections

KAP registries record many source objects and prior metadata scans even when the corresponding top-level operational folders are empty.

### AKCL-005 — Root topology has unresolved collisions

`03_AUTOMATIONS` versus `05_AUTOMATION`, and `CANON` versus other governance/knowledge roots, require explicit lineage and authority decisions.

## 8. Classification decisions

| Asset/family | Preliminary classification | Decision |
|---|---|---|
| `06_APPS_PRODUCTS` named empty trees | canonical scaffolds | KEEP; do not claim migration complete |
| substantive app trees | candidate implementations | DEEP AUDIT + FACT SHEETS |
| `05_KNOWLEDGE_DOMAINS/*` empty roots | semantic scaffolds | KEEP; populate only after KAP reconciliation |
| legacy Y-WORLD vault | primary source evidence | PRESERVE + ASSIMILATE |
| `07_SOURCE_CORPUS/chatgpt`, `RAINDROP` | active raw-source collections | REGISTER + AUDIT |
| empty source-corpus folders | intended KAP structure | KEEP; locate external equivalents |
| populated global log roots | durable evidence | INVENTORY + CROSSWALK |
| empty global log roots | unimplemented projections | KEEP; no absence inference |
| `05_AUTOMATION` | topology anomaly | INVESTIGATE |
| `CANON` | possible authority root | DEEP AUDIT before source-of-truth changes |

## 9. Coverage statement

This wave completes structural first-pass coverage of all major top-level YOS domains. It does **not** complete semantic, file-by-file assimilation of the repository.

A truthful state is:

```yaml
top_level_structural_coverage: COMPLETE
family_level_semantic_coverage: PARTIAL
file_level_semantic_coverage: INCOMPLETE
canonical_reconciliation: INCOMPLETE
global_github_assimilation: IN_PROGRESS
```

## 10. Remaining gates

1. Deep app/prototype census with one fact sheet per substantive project.
2. Note-level Y-WORLD semantic assimilation and duplicate detection.
3. Source-corpus object registration and lineage.
4. Ledger/log crosswalk.
5. Full duplicate and contradiction reconciliation.
6. Regenerated canonical module/topology registry.
7. Final residual-unknown proof.

No claim of 100% assimilation is justified until these gates pass.
