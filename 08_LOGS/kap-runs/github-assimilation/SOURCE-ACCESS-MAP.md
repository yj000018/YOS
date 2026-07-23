# Source Access Map — Definitive YOS Canon

**Run:** `KAP-GITHUB-ASSIMILATION-2026-07-23`  
**Status:** ACTIVE  
**Purpose:** record which YOS source systems are accessible, how they can be queried, and what evidence remains unavailable.

## Access status vocabulary

- `DIRECT_READ` — source content can be searched and fetched now.
- `PARTIAL_READ` — only indexed summaries, exported files or selected artifacts are available.
- `REFERENCE_ONLY` — sources are named but their content is not directly accessible in the current environment.
- `USER_EXPORT_REQUIRED` — an export, archive or mounted folder is required.
- `NOT_YET_CENSUSED` — access may exist but the source has not yet been systematically inventoried.

## Current source map

| Source system | Access | Current capability | Current limitation | Immediate action |
|---|---|---|---|---|
| GitHub | `DIRECT_READ` | Repositories, metadata, files, commits, branches, PRs, issues and writes to audit branch | No automatic full-estate clone or branch-tree export in one operation | Continue eight-lane repository archaeology |
| Notion | `DIRECT_READ` | Semantic search, page/database fetch, discussions and database queries | Ranked search is not an exhaustive workspace export; root traversal remains required | Build root/page census and fetch all YOS authority/candidate pages |
| ChatGPT File Library | `DIRECT_READ` | Search and open uploaded/exported YOS reports, Fact Sheets and artifacts | Not equivalent to all raw conversations; duplicates and derived reports exist | Register every YOS file and map it to raw conversation/archive lineage |
| ChatGPT internal memory | `PARTIAL_READ` | Existing July 12 exhaustion corpus and persistent project context | Raw transcript completeness cannot be guaranteed | Treat exhaustion report as source map, not verbatim evidence |
| Current ChatGPT project conversation | `DIRECT_READ` | Current decisions and audit artifacts | Only active context is continuously available | Preserve new decisions in Git immediately |
| Manus historical workspace | `REFERENCE_ONLY` | Notion and Git artifacts identify Manus missions, sessions and outputs | Current connector cannot enumerate historical Manus sessions/projects | Obtain Manus export or dedicated historical data access |
| Obsidian / Markdown vaults | `USER_EXPORT_REQUIRED` | Existing reports name expected vaults, docs and context packs | No vault is mounted or connected in this run | Materialize or export the relevant Markdown tree |
| Google Drive / cloud files | `NOT_YET_CENSUSED` | Notion pages contain Drive links and references | No systematic Drive census has been completed | Search connected source or obtain folder export |
| Local filesystem / pCloud | `USER_EXPORT_REQUIRED` | User has local/cloud synchronized stores that may contain YOS material | Not mounted in the current environment | Mount or export relevant roots, then fingerprint content |
| Claude / Gemini / Grok histories | `USER_EXPORT_REQUIRED` | Mentioned in architecture and earlier syntheses | No complete raw conversation archive currently accessible | Export relevant histories and attachments |
| Runtime systems | `REFERENCE_ONLY` | Claims/configuration traces appear in Git, Notion and ChatGPT artifacts | Live state, logs, versions and deployed-source provenance unverified | Perform runtime evidence audit after source census |

## Current conclusions

1. GitHub and Notion can be audited immediately and in parallel.
2. ChatGPT evidence includes the active context, a substantial consolidation corpus and at least one paired JSON/Markdown raw-export lineage.
3. Manus historical sessions are a major evidence gap.
4. Obsidian, local files, pCloud and other LLM histories require export or mounting.
5. No source is exhausted merely because semantic search returns no further high-ranked results.

## Source-completeness rule

A source system reaches `CENSUS_COMPLETE` only when:

- all relevant containers are enumerated;
- relevant items have durable identifiers;
- pagination and archived/hidden areas are checked;
- attachments and child pages are accounted for;
- known references to missing items are registered;
- remaining access gaps are explicit.

## Current gate status

- GitHub source access: **DIRECT / census in progress**
- Notion source access: **DIRECT / census started**
- ChatGPT File Library: **DIRECT / corpus discovery started**
- Manus historical access: **BLOCKED / export required**
- Obsidian/local/cloud files: **BLOCKED / materialization required**
- Other LLM histories: **BLOCKED / export required**
