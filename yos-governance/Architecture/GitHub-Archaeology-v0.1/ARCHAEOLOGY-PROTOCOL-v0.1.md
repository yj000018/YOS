# Archaeology Protocol v0.1

**Status:** Working protocol — derived from prior archaeology, not invented from scratch  
**Scope:** all repositories owned by `yj000018`  
**Principle:** archaeology must first archaeologize its own prior methods.

## 1. Evidence classes

Every finding must be classified as one or more of:

- `artifact` — file, schema, prompt, code, workflow, diagram, issue, PR, commit;
- `claim` — architectural or conceptual statement;
- `decision` — explicit choice with rationale;
- `probe` — bounded empirical test;
- `result` — validated outcome of a probe;
- `hypothesis` — unresolved interpretation;
- `lineage-node` — concept in an evolutionary chain;
- `supersession-edge` — relation from an older formulation to a newer one;
- `hidden-gem` — high-value reusable fragment outside its apparent local scope;
- `dead-end` — abandoned path whose reasoning must still be preserved;
- `vertical-embodiment` — product or interface that instantiates a larger Y-OS/KOSMOS principle.

## 2. Authority scale

- `PROVEN_OPERATIONAL` — observed working with runtime evidence;
- `PROVEN_STATIC` — file/code/schema exists and is internally coherent;
- `DECIDED` — explicit architectural decision, not necessarily implemented;
- `CANDIDATE` — plausible and supported but not validated;
- `HYPOTHESIS` — open interpretation;
- `SUPERSEDED` — replaced by a later decision;
- `REJECTED` — tested and found unsuitable;
- `UNKNOWN` — insufficient evidence.

No item becomes canonical solely because it is newer or labelled canonical in its source.

## 3. Mandatory provenance

Each extracted item records:

- repository;
- branch/ref;
- exact path or commit;
- date;
- original terminology;
- author/executor where available;
- local context;
- current interpretation;
- confidence;
- possible destination;
- relationships to prior and later items.

## 4. Fractal excavation sequence

```text
Prior archaeology
→ prior archaeology of prior work
→ extraction of methods and invariants
→ critique against current evidence
→ consolidated archaeology method
→ repository excavation
→ cross-repository lineage
→ canon reconciliation
```

## 5. Layered reading order

For every repository:

1. metadata and status;
2. branch and commit chronology;
3. README and root manifests;
4. architecture/docs/specifications;
5. issues, PRs, review discussions;
6. code, workflows, schemas, runtime evidence;
7. deleted/replaced paths visible through history;
8. comparison with related repositories;
9. timeline and supersession reconstruction;
10. disposition recommendation only after all prior layers.

## 6. Consolidation rule

Consolidation is not summarization.

A valid consolidation must:

- preserve all unique claims and evidence;
- remove accidental repetition;
- identify conflicts rather than smoothing them over;
- preserve original language when terminology matters;
- separate historical truth from current-best architecture;
- retain reusable code and patterns;
- increase semantic density and navigability;
- keep links back to original evidence.

## 7. Timeline model

Every major concept should eventually have:

```yaml
concept_id:
current_name:
aliases: []
first_seen:
major_iterations: []
turning_points: []
superseded_forms: []
current_status:
remaining_open_questions: []
```

## 8. Repository disposition rule

Allowed recommendations:

- `KEEP_CANONICAL`
- `KEEP_ACTIVE_VERTICAL`
- `MERGE_INTO_CANON`
- `REFERENCE_HISTORICAL`
- `ARCHIVE_AFTER_MIGRATION`
- `DELETE_AFTER_VERIFIED_EXTRACTION`
- `UNRESOLVED`

No destructive action is authorized by this protocol.

## 9. Current inherited methodological assets

The protocol explicitly inherits and will reconcile:

- prior-work archaeology;
- manifests and checksums;
- persistence gates;
- source cards;
- task-vs-session separation;
- manual extraction fallbacks;
- quarantine and bounded comparison;
- Thought Lines;
- Decision Threads;
- contradiction and supersession registries;
- discovery genealogies;
- emergence events;
- fulgurances;
- uncertainty preservation;
- probe-based epistemology;
- A&G validation.

## 10. First governing maxim

> Never invent a new structure before searching for its ancestral forms, prior failures, partial implementations, and forgotten names.