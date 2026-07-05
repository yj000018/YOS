# YOS Constitution

> **Version:** 1.0.0 | **Status:** Active | **Last updated:** 2026-07-05

---

## 1. Identity

`YOS` is the single canonical Git repository for the entire yOS system.

Everything important to yOS must be findable in one clear place.

---

## 2. Architecture Decision

```
YOS = the single canonical Git repository for the entire yOS system.
```

**KAP is a backbone module, not a project.**

```
Correct:   YOS/01_BACKBONE/KAP/
Incorrect: YOS/07_PROJECTS/KAP/
```

**MPM is a backbone module.**

```
YOS/01_BACKBONE/MPM/
```

---

## 3. Source of Truth Hierarchy

| Layer | Source | Format |
| :--- | :--- | :--- |
| Machine-readable data | JSON | Canonical |
| Human-readable views | Markdown | Generated |
| Knowledge base | Obsidian vault | `05_KNOWLEDGE_DOMAINS/Y-WORLD/` |
| Governance | ADRs + policy-manifest | `01_BACKBONE/GOVERNANCE/` |

**Rule:** Never edit MD as source of truth. Update JSON first, regenerate MD.

---

## 4. Module Ownership

| Module | Path | Owner |
| :--- | :--- | :--- |
| MPM — Mega Prompt Manager | `01_BACKBONE/MPM/` | yOS Backbone |
| KAP — Knowledge Absorption Pipeline | `01_BACKBONE/KAP/` | yOS Backbone |
| Agents | `02_AGENTS/` | yOS Agents |
| Automations | `03_AUTOMATIONS/` | yOS Automations |
| Interfaces | `04_INTERFACES/` | yOS Interfaces |
| Knowledge Domains | `05_KNOWLEDGE_DOMAINS/` | yOS Knowledge |
| Apps & Products | `06_APPS_PRODUCTS/` | yOS Products |
| Source Corpus | `07_SOURCE_CORPUS/` | yOS KAP |
| Logs | `08_LOGS/` | yOS Ops |
| Archive | `99_ARCHIVE/` | yOS Archive |

---

## 5. Absolute Rules

- No destructive deletion without explicit Architect & Guardian approval
- No force push
- No rewrite of Git history
- No live source mutation
- No semantic merge or canonicalization without explicit gate approval
- All migrations must be traceable
- JSON = canonical machine source; MD = generated human-readable view

---

## 6. Bootstrap History

`kap-control-plane` (private repo) is the bootstrap runtime location for MPM and KAP.
It remains operational. Migration to `YOS/01_BACKBONE/` is in progress.
`kap-control-plane` must not be deleted until migration is complete and Guardian-approved.

---

*YOS Constitution v1.0.0 — Architect & Guardian + Manus — 2026-07-05*
