# 📊 Y-OS KAP Dashboard
*(Capture, Absorption & Processing Dashboard)*

**Dernière mise à jour automatique :** 2026-07-31 14:21:36 UTC

Ce tableau de bord centralise le suivi du pipeline complet d'ingestion des données pour l'écosystème Y-OS. Il trace le parcours de chaque donnée depuis son identification jusqu'à sa transformation en *Fact Sheet* enrichie.

---

## 🟢 Pipeline Status Legend

* 🟢 **OK** : Étape complétée à 100% pour le delta identifié.
* 🟡 **En cours** : Traitement partiel ou en attente d'une action automatisée.
* 🔴 **Action Requise** : Bloqué, nécessite une intervention manuelle (export, auth).
* ⚪ **N/A** : Étape non applicable pour cette source.

---

## 🧠 1. Y-OS Cognitif (LLM Sources)
*Sources documentant les processus de pensée, d'architecture et de création.*

| Source | Cutoff Date | Identifié (Total) | Absorbé | Processé | Dédupliqué | Mergé | Synthétisé | Fact Sheet | Status Global |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Manus** | `2026-07-31` | **565** | 565 🟢 | 565 🟢 | 565 🟢 | ⚪ | 565 🟢 | 565 🟢 | 🟢 **100%** |
| **ChatGPT** | *En attente* | **?** | 0 🔴 | 0 🔴 | 0 🔴 | ⚪ | 0 🔴 | 0 🔴 | 🔴 *Bore tunnel* |
| **Claude** | *En attente* | **?** | 0 🔴 | 0 🔴 | 0 🔴 | ⚪ | 0 🔴 | 0 🔴 | 🔴 *Export manuel* |
| **Gemini** | *En attente* | **?** | 0 🔴 | 0 🔴 | 0 🔴 | ⚪ | 0 🔴 | 0 🔴 | 🔴 *Takeout* |
| **Grok** | *En attente* | **?** | 0 🔴 | 0 🔴 | 0 🔴 | ⚪ | 0 🔴 | 0 🔴 | 🔴 *Pas d'export* |

---

## 🌍 2. Universe Knowledge (Context Sources)
*Sources documentant l'univers, les réunions, les mémos et l'environnement.*

| Source | Cutoff Date | Identifié (Total) | Absorbé | Processé | Dédupliqué | Mergé | Synthétisé | Fact Sheet | Status Global |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Plaud** | `2024-12-28` | **7** | 7 🟢 | 7 🟢 | 7 🟢 | ⚪ | 7 🟢 | 7 🟢 | 🟢 **100%** |
| **Fireflies** | `2026-07-31` | **3** | 3 🟢 | 3 🟢 | 3 🟢 | ⚪ | 3 🟢 | 3 🟢 | 🟢 **100%** |
| **Raindrop** | `Unknown` | **10** | 10 🟢 | 10 🟢 | 10 🟢 | ⚪ | 10 🟢 | 10 🟢 | 🟢 **100%** |
| **Granola** | *En attente* | **0** | 0 🟡 | 0 🟡 | 0 🟡 | ⚪ | 0 🟡 | 0 🟡 | 🟡 *Vide* |
| **Otter.ai** | *En attente* | **0** | 0 🟡 | 0 🟡 | 0 🟡 | ⚪ | 0 🟡 | 0 🟡 | 🟡 *Vide* |

---

## 📂 3. Y-OS Vaults (GitHub Structure)
*État de l'organisation interne du dépôt de vérité (`yj000018/YOS`).*

| Vault | Description | Fichiers Actuels | Status |
|---|---|:---:|:---:|
| `00_META` | Configuration, state files, lessons learned | **34** | 🟢 Actif |
| `01_SOURCES` | Données brutes (KAP) | **0** | 🟡 À structurer |
| `02_CENSUS` | Inventaires et index (KAP) | **0** | 🟡 À structurer |
| `03_SYNTHESES` | Synthèses consolidées (KAP) | **0** | 🟡 À structurer |
| `02_AGENTS` | Tool Fact Sheets | **10** | 🟢 Actif |
| `05_AUTOMATION`| Scripts et crons d'ingestion | **3** | 🟢 Actif |

---

## 🔄 Définition du Pipeline (Workflow)

1. **Identifié** : Le volume total d'éléments existant dans la source d'origine à la *Cutoff Date*.
2. **Absorbé** : Données brutes extraites via API, export ou scraping et sauvegardées localement.
3. **Processé** : Données nettoyées, formatées (ex: JSON vers Markdown) et prêtes pour l'analyse.
4. **Dédupliqué** : Vérification des doublons stricts ou sémantiques par rapport à l'existant.
5. **Mergé** : Fusion de données complémentaires (ex: un mémo vocal Plaud lié à une réunion Fireflies). *(Optionnel selon la source)*
6. **Synthétisé** : Analyse sémantique par LLM (Gemini 2.5 Flash) pour extraire l'essence, les entités et le contexte.
7. **Fact Sheet** : Création du livrable final (Markdown avec YAML front matter) et push sur GitHub.

---
*Généré automatiquement par le Cloud Computer Y-OS (`8cd489il`).*
