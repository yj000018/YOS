# Manus API Reference Guide

Ce document centralise la documentation complète de l'API Manus, combinant les endpoints publics officiels (v2) et les endpoints internes (gRPC-web) découverts par reverse engineering.

## 1. Architecture & Authentification

Manus expose deux APIs distinctes :
1. **API Publique (REST)** : `https://api.manus.ai/v2/` — Documentée, stable, utilisée pour les intégrations externes.
2. **API Interne (gRPC-web)** : `https://api.manus.im/` — Non documentée, utilisée par le frontend web, permet de gérer les paramètres internes (Knowledge, Profile, etc.).

### Authentification Publique (v2)
- **Header** : `x-manus-api-key: <API_KEY>` ou `Authorization: Bearer <oauth_token>`
- **Génération** : Récupérable via Settings > Integrations > API Keys.

### Authentification Interne (gRPC-web)
- **Header** : `Authorization: Bearer <session_id>`
- **Génération** : Le token est stocké dans le cookie `session_id` lors de la connexion au webapp. Il peut être extrait via JavaScript dans le navigateur :
  ```javascript
  const sessionId = document.cookie.split(';').find(c => c.trim().startsWith('session_id='))?.split('=')[1];
  ```

---

## 2. API Publique Officielle (v2)

URL de base : `https://api.manus.ai/v2/`

### 2.1 Tasks (Tâches)
| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/task.create` | POST | Crée une tâche asynchrone. Accepte `message.content`, `connectors`, `structured_output_schema`. |
| `/task.list` | GET | Liste les tâches avec pagination (cursor) et filtres (`scope`, `agent_id`, `project_id`). |
| `/task.detail` | GET | Récupère le statut (`running`, `stopped`, `waiting`, `error`) et métadonnées. |
| `/task.listMessages` | GET | Polling des événements d'une tâche. Retourne les messages, erreurs, et demandes d'input. |
| `/task.sendMessage` | POST | Envoie un message de suivi à une tâche existante. |
| `/task.confirmAction` | POST | Confirme une action en attente (ex: `needConnectMyBrowser`, `gmailSendAction`). |
| `/task.stop` | POST | Arrête une tâche en cours. |
| `/task.delete` | POST | Supprime définitivement une tâche. |
| `/task.update` | POST | Met à jour le titre ou la visibilité. |

### 2.2 Projects & Agents
| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/project.create` | POST | Crée un projet pour regrouper des tâches. |
| `/project.list` | GET | Liste tous les projets. |
| `/agent.list` | GET | Liste les agents custom. |
| `/agent.detail` | GET | Détails d'un agent. |
| `/agent.update` | POST | Met à jour un agent. |

### 2.3 Files & Webhooks
| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/file.upload` | POST | Retourne une URL presigned pour uploader un fichier (max 512MB). |
| `/file.detail` | GET | Vérifie le statut d'un fichier uploadé. |
| `/file.delete` | POST | Supprime un fichier. |
| `/webhook.create` | POST | Enregistre un webhook pour les événements (ex: `task_stopped`). |
| `/webhook.list` | GET | Liste les webhooks. |
| `/webhook.publicKey`| GET | Clé publique pour vérifier les signatures des webhooks. |

### 2.4 Rate Limits
- `task.create`, `task.sendMessage` : 10 / min
- `task.list`, `task.detail`, `task.listMessages` : 100 / min
- `usage.*` : 600 / min
- Dépassement : HTTP 429 avec code `rate_limited`.

---

## 3. API Interne Découverte (gRPC-web)

URL de base : `https://api.manus.im/`
*Note : Ces endpoints requièrent le token `session_id` extrait du cookie du navigateur.*

### 3.1 Knowledge Service (Personalization)
Gère les 100 entrées "Knowledge" du Personalization Center.

| Endpoint | Méthode | Payload JSON |
|----------|---------|--------------|
| `/knowledge.v1.KnowledgeService/ListKnowledge` | POST | `{}` |
| `/knowledge.v1.KnowledgeService/CreateKnowledge` | POST | `{"name": "Titre", "content": "Contenu"}` |
| `/knowledge.v1.KnowledgeService/UpdateKnowledge` | POST | `{"uid": "...", "name": "Nouveau", "content": "..."}` |
| `/knowledge.v1.KnowledgeService/DeleteKnowledge` | POST | `{"knowledgeUid": "..."}` |

**Attention :** Le champ pour le titre est `name` et non `title`.

### 3.2 Autres Services Internes Identifiés
Ces endpoints retournent un HTTP 200 lorsqu'ils sont appelés avec `{}` :
- `/user.v1.UserService/GetUserInfo` : Infos utilisateur (ID, email, etc.)
- `/profile.v1.ProfileService/GetProfile` : Profil utilisateur
- `/notification.v1.NotificationService/ListNotifications` : Notifications in-app
- `/personalization.v1.PersonalizationService/GetPersonalization` : Settings globaux
- `/settings.v1.SettingsService/GetSettings` : Préférences compte

---

## 4. Workflows & Patterns

### 4.1 Structured Output
Permet d'imposer un schéma JSON strict à la sortie d'une tâche.
1. Envoyer `structured_output_schema` dans `task.create`.
2. Le schéma doit avoir `additionalProperties: false` et lister tous les champs dans `required`.
3. Le résultat est retourné dans l'événement `structured_output_result` via `task.listMessages` ou webhook.

### 4.2 My Browser (Cloud Browser)
1. L'agent rencontre un blocage nécessitant le navigateur local.
2. Il émet un événement `needConnectMyBrowser`.
3. Récupérer les clients dispo via `/browser.onlineList`.
4. Confirmer via `task.confirmAction` avec `{"action": "select", "client_id": "..."}`.

### 4.3 Script de gestion Knowledge (Exemple JS)
```javascript
const sid = document.cookie.split(';').find(c => c.trim().startsWith('session_id='))?.split('=')[1];
const h = { 'Content-Type': 'application/json', 'Authorization': `Bearer ${sid}` };

// Créer une entrée
fetch('https://api.manus.im/knowledge.v1.KnowledgeService/CreateKnowledge', {
  method: 'POST', headers: h,
  body: JSON.stringify({name: 'SYS-TEST', content: 'Test'})
});
```

---
*Dernière mise à jour : 29 Juillet 2026*
