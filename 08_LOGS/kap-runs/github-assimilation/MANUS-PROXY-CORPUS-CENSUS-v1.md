# Manus Proxy Corpus Census v1

**Program:** Definitive YOS Canon / Source Assimilation  
**Date:** 2026-07-23  
**Mode:** PARA evidence recovery  
**Status:** `PARTIAL_DIRECT_ACCESS_CONFIRMED`  
**Constraint:** archaeology only; no new Manus runtime, API integration or redesign.

## Executive finding

The Manus historical corpus is **not fully blocked**.

Direct access to Manus-native project/session history is still unavailable, but substantial Manus evidence is already reachable through two durable proxy surfaces:

1. **Notion — Manus Memory Sessions database**;
2. **Google Drive — Manus website registry, crawl outputs, MPM/MPR reports, exported pages and URL registries**.

Therefore the previous classification `REFERENCE_ONLY / export required` is superseded by:

```text
PARTIAL_DIRECT_READ_VIA_DURABLE_PROXIES
```

The remaining task is to reconcile these representations with Git, not to start collection from zero.

## Lane M1 — Notion Manus Memory Sessions

### Container

- Database: `Manus Memory — Sessions`
- Data source: `collection://0720db9b-5e1d-41a2-bd0c-6721fe0dab94`
- Parent chain: `Y-OS ROOT → MEMORY MGMT → Manus Memory — Sessions`

### Schema recovered

Each row may contain:

- stable Notion page URL;
- creation time;
- `Title`;
- `UID`;
- `Project`;
- `Date`;
- `Themes`;
- `Subthemes`;
- `Language`;
- `Length`;
- `Depth`;
- application-level `Archived` flag.

The project vocabulary currently includes `yOS`, `eia`, `VISUAL_REALITY`, `DOMUS`, `GEN5`, `ODYSSEY`, and `UNKNOWN`.

### Enumeration state

The database view was exhaustively paginated at 100 rows per page:

- page 1: full;
- page 2: full;
- page 3: full;
- page 4: terminal (`has_more=false`).

This is consistent with the previously recovered **363 metadata-record** statement. No Notion-trash/archive partition rows were returned.

### Content depth

The database is not merely a title index. Fetched pages contain structured session records with:

- executive summary;
- context and intent;
- work performed;
- outputs;
- decisions;
- lessons;
- failures;
- blockers;
- open questions;
- next steps;
- source UID/model/cost metadata on some records.

However, content depth is heterogeneous:

- some records are `MASTER SESSION` syntheses;
- some are detailed factsheet-style reconstructions;
- some historically claim attached/collapsed verbatim sections;
- complete verbatim body coverage has not yet been proven row by row.

## Lane M2 — Historical count reconciliation

### Count statements now present

| Count | Historical meaning | Evidence state |
|---:|---|---|
| 194 | historical tasks / archived factsheet representations in KAP evidence | overlap unresolved |
| 325 | claim dated 2026-04-07: `325/325 Manus sessions archived` | historical completion claim |
| 278 | claim: pages updated with collapsed verbatim sections | historical processing claim |
| 363 | current Manus Memory Sessions metadata corpus | direct container traversal consistent |

### Required interpretation

These counts must not be added together or treated as contradictions without identity mapping.

Working lineage:

```text
Manus task/session
→ platform metadata
→ Notion session page
→ optional verbatim body
→ optional synthesis/factsheet
→ optional Mem0 representation
→ optional Git artifact
```

The `325 → 363` delta may represent later sessions, master/fusion pages, duplicates, imported records or taxonomy changes. It remains an explicit reconciliation question.

## Lane M3 — Manus websites and generated experiences

### Drive corpus

Google Drive contains a durable Manus website recovery package with:

- registry of **30** website entries;
- crawl summary;
- crawl results JSON;
- duplicate groups;
- one folder per website;
- normalized text/Markdown;
- route metadata;
- screenshots and resource inventories where captured.

### Crawl result

| Metric | Result |
|---|---:|
| Registry entries | 30 |
| Accessible/published | 22 |
| Unpublished or without URL | 8 |
| Routes captured | 69 |
| Extracted text characters | 164,591 |
| Crawl errors | 0 in the final v1 summary |
| Exact-content duplicate groups | 2 |

### YOS-relevant recovered sites

Priority candidates include:

- `MWS-017 — Y-WORLD`;
- `MWS-019 — Y-OS Dashboard`;
- `MWS-027 — Multi-Agent LLM`;
- other system/oeuvre experiences whose content may contain architectural or product evidence.

The crawl proves that Manus websites are durable knowledge-bearing outputs, not merely presentation surfaces.

### Duplicate groups

Two pairs have identical site-level content hashes:

- `MWS-015` / `MWS-016`;
- `MWS-029` / `MWS-030`.

These are representation duplicates until provenance and project lineage are checked.

## Lane M4 — Manus URL and export traces

Drive contains a clipboard-derived registry of **99 Manus share URLs**. It is a discovery surface, not yet a complete body corpus.

Additional exported Manus evidence includes:

- saved HTML pages;
- MPM packets;
- MPR execution reports;
- project packs;
- website crawl folders;
- source-adapter documentation;
- local browser-profile and crawler packages.

No credentials or access codes are copied into this audit.

## Lane M5 — Historical Manus API capability evidence

A 2026-07-05 execution report records the following as historically proven:

- task creation;
- sending messages to an existing task;
- file upload and attachment;
- conversation continuation;
- structured JSON output;
- webhook notification.

The same report records:

- no direct workspace file read API;
- no direct workspace file write API;
- indirect workspace access only through agent task instructions.

This is historical capability evidence only. The development freeze prohibits implementing or testing a new runtime integration during archaeology.

## Lane M6 — Doctrine recovered from Manus proxies

High-value dated historical positions include:

### 2026-05-02 infrastructure synthesis

```text
Manus = central living UI
Notion = memory SSOT
GitHub = code
n8n = complex automation
Telegram = voice/mobile interface
```

This supports the durable architectural fact that Manus was already positioned as the primary human interaction surface.

### 2026-05-02 memory synthesis

Notion was described as the unique memory SSOT, with `/hydrater`, `/memoriser` and `/session-synthesis` workflows.

This is **historical doctrine**, not current canon. Later source-of-truth decisions must be represented as supersession, not silent replacement.

### 2026-04-07 multi-LLM extraction synthesis

A detailed session claims that Manus built:

- a unified multi-LLM extraction orchestrator;
- adapters for ChatGPT, Gemini, Grok, Claude and Perplexity;
- cross-LLM clustering;
- Notion archival of 325 sessions;
- verbatim collapsing on 278 pages.

These are implementation claims requiring Git/file/runtime verification before promotion.

## Immediate conclusions

1. **Manus is no longer a zero-access source lane.**
2. Notion exposes a large structured Manus-session corpus.
3. Google Drive exposes a separate generated-output and execution-report corpus.
4. The largest remaining gap is direct Manus-native body/output verification and stable identity mapping.
5. Existing collectors, crawlers and session-processing machinery must be reused or reconciled, never recreated.

## Next PARA pass

### M1 — Session identity bridge

Map:

- Manus UID/task ID;
- Notion page ID;
- date/title;
- factsheet ID;
- Git path/commit;
- Mem0 ID where available;
- normalized content hash.

### M2 — YOS-only session filter

Extract the YOS session subset by project, title, themes and depth, then prioritize `landmark` and `substantial` records.

### M3 — Website lineage

Compare `Y-WORLD`, `Y-OS Dashboard` and `Multi-Agent LLM` crawl content against Git repositories and deployed-source claims.

### M4 — Count resolution

Resolve the relationship among 194, 325, 278 and 363 without deleting any representation.

### M5 — Unpublished sites

Register the eight unpublished/no-URL Manus websites as explicit missing source objects. Recovery requires Manus project export or native access.

### M6 — Authority timeline

Date and reconcile:

```text
Notion memory SSOT
→ Git/Markdown durable authority
→ Obsidian human knowledge interface
→ Notion operational/secondary role
```

## Stop rule

No new collector, memory system, API relay, crawler, database or ontology is authorized during this pass.
