# METADATA-PILOT-RUNBOOK

> Y-OS / KAP Cognitive Architecture
> Gate: PROCESS-DOCS-RUNBOOK-GATE
> Last Updated: 2026-07-03

## 1. Definition of a Metadata-Only Pilot

A metadata-only pilot is a non-invasive scan of a Source Instance designed to catalog available Source Objects without ingesting their internal content. It maps the terrain before extraction begins.

## 2. Strict Boundaries

**Allowed Actions:**
- List files, directories, databases, or tables.
- Read file names, titles, paths, and URLs.
- Read timestamps (created, modified).
- Read object types (markdown, json, pdf, page).
- Read structural relations (parent-child folders).

**Forbidden Actions:**
- Reading file bodies.
- Extracting text snippets.
- Summarizing content.
- Creating Source Fragments.
- Extracting Claims.

## 3. Execution by Source Channel

### A. Git Repositories
- Use `git ls-tree` or GitHub API `GET /repos/{owner}/{repo}/git/trees/{sha}?recursive=1`.
- Capture paths, blobs, and commit timestamps.

### B. Obsidian / Markdown
- Use filesystem `find` or `ls -R`.
- Capture `.md` file names, folder structure, and file creation dates.
- Do NOT `cat` or `read` the files.

### C. Notion
- Use Notion API `POST /v1/search` with `filter: { property: "object", value: "page" }`.
- Extract `id`, `title`, `url`, `created_time`, `last_edited_time`.
- Do NOT call `GET /v1/blocks/{block_id}/children`.

### D. ChatGPT Capture Packs / Manus Outputs
- If already in Git, read markdown headers (`#`, `##`) and frontmatter.
- Do NOT parse paragraphs.

### E. Generated Sites / Apps
- Perform Provenance Census: map URLs/routes to GitHub repos or Replit project IDs.
- Do NOT scrape site text.

## 4. Output Artifacts

The output of a Metadata Pilot must be a list of candidate Source Objects, which are then registered in `SOURCE-OBJECT-REGISTRY.md` with canonical `SO-*` IDs.

## 5. Blockers & Readiness

**Log a Blocker IF:**
- API rate limits are hit during listing.
- File count exceeds 10,000 (requires chunking strategy).
- Folder structure is cyclical/recursive.

**Ready for Content Pilot WHEN:**
- All objects are registered in `SOURCE-OBJECT-REGISTRY.md`.
- Guardian Architect approves the transition to Content Pilot for specific `SO-*` IDs.

---

## QC-RULE-001 — Post-Scan Metadata Sanity Check (MANDATORY)

> Added: 2026-07-03 — following OBSIDIAN-METADATA-CORRECTION-PATCH-v1.1 incident

After every metadata scan, before proceeding to any downstream gate, verify:

| Check | Threshold | Action if failed |
|---|---|---|
| Frontmatter coverage | ≥ 50% for Obsidian vaults | Re-scan mandatory |
| Wikilinks per file | ≥ 1.0 average for active vaults | Re-scan mandatory |
| Files with empty metadata | < 20% | Investigate + re-scan |
| Scanner warnings / 404s | Zero silent errors | Fix encoding + re-scan |

**Rationale:** A well-maintained Obsidian vault has 80-100% frontmatter coverage. Coverage below 50% is a strong signal of a scanner encoding or access issue, not a vault characteristic.

**Implementation:** Add a `post_scan_qc()` function to all scanner scripts that computes these metrics and raises an **explicit error** (not a warning) if thresholds are not met. Silent failures must never be allowed to propagate.

**Incident reference:** Y-WORLD v1.0 scan — 213/235 files with spaces caused silent GitHub API 404s. Result: 7% FM coverage reported as valid. Fixed in scanner v1.1 with `urllib.parse.quote()` per path segment.
