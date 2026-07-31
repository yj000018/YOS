# yos_memory — Y-OS Shared Memory Package

**Version:** 1.0.0 — Phase 4 (MPX-20260731-YOS-MEMORY-GIT-MEM0-REFACTOR)
**Status:** Active — Production-ready on `refactor/memory-git-mem0`

---

## Architecture

```
yos_memory/
├── config.py             # Config singleton — env-based, zero secrets hardcoded
├── ids.py                # generate_global_uid, generate_content_hash, generate_memory_key
├── schemas.py            # validate_frontmatter, create_base_frontmatter (schema yos-memory/v1)
├── frontmatter.py        # read_markdown / write_markdown — YAML round-trip
├── git_store.py          # write_canonical_file — atomic POSIX writes
├── mem0_store.py         # Mem0Store — push_projection + search + JWT security guard
├── dedup.py              # DedupState — JSON-persisted, cross-instance deduplication
├── ledger.py             # SessionLedger — atomic CSV
├── session_store.py      # SessionStore — orchestrates Git + Mem0
├── project_store.py      # ProjectStore — living project cards
├── memory_intake.py      # MemoryIntake — generic ingestion entry point
├── legacy_notion_reader.py  # LegacyNotionReader — READ-ONLY Notion bridge
├── pipeline_adapter.py   # PipelineAdapter — non-destructive intercept for llm_distillation_pipeline
└── README.md             # This file
```

---

## Design Principles

1. **Git = canonical store** — all memory objects are Markdown files with YAML frontmatter
2. **Mem0 = projection layer** — semantic search index, not source of truth
3. **Notion = legacy READ-ONLY** — `legacy_notion_reader.py` reads only, never writes
4. **Zero hardcoded secrets** — all credentials via `os.environ`
5. **Atomic writes** — POSIX `os.replace()` on all file operations
6. **Deduplication** — content-hash based, persisted across runs

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `YOS_MEMORY_GIT_REPO` | Yes | Absolute path to the YOS git repo root |
| `MEM0_API_KEY` | Yes | Mem0 API key |
| `MANUS_JWT_TOKEN` | For collection | Manus API JWT (never hardcode) |
| `MANUS_CLIENT_ID` | For collection | Manus API client ID |
| `YOS_MEMORY_ADAPTER` | Optional | Set to `1` to enable pipeline_adapter intercept |

---

## Usage

### Archive a session

```python
from yos_memory.session_store import SessionStore

store = SessionStore()
result = store.archive_session(
    source="Manus",
    source_id="session_uid_123",
    title="My Session Title",
    body_markdown="# Content\n\nFull markdown content...",
    created_at="2026-07-31T00:00:00Z",
    project_id="YOS",
    tags=["memory", "refactor"]
)
# result = {"status": "success", "path": "...", "mem0_status": "pushed"}
```

### Ingest arbitrary memory

```python
from yos_memory.memory_intake import MemoryIntake

intake = MemoryIntake()
result = intake.ingest(
    title="Lesson Learned: JWT rotation",
    content="Always rotate JWTs before committing to public repos.",
    source="manual",
    tags=["security", "jwt"]
)
```

### Search memory (Mem0)

```python
from yos_memory.mem0_store import Mem0Store

store = Mem0Store()
results = store.search("memory refactor architecture", user_id="yannick", limit=5)
```

### Read legacy Notion (READ-ONLY)

```python
from yos_memory.legacy_notion_reader import LegacyNotionReader

reader = LegacyNotionReader()
pages = reader.list_pages(database_id="0720db9b-5e1d-41a2-bd0c-6721fe0dab94")
```

---

## Canonical File Schema (yos-memory/v1)

Every memory object stored in Git follows this frontmatter schema:

```yaml
---
schema: yos-memory/v1
uid: MEM-20260731-abc123
source: Manus
source_id: native_session_id
title: Session Title
created_at: 2026-07-31T00:00:00Z
archived_at: 2026-07-31T12:00:00Z
project_id: YOS
tags:
  - memory
  - refactor
content_hash: sha256:abcdef...
---
```

---

## Skills Integration Map

| Manus Skill | Script | Integration |
|---|---|---|
| `session-synthesis` | `archive_to_notion.py` | `SessionStore.archive_session()` |
| `memory-manager` | `archive_conversation.py` | `SessionStore.archive_session()` |
| `memoriser` | `example.py` | `MemoryIntake.ingest()` |
| `mem0-sync` | *(obsolete)* | Handled natively by `Mem0Store` |
| `memory-pipeline` | `run_pipeline.py` | `MANUS_JWT_TOKEN` env var |

---

## Migration History

| Phase | Commit | Description |
|---|---|---|
| Phase 1 | `a86a093` | Package creation + 23 unit tests |
| Phase 2 | `1b71124` | Script migration (delta_sync, process_ledger, pipeline_adapter) |
| Phase 3 | `85f39df` | Skills wrappers (session-synthesis, memory-manager, memoriser) |
| Phase 4 | *(current)* | Documentation + SKILL.md updates |

---

## Tests

```bash
cd yos-automations/scripts/yos-llm-pipeline
python3 -m pytest tests/test_yos_memory.py -v
```

23 tests — all passing.
