# Wave 2 — Consolidated Evidence Ledger

**Program:** GitHub Account Archaeology v0.1  
**Branch:** `agent/github-account-archaeology-wave1`  
**Status:** ACTIVE — EVIDENCE PASS 1 COMPLETE  
**Primary rule:** consolidate recovered evidence before creating new machinery.  
**Parent control plane:** `07-WAVE-2-CONSOLIDATION-CONTROL-PLANE.md`

## 1. Purpose

This is the single Wave 2 evidence ledger for the Manus/KAP acquisition lineage.

It consolidates the parallel lanes into one surface:

- corpus boundary;
- reported-count semantics;
- acquisition depth;
- recovered capabilities;
- reuse decisions;
- unresolved overlaps;
- work that genuinely remains Manus-dependent.

It does not replace the KAP L0→L3 registries, the Meta-Archaeology Register, or the original source artifacts.

## 2. Executive finding after Evidence Pass 1

The historical corpus was not absent. It was acquired and processed at several different depths, through several representations, at different dates.

The central problem is therefore not “collect everything from zero.” It is:

```text
identify objects
→ map representations
→ distinguish metadata from bodies and outputs
→ prove overlaps
→ preserve provenance
→ complete only the missing stages
```

The values `194`, `363`, `316`, and `593` are not one cumulative corpus count and must not be added together.

## 3. Reconstructed chronology

### Stage A — Registry state dated 2026-07-03

The canonical KAP registries identify:

- `INST-MAN-001` — Manus Durable Gate Reports: `ACQUIRED`, with reports, registries and models in Git;
- `INST-MAN-002` — Manus Historical Tasks: **194 sessions**, `CATALOGUED`;
- metadata-only pipeline for the 194 historical items: `COMPLETE`;
- content pilot, extraction pilot and full extraction: `PENDING-GATE`;
- next gate: `MANUS-HISTORICAL-ACQUISITION-GATE`.

The same registry notes “Full session content in Notion/Mem0.” This is a historical claim about location, not proof that the full bodies were durably acquired, normalized, compared or synthesized in Git.

Relevant sources:

- `01_BACKBONE/KAP/04_REGISTRIES/SOURCE-INSTANCE-REGISTRY.md`
- `01_BACKBONE/KAP/04_REGISTRIES/SOURCE-PIPELINE-REGISTRY.md`
- `01_BACKBONE/KAP/04_REGISTRIES/KAP-SOURCE-MATRIX.md`

### Stage B — 194 factsheets archived

KAP commit `884c871d771f604e66b56fad59162ed8e9fa23a6` later reports:

- evolutionary merge architecture;
- Thought Line, Decision Thread, Contradiction, Dedup and Current Best Knowledge models;
- Obsidian and Notion access work;
- **194 factsheets archived**.

This proves that a 194-item factsheet archive existed. It does not yet prove that:

- the 194 factsheets correspond one-to-one with the earlier 194 historical tasks;
- each factsheet contains the complete task body and complete output;
- all factsheets were normalized into L2/L3 objects and fragments;
- all were compared, synthesized or canonized.

### Stage C — broader WP2 acquisition corpus

KAP commit `b0fb8414ebbcb45cb62e3dc4ffdabd6073e8b7e8` reports:

- fourteen sprint folders from WP2-E1 through WP2-M7;
- **363 Manus Memory Session metadata records**;
- **316 Mem0 memories**;
- **seven Notion databases containing 593 entries**;
- scripts, reports, registries, checksums and an infrastructure audit.

This proves a broader acquisition surface than the earlier 194-item snapshot. It does not prove full-body or full-output coverage for all 363 session records.

## 4. Semantic count dictionary

| Count | Working object type | What is proven | What is not proven | Current status |
|---:|---|---|---|---|
| 194-A | Manus Historical Tasks / sessions | registry identifies 194 historical items; metadata pipeline complete | complete bodies, complete outputs, one-to-one factsheet mapping | `PARTIAL_REQUIRES_COMPLETION` |
| 194-B | archived factsheets | commit reports 194 factsheets archived | equality with 194-A; completeness and processing depth | `REQUIRES_OVERLAP_PROOF` |
| 363 | Manus Memory Session metadata records | metadata corpus exists in WP2 acquisition | bodies, outputs, factsheet coverage, deduplication against 194 | `METADATA_CONFIRMED` |
| 316 | Mem0 memories | memory/index records acquired | primary-source completeness or canonical authority | `SIGNAL_ONLY` |
| 593 | Notion database entries across seven databases | aggregate database-record count exists | record types, duplicate representations, session equivalence | `AGGREGATE_CONFIRMED` |
| 40 | currently owned GitHub repositories | current account census | equality with historical 41-slot registry | `CURRENT_CENSUS` |

## 5. First overlap conclusion

The evidence currently supports the following model:

```text
Manus historical work objects
├── session/task metadata representations
├── task or session body representations
├── output/artifact representations
├── factsheet representations
├── Notion page/database representations
└── Mem0 semantic-memory representations
```

These are potentially multiple representations of the same underlying work objects.

Therefore deduplication must occur by stable identity and provenance, not by matching totals.

### Required identity bridge

The next reconciliation must attempt to map:

- Manus task/session ID;
- title;
- creation/update timestamp;
- source URL or platform identifier;
- factsheet ID;
- Notion page/database ID;
- Mem0 memory ID;
- Git path and commit SHA;
- output/artifact IDs;
- checksum or normalized-content fingerprint.

Without this bridge, `194`, `363`, `316`, and `593` remain incomparable aggregates.

## 6. Corpus-boundary matrix — Pass 1

| Corpus / mechanism | Discovered | Metadata acquired | Body acquired | Output acquired | Factsheet processed | Compared / synthesized | Current judgement |
|---|---:|---:|---:|---:|---:|---:|---|
| Manus Durable Gate Reports (`INST-MAN-001`) | yes | yes | yes, in Git | yes, where reports are outputs | mixed | mixed | `REUSE_AS_IS` as durable evidence |
| Manus Historical Tasks 194 (`INST-MAN-002`) | yes | yes | historically claimed external | unproven | 194 archive reported, mapping unproven | not proven corpus-wide | `PARTIAL_REQUIRES_COMPLETION` |
| Manus Memory Sessions 363 | yes | yes | not proven corpus-wide | not proven | overlap unknown | not proven | `METADATA_CONFIRMED` |
| Mem0 316 | yes | yes | not applicable as corpus | not applicable | not applicable | routing/index only | `SIGNAL_ONLY` |
| Notion seven databases / 593 entries | yes | yes | partial extraction evidence | mixed/unknown | may contain factsheets | not proven corpus-wide | `PARTIAL_REQUIRES_COMPLETION` |
| ChatGPT bootstrap/current packs | yes | yes | full body in Git for two packs | represented in packs | not fully processed | pending later stages | `REUSE_AS_IS` as source packs |
| ChatGPT parallel/general sessions | yes | no | blocked pending export | blocked | no | no | `BLOCKED_UNTIL_EXPORT` |

## 7. Recovered capability matrix

Historical commits and migrations confirm the following Manus/Y-OS capability family:

| Capability | Recovered evidence | Original destination / role | Current reuse decision |
|---|---|---|---|
| `memoriser` | skill history | push content into Y-OS Memory Inbox / Notion | `REUSE_WITH_DESTINATION_UPDATE` |
| `hydrater` | skill history | pull Notion Memory context into sessions | `RECONCILE_WITH_LATER_DOCTRINE` |
| `memory-manager` | skill history | persistent memory management | `REUSE_LOGIC_AFTER_AUTHORITY_REVIEW` |
| `session-synthesis` | skill, API reference, scripts and template migrated into YOS | collect sessions, generate cards, archive to Notion | `REUSE_WITH_DESTINATION_UPDATE` |
| `summary` | skill history | strategic session synthesis | `REUSE_AS_TRANSFORMATION_STEP` |
| `status` | skill history | tactical checkpoint generation | `REUSE_AS_TRANSFORMATION_STEP` |
| `dev` | skill history | Manus code/development execution | `HISTORICAL_CAPABILITY_REFERENCE` |
| `collect_session.py` | migrated implementation | collect session material | `REUSE_AFTER_INPUT_CONTRACT_AUDIT` |
| `generate_card.py` | migrated implementation | produce session card/factsheet | `REUSE_AFTER_SCHEMA_RECONCILIATION` |
| `archive_to_notion.py` | migrated implementation | publish/archive to Notion | `REUSE_LOGIC_ONLY`; destination policy requires update |
| KAP gates / MPMs / MPRs | extensive Git evidence | controlled execution and transfer | `REUSE_AS_IS`, reconcile stale assumptions |
| Thought Lines / Decision Threads / Contradiction / CBK models | commit `884c871...` | synthesis and evolution management | `REUSE_AS_EXISTING_CONSOLIDATION_MODEL` |

## 8. Consolidation decisions established by Pass 1

### Decision W2-D01 — Do not build a new session collector

Existing collection, card-generation and archival machinery already exists. The next work is contract and destination reconciliation, not recreation.

### Decision W2-D02 — Separate transformation logic from storage destination

The historical pipeline often points to Notion as the archival destination. The useful processing logic must be preserved independently of that destination.

Current operating direction:

```text
Git / Markdown = durable evidence and authority
Obsidian = preferred human navigation and knowledge interface
Notion = transitional or operational surface, subject to evidence
Mem0 = active semantic memory / signal layer, never primary proof
```

This is a working architectural consequence, not a destructive migration authorization.

### Decision W2-D03 — Treat Mem0 as an index, not a corpus

The KAP Source Matrix explicitly marks Mem0 `SIGNAL_ONLY`. A Mem0 record may route to knowledge, but cannot substitute for a durable source artifact.

### Decision W2-D04 — Preserve the 194 ambiguity

Until identity mapping is executed, “194 sessions” and “194 factsheets” remain two evidence statements, not a proven equivalence.

### Decision W2-D05 — The 363 corpus is metadata-confirmed, not body-complete

No current evidence permits calling the 363-session corpus fully acquired at body/output level.

## 9. What remains genuinely Manus-dependent

The following work should remain reserved for Manus or another operator with the relevant platform access:

1. retrieve inaccessible Manus-native session/task bodies not already present in Git;
2. retrieve complete task outputs and artifact references where metadata exists but bodies do not;
3. export stable platform identifiers needed for overlap mapping;
4. verify whether the 194 factsheets correspond exactly to a subset of the 363 metadata records;
5. inspect Notion databases/pages where current Git evidence only proves metadata or partial extraction;
6. produce missing durable source packs, without redesigning KAP or the ontology;
7. stop when the declared missing objects are recovered or formally confirmed unavailable.

## 10. Work that does not require Manus

ChatGPT/A&G can continue directly from Git with:

- reconstructing the WP2 sprint lineage;
- inventorying gates, reports, scripts, skills and schemas;
- comparing historical and current source-authority doctrine;
- mapping repository and commit chronology;
- detecting duplicated or migrated implementations;
- preparing the identity-bridge schema;
- preparing the final bounded continuation package;
- synthesizing KOSMOS and Y-OS architecture from validated Git evidence.

## 11. Next evidence pass

The next pass remains consolidation-only:

```text
A. Recover WP2-E1 → WP2-M7 completion reports
B. classify each sprint by deepest completed pipeline stage
C. locate the 194 factsheet manifest or archive index
D. locate the 363 metadata manifest and identifier fields
E. identify the seven Notion database names and record classes
F. map migrated session-synthesis files to their original repository history
G. update this ledger with proven overlap and explicit gaps
```

No new source architecture or agent framework is required for this pass.
