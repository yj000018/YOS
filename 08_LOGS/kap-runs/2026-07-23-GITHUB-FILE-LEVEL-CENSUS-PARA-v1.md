# GitHub File-Level Census — PARA v1

**Run:** `KAP-GITHUB-FILE-CENSUS-2026-07-23`  
**Status:** `IN_PROGRESS`  
**Doctrine:** inventory and understand before reorganizing  
**Mutation policy:** source repositories remain read-only; only audit evidence may be written.

## Completion definition

A repository is not `EXHAUSTED` until repository metadata, all reachable refs, recursive trees, current blobs, relevant text, non-text metadata, PR-only content, issues, releases, workflows, exact duplicates, semantic roles, lineage, security flags and residual unknowns are recorded.

## PARA lanes

| Lane | Corpus | Repositories |
|---|---|---|
| A | Architecture / control plane | `YOS`, `KAP`, `kap-control-plane`, `yos-cognitive-os`, `yos-bus`, `new-to-be-merged`, `yos-continuity-protocol` |
| B | Shell / Manus / interfaces | `yos-manus-client`, `yos-cockpit`, `manus-enhancer`, `yos-userscripts`, `Y-Browser-Admin`, `y-menu`, `UniversalChatThemeCanon` |
| C | Skills / pipelines / voice | `yos-skills`, `yos-scripts`, `yos-llm-pipeline`, `yos-voice-gateway`, `yos-voice-vision`, `y-llm-exporter`, `relevance-ai-workforce` |
| D | Knowledge / YOUniverse | `Y-WORLD`, `youniverse`, `yannick`, `YMap`, `one-galaxy` |
| E | Products / prototypes | `casa-tao-nest`, `daylog`, `daylog-mvp`, `pulse-app`, `future-news-project`, `remotion-project` |
| F | ELYSIUM / awakening / creative | `civilizational-awakening`, `eia-awakening-petal`, `elysium-book`, `elysium-civilizational-ontology`, `eya-autolive2d-demo` |
| G | Empty / legacy / special | `desktop-tutorial`, `yos-governance`, `yos-project` |
| H | Cross-estate reconciliation | duplicates, lineage, security, LFS, submodules, PR-only content, coverage proof |

## Required machine outputs

- repository registry;
- branch and tag registry;
- recursive tree manifest per ref;
- blob and file manifest with Git SHA, size, mode and extension;
- text mirror in a protected evidence location;
- PR, issue, release, workflow and Actions artifact registries;
- exact-duplicate blob groups and normalized near-duplicate candidates;
- Git LFS pointer and submodule registries;
- error and inaccessible-object registry;
- semantic artifact registry and final disposition matrix.

## Security boundary

Raw content from private repositories must not be copied into the public `YOS` repository. The raw census and text mirror belong in a private evidence environment. Only sanitized manifests, fingerprints, provenance and approved canon material may be promoted to public YOS.

## Initial evidence

- The historical YOS inventory reports 940 files but classifies mostly top-level folders, not every current path.
- The July 5 reorganization added 134 files and explicitly deferred the vault, agents, apps and automations corpora.
- `yos-cockpit/README.md` and `manus-enhancer/README.md` share the same Git blob SHA, proving an exact cross-repository duplicate.
- README documents are navigation evidence, not substitutes for recursive API tree enumeration.

## Status

| Layer | Status |
|---|---|
| 40-repository metadata census | `COMPLETE` |
| PARA lane assignment | `COMPLETE` |
| Existing migration evidence | `INGESTED` |
| Private machine collector | `BUILDING` |
| Recursive tree extraction | `PENDING_COLLECTOR_RUN` |
| Text mirror | `PENDING_COLLECTOR_RUN` |
| PR / issue / release census | `PARTIAL` |
| Exact duplicate graph | `PARTIAL` |
| Semantic classification | `STARTED` |
| Reorganization | `FROZEN` |

GitHub can be marked `SOURCE_EXHAUSTED` only when every reachable object has an evidence record or an explicit recorded access failure.