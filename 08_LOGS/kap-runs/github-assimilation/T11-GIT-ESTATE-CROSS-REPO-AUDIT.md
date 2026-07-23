# T11 — Complete Git Estate and Cross-Repository Lineage Audit

**Run:** `KAP-GITHUB-ASSIMILATION-2026-07-23`  
**Track:** T11  
**Status:** ESTATE CENSUS COMPLETE — CROSS-REPO DEEP AUDIT STARTED  
**Development:** FROZEN

## Expanded scope

The assimilation scope is no longer limited to the `yj000018/YOS` monorepo.

It now includes:

- every repository owned by `yj000018`;
- archived repositories;
- private repositories;
- default branches;
- non-default branches;
- open and draft pull requests;
- original standalone deployment repositories;
- copies inside the YOS monorepo;
- runtime-local or externally deployed descendants referenced by Git.

## Estate census

GitHub currently exposes **40 owned repositories** for this account.

No collaborator-only or organization-member repositories were returned by the connector during this census.

The estate includes:

- YOS core and control-plane repositories;
- KAP and MPM repositories;
- Manus interfaces and skills;
- memory, continuity and routing systems;
- voice and visual interfaces;
- knowledge vaults and ontologies;
- products and prototypes;
- migration buffers;
- archived standalone repositories that still act as update/deployment origins.

A machine-readable first census is stored in:

`08_LOGS/kap-runs/github-assimilation/GIT-ESTATE-MASTER-REGISTRY.json`

## Existing cartography recovered — do not reinvent

A pre-existing repository registry was discovered in:

- `yj000018/yos-cognitive-os/05_Registries/REPO-REGISTRY.md`
- `yj000018/yos-cognitive-os/07_AI_Indexes/repo_index.json`

This registry already describes most of the estate and explicitly encodes the doctrine **Reuse Before Rebuild**.

### Value

It provides:

- repository IDs;
- domain and role assignments;
- authority levels;
- status labels;
- agent navigation notes;
- a machine-readable subset.

### Staleness and gaps

The registry was last updated on 2026-07-03 and requires reconciliation.

It omits at least these currently owned repositories:

1. `kap-control-plane`
2. `new-to-be-merged`
3. `eya-autolive2d-demo`

It also marks repositories as `ACTIVE` that GitHub now reports as archived, including multiple standalone YOS sources and product prototypes.

The JSON index is only a high-authority subset; it is not a complete 40-repository inventory.

**Disposition:** KEEP and ingest as prior cartography; do not replace it blindly. Reconcile it into the estate registry with provenance.

## Competing authority claims discovered

### `yos-cognitive-os`

Its README declares itself the **Master Control Plane for the Y-OS cognitive architecture** and states that KAP is a module inside YOS.

Its repository registry identifies:

- `yos-cognitive-os` as the primary master repo;
- `KAP` as a high-authority module repo;
- `YOS` as a legacy core to be migrated or linked.

### `YOS`

The current monorepo contains the newer canonical topology work, backbone modules, governance, migration reports and the active assimilation branch.

### `kap-control-plane`

Its README explicitly says it is a draft-candidate control-plane repository, not source corpus and not automatically canonical. It also states that MPM's final conceptual home is the YOS backbone.

### Conclusion

There is a real historical authority transition that has not yet been formally reconciled:

```text
yos-cognitive-os master-control-plane model
        ↓
kap-control-plane bootstrap/runtime contributions
        ↓
YOS canonical monorepo reorganization and backbone build
```

No repository should be declared obsolete until this transition is proven file-by-file and decision-by-decision.

## Open branches and PRs are part of the source estate

Default-branch inventory alone is insufficient.

### KAP PR #1 — Y-PIE

Draft PR `agent/y-pie-canon-foundation` contains 30 changed files and 30 commits defining:

- Y-PIE visual cognition;
- visual ontology;
- Visual Knowledge Graph;
- Visual DNA;
- KAP publication contracts;
- cognitive layer boundaries;
- runtime/deployment topology;
- roadmap and governance.

This corpus is not on KAP `main` and must be included in project and Ariane/Y-PIE lineage analysis.

### yos-bus PRs #1–#6

Six open architecture PRs contain substantial unmerged YOS design work:

1. 13-layer Architecture Bible, Constitution, ontology, object model, KRE and registries;
2. REP reporting/execution pulse;
3. YOS Meta-Model;
4. KAP architecture;
5. Cognitive Lifecycle;
6. Living Backbone, Chronicles and Architectural Discoveries.

PR #1 alone changes approximately sixty files across architecture, constitution, ADRs, schemas, registries, context packs, reviews and protocols.

These branches may contain concepts not present in either `yos-bus/main` or the current YOS monorepo.

### new-to-be-merged PR #1

Draft PR `agent/coc-map-contract` adds the Mission-Adaptive Parallelism contract on top of another non-default bootstrap branch.

**Rule:** branch and PR census is mandatory for every repository before its lineage can be closed.

## Exact standalone-to-monorepo duplicates confirmed

The following representative files have identical Git blob SHAs in their standalone repository and YOS monorepo copy:

| Standalone source | YOS monorepo copy | SHA status |
|---|---|---|
| `yos-manus-client/yos-manus-client.user.js` | `yos-agents/manus/yos-manus-client/yos-manus-client.user.js` | EXACT |
| `manus-enhancer/manus-enhancer.user.js` | `yos-agents/manus/manus-enhancer/manus-enhancer.user.js` | EXACT |
| `yos-cockpit/shared/yos-core.js` | `yos-automations/scripts/yos-cockpit/shared/yos-core.js` | EXACT |
| `yos-scripts/docs/YOS-MEMORY-BRIDGE-ARCHITECTURE.md` | `yos-automations/scripts/yos-scripts/docs/YOS-MEMORY-BRIDGE-ARCHITECTURE.md` | EXACT |
| `yos-llm-pipeline/llm_distillation_pipeline.py` | `yos-automations/scripts/yos-llm-pipeline/llm_distillation_pipeline.py` | EXACT |
| `y-menu/README.md` | `yos-apps/y-family/y-menu/README.md` | EXACT |
| `Y-WORLD/01_Cockpit/Y-WORLD Command Center.md` | `yos-vault/knowledge/Y-WORLD/01_Cockpit/Y-WORLD Command Center.md` | EXACT |
| `yos-skills/README.md` | `yos-agents/manus/yos-skills/README.md` | EXACT |
| `yos-userscripts/scripts/yos-panel.user.js` | `yos-automations/scripts/yos-userscripts/scripts/yos-panel.user.js` | EXACT |

These exact matches prove that substantial standalone repositories were copied into YOS without transformation.

They do **not** yet prove that every file or branch was copied, nor that YOS is the deployed runtime source.

## Non-duplicate and unique candidates

### yos-bus

`yos-bus/main/README.md` and `YOS/01_BACKBONE/BUS/README.md` are not identical and describe different architectural generations.

The standalone repository also contains major unmerged architecture branches.

**Disposition:** DEEP COMPARE; do not classify as superseded.

### yos-continuity-protocol

This repository declares a canonical portable Continuity Protocol with Manus and ChatGPT wrappers and a strict boundary between CP and the future Context Synthesis Engine.

No matching Continuity Protocol corpus was located in the YOS monorepo during this pass.

**Disposition:** UNIQUE HIGH-PRIORITY SOURCE CANDIDATE.

### yos-voice-gateway

This large active private repository contains a Voice UX Intelligence Layer, Car Mode PWA, canonical spoken/full response contract, voice navigation state and Canvas surface.

No matching implementation was located in YOS during this pass.

**Disposition:** UNIQUE HIGH-PRIORITY INTERFACE/RUNTIME SOURCE CANDIDATE.

### KAP Y-PIE branch

The Y-PIE draft contains a complete visual cognition architecture and may intersect strongly with Ariane — Visual Memory Studio.

**Disposition:** CROSS-PROJECT LINEAGE REVIEW REQUIRED; do not rebuild visual cognition concepts before comparison.

### new-to-be-merged

The artifact registry contains durable packages including:

- The Making of yOS seed;
- artifact-preservation doctrine;
- KAP resumption audit;
- continuity/context package;
- project genealogy;
- buffer review reports;
- superseded MPM staging evidence.

**Disposition:** SOURCE BUFFER TO ASSIMILATE, not disposable migration scaffolding.

## Revised no-rebuild/no-remigration gate

Before any new implementation or migration, the responsible agent must answer:

1. Does the capability already exist in any of the 40 repositories?
2. Does it exist on a non-default branch or open PR?
3. Is there an exact or near-exact copy inside YOS?
4. Which copy has the newest meaningful commit?
5. Which copy is used by deployed update URLs, loaders or runtimes?
6. Does the standalone repo contain unique history, issues, releases or branches?
7. Is the YOS copy complete or only a snapshot?
8. Has a KEEP / MERGE / REFERENCE / SUPERSEDE decision been recorded?

Until all eight are answered, the asset is not safe to recreate, copy again, archive or delete.

## Parallel audit lanes

The 40 repositories will now be processed in parallel conceptual lanes:

| Lane | Scope |
|---|---|
| E1 | Core architecture: YOS, yos-cognitive-os, yos-bus, KAP, kap-control-plane |
| E2 | Manus/Shell/interfaces: manus-enhancer, yos-manus-client, yos-cockpit, y-menu, userscripts |
| E3 | Memory/continuity/knowledge: Y-WORLD, yos-continuity-protocol, pipelines, scripts, skills |
| E4 | Voice/vision/runtime: yos-voice-gateway, yos-voice-vision, Y-PIE branches |
| E5 | Products/prototypes: CasaTAO, Daylog, YOUniverse, EIA, future-news, Remotion, Pulse |
| E6 | Civilizational/Œuvre: ELYSIUM, civilizational-awakening, one-galaxy and related works |
| E7 | Buffers/unknowns: new-to-be-merged, YMap, Y-Browser-Admin, empty repositories |
| E8 | Deployment and security provenance across all repositories |

## Completion condition

The Git estate audit is complete only when every repository has:

- metadata profile;
- complete tree inventory;
- branch and PR inventory;
- significant-content summary;
- YOS overlap comparison;
- duplicate fingerprints;
- deployment-source status;
- secrets/security status;
- lineage decision;
- canonical destination or explicit standalone role.
