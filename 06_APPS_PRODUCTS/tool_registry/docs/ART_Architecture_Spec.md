# ART (Autonomous Resource & Tool) — Spécification d'Architecture v1.1

## 1. Vision et Objectifs
ART est le module d'intelligence des outils de Y-OS. Il s'abstrait de la couche d'exécution de chaque LLM (Manus, ChatGPT, Claude) pour gérer un registre centralisé, autonome et intelligent de tous les outils externes SaaS et API.

Ses trois missions principales :
1. **Inventaire et Connaissance (Tool Fact Sheets) :** Maintenir une base de connaissances cross-LLM sur ce que chaque outil peut faire, comment y accéder, et à quel prix.
2. **Monitoring et Auto-Remédiation (Health Checks) :** Vérifier activement si l'accès est fonctionnel et réparer les accès cassés de manière autonome.
3. **Routing Intelligent :** Décider quel outil utiliser face à une tâche donnée, en optimisant la matrice Coût × Performance × Autonomie.

---

## 2. Modèle de Données : La Tool Fact Sheet Enrichie

La Fact Sheet n'est plus un simple document texte, c'est un objet structuré qui nourrit l'intelligence de Y-OS.

```json
{
  "id": "canva",
  "name": "Canva",
  "category": "Design/Video",
  "capabilities": {
    "image_generation": { "max_resolution": "4K", "quality": "high", "speed": "fast" }
  },
  "membership": {
    "status": "active",
    "plan": "Pro",
    "cost_per_month_chf": 0
  },
  "access_matrix": {
    "manus": { "method": "mcp_token", "status": "active", "autonomy": "full" },
    "chatgpt": { "method": "oauth", "status": "active", "autonomy": "manual_login_required" }
  },
  "health": {
    "status": "healthy",
    "last_checked": "2026-08-02T18:00:00Z",
    "remediation_protocol": "playwright_oauth_login"
  }
}
```

---

## 3. Interfaçage & Délégation (Phase 3 Module Factory)

Conformément au principe de séparation des préoccupations de Y-OS, ART ne gère pas directement le stockage sécurisé des mots de passe. Il orchestre les flux et délègue.

### 3.1. Interface avec `Secret Management`
- **Découverte :** Lorsqu'ART détecte un nouvel outil, il crée la Fact Sheet, mais délègue la vérification de l'existence des credentials à `yos_secrets.py`.
- **Remédiation :** Si ART génère un nouveau token via Playwright, il ne le stocke pas lui-même. Il appelle le module `Secret Management` pour injecter le token dans 1Password (`op item create/edit`).
- **Synchronisation :** Une fois le token dans 1Password, ART déclenche le module `sync_1p_to_manus.py` pour propager le secret dans l'environnement du LLM actif.

### 3.2. Interface avec `yTools` / `tool-router`
- ART est le moteur sous-jacent. Les skills existantes comme `tool-router` et `ytools` deviennent des interfaces de lecture qui consomment les données d'ART pour prendre des décisions en temps réel.

---

## 4. Déclenchement & Triggering (Phase 4 Module Factory)

Comment le module ART prend-il vie dans Y-OS ?

### 4.1. Event-Driven (Réactif)
- **Erreur d'Authentification :** Si un appel API ou MCP échoue avec un code HTTP 401 (Unauthorized) ou 403 (Forbidden), le kernel Y-OS intercepte l'erreur et déclenche le flux de remédiation ART.
- **Nouvel Outil Détecté :** Si l'utilisateur demande d'utiliser un outil inconnu, ART est déclenché pour créer la Fact Sheet et chercher un accès.

### 4.2. Scheduled (Proactif)
- **Health Check Hebdomadaire :** Un cron job Manus exécute `art_health_monitor.py` tous les dimanches à 03h00 pour pinger les APIs de tous les outils du registre et s'assurer que les tokens sont toujours valides.

### 4.3. Human-in-the-Loop (Manuel)
- **Menu d'Administration :** Accessible via `/art` ou `/yMenu`, permettant à Yannick de forcer un audit, d'ajouter un outil manuellement, ou de valider un accès OAuth complexe (cas D).

---

## 5. Workflow Opérationnel de Remédiation (Exemple : Canva)

1. **Événement :** Le token Canva expire. Manus tente une génération d'image et échoue (HTTP 401).
2. **Détection :** Le LLM capture l'erreur et appelle le module ART Health.
3. **Diagnostic :** ART vérifie la Fact Sheet de Canva. Méthode : `MANUAL_SIMPLE`.
4. **Délégation :** ART notifie Yannick : "Token Canva expiré. Rends-toi sur canva.com/developers, clique sur Get API Key, et donne-moi la clé."
5. **Propagation :** Une fois la clé fournie, ART l'envoie au Secret Management (1Password) et déclenche la synchronisation Manus.
6. **Reprise :** La tâche de génération d'image reprend.
