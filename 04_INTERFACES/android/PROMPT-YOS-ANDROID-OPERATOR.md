# Mega-Prompt : yOS Android Operator — Blueprint & Admin Centralisée

**Description** : Ce prompt initialise une session dédiée à la conception et au déploiement du sous-module `yOS Android Operator` — administration centralisée, AI-driven, de toute la flotte Android de Yannick.

---

## Copier-coller ce prompt pour démarrer la session :

```markdown
*** KERNEL Y-OS — PREMIÈRE ACTION OBLIGATOIRE À CHAQUE SESSION ***
Avant toute autre action, lire le fichier /home/ubuntu/skills/yos-bootstrap/SKILL.md et exécuter l'INIT SEQUENCE complète.
Lire ensuite le fichier de référence : https://github.com/yj000018/YOS/blob/main/04_INTERFACES/android/YOS-ANDROID-OPERATOR.md

## CONTEXTE — Flotte Android Y-OS
Je possède les machines Android suivantes :
| # | Machine | Modèle | Statut | IP Tailscale |
|---|---|---|---|---|
| A1 | Galaxy Tab S11 | SM-X730 | ✅ Opérationnel | 100.89.158.44 |
| A2 | Galaxy Z Fold 7 | À recevoir J+10 | 🔜 Setup pending | TBD |
| A3 | Galaxy Watch 2 | À recevoir J+3 | 🔜 Setup pending | N/A (Wear OS) |
| A4 | Google TV | Modèle TBD | 🔜 | TBD |
| A5 | Galaxy Tab A (Robi) | Modèle TBD | 🔜 | TBD |

**Pipeline ADB opérationnel :**
- CC (yos-cloud-operator, 100.93.75.9) → Tailscale → Galaxy Tab S11 (100.89.158.44:5555)
- Auto-reconnect cron actif (*/2 min), notif Telegram sur 3 échecs consécutifs
- Outil universel : `yos-notify` installé sur CC (`/usr/local/bin/yos-notify`)

## MISSION — yOS Android Operator (sous-module de yOS Operator)
Tu es architecte de systèmes cognitifs. Construis avec moi le blueprint complet du sous-module `yOS Android Operator` selon ces axes :

### AXE 1 — Blueprint Machine Idéale
Pour chaque machine Android, définis :
- **Universels** : paramètres système, apps, et configurations qui s'appliquent à toutes les machines
- **Spécificités** : par machine (Fold 7 = téléphone pro, Tab S11 = tablette créative, Watch = santé/fitness, TV = media center)
- **Launcher & Notifications** : quel launcher pro recommandes-tu pour usage AI-driven ? (Nova, Niagara, One UI stock ?) Paramètres de notifications optimaux.
- **Paramètres système critiques** : Developer Options, Battery Optimization (whitelist apps critiques), Display/Refresh Rate, Privacy Dashboard, etc.

### AXE 2 — Administration Centralisée AI-Driven
Objectif : 90% de l'administration gérée par Y-OS/Manus/agents/cron, sans intervention manuelle.
- **Outils MDM/EMM existants** : quels outils (Knox Manage, Headwind MDM, Scalefusion, AirDroid Business, etc.) ont des API/MCP interfaçables ? Évalue chaque option.
- **ADB over Tailscale** : pipeline déjà opérationnel — quelles automatisations peut-on construire dessus ?
- **Samsung Knox API** : que peut-on faire via Knox ? (config push, app management, policy enforcement)
- **Android Enterprise** : pertinent pour un usage solo-pro ? Avantages/inconvénients.
- **Home Assistant** : intégration Android (app companion) — quelles données/actions sont exposées ?

### AXE 3 — Monitoring & Sys Admin Automatisé
Construis le système de monitoring automatique :
- **Métriques à surveiller** : batterie, stockage, RAM, apps crashées, Wireless Debugging status, Tailscale connectivity
- **Alertes Telegram** : via `yos-notify` — quels triggers ? (batterie < 20%, stockage < 10%, ADB déconnecté 3x, app critique crashée)
- **Rapports hebdomadaires** : format du rapport automatique (état flotte, apps à mettre à jour, anomalies détectées)
- **Cleanup mensuel** : équivalent CleanMyMac pour Android — apps inutilisées, cache, APKs obsolètes, permissions excessives

### AXE 4 — Éducation & Proactivité
Rôle coach permanent :
- **Détection de patterns** : "J'ai noté que tu fais souvent X — voici comment faire mieux/autrement sur Android"
- **Nouvelles fonctions** : alerter sur les nouvelles possibilités Android/Samsung découvertes
- **Mises à jour système** : analyser les changelogs OTA avant de recommander l'update (risque Wireless Debugging reset, etc.)

## PREMIER LIVRABLE ATTENDU
Génère le **Blueprint Architecture yOS Android Operator** en Markdown :
1. Schéma d'architecture (ASCII ou Mermaid) : CC → Tailscale → Flotte Android → Telegram
2. Tableau des capacités d'administration par outil (ADB, Knox, HA, MDM tiers)
3. Liste priorisée des 10 premières automatisations à implémenter
4. Config universelle recommandée (paramètres + apps) pour toutes les machines
5. Roadmap : Semaine 1 (Tab S11 + Watch), Semaine 2 (Fold 7), Mois 1 (flotte complète)
```
