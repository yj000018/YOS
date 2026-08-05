# Wispr Flow — Y-OS Tool Fact Sheet

## Identité

| Champ | Valeur |
|-------|--------|
| **Nom** | Wispr Flow |
| **Catégorie** | Voice-to-Text / AI Dictation / Meeting Notes |
| **URL** | https://wisprflow.ai |
| **Status Y-OS** | ✅ Actif |
| **Priorité** | HIGH |
| **Ajouté** | 2026-08-05 |

## Description

Wispr Flow est un outil de dictée vocale IA universel : speech-to-text avec auto-édition, suppression des mots de remplissage, dictionnaire personnel, 100+ langues. Fonctionne dans toutes les apps (Mac, Windows, iOS, Android). Inclut un **Notetaker** (transcription de réunions) accessible via MCP.

**Cas d'usage Y-OS :**
- Dicter des prompts à la voix dans Manus, Claude, ChatGPT
- Rechercher dans les notes de réunions via MCP
- Accéder aux transcriptions de calls depuis n'importe quel agent

## Accès par plateforme

| Plateforme | Protocole | Endpoint | Auth | Status |
|-----------|-----------|----------|------|--------|
| **Manus** | MCP Custom (HTTP) | `https://api.wisprflow.ai/connect/mcp` | OAuth (browser sign-in) | ✅ À connecter |
| **Claude** | MCP Connector | `https://api.wisprflow.ai/connect/mcp` | OAuth (browser sign-in) | ✅ Supporté |
| **ChatGPT** | MCP Custom App | `https://api.wisprflow.ai/connect/mcp` | OAuth (Developer mode) | ✅ Supporté |
| **Cursor** | MCP Server | `https://api.wisprflow.ai/connect/mcp` | OAuth | ✅ Supporté |
| **VS Code** | MCP Remote | `https://api.wisprflow.ai/connect/mcp` | OAuth | ✅ Supporté |
| **API Voice** | WebSocket / REST | `wss://api.wisprflow.ai/ws` / `POST /api` | API Key ou Client Token | ✅ Disponible |

**Note importante :** Le MCP est **read-only** — les agents peuvent lire les notes de réunions mais ne peuvent pas les modifier.

## Configuration MCP

### Manus (Custom MCP)
Ajouter dans Manus Settings → Custom MCP :
```json
{
  "name": "wispr-flow",
  "url": "https://api.wisprflow.ai/connect/mcp",
  "auth": "oauth"
}
```
Puis cliquer "Connect" et s'authentifier avec le compte Wispr Flow.

### Cursor / VS Code
```json
{
  "mcpServers": {
    "wispr-flow": {
      "url": "https://api.wisprflow.ai/connect/mcp"
    }
  }
}
```

### ChatGPT
Settings → Apps → Developer mode → Create → Paste URL → OAuth → Scan Tools.

## Prérequis

- **Notetaker activé** sur le compte Wispr Flow (onglet MCP visible dans Settings)
- **Cloud Sync activé** pour que les notes soient accessibles via MCP
- **Même compte** utilisé pour l'auth MCP et l'app Wispr Flow

## Credentials

| Credential | Stockage | Notes |
|-----------|---------|-------|
| `WISPR_FLOW_MCP_URL` | Manus Custom MCP config | `https://api.wisprflow.ai/connect/mcp` |
| API Key (Voice API) | 1Password MAIN VAULT (si créée) | Pour l'API WebSocket/REST directe |
| OAuth token | Géré par Manus/Claude/ChatGPT | Renouvelé automatiquement |

**Auth MCP :** Pas de token statique — OAuth browser sign-in. Si révoqué : aller dans Wispr Flow Settings → MCP → Réautoriser.

## Capabilities Y-OS

- Recherche sémantique dans les notes de réunions
- Récupération de transcriptions de calls
- Action items et résumés de meetings
- Dictée vocale dans toutes les apps (usage desktop, pas via MCP)

## Health Check

```bash
# Tester la disponibilité de l'endpoint MCP
curl -I "https://api.wisprflow.ai/connect/mcp" --max-time 10

# Si 401 → OAuth non connecté (normal)
# Si 200 → Connecté et fonctionnel
# Si 403/timeout → Problème réseau ou IP bloquée
```

**Renouvellement OAuth :** Wispr Flow → Settings → MCP → Disconnect → Reconnect → Sign in.

## Liens utiles

- [Documentation MCP](https://docs.wisprflow.ai/articles/4759919286-how-to-connect-wispr-flow-to-claude-chatgpt-and-other-ai-tools-mcp)
- [API Voice Documentation](https://api-docs.wisprflow.ai/introduction)
- [Trust Center](https://trust.wisprflow.ai)
- [Status Page](https://statuspage.incident.io/wispr-flow)

## Historique

| Date | Action |
|------|--------|
| 2026-08-05 | Outil identifié, endpoint MCP fourni par Yannick |
| 2026-08-05 | Fact Sheet créée, documentation complète récupérée |
| 2026-08-05 | Custom MCP Connector ajouté dans Manus |
| 2026-08-05 | Poussé sur GitHub YOS Tool Registry |
