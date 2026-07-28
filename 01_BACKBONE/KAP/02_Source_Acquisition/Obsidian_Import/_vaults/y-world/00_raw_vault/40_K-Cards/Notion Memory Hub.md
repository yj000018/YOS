---
type: k-card
domain: Y-OS
tags: [memory, notion, database, yos]
created: 2026-05-29
status: active
---

# Notion Memory Hub

The **Notion Memory Hub** is the persistent, structured cloud database of [[Y-WORLD]]. It serves as the long-term semantic memory for both the human operator (Yannick) and the AI agents [[Manus Operations]].

## Database Structure

The hub is divided into three primary databases:
1. **Sessions Database**: Logs every AI interaction session with structured metadata (duration, cost, focus, outcomes).
2. **Projects Database**: Tracks all active initiatives across [[CasaTAO]], [[ARC Anandaz]], and [[Y-Publishing]].
3. **Knowledge Base**: Stores persistent, public-by-default concepts and resources.

## Synchronization Loop

```
[Obsidian Vault] ──(Obsidian Git)──> [GitHub Private Repo]
       │                                     ▲
 (n8n Sync)                              (Sync Node)
       ▼                                     │
[Notion Memory Hub] ◄────────────────────────┘
```\n