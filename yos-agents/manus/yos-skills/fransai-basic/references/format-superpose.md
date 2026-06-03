# Format Superposé — Fransai Basic

## Principe

Chaque groupe de mots original est aligné avec sa version simplifiée sur la ligne suivante.
Deux colonnes : FRANÇAIS STANDARD (rouge/gauche) | FRANSAI BASIC (vert/droite).

## Format Markdown

```markdown
| FRANÇAIS STANDARD | FRANSAI BASIC |
|-------------------|---------------|
| Nonobstant les dispositions susmentionnées, | Malgre la regl en vigu, |
| et conformément aux dispositions en vigueur | selon la regl |
| il convient de noter que | not ke |
| dans le cadre de cette réforme | dan set reform |
| il y a lieu de procéder à | il fo fer |
| une réévaluation exhaustive | enn reevalüasion konplet |
| **LES CAS EXTRÊMES** | |
| Veuillez agréer l'expression de mes sentiments les plus distingués | Kordialman |
| Anticonstitutionnellement (25 lettres) | Antikonstitusionelman (21) |
```

## Règles de découpage

- Découper par groupe de sens (syntagme), pas mot par mot
- Maximum 8-10 mots par ligne
- Conserver la ponctuation sur la ligne originale
- Séparateur de section : ligne avec `**TITRE**` en gras

## Statistiques à inclure en bas

```markdown
---
**Original** : X caractères · Y mots · ~Z min de lecture · Niveau C2
**Fransai Basic** : X' caractères · Y' mots · ~Z' sec de lecture · Niveau A2-B1
**Gain** : −Z%
```
