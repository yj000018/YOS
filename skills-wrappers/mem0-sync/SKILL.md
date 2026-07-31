---
name: mem0-sync
description: "[DEPRECATED — MPX-20260731] Les scripts standalone de ce skill sont obsolètes. La synchronisation Mem0 est désormais intégrée nativement dans yos_memory.Mem0Store (repo YOS, branche main). Utiliser session-synthesis ou memory-manager à la place."
status: deprecated
deprecated_by: MPX-20260731-YOS-MEMORY-GIT-MEM0-REFACTOR
replaced_by: "yos_memory.Mem0Store (yos-automations/scripts/yos-llm-pipeline/yos_memory/)"
---

> ⚠️ **DEPRECATED** — MPX-20260731-YOS-MEMORY-GIT-MEM0-REFACTOR (2026-07-31)
>
> Les scripts de ce skill (`sync_notion_to_mem0.py`, `sync_manus_to_mem0.py`) sont **obsolètes**.
> La synchronisation Mem0 est désormais intégrée nativement dans `yos_memory.Mem0Store`.
>
> **→ Utiliser `session-synthesis` ou `memory-manager` à la place.**
>
> Pour la migration batch des anciennes sessions Notion → Git, voir le MPX `YOS-NOTION-TO-GIT-MIGRATION` (à venir).

---

# Mem0 Sync Pipeline [DEPRECATED]

> Ce skill est conservé pour référence historique uniquement.
> Les scripts ci-dessous ne doivent plus être exécutés.

## Migration vers yos_memory

Depuis MPX-20260731, la sync Mem0 est gérée par :

```python
from yos_memory.mem0_store import Mem0Store
from yos_memory.config import YosMemoryConfig

config = YosMemoryConfig()
store = Mem0Store(config)
store.push_projection(uid, title, summary, metadata)
```

Ce code est appelé automatiquement par `session_store.archive_session()` et `memory_intake.ingest()`.

## Anciens modes (OBSOLÈTES — ne pas utiliser)

### ~~Mode 1 : Notion → Mem0~~ (OBSOLÈTE)

```bash
# NE PAS UTILISER — remplacé par yos_memory.Mem0Store
# python /home/ubuntu/skills/mem0-sync/scripts/sync_notion_to_mem0.py
```

### ~~Mode 2 : Manus API → Mem0~~ (OBSOLÈTE)

```bash
# NE PAS UTILISER — remplacé par yos_memory.Mem0Store
# python /home/ubuntu/skills/mem0-sync/scripts/sync_manus_to_mem0.py --input /chemin/vers/sessions.json
```

## Format des données dans Mem0 (référence)

Les mémoires sont poussées avec `user_id: yannick` et des métadonnées structurées :

```json
{
  "metadata": {
    "source": "session_synthesis",
    "uid": "id_de_la_session",
    "project": "yOS",
    "type": "session_card",
    "date": "2026-07-31"
  }
}
```
