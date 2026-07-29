# Protocole de Maintenance des Outils & API (Y-OS)

Ce protocole définit la boucle de maintenance continue pour les outils (MCP, Skills) et les APIs intégrées dans Y-OS. Il garantit que les capacités du système évoluent en même temps que les écosystèmes externes.

---

## 1. La Boucle de Maintenance Continue

La maintenance n'est pas un événement ponctuel mais une boucle itérative en 4 phases :

1. **Découverte (Discovery)** : Identification de nouvelles capacités.
2. **Exploration (Probing)** : Tests et reverse-engineering.
3. **Documentation (Registry)** : Mise à jour des sources de vérité.
4. **Intégration (Skills)** : Création ou mise à jour des workflows opérationnels.

---

## 2. Phase 1 : Découverte (Discovery)

Les nouvelles capacités émergent de 3 sources principales :

| Source | Méthode d'acquisition | Fréquence |
|--------|-----------------------|-----------|
| **Doc Officielle** | Veille sur les changelogs, release notes, et `llms.txt` des fournisseurs. | Mensuelle |
| **Communauté** | Veille sur les forums, GitHub issues, Reddit, X/Twitter. | Continue |
| **Intuition/Tests** | Déduction de patterns (ex: `user.v1.UserService` suggère `profile.v1.ProfileService`). | Ad-hoc |

### Action de maintenance
Lorsqu'un utilisateur ou un agent signale une nouvelle fonctionnalité potentielle, ouvrir une tâche de découverte :
1. Chercher dans la doc officielle.
2. Si non documenté, chercher dans les forums.
3. Si introuvable, passer en phase d'Exploration (Probing).

---

## 3. Phase 2 : Exploration & Probing (Reverse Engineering)

Pour les APIs non documentées (comme l'API interne gRPC-web de Manus) ou les outils MCP opaques, utiliser le probing systématique.

### Protocole de Probing API Web
1. **Capture Réseau** : Ouvrir l'application cible dans le navigateur Manus (`browser_navigate`).
2. **Interception** : Utiliser `browser_console_exec` pour intercepter les requêtes `fetch` et `XMLHttpRequest`.
3. **Déclenchement** : Simuler l'action utilisateur (`browser_click`).
4. **Analyse** : Capturer l'URL, les headers (notamment l'Auth), et le payload.
5. **Test Actif** : Rejouer la requête modifiée via `browser_console_exec` pour valider les paramètres (ex: découvrir que `title` doit être `name`).

### Protocole de Probing MCP
1. Lister les outils du serveur : `mcp tool.list`.
2. Obtenir le schéma exact : `mcp tool.get`.
3. Tester avec des paramètres minimaux.
4. Tester les limites (pagination, filtres, erreurs).

---

## 4. Phase 3 : Documentation & Tools Registry

Toute découverte validée doit être documentée dans les sources de vérité canoniques de Y-OS.

### 4.1. Hiérarchie de la Documentation

1. **Tools Registry** : Base de données centrale (Notion ou équivalent Git).
2. **Factsheets** : `01_BACKBONE/KAP/02_Source_Acquisition/.../factsheets/`. Description sémantique de l'outil.
3. **API Reference** : Dans le dossier du skill associé (ex: `yos-agents/manus/yos-skills/manus-api/`).
   - `docs/v2/` : Documentation officielle.
   - `internal/` : Endpoints découverts par probing.

### 4.2. Convention de mise à jour (Git)
- Commit message : `docs(api): Add <endpoint_name> discovered via probing`
- Toujours inclure un exemple de payload et de réponse.
- Noter les limites (rate limits, auth requise).

---

## 5. Phase 4 : Intégration (Skills)

La documentation seule est insuffisante ; l'outil doit devenir actionnable.

1. **Création/Mise à jour de Skill** : Modifier le `SKILL.md` pertinent (ex: `memory-manager` pour l'API Knowledge).
2. **Ajout d'un Workflow** : Décrire précisément *quand* et *comment* utiliser la nouvelle capacité.
3. **Fournir le Code** : Inclure le snippet exact (ex: le script JS de bulk create).
4. **Guardrails** : Documenter les pièges (ex: "Ne jamais utiliser `alert()` dans `browser_console_exec`").

---

## 6. Chantier de Mise à Jour Périodique

Pour maintenir l'écosystème à jour, un chantier périodique (ex: mensuel) doit être lancé avec le prompt suivant :

> *"Lance un chantier d'audit des outils Y-OS. 1. Vérifie les changelogs des APIs clés (Manus, Notion, GitHub). 2. Teste les endpoints hypothétiques listés dans `INTERNAL-API-REFERENCE.md`. 3. Mets à jour le Tools Registry et les Skills en conséquence."*

Ce protocole assure que Y-OS ne subit pas l'obsolescence technique mais s'enrichit organiquement au fil du temps.
