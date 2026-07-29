# KAP Source — Manus Knowledge Entries

> **Source ID:** SF-MAN-KNOWLEDGE  
> **Type:** System Source — Manus Settings/Knowledge  
> **Acquisition method:** Playwright / My Browser (no API available)  
> **Status:** Active  
> **First capture:** 2026-07-29

---

## Description

Les **Manus Knowledge Entries** sont les fiches système injectées par Manus à chaque session via `Settings > Knowledge`. Elles constituent la mémoire persistante active de l'agent Manus.

Cette source est à saturation de quota — le nombre d'entrées dépasse la limite système.

---

## Structure des captures

Chaque capture est un fichier versionné :

```
YYYY-MM-DD_capture.md     ← snapshot brut extrait via Playwright
YYYY-MM-DD_consolidated.md ← version après consolidation LLM
```

---

## Workflow KAP

```
Manus Settings/Knowledge (source)
    ↓ Playwright capture (My Browser)
03_SOURCES/manus-knowledge-entries/YYYY-MM-DD_capture.md
    ↓ LLM consolidation (Claude Opus)
03_SOURCES/manus-knowledge-entries/YYYY-MM-DD_consolidated.md
    ↓ Playwright réécriture
Manus Settings/Knowledge (destination mise à jour)
```

---

## Contraintes

- Aucune API Manus pour lire/écrire les Knowledge entries
- Accès exclusivement via interface web (My Browser requis)
- Quota = nombre d'entrées (pas taille) — objectif : réduire à < 20 entrées actives
