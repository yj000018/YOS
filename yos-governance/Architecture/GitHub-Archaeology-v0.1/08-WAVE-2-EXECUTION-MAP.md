# Wave 2 — Execution Map

**Program:** GitHub Account Archaeology v0.1  
**Branch:** `agent/github-account-archaeology-wave1`  
**Mode:** MAP  
**Status:** ACTIVE / CONSOLIDATION ONLY  
**Rule:** no new framework; map the actual state of the existing KAP/Manus machinery.

## 1. System map

```text
SOURCE SURFACES
├─ Git / GitHub
├─ ChatGPT capture packs
├─ Manus durable outputs
├─ Manus historical tasks / sessions
├─ Obsidian / Markdown vaults
├─ Notion workspaces / databases / blocks
├─ Mem0
├─ Other LLM histories
└─ Generated sites / apps
        │
        ▼
L0 CHANNEL
        │
        ▼
L1 SOURCE INSTANCE
        │
        ▼
DISCOVERY / CATALOGUE
        │
        ▼
METADATA ACQUISITION
        │
        ├─ structure
        ├─ identifiers
        ├─ dates
        ├─ checksums
        └─ provenance
        │
        ▼
BODY / OUTPUT ACQUISITION
        │
        ▼
L2 SOURCE OBJECT
        │
        ▼
L3 SOURCE FRAGMENT
        │
        ▼
FACTSHEET / CLAIM EXTRACTION
        │
        ▼
THOUGHT LINES / DECISION THREADS
        │
        ▼
CONTRADICTION + SUPERSESSION
        │
        ▼
CURRENT BEST KNOWLEDGE
        │
        ▼
HUMAN VALIDATION / CANON
```

The historical KAP registries model this pipeline, but their July 3 snapshots must be reconciled with later execution commits. A registry row marked `PENDING-GATE` is not proof that no later work occurred.

## 2. Consolidated source-state map

| Surface | Historical registry state | Later execution evidence | Consolidated current interpretation | Genuine missing work |
|---|---|---|---|---|
| **Git — KAP + yos-cognitive-os** | Metadata and content pilots complete; extraction pending | Large KAP/YOS migrations, archaeology, gates and baseline artifacts exist | Durable source corpus exists and is directly analyzable | Complete account-wide cross-repo extraction and supersession mapping |
| **Git — remaining repositories** | 33+ repositories catalogued; metadata ready; content gated | Current census identifies 40 owned repositories and Wave 1 has begun selective archaeology | Access is not the blocker; systematic coverage is incomplete | Repository dossiers, branch archaeology, hidden-gem and duplication maps |
| **ChatGPT capture packs** | Two packs acquired with full bodies; 6+ parallel sessions pending | No evidence that all pending sessions were exported | Two durable full-body packs are usable; broader history remains incomplete | Export/capture only the sessions not already represented elsewhere |
| **Manus durable gate reports** | Acquired; metadata and content pilots complete | MPM, MPR, registries, skills, scripts, gates and Chronicles are present in Git | High-confidence durable corpus; do not reacquire through Manus | Compare, synthesize and supersede using Git evidence |
| **Manus historical corpus** | Historical registry labels 194 sessions, metadata complete, content pending-gate | Later evidence distinguishes 363 session metadata records and 194 archived factsheets | The historical registry mixed representation types; 194 and 363 are not equivalent | Join identifiers; classify body/output/factsheet coverage per session |
| **Obsidian — Git-backed** | Two vault representations catalogued; metadata gate pending | Later discovery reports Y-World snapshots and local Ludivine vault counts | Multiple snapshots exist with probable overlap and temporal drift | Hash/path comparison; canonical-vs-backup map; no destructive merge |
| **Obsidian — local vaults** | Seven paths unknown in the July 3 registry | Later archaeology reports additional discovered vaults, including Ludivine 1842 notes | July 3 blocker is partially stale, but full current inventory is not yet proven | Exact vault census, authorization boundaries, metadata/body coverage |
| **Notion** | Census incomplete; 1300+ pages estimated; controlled execution gated | Seven databases / 593 entries acquired; later M6C reports 431 pages, 14,356 blocks and 793 files | Significant block-level extraction occurred; it is not merely metadata-only | Determine workspace scope, failures, omitted pages, overlap and freshness |
| **Mem0** | 316 entries acquired; `SIGNAL_ONLY` | Same count appears in acquisition consolidation | Semantic routing/index layer, not durable source corpus | Provenance links back to Git/Notion/session objects |
| **Internal LLM knowledge** | Deferred until taxonomy complete | No durable evidence of full structured extraction | Heuristic context only | Use only after source taxonomy and only with explicit uncertainty |
| **Other LLM histories** | Blocked/manual export | No complete export evidence | Incomplete historical surface | Targeted export only where unique value is probable |
| **Generated Git-backed sites/apps** | Metadata ready or catalogued | Repositories are included in the 40-repo account census | Source code can be archaeologized through Git | Classify reusable components and vertical embodiments |
| **Deployed sites/apps without Git** | Blocked because URLs/inventory unknown | No complete provenance census recovered | Genuine external-surface gap | Manus/user-assisted URL and project inventory later |

## 3. Manus representation map

```text
MANUS PLATFORM OBJECT
│
├─ task/session identifier
├─ title/date/status metadata
├─ prompt / instructions
├─ intermediate execution state
├─ final output
└─ attachments / deployed artifacts
        │
        ├──────────────► Manus metadata record corpus: 363
        │
        ├──────────────► normalized / archived factsheets: 194
        │
        ├──────────────► Notion database/page representations
        │
        ├──────────────► Mem0 semantic memories: 316 total store entries
        │
        └──────────────► Git durable reports, MPRs, gates, scripts and artifacts
```

### Non-equivalence rule

```text
363 metadata records ≠ 194 factsheets ≠ 316 Mem0 memories ≠ 593 Notion records
```

These are different representation layers. They may overlap around the same original Manus object.

### Required join graph

```text
manus_session_id
      │
      ├─► metadata_record_id
      ├─► factsheet_id
      ├─► notion_page_or_record_id
      ├─► mem0_memory_id
      ├─► git_path / commit_sha
      ├─► body_checksum
      └─► output_checksum
```

Without these joins, no completeness percentage is trustworthy.

## 4. Historical registry → later evidence delta map

| Historical statement | Later evidence | Consolidation decision |
|---|---|---|
| `INST-MAN-002 Historical Tasks (194 sessions)` | Pipeline report says 194 factsheets archived; later corpus says 363 session metadata records | Mark historical label as semantic drift; preserve it, but do not reuse the count as a session total |
| Manus historical metadata `COMPLETE`, content `PENDING-GATE` | Some complete outputs became factsheets and durable Git artifacts | Classify per object; never upgrade the entire corpus to body-complete |
| Notion metadata ready, content gated | M6C extracted 431 pages, 14,356 blocks and 793 files | Registry snapshot is stale after M6C; update current assessment without erasing the earlier gate state |
| Obsidian local vaults blocked / paths unknown | Later discovery found major vault surfaces | Treat blocker as partially superseded, not fully resolved |
| Git acquisition focused on two repos; 39 metadata-ready | Account-wide Wave 1 now covers 40 owned repos at census level | Extend existing Git acquisition model; do not invent a parallel Git crawler architecture |
| Mem0 acquired | KAP explicitly marks Mem0 `SIGNAL_ONLY` | Never count Mem0 entries as canonical documents or source-session proof |

## 5. WP2 execution map — current resolution

```text
WP2 PROGRAM
│
├─ E-series: engineering / acquisition foundations
│   ├─ existence confirmed
│   ├─ registries, gates, schemas, checksums and infrastructure present
│   └─ exact sprint-by-sprint completion boundary: unresolved
│
└─ M-series: Manus / memory / source acquisition work
    ├─ M1–M5: broad Manus, memory and source-surface acquisition evidence
    ├─ M6: Notion acquisition family
    │   └─ M6C: 431 pages / 14,356 blocks / 793 files reported
    ├─ M7: included in the consolidated fourteen-sprint corpus
    └─ exact body/output/normalization completion by sprint: unresolved
```

### Safe interpretation

- The WP2 program produced substantial real artifacts.
- The existence of fourteen sprint folders does not prove fourteen fully completed pipelines.
- The consolidated commit proves corpus presence, not semantic completion.
- Completion must be measured by the deepest proven pipeline stage per source instance.

## 6. Deepest proven stage map

| Source instance | Deepest proven stage | Confidence | Not yet proven |
|---|---|---:|---|
| Manus durable reports | body/output acquired in Git | high | full claim/thought-line synthesis across all reports |
| Manus 363 corpus | metadata acquired | high | complete bodies, outputs, factsheets and deduplicated uniqueness |
| Manus 194 factsheets | factsheet processing / archival | high for representation count | one-to-one relation with unique sessions and complete source fidelity |
| Notion M6C sample/corpus | block and file extraction | high for reported batch | whole-workspace completeness and overlap-free uniqueness |
| Mem0 | signal/index acquisition | high | durable-source equivalence or canonical authority |
| Git KAP + yos-cognitive-os | content acquired and partially architecturally processed | high | full cross-repo comparison and canon reconciliation |
| Remaining Git repos | census / metadata / selective content review | medium-high | exhaustive content and branch archaeology |
| Obsidian Git-backed | metadata and selective content evidence | medium | complete dedupe and canonical snapshot decision |
| Local Obsidian | discovery partial | medium | current full census and authorized body acquisition |
| ChatGPT acquired packs | full body in Git | high | all relevant historical sessions represented |

## 7. Consolidation funnel

```text
ALL HISTORICAL WORK
        │
        ▼
Already durable and reproducible from Git
        │
        ├─► architecture reconstruction now
        ├─► terminology and supersession now
        ├─► capability reuse decisions now
        └─► repo archaeology now

Not durable / inaccessible / semantically ambiguous
        │
        ├─► Manus session ID joins
        ├─► missing body/output verification
        ├─► deployed site/app census
        ├─► remaining Notion/local Obsidian gaps
        └─► targeted historical session recovery
                │
                ▼
       FUTURE MINIMAL MANUS PACKAGE
```

## 8. Genuine delta — work that remains

### Do now from Git

1. Audit the fourteen WP2 sprint folders and their completion reports.
2. Extract all factsheet IDs from the 194 archive and all session IDs from the 363 metadata corpus.
3. Build the join table and calculate verified overlap.
4. Recover exact contracts and execution evidence for prior skills and scripts.
5. Date the authority transition: Notion-primary → Git durable authority → Markdown/Obsidian human layer.
6. Continue account-wide repo archaeology and map reusable vertical components.

### Reserve for Manus or human-assisted access

1. Retrieve original platform bodies/outputs only where the Git join table proves them absent.
2. Inventory deployed Manus/Lovable/Replit projects lacking Git provenance.
3. Complete remaining Notion and local Obsidian access gaps.
4. Verify ambiguous historical session surfaces that cannot be resolved from durable artifacts.

### Explicitly exclude from future Manus work

- rebuilding KAP taxonomy;
- recreating L0→L3 registries;
- redesigning factsheets;
- recreating `session-synthesis` collection/card logic;
- re-extracting durable gate reports already in Git;
- rediscovering KAP contradiction, deduplication or supersession policies;
- repeating the Git account census without a delta reason.

## 9. Wave 2 state map

```text
W2-A Manus corpus boundary       ██████░░░░  60% evidence-resolved
W2-B Recovered capabilities      ██████░░░░  60% first classification complete
W2-C Count reconciliation        ████████░░  80% semantics resolved, joins missing
W2-D WP2 pipeline lineage        ████░░░░░░  40% program mapped, sprint audit missing
W2-E Authority supersession      █████░░░░░  50% direction known, dates incomplete
W2-F Manus continuation package  ███░░░░░░░  30% exclusions known, final inputs pending
```

Percentages are operational estimates, not statistical completeness claims.

## 10. Immediate next map operation

```text
WP2 FOLDER / REPORT INVENTORY
        +
194 FACTSHEET ID EXTRACTION
        +
363 SESSION METADATA ID EXTRACTION
        │
        ▼
IDENTIFIER JOIN TABLE
        │
        ▼
PROVEN COVERAGE MATRIX
        │
        ▼
MINIMAL MANUS DELTA
```
