# MyMind — Y-OS Tool Fact Sheet

## Identité

| Champ | Valeur |
|-------|--------|
| **Nom** | MyMind |
| **Catégorie** | Knowledge Management / Personal AI |
| **URL** | https://mymind.com |
| **Status Y-OS** | ✅ Actif |
| **Priorité** | HIGH |

## Description

MyMind est un espace de sauvegarde personnel augmenté par IA : capture de notes, images, liens, citations. Recherche sémantique native. Pas de dossiers — l'IA organise automatiquement.

## Accès par plateforme

| Plateforme | Protocole | Endpoint | Auth | Status |
|-----------|-----------|----------|------|--------|
| **Manus** | MCP (OAuth) | `https://mcp.mymind.com/mcp` | OAuth — installé | ✅ Actif |
| **ChatGPT** | MCP (OAuth) | `https://mcp.mymind.com/mcp/chatgpt` | OAuth — installé | ✅ Actif |
| **API directe** | REST | `https://api.mymind.com/v1/` | Key ID + Private Key (HMAC) | ⚠️ 403 sandbox |

## Credentials

| Credential | Stockage | Valeur |
|-----------|---------|--------|
| `MYMIND_KEY_ID` | 1Password MAIN VAULT + Manus Custom API | `kDrpZkrL0eHa5iMU2gcrT6` |
| `MYMIND_PRIVATE_KEY` | 1Password MAIN VAULT | `y9NRtf0y...` (HMAC-SHA256, 32 bytes) |

**1Password item :** `MyMind API Credentials — yOS` (tags: `yos-manus`, `yos-secret`)

## Auth MCP — Notes

- **Manus** : MCP installé via OAuth. Le connecteur `mymind` est dans la liste des MCP managed. Pas de token manuel requis — Manus gère l'auth.
- **ChatGPT** : MCP installé via OAuth sur endpoint `/mcp/chatgpt`. Même compte, endpoint dédié.
- **Renouvellement OAuth** : Si l'accès est révoqué, aller sur https://mymind.com/settings → Integrations → réautoriser Manus / ChatGPT.

## Capabilities Y-OS

- Capture de notes, liens, images depuis n'importe quel agent
- Recherche sémantique dans la base de connaissances personnelle
- Récupération de contexte pour enrichir les prompts
- Archivage de sessions Y-OS

## Health Check

```bash
# Tester via MCP Manus (depuis une session active)
# Le connecteur mymind est dans la liste des MCP managed — pas de test API direct requis

# Test API direct (hors sandbox)
curl -H "Authorization: Bearer kDrpZkrL0eHa5iMU2gcrT6" https://api.mymind.com/v1/user
```

## Historique

| Date | Action |
|------|--------|
| 2026-08-03 | Credentials stockés dans 1Password MAIN VAULT |
| 2026-08-03 | Custom API Connector créé dans Manus (`MYMIND_KEY_ID`) |
| 2026-08-03 | MCP installé sur Manus + ChatGPT via OAuth |
| 2026-08-03 | Fact Sheet créée |
