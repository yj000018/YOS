# Manus Internal API Reference (gRPC-web)

> **Statut** : Découverte par reverse engineering — non documenté officiellement.
> **Dernière validation** : 2026-07-29
> **Base URL** : `https://api.manus.im/`
> **Transport** : gRPC-web (JSON over HTTP/1.1 POST)

---

## Authentification

Le token est le cookie `session_id` extrait du navigateur connecté à `manus.im`.

```javascript
// Extraction du token depuis le browser (browser_console_exec)
const sessionId = document.cookie
  .split(';')
  .find(c => c.trim().startsWith('session_id='))
  ?.split('=')[1];

const headers = {
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${sessionId}`
};
```

**Durée de vie** : Durée de la session browser. Expire à la déconnexion.
**Scope** : Uniquement utilisable depuis le browser Manus (CORS restrictif).

---

## Services Découverts

### knowledge.v1.KnowledgeService

Gère les 100 entrées "Knowledge" du Personalization Center (`settings/personalization-center/knowledge`).

| Endpoint | Payload | Réponse | Statut |
|----------|---------|---------|--------|
| `ListKnowledge` | `{}` | `{knowledge: [{uid, name, content, createTime, updateTime}], total}` | ✅ Validé |
| `CreateKnowledge` | `{name: "...", content: "..."}` | `{knowledge: {uid, name, content...}}` | ✅ Validé |
| `UpdateKnowledge` | `{uid: "...", name: "...", content: "..."}` | `{knowledge: {...}}` | ✅ Validé |
| `DeleteKnowledge` | `{knowledgeUid: "..."}` | `{}` | ✅ Validé |

**Limites** :
- Maximum 100 entrées. Au-delà : HTTP 429 `KNOWLEDGE_LIMIT_REACHED`.
- Champ titre = `name` (pas `title`).

**Exemple complet — Bulk Create** :
```javascript
async function bulkCreate(entries) {
  const sid = document.cookie.split(';').find(c => c.trim().startsWith('session_id='))?.split('=')[1];
  const h = { 'Content-Type': 'application/json', 'Authorization': `Bearer ${sid}` };
  let ok = 0, fail = 0;
  for (const e of entries) {
    const r = await fetch('https://api.manus.im/knowledge.v1.KnowledgeService/CreateKnowledge', {
      method: 'POST', headers: h,
      body: JSON.stringify({name: e.name, content: e.content})
    });
    if (r.status === 200) ok++; else fail++;
  }
  window._result = {ok, fail};
}
// Lire le résultat : return JSON.stringify(window._result)
```

**Exemple complet — Bulk Delete** :
```javascript
async function bulkDelete() {
  const sid = document.cookie.split(';').find(c => c.trim().startsWith('session_id='))?.split('=')[1];
  const h = { 'Content-Type': 'application/json', 'Authorization': `Bearer ${sid}` };
  const list = await fetch('https://api.manus.im/knowledge.v1.KnowledgeService/ListKnowledge', {
    method: 'POST', headers: h, body: JSON.stringify({})
  }).then(r => r.json());
  let deleted = 0;
  for (const k of list.knowledge) {
    const r = await fetch('https://api.manus.im/knowledge.v1.KnowledgeService/DeleteKnowledge', {
      method: 'POST', headers: h,
      body: JSON.stringify({knowledgeUid: k.uid})
    });
    if (r.status === 200) deleted++;
  }
  window._deleted = deleted;
}
```

---

### user.v1.UserService

| Endpoint | Payload | Statut |
|----------|---------|--------|
| `GetUserInfo` | `{}` | ✅ Validé (retourne ID, email, plan) |

---

### profile.v1.ProfileService

| Endpoint | Payload | Statut |
|----------|---------|--------|
| `GetProfile` | `{}` | ✅ Validé |

---

### notification.v1.NotificationService

| Endpoint | Payload | Statut |
|----------|---------|--------|
| `ListNotifications` | `{}` | ✅ Validé |

---

### personalization.v1.PersonalizationService

| Endpoint | Payload | Statut |
|----------|---------|--------|
| `GetPersonalization` | `{}` | ✅ Validé |

---

## Endpoints à Explorer (Hypothèses)

Les patterns gRPC-web suggèrent l'existence probable de ces endpoints. À tester :

| Endpoint Hypothétique | Probabilité | Méthode de test |
|-----------------------|-------------|-----------------|
| `profile.v1.ProfileService/UpdateProfile` | Haute | POST `{}` → voir erreur de validation |
| `settings.v1.SettingsService/GetSettings` | Haute | POST `{}` |
| `settings.v1.SettingsService/UpdateSettings` | Haute | POST avec payload settings |
| `connector.v1.ConnectorService/ListConnectors` | Moyenne | POST `{}` |
| `task.v1.TaskService/ListTasks` | Faible | Probablement via API publique |
| `billing.v1.BillingService/GetBalance` | Moyenne | POST `{}` |

**Convention de test** :
```javascript
// Template de test d'un endpoint hypothétique
fetch('https://api.manus.im/<service>/<method>', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${sessionId}` },
  body: JSON.stringify({})
}).then(async r => {
  window._probe = {status: r.status, body: (await r.text()).substring(0, 200)};
});
// Lire: return JSON.stringify(window._probe)
```

---

## Règles & Pièges

| Règle | Détail |
|-------|--------|
| **Ne jamais utiliser `alert()`** | Navigue vers `about:blank` et détruit la session browser. Utiliser `window._var = ...` + `return JSON.stringify(window._var)`. |
| **Backup avant bulk delete** | Committer dans `YOS/01_BACKBONE/KAP/03_SOURCES/manus-knowledge-entries/` avant toute suppression massive. |
| **Champ `name` pas `title`** | L'API Knowledge utilise `name` pour le titre, contrairement à ce qu'on pourrait attendre. |
| **Limite 100 entrées** | HTTP 429 si dépassement. Supprimer avant de créer si proche de la limite. |
| **CORS restrictif** | Ces endpoints ne sont pas accessibles depuis un script Python externe — uniquement depuis le browser Manus connecté. |

---

*Voir aussi* : `SKILL.md` (section Workflow 0) · `YOS/MANUS-API-REFERENCE.md` (vue consolidée) · `docs/v2/` (API publique officielle)
