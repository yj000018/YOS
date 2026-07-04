# yOS MPM — Canon: Manus `MP` Command Behavior v2

> **Version:** 2.0.0
> **Status:** CANONICAL
> **Supersedes:** mpm-command-taxonomy.md §MPM Manager menu (v1.x menu-first behavior)
> **Source:** Architect & Guardian — 2026-07-04
> **Bootstrap note:** This doc lives in `kap-control-plane` (bootstrap runtime). Final home: `yOS Backbone / MPM` pending topology gate.

---

## 1. Default Behavior — Auto-Run

```
MP
```

**Means:**

> Fetch the next ready Mega Prompt packet from Git, execute it, write the structured Mega Prompt Report back to Git, then stop for source-LLM review.

**Rule:**

> If exactly one unprocessed ready MP exists and no risk/ambiguity is detected: run it immediately.

No menu. No extra confirmation. No friction.

---

## 2. Auto-Run Safety Check

Before running, Manus MUST check the MP frontmatter for any of the following `risk_flags`:

| Risk Flag | Description |
| :--- | :--- |
| `source_mutation` | Any write to live source corpus |
| `github_push` | Push to canonical repos (Y-WORLD, yos-cognitive-os) |
| `gdrive_mutation` | Any GDrive write |
| `icloud_mutation` | Any iCloud write |
| `merge_execution` | Actual merge of content |
| `canonicalization_execution` | Executing canonicalization |
| `destructive_deduplication` | Deleting or overwriting source files |
| `broad_scan` | Unbounded filesystem or cloud scan |
| `ludivine_content_access` | Any access to LUDIVINE vault content |
| `notion_body_block_export` | Exporting Notion page bodies |
| `unclear_authorization` | No explicit A&G authorization for destructive action |
| `unclear_target` | Ambiguous target repo/folder/source |

If **any** risk flag is present or inferred: **do not auto-run** → trigger Exception Case 1 micro-menu.

---

## 3. Exception Cases — Micro-Menu Only

### Exception 1 — Ambiguity or Risk Detected

```
Risk or ambiguity detected.

1. Explain blocker
2. Request clarification
3. Mark MP as blocked
4. Cancel
```

### Exception 2 — Multiple Ready MPs

```
Multiple ready MPs found.

1. Run next recommended MP
2. Run latest MP
3. Show ready queue
4. Run specific MP by ID
5. Archive/supersede stale queue entries
6. Cancel
```

### Exception 3 — No MP Available

```
No ready MP found in queue.
Use `MP queue` to inspect queue/status.
```

*(Short info message only — no full menu.)*

---

## 4. Explicit Commands Supported

| Command | Behavior |
| :--- | :--- |
| `MP` | Auto-run if 1 safe ready MP; else exception handler |
| `MP next` | Run next ready MP (same as `MP`) |
| `MP latest` | Run most recently created ready MP |
| `MP queue` | Show full queue with status |
| `MP run <mp_id>` | Run specific MP by ID |
| `MP status` | Show ledger summary |
| `MP clear queue` | Archive/supersede stale entries (requires confirmation) |
| `MP archive stale` | Archive entries older than threshold (requires confirmation) |

---

## 5. Canonical Summary

```
MP = auto-run by default if one safe ready MP exists.

Micro-menu only if:
1. ambiguity/risk detected;
2. multiple unprocessed MPs;
3. no MP exists → info message only.

Manus MP is auto-run by default, not menu-first.
Menus are exception handlers, not the normal path.
```

---

## 6. Deletion Policy

Deletion of queue entries must **never** be automatic.

- Require explicit user confirmation.
- Preserve traceability: move to `superseded/` folder, update ledger JSON.
- Never hard-delete without A&G authorization.

---

*Architect & Guardian — 2026-07-04 | Implemented by Manus*
