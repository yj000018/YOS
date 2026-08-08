# Y-OS Dashboard Architecture (Notion)

**Concept :** Le Dashboard Y-OS dans Notion n'est pas un wiki documentaire. C'est une **interface opérationnelle centralisée** conçue pour être lue par Yannick et mise à jour dynamiquement par les agents IA (Manus, scripts cron).

---

## 1. Structure des Bases de Données (Backend)

Le dashboard repose sur 4 bases de données relationnelles principales.

### DB 1 : 📱 Fleet (Devices)
Inventaire dynamique des appareils physiques et virtuels.
- **Champs :** ID (ex: AND-001), Nom, Type (Tablette, Téléphone, Montre, Serveur), Statut (🟢 Actif, 🔴 Offline, 🟡 Warning), Batterie %, Stockage %, Dernière synchro (Date).
- **Mis à jour par :** `health_probe.py` via API Notion.

### DB 2 : ✅ Action Items (Tâches)
Tâches manuelles requises de l'utilisateur ou issues de développement.
- **Champs :** Nom, Priorité (P1-P4), Statut (To Do, In Progress, Done), Device (Relation → Fleet), Type (Setup, Maintenance, Bug, Feature), Due Date.
- **Mis à jour par :** Manus (création), Yannick (complétion).

### DB 3 : 🔔 Alertes & Logs
Journal des événements système importants.
- **Champs :** Message, Sévérité (Info, Warning, Critical), Source (Cron, Manus, HA), Date.
- **Mis à jour par :** `yos-notify` (qui écrit dans Notion en plus de Telegram).

### DB 4 : 🔗 Key Links & Shortcuts
Raccourcis rapides vers les outils et interfaces Y-OS.
- **Champs :** Nom, URL, Catégorie (Admin, Dev, Dashboard).
- **Mis à jour par :** Yannick/Manus.

---

## 2. Structure de la Page Dashboard (Frontend)

La page principale `🤖 Y-OS Command Center` agrège ces bases via des **vues liées (Linked Views)** pour présenter l'information de manière actionnable.

### 🔴 Section 1 : Attention Requise (P1)
- Vue de `Action Items` filtrée sur : `Statut != Done` ET `Priorité = P1`.
- Vue de `Alertes & Logs` filtrée sur : `Sévérité = Critical` (24h).

### 📱 Section 2 : Fleet Status
- Vue de `Fleet` en mode Galerie (cartes).
- Affiche visuellement la batterie, le stockage et le statut (vert/rouge) de chaque device.

### 📋 Section 3 : Pipeline (Tâches P2-P4)
- Vue de `Action Items` en mode Kanban (Board) groupé par `Statut`.
- Permet à Yannick de voir ce qui arrive et de glisser les cartes.

### ⚡ Section 4 : Quick Links
- Vue de `Key Links` en mode Liste simple.
- Liens vers GitHub YOS, Todoist, Tailscale Admin, etc.

---

## 3. Pipeline d'Automatisation (Manus ↔ Notion)

1. **Création du Dashboard :** Manus utilise le MCP Notion pour créer la page racine, les 4 bases de données avec leurs schémas exacts, et les vues liées.
2. **Peuplement initial :** Manus injecte les données actuelles (AND-001, les 34 tâches Todoist répliquées ou liées, les liens GitHub).
3. **Mise à jour continue :** Les scripts cron sur le Cloud Computer (ex: `health_probe.py`) seront mis à jour pour pousser les métriques (batterie, stockage) directement dans la DB `Fleet` via l'API Notion.
