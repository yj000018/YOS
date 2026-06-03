---
name: yos-mmm
description: Y-OS Multi-session Multi-LLM Memory Management (MMM) v2.0. Provides Session Load (I2), Knowledge Load (I3), Session Replay (I4), Archive Pipeline, Native Memory Engine (yos_memory), Audit Trail (yos_audit), Memory Graph (yos_memory_graph), Sync, and Backup. Use when Yannick asks to load context, recall a project, archive a session, sync memory, backup data, view audit trail, or visualize memory cloud.
---

# Y-OS MMM — Memory Management Skill v2.0

## System Overview

The MMM stack manages Yannick's persistent memory across all sessions and LLMs.

**Architecture:**
```
MMM v2.0
├── PROFILE MEM  (native Manus — auto-injected)
│   ├── UI Profile       → Manus settings
│   └── Native MEM       → Manus related_knowledge
└── AMM  (Y-OS extension)
    ├── yos_memory.py    → Native memory engine (ADD/UPDATE/DELETE/NONE + dedup)
    ├── ChromaDB local   → semantic embeddings (snippets + sessions + memory_v2)
    ├── mem0 cloud       → cross-LLM injection via Chrome extension
    ├── yos_audit.py     → Universal sandbox audit trail
    ├── yos_memory_graph → memory-cloud visualization (D3.js + Obsidian)
    └── Notion
        ├── SSA          → Session Synthetic Archive
        └── KOR          → Knowledge Object Repository
    + Git SCA            → Session Cold Archive (verbatim JSON)
```

**Config file:** `/home/ubuntu/yos/mmm/yos_config.yaml`
**Scripts dir:** `/home/ubuntu/yos/mmm/scripts/`

---

## Injection Levels

| Code | Name | Trigger | Source |
|---|---|---|---|
| I1 | Profile Inject | Auto / every prompt | Native Manus |
| I2 | Session Load | Auto / session start | ChromaDB embeddings |
| I3 | Knowledge Load | Manual | ChromaDB + KOR Notion |
| I4 | Session Replay | Manual | SSA Notion (specific session) |

---

## Core Workflows

### I2 — Session Load (automatic context at session start)

**Trigger:** User starts a new session, or says "load session context" / "session load"

**Steps:**
1. Detect project/theme from first prompt (keyword match or embedding similarity)
2. Run: `python3.11 /home/ubuntu/yos/mmm/scripts/yos_context_loader.py --mode session --query "[detected_topic]"`
3. Inject the returned context block at the top of the response
4. Inform user: "Session context loaded for: [topic]"

**Example command:**
```bash
python3.11 /home/ubuntu/yos/mmm/scripts/yos_context_loader.py \
  --mode session --query "Y-OS architecture"
```

---

### I3 — Knowledge Load (full context on demand)

**Trigger:** User says "load context [project/topic]", "knowledge load [X]", "rappelle-toi tout sur [X]"

**Steps:**
1. Extract project/topic from user request
2. Run context loader in full mode (ChromaDB + KOR):
```bash
python3.11 /home/ubuntu/yos/mmm/scripts/yos_context_loader.py \
  --mode knowledge --query "[topic]"
```
3. Inject the full context block
4. Inform user: "Full context loaded for: [topic] — [N snippets, M sessions]"

---

### I4 — Session Replay (replay a specific past session)

**Trigger:** User says "replay session [title/date]", "continue session [X]", "load SSA [X]"

**Steps:**
1. If no specific session given, list recent SSAs:
```bash
python3.11 /home/ubuntu/yos/mmm/scripts/yos_context_loader.py --mode replay
```
2. Present a numbered picklist to user
3. Load selected session:
```bash
python3.11 /home/ubuntu/yos/mmm/scripts/yos_context_loader.py \
  --mode replay --session-id "[session_id]"
```

---

### Archive — Archive current session

**Trigger:** User says "archive session", "archive this conversation", "save session"

**Steps:**
1. Ask user for session title if not provided
2. Summarize the current conversation (key decisions, facts, actions)
3. Run archive pipeline:
```bash
python3.11 /home/ubuntu/yos/mmm/scripts/yos_archive_pipeline.py \
  --session-text "[full_conversation_summary]" \
  --title "[session_title]"
```
4. Report: session_id, facts extracted, SCA path, Notion SSA link, memory_added

---

### Memory — Native memory engine

**Trigger:** User says "mémorise", "ajoute à la mémoire", "qu'est-ce que tu sais sur..."

**Commands:**
```bash
# Ajouter un fait
python3.11 /home/ubuntu/yos/mmm/scripts/yos_memory.py add "Fait à mémoriser" --source "session_id"

# Recherche sémantique
python3.11 /home/ubuntu/yos/mmm/scripts/yos_memory.py search "requête" -n 5

# Stats
python3.11 /home/ubuntu/yos/mmm/scripts/yos_memory.py stats
```

**Note:** Le modèle SentenceTransformer prend ~17s au premier appel — normal.

---

### Memory Graph — Visualisation memory-cloud

**Trigger:** User says "visualise ma mémoire", "memory cloud", "memory graph"

**Commands:**
```bash
# Générer HTML + Obsidian vault
python3.11 /home/ubuntu/yos/mmm/scripts/yos_memory_graph.py all

# HTML seul (D3.js interactif)
python3.11 /home/ubuntu/yos/mmm/scripts/yos_memory_graph.py html
# Ouvrir : /home/ubuntu/yos/mmm/exports/memory_cloud.html

# Obsidian vault seul
python3.11 /home/ubuntu/yos/mmm/scripts/yos_memory_graph.py obsidian
# Vault : /home/ubuntu/yos/mmm/exports/obsidian_vault/
```

---

### Audit Trail — Log universel sandbox

**Trigger:** User says "audit trail", "qu'est-ce qui s'est passé", "undo", "snapshot"

**Commands:**
```bash
# Status global
python3.11 /home/ubuntu/yos/mmm/scripts/yos_audit.py status

# 20 dernières entrées
python3.11 /home/ubuntu/yos/mmm/scripts/yos_audit.py tail -n 20

# Filtrer par catégorie
python3.11 /home/ubuntu/yos/mmm/scripts/yos_audit.py tail -n 20 -c ARCHIVE

# Logger une action
python3.11 /home/ubuntu/yos/mmm/scripts/yos_audit.py log CATEGORY action "description" --status success

# Snapshot (point de restauration)
python3.11 /home/ubuntu/yos/mmm/scripts/yos_audit.py snapshot --label "avant_test"

# Undo (restaurer un snapshot)
python3.11 /home/ubuntu/yos/mmm/scripts/yos_audit.py undo --snapshot-id "[id]"
```

**Catégories standards:** ARCHIVE, MEMORY, BACKUP, SYNC, FILE, TEST, SYSTEM

---

### Sync — Sync ChromaDB ↔ mem0 cloud

**Trigger:** User says "sync memory", "sync mem0", or scheduled

**Steps:**
```bash
# Stats first
python3.11 /home/ubuntu/yos/mmm/scripts/yos_sync.py --stats

# Push local → cloud
python3.11 /home/ubuntu/yos/mmm/scripts/yos_sync.py --direction local_to_cloud

# Full bidirectional sync
python3.11 /home/ubuntu/yos/mmm/scripts/yos_sync.py --direction both
```

---

### Backup — Backup to GDrive

**Trigger:** User says "backup mmm", "backup memory", or scheduled

**Steps:**
```bash
python3.11 /home/ubuntu/yos/mmm/scripts/yos_backup.py
```

**Note:** Si le token GDrive est expiré, utiliser `manus-upload-file` pour backup manuel.

---

## Stats & Health Check

```bash
python3.11 /home/ubuntu/yos/mmm/scripts/yos_archive_pipeline.py --stats
python3.11 /home/ubuntu/yos/mmm/scripts/yos_sync.py --stats
python3.11 /home/ubuntu/yos/mmm/scripts/yos_memory.py stats
python3.11 /home/ubuntu/yos/mmm/scripts/yos_audit.py status
```

---

## Key Files

| File | Purpose |
|---|---|
| `yos_config.yaml` | All parameters — edit here, never in scripts |
| `scripts/yos_context_loader.py` | Core injection engine (I2/I3/I4) |
| `scripts/yos_archive_pipeline.py` | Archive + index sessions |
| `scripts/yos_memory.py` | Native memory engine (prompts Y-OS-aware + dedup) |
| `scripts/yos_memory_graph.py` | Memory-cloud visualization (D3.js + Obsidian) |
| `scripts/yos_audit.py` | Universal sandbox audit trail |
| `scripts/yos_sync.py` | Bidirectional sync ChromaDB ↔ mem0 cloud |
| `scripts/yos_backup.py` | Backup to GDrive |
| `scripts/yos_utils.py` | Shared utilities |
| `exports/memory_cloud.html` | Latest memory-cloud visualization |
| `exports/obsidian_vault/` | Latest Obsidian vault export |

---

## Notion IDs (configured in yos_config.yaml)

- SSA Database: `ebafd590ce9245c79fe7068f7ca6d415`
- KOR Database: `f2c0bc6c54cd46eea663f7b2952fc967`
- Design Page: `31835e218cf881c587c4e5fcca8bc65e`

---

## Current State (2026-03-04)

| Metric | Value |
|---|---|
| ChromaDB sessions | 11 |
| ChromaDB snippets | 143 |
| yos_memory_v2 facts | 21 |
| mem0 cloud snippets | 85 |
| Notion SSA | ✅ Operational |
| Notion KOR | ✅ Created |
| Audit trail | ✅ Active |
| Memory graph | ✅ 30 nodes, 49 links |

---

## Separator Protocol (Y-OS Internal)

When Yannick sends `——`, respond with:
`=========== N N N N N N N N N N N N ===========`
where N is the next number in sequence 1→9→1.
This is a visual bookmark for scrolling in long sessions on iOS.
