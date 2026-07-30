---
tool_id: YOT-71
tool_name: Raindrop.io
tool_type: MCP Connector
category: Memory / Knowledge
status: Production
pricing: Payant
source_type: Officiel
source_url: https://developer.raindrop.io/mcp/mcp
auth_credentials: OAuth MCP
last_updated: 2026-07-30
notion_origin: https://app.notion.com/p/3ac35e218cf881ff9760c45639a157b7
---

# Raindrop.io — Fiche Outil Y-OS

## Business Value

Bibliothèque universelle de bookmarks pilotable à 100% par Y-OS. Pipeline principal pour capturer, organiser, tagger et retrouver tout lien web. Nourrit YOUniverse via highlights et tags IA.

## Capabilities

22 outils MCP officiels : CRUD bookmarks/collections/tags/highlights. Recherche sémantique, filtres (broken/duplicates/untagged). Opérations en masse par lots 150. Tagging IA Gemini. Rate limit 120 req/sec. API REST v1 stable.

## Dependencies

- `RAINDROP_TOKEN` env var
- Manus MCP connector actif

## Known Limits and Bugs

- MCP en beta Pro requis
- Pagination 150 items/page max
- Pas de sous-collections infinies

## Workarounds and Lessons

Testé prod juillet 2026 : 7 790 signets nettoyés (311 liens morts, 358 doublons, 157 collections vides). YouTube classifié en 9 thèmes. Tagging IA nocturne schedulé (02h00 Europe/Zurich, 1 500 signets/run, ~3 nuits pour compléter).

## Architecture Y-OS

Raindrop est le **pipeline principal de capture** dans l'architecture YOUniverse :

```
Internet / Web → Raindrop (capture + tag IA) → YOUniverse (connaissance structurée)
```

- Bookmarks généraux : articles, outils, docs, vidéos, liens
- Highlights → extractibles comme connaissance brute
- Tags IA → classification automatique par Gemini
- Collections thématiques → navigation par domaine

## Comparaison vs alternatives

| Critère | Raindrop | MyMind | Pinterest |
| :--- | :---: | :---: | :---: |
| API publique | ✅ | ❌ | ✅ |
| MCP officiel | ✅ (22 outils) | ⚠️ communautaire | ⚠️ communautaire |
| Opérations masse | ✅ | ❌ | ❌ |
| Pilotabilité IA | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |

**Verdict : outil de référence Y-OS pour les bookmarks.**
