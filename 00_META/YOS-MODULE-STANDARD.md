# Y-OS Module Standard

## Philosophie
Un module Y-OS n'est pas un simple script. C'est un composant cognitif et fonctionnel complet qui doit s'intégrer de manière prévisible dans l'architecture globale.

Ce document définit la structure canonique à 8 couches (8-Layer Template) que tout nouveau module Y-OS doit respecter.

## Les 8 Couches du Standard Y-OS

Chaque module Y-OS doit implémenter ou documenter les couches suivantes :

### 1. Architecture & Rôle
- **Objectif clair** : Une phrase décrivant ce que fait le module et ce qu'il ne fait pas.
- **Périmètre** : Les limites du module (ex: `yos-notif` gère l'envoi, pas le formatage des logs).
- **Dépendances** : Quels autres modules ou nœuds (CC, Mac, N100) sont requis.

### 2. Exécution & Code-Interface
- **Méthodes d'invocation** :
  - *Auto-launch* : Déclenché par le Kernel (yos-bootstrap) ?
  - *On-request* : Appelé par un autre module ?
  - *Manuel* : Via commande CLI ou menu Y-OS ?
  - *Auto-schedule* : Via cron ou pm2 ?
- **Interface Code** : L'API Python ou Bash exposée (ex: `yos_notif.send(msg, level)`).

### 3. Interfaces avec autres Systèmes
- **Entrées (Inputs)** : D'où viennent les données ? (API externes, fichiers locaux, autres modules).
- **Sorties (Outputs)** : Où vont les données ? (Telegram, xbar, GitHub, Notion).

### 4. Référentiels & Data Source
- **Ledger / Registry** : Où l'état du module est-il stocké ? (ex: `state.json`, `/tmp/locks/`).
- **Source de Vérité** : Quel est le système maître pour les données manipulées ? (ex: GitHub pour le code, 1Password pour les secrets).

### 5. Maintenance & Hygiène du Système
- **Nettoyage automatique** : Comment le module nettoie-t-il ses traces ? (ex: suppression des locks zombies).
- **Protocole de mise à jour** : Comment mettre à jour le module sans casser le système ?

### 6. Logs & Reporting Auto
- **Niveaux de log** : INFO, WARN, ERROR, DEBUG.
- **Destination** : Où sont écrits les logs ? (ex: `/home/ubuntu/yos/ledger/logs/`).
- **Format** : Standard Y-OS (Timestamp ISO 8601 | Module | Niveau | Message).

### 7. Documentation & Tool Fact Sheet
- **TOOL-FACT-SHEET.md** : Doit exister dans `02_AGENTS/<module>/`.
- **AGENTS.md** : Mise à jour si le module introduit une nouvelle règle canonique ou modifie l'infrastructure.

### 8. Représentation Visuelle (Diagramme)
- **Excalidraw** : Un diagramme clair montrant les flux d'information et les interactions entre les composants du module. Doit être lisible par l'utilisateur en 30 secondes.

---

## Exemple d'Application : Module NOTIF

*(Voir la documentation spécifique du module NOTIF pour l'implémentation de ce standard).*
