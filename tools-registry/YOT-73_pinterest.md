---
tool_id: YOT-73
tool_name: Pinterest
tool_type: MCP Connector
category: Design / Visual
status: A tester
pricing: Freemium
source_type: Communauté
source_url: https://github.com/clugtu/pinterest-mcp
auth_credentials: OAuth MCP
last_updated: 2026-07-30
notion_origin: https://app.notion.com/p/3ac35e218cf8816288fef6ab13a7580c
---

# Pinterest — Fiche Outil Y-OS

## Business Value

Découverte visuelle publique et diffusion de contenu. Usage principal : inspiration tendances (design, architecture, lifestyle, Anandaz). Usage secondaire : partage public de contenu Y-OS.

## Capabilities

API v5 officielle stable (OAuth 2.0, 1 000 req/min). MCP communautaire 11 outils : create/update/delete pin, analytics, list boards, search pins, trending, bulk_create. Rate limit 10 pins/min, 250 pins/jour.

## Dependencies

- Pinterest Business Account
- OAuth 2.0 client ID/secret

## Known Limits and Bugs

- Lecture boards privés nécessite Business Account OAuth
- MCP communautaire (0 étoiles, mars 2026)
- Pinterest MCP interne = usage interne Pinterest Inc uniquement
- Pas d'accès aux boards personnels sans auth Business

## Workarounds and Lessons

Positionné comme outil de découverte et diffusion, pas de stockage personnel. Raindrop reste la source de vérité pour les liens.

## Architecture Y-OS

Pinterest est l'outil de **découverte et diffusion** dans l'architecture YOUniverse :

```
Pinterest (découverte tendances) → Inspiration → MyMind ou Raindrop (capture)
Y-OS contenu → Pinterest (diffusion publique)
```

## Positionnement vs MyMind vs Raindrop

| Usage | Raindrop | MyMind | Pinterest |
| :--- | :---: | :---: | :---: |
| Stocker un lien web | ✅ | ❌ | ❌ |
| Capturer un visuel | ❌ | ✅ | ⚠️ |
| Découvrir des tendances | ❌ | ❌ | ✅ |
| Diffuser du contenu | ❌ | ❌ | ✅ |
| Pilotabilité IA | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
