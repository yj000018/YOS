# Y-OS Telegram Interaction Layer (TIL)
# Design Document v1.0 — 2026-08-08

## 1. Vision

Le **Telegram Interaction Layer (TIL)** est l'interface asynchrone, universelle et bidirectionnelle de Y-OS. Il permet de recevoir des informations d'état et de prendre des décisions bloquantes pour n'importe quel agent (Manus, ChatGPT, Claude, scripts, outils MCP) sans surveiller l'exécution.

**Principe** : l'utilisateur n'est sollicité que quand son attention ou sa décision est requise. Il agit directement depuis la notification.

---

## 2. Deux Types de Notifications

### TYPE A — Informatif (Fire-and-Forget)

Aucune action requise. Informe de l'avancement ou de la complétion.

| Icône | Tag | Usage |
|---|---|---|
| 🟢 | `[DONE]` | Tâche longue terminée |
| 🔄 | `[STEP]` | Étape franchie dans un pipeline |
| ⚠️ | `[WARN]` | Alerte non bloquante |

**Format :**
```
🟢 [DONE] Génération d'images terminée
Agent: Midjourney via MCP (Session: 8f4a2b)

4 variations du logo ELYSIUM générées → /assets/logos/

Prochaine étape : intégration Figma.
[🔗 Voir les résultats]
```

### TYPE B — Actionnable (Intervention Requise)

Bloque l'exécution jusqu'à la réponse de l'utilisateur.

| Icône | Tag | Usage |
|---|---|---|
| 🟡 | `[APPROVE]` | Validation simple oui/non |
| 🔵 | `[CHOICE]` | Choix entre N options |
| 🔴 | `[INPUT]` | Saisie libre requise |

**Format :**
```
🔵 [CHOICE] Stratégie de scraping bloquée
Agent: Manus (Session: a1b2c3)

Cloudflare bloque l'accès API direct. Comment procéder ?

[1. CDP via Brave] [2. Playwright] [3. Abandonner]
[🔗 Ouvrir la session Manus]
```

---

## 3. Architecture Technique

### Flux Émission (Agent → Telegram)

```
Agent (Manus / script / MCP)
  │
  ├─ TYPE A → appelle yos-notify.py → sendMessage API → Notification push
  │
  └─ TYPE B → dépose /tmp/yos_approvals/<task_id>.json (status: pending)
                │
                └─ Bot Watcher détecte → sendMessage avec InlineKeyboard
```

### Flux Réception (Telegram → Agent)

```
Utilisateur clique bouton ou répond texte
  │
  └─ Bot reçoit CallbackQuery
       │
       └─ Met à jour /tmp/yos_approvals/<task_id>.json (status: resolved, answer: "1")
            │
            └─ Agent boucle sur le fichier → détecte resolved → reprend exécution
```

---

## 4. Format IPC (Fichier JSON)

**Créé par l'Agent :**
```json
{
  "task_id": "a1b2c3",
  "source": "Manus",
  "type": "CHOICE",
  "message": "Cloudflare bloque l'accès API direct. Comment procéder ?",
  "options": {
    "1": "Utiliser CDP",
    "2": "Utiliser Playwright",
    "3": "Abandonner"
  },
  "session_url": "https://manus.im/...",
  "status": "pending",
  "answer": null,
  "created_at": "2026-08-08T14:30:00Z"
}
```

**Mis à jour par le Bot :**
```json
{
  "status": "resolved",
  "answer": "1",
  "resolved_at": "2026-08-08T14:35:00Z"
}
```

---

## 5. Implémentation — Évolutions du Handler v2

Trois ajouts requis dans `yos_telegram_handler_v2.py` :

1. **InlineKeyboardMarkup** : boutons cliquables sous les messages TYPE B
2. **Watcher de dossier** : polling `/tmp/yos_approvals/` toutes les 2s pour auto-envoi des notifications
3. **CallbackQueryHandler** : intercepte les clics boutons et met à jour le fichier JSON

---

## 6. Périmètre Sources (Trans-LLM / Trans-Outil)

| Source | Méthode d'intégration | Priorité |
|---|---|---|
| **Manus** | Appel direct `yos-notify.py` depuis sandbox | P1 |
| **Scripts CC** (crons, pipelines) | Appel direct `yos-notify.py` | Déjà actif |
| **ChatGPT** | Via Manus API ou script CC | P2 |
| **Claude** | Via Manus API ou script CC | P2 |
| **Outils MCP** (Midjourney, Flux, etc.) | Hook post-exécution via script CC | P2 |
| **Android fleet** | Déjà intégré dans health_probe.py | Actif |

---

## 7. Prochaine Étape

Implémenter le **Watcher + InlineKeyboard** dans `yos_telegram_handler_v2.py` et déployer via `pm2 restart yos-telegram`.
