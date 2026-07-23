# T09 — Automations, Scripts and Runtime Audit

**Run:** `KAP-GITHUB-ASSIMILATION-2026-07-23`  
**Track:** T09  
**Status:** FIRST DEEP PASS COMPLETE — SECURITY ACTION REQUIRED  
**Development:** FROZEN — inventory, evidence classification and remediation planning only

## Scope reviewed

- legacy `yos-automations/` tree;
- canonical `03_AUTOMATIONS/` assets discovered so far;
- cross-LLM memory push scripts;
- Memory Bridge architecture;
- LLM-to-Notion distillation pipeline;
- yOS global userscript/Life Panel;
- Components Registry proposal and implementation;
- notification module;
- Manus-linked scheduling and deployment claims.

## Automation families discovered

### A-01 — Cross-LLM memory push scripts

**Path:** `yos-automations/scripts/yos-scripts/`

Surfaces:

- shared parsing/push core;
- Tampermonkey/Gear script;
- Scriptable iOS Share Sheet script;
- loader-based auto-update path;
- Fly.io push webhook;
- Mem0 ingestion.

**Classification:** IMPLEMENTED ASSETS; DEPLOYMENT PROVENANCE EXTERNAL TO MONOREPO.

The monorepo documentation still points runtime updates to the original standalone `yos-scripts` repository. Therefore the monorepo copy cannot yet be declared the deployed source.

### A-02 — Y-OS Memory Bridge

**Document:** `yos-automations/scripts/yos-scripts/docs/YOS-MEMORY-BRIDGE-ARCHITECTURE.md`

Recovered architecture:

```text
iOS Share Sheet
  → stable Scriptable loader
  → GitHub Raw script update
  → local offline cache
  → Mem0 semantic extraction
  → optional Manus-hosted dashboard
```

Strengths:

- simple user interaction;
- offline cache fallback;
- multi-LLM parsing;
- automatic script delivery;
- clear operational ownership by Manus.

Drift/contradictions:

- one section says the Mem0 bearer token is stored in the script;
- a later security section says secrets are obtained through 1Password;
- URLs and deployment responsibility refer to standalone infrastructure and a Manus-hosted dashboard that have not been revalidated in this audit.

**Classification:** IMPLEMENTED HISTORICAL ARCHITECTURE; CURRENT OPERATIONAL STATUS UNVERIFIED.

### A-03 — LLM Knowledge Distillation Pipeline

**Path:** `yos-automations/scripts/yos-llm-pipeline/`

Implemented code includes:

- Notion session intake;
- LLM extraction;
- canonical-key generation;
- conservative merge thresholds;
- duplicate/extension/supersession/conflict handling;
- Active Context refresh;
- optional clusters;
- pipeline state updates;
- dry-run and force-all modes.

Configuration declares a daily 03:00 source sync and 05:00 pipeline run, with Notion databases for sessions, knowledge, clusters, Active Context and pipeline state.

**Classification:** IMPLEMENTED CODE, RUNNABILITY UNVERIFIED, OPERATIONAL STATUS UNVERIFIED.

#### Pipeline defects and risks

1. **Nested GitHub workflow location**
   - Workflow file exists under `yos-automations/scripts/yos-llm-pipeline/.github/workflows/`.
   - No root-level equivalent was located.
   - In the monorepo, this is an archived/nested workflow definition rather than evidence of an active repository workflow.

2. **Runtime dependency uncertainty**
   - Code shells out to `manus-mcp-cli` for Notion.
   - The workflow installs `manus-mcp-cli || true`, which can mask installation failure.
   - The comment promises a bundled fallback adapter, but the run step invokes the main script without visibly switching to that fallback.

3. **Schema ambiguity in the extraction prompt**
   - `confidence` appears twice with incompatible vocabularies: `low|medium|high` and `confirmed|likely|uncertain`.
   - JSON parsers generally keep only one duplicate key, making intended semantics ambiguous.

4. **Canonical-key comparison mismatch**
   - Candidate canonical keys are compared against a normalized result title rather than a retrieved canonical-key field.
   - This weakens the claim that canonical key is the primary deduplication signal.

5. **Conflict detection is heuristic and English-biased**
   - Contradiction detection relies on a small English negation-word set despite FR/EN/IT source scope.

6. **Synthesis layer is a stub**
   - The code explicitly contains a TODO for section-level synthesis.
   - It must not be classified as implemented or operational.

7. **No committed successful run evidence located**
   - Documentation names runtime log paths, but no current successful execution artifact was found in the repository during this pass.

### A-04 — yOS Life Panel / universal userscript

**Path:** `yos-automations/scripts/yos-userscripts/scripts/yos-panel.user.js`

Implemented cross-site surface with:

- Shadow DOM isolation;
- capture and context-builder calls;
- VIVI backend endpoints;
- optional Manus API key in Tampermonkey storage;
- Y Life project routing.

**Classification:** IMPLEMENTED CLIENT; BACKEND AND DEPLOYMENT STATUS UNVERIFIED.

This is a cross-site capture/router interface, not the YOS Shell itself.

### A-05 — Components Registry

**Path:** `yos-automations/scripts/yos-scripts/components-registry/`

Architecture proposes four component layers:

1. primitives;
2. renderers;
3. composites;
4. workflows.

A machine-readable registry exists with eight recorded components. Only the Mermaid renderer is marked beta; the rest are drafts. The architecture document remains `1.0.0-draft` and explicitly records unresolved decisions about repository strategy, loader TTL, Notion sync, visibility and schema format.

**Classification:** PARTIALLY IMPLEMENTED REGISTRY PROTOTYPE; DO NOT TREAT AS Y-REG CANON.

Potential reuse:

- component metadata model;
- version lifecycle;
- explicit I/O contracts;
- loader/cache concepts;
- component/workflow distinction.

Required reconciliation:

- Y-REG and AGENTS capability registries;
- KAP source/object registries;
- Manus skill registry;
- Shell capability inventory;
- deployment/runtime registries.

### A-06 — yOS Notify

**Path:** `03_AUTOMATIONS/modules/yos-notify/`

Implemented capabilities:

- unified Python and CLI interface;
- Pushover and Telegram channels;
- device targeting;
- Manus iOS task deep links;
- standardized task completion notifications;
- environment/config based credential loading.

**Classification:** IMPLEMENTED MODULE; OPERATIONAL STATUS UNVERIFIED.

## CRITICAL SECURITY FINDING

### SEC-T09-001 — Live-looking notification credentials committed in documentation

The public repository contains credential-looking values in the `yos-notify` README, including notification service credentials and a Telegram bot token. Search also locates credential variable references across the README, skill, installer and implementation.

**Severity:** CRITICAL  
**Confidence:** HIGH  
**Impact:** unauthorized notification access, bot compromise, spam, data leakage, abuse of linked channels.

### Required remediation

1. revoke and rotate the exposed Telegram bot token;
2. rotate Pushover credentials/keys where supported;
3. remove all literal credentials from the current repository files;
4. replace documentation values with placeholders;
5. audit Git history and original source repositories because deleting current files does not remove exposed history;
6. verify whether GitHub secret scanning or third-party indexing has already detected them;
7. test new credentials only through environment variables or the designated secret manager;
8. document the incident without copying secret values into KAP reports.

No automatic rotation or destructive history rewrite was attempted during this audit.

## Legacy-to-canonical migration state

The pre-reorganization inventory classified approximately 70 files under `yos-automations/` for copying to `03_AUTOMATIONS/`. The current repository still contains substantial automation implementations only at legacy paths, while at least some newer modules exist directly under `03_AUTOMATIONS/modules/`.

**Conclusion:** migration is incomplete and mixed-mode.

```text
legacy implementation paths
    + selected canonical modules
    + standalone deployment repositories
    + Manus runtime-local files
    + SaaS schedules
```

No single automation directory currently represents the complete operational truth.

## Keep / Merge / Archive direction

| Asset | Direction |
|---|---|
| Cross-LLM memory push scripts | KEEP; verify deployed standalone source and secrets model |
| Memory Bridge architecture | KEEP HISTORICAL; revalidate runtime and update contradictions |
| LLM distillation pipeline | KEEP AS IMPLEMENTED CANDIDATE; repair/test before promotion |
| Nested workflow file | KEEP AS SOURCE; relocate only after runtime decision |
| yOS Life Panel | KEEP SEPARATE; map backend contracts |
| Components Registry | KEEP/RECONCILE; merge concepts into Y-REG rather than creating a competing registry |
| yOS Notify | KEEP CODE; immediate credential remediation required |
| legacy `yos-automations/` path | DO NOT ARCHIVE until deployed-source and file-hash census completes |

## Next audit actions

1. credential incident remediation approval and execution;
2. enumerate every file under legacy and canonical automation trees;
3. locate original standalone repositories and determine deployed branch/version;
4. inspect GitHub Actions run history and external scheduler evidence;
5. map each automation to a runtime owner and transport contract;
6. reconcile Mem0, Notion pipeline, KAP and ARCH roles;
7. produce an automation registry with statuses: `DOCUMENTED`, `IMPLEMENTED`, `RUNNABLE`, `DEPLOYED`, `OPERATIONAL`, `STALE`;
8. validate one safe dry-run per critical automation only after the development freeze permits execution testing.
