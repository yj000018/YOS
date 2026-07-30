---
tool_id: YOT-72
tool_name: MyMind
tool_type: MCP Connector
category: Design / Visual
status: Experimental
pricing: Payant
source_type: Communauté
source_url: https://github.com/iamumeransari/mymind-mcp
auth_credentials: Session Cookie
last_updated: 2026-07-30
notion_origin: https://app.notion.com/p/3ac35e218cf881ec8ed5cfe9a3aa3ee6
---

# MyMind — Fiche Outil Y-OS

## Business Value

Moodboard visuel privé et mémoire inspirationnelle. Capture rapide d'images, screenshots, références design. Complément de Raindrop pour le contenu visuel non structuré.

## Capabilities

MCP communautaire ~5 outils : search, read, create, tags, spaces. Recherche visuelle IA native. Capture rapide mobile/desktop. Organisation automatique sans effort.

## Dependencies

- Session cookie MyMind
- MCP communautaire non officiel

## Known Limits and Bugs

- **PAS d'API publique officielle**
- MCP = reverse-engineering d'endpoints internes, fragile
- Peut casser à chaque update MyMind
- Auth par session cookie instable
- Pas d'opérations en masse

## Workarounds and Lessons

Annonce API officielle par van Schneider le 23 juillet 2026 sans documentation publiée. Veille hebdo schedulée (lundi 9h) pour détecter la sortie. À réévaluer dès API officielle disponible.

## Statut de veille

**Veille active** : schedule Manus chaque lundi 09h00 — surveille mymind.com, GitHub iamumeransari/mymind-mcp, @mymind @vanschneider.

## Architecture Y-OS

MyMind est le **pipeline visuel** dans l'architecture YOUniverse :

```
Web / Screenshots → MyMind (capture visuelle) → Inspiration / Moodboard
```

- Usage : visuels, screenshots, références design, inspiration
- Pas de stockage de liens textuels (→ Raindrop pour ça)
- Pas de pipeline IA fiable tant que l'API officielle n'est pas publiée

## Comparaison vs Raindrop

| Critère | MyMind | Raindrop |
| :--- | :---: | :---: |
| Contenu visuel | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| API publique | ❌ | ✅ |
| Pilotabilité IA | ⭐⭐ (fragile) | ⭐⭐⭐⭐⭐ |
| Opérations masse | ❌ | ✅ |
