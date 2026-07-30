# Y-OS Client — Projet Pending
> **Status:** 🅿️ PARKED — 2026-07-30
> **Priorité:** Haute (infrastructure cognitive core)
> **Prérequis:** Bootstrap Y-OS stabilisé + LL Registry opérationnel

---

## Pourquoi ce projet existe

**Problème fondamental identifié le 2026-07-30 :**

Le cerveau reptilien de Y-OS (réflexes automatiques de session) repose actuellement sur le **system prompt Manus** qui dit `"lance yos-bootstrap"`. C'est semi-automatique : ça dépend que Manus obéisse aux instructions, pas d'un vrai trigger système.

**Ce qui manque :** un client Y-OS qui s'exécute **avant** Manus et orchestre les triggers de session de façon garantie, indépendante du LLM. Ce client **est** le KERNEL matérialisé.

---

## Vision

Un **client léger** (CLI ou app) qui agit comme **Startupizer macOS** pour Y-OS :

```
Session start
  → Y-OS Client (pré-cortex)
    ├── Mem0 search(projets actifs) → injection contexte
    ├── AGENTS.md CC → chargé une fois
    ├── Tool registry → index disponible
    └── → Manus (cortex) avec contexte pré-chargé
```

**Lazy tool loading :** la première fois qu'un outil X est utilisé dans la session, le client charge `02_AGENTS/X/TOOL-FACT-SHEET.md` automatiquement. Une seule fois par session (pas à chaque appel).

---

## Pourquoi parqué maintenant

**Décision 2026-07-30 :** le system prompt Manus + skill `yos-bootstrap` est suffisamment robuste pour l'usage actuel. Le client Y-OS apporterait une garantie d'exécution supérieure mais n'est pas bloquant.

**Conditions de réactivation :**
- Bootstrap Manus devient insuffisant (oublis fréquents, contexte perdu)
- Y-OS atteint une maturité nécessitant une orchestration multi-LLM garantie
- Disponibilité pour un sprint dédié (2-3 jours)

---

## Architecture cible (esquisse)

```
yos-client/
├── bootstrap.py          ← session init (Mem0 + AGENTS.md + tool registry)
├── tool_loader.py        ← lazy loading Tool Fact Sheets (1x per session)
├── session_tracker.py    ← track tools used this session
├── config.yaml           ← active projects, default tools
└── README.md
```

**Interfaces possibles :**
- CLI : `yos start` → affiche contexte chargé, puis passe la main à Manus
- macOS app (menu bar) : status Y-OS, trigger bootstrap, log session
- n8n webhook : trigger automatique à l'ouverture d'une session Manus

---

## KERNEL actuel (solution intermédiaire)

En attendant le client, le KERNEL Y-OS est implémenté dans le skill `yos-bootstrap` :

1. **System prompt Manus** → `"*** ALWAYS read skill yos-bootstrap at session start ***"`
2. **yos-bootstrap skill** → Mem0 search + AGENTS.md CC + lazy tool loading (instruction)
3. **Règle lazy loading** : première utilisation d'un outil → lire sa Tool Fact Sheet → garder en contexte pour toute la session

---

## Références

- Skill actuel : `/home/ubuntu/skills/yos-bootstrap/SKILL.md`
- LL Registry : `00_META/LESSONS-LEARNED/`
- Tool Fact Sheets : `02_AGENTS/<tool>/TOOL-FACT-SHEET.md`
- Discussion originale : session Manus 2026-07-30 (ChatGPT pipeline + LL architecture)

---

*Y-OS Client — Projet Pending · yj000018/YOS · 06_APPS_PRODUCTS/yos-client/*
