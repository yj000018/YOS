---
name: webapp-factory
description: Pipeline orchestré de création d'apps web (Next.js + Sanity + Vercel + GitHub). Utiliser quand l'utilisateur demande de créer une app web, un site, une landing page, ou un MVP. Couvre la conception (GPT), les specs (Claude), le scaffolding, le CMS, le déploiement et le visual editing. Encode les versions validées, les pièges connus, et les workflows optimisés.
---

# Webapp Factory

Pipeline de production d'apps web en 6 couches orchestrées par Manus.

## Trigger

Activer quand la tâche implique :
- Création d'app web / site / landing page / MVP
- Déploiement Next.js + Vercel
- Intégration CMS (Sanity)
- Pipeline multi-LLM pour conception + specs

## Stack validée — NE PAS MODIFIER

| Composant | Version | Raison |
|---|---|---|
| Next.js | **14.2.x** | Stable, compatible Sanity v3 |
| React | **18.3.x** | Sanity v3 incompatible React 19 |
| Sanity | **3.99.0** (dernière v3) | v5 requiert `useEffectEvent` absent de React 19 stable |
| next-sanity | **9.x** | Compatible Sanity v3 + React 18 |
| @sanity/vision | **3.x** | Doit matcher Sanity v3 |
| TypeScript | 5.x | Standard |
| Tailwind CSS | 3.x | Standard |

**INTERDIT** : `sanity@5`, `react@19`, `next@15+`, `next-sanity@10+`

## Workflow — 6 couches

### Couche 0 — Pré-requis (5 min)

1. Créer le repo GitHub via browser (si PAT n'a pas `repo` scope)
2. Ajouter SSH deploy key avec write access :
   ```bash
   ssh-keygen -t ed25519 -f ~/.ssh/<project>_deploy -N ""
   ```
3. Ajouter la clé via GitHub browser → Settings → Deploy keys → Allow write
4. Configurer SSH :
   ```
   Host github.com
     IdentityFile ~/.ssh/<project>_deploy
   ```
5. Créer le projet Vercel via API ou lier le repo GitHub
6. Configurer les env vars Vercel via **API v10** (pas CLI) :
   ```bash
   curl -X POST "https://api.vercel.com/v10/projects/<name>/env" \
     -H "Authorization: Bearer $VERCEL_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"key":"...","value":"...","type":"plain","target":["production","preview","development"]}'
   ```
   Pour les secrets : `"type":"sensitive"`

### Couche 1 — Conception produit (3 min)

Appeler GPT via OpenAI API. Voir `references/prompts.md` pour le prompt exact.

Livrable : brief produit structuré (vision, scope MVP, user flows).

### Couche 2 — Specs techniques (3 min)

Appeler Claude via Anthropic API (ou OpenRouter fallback). Voir `references/prompts.md`.

Livrable : specs techniques (schémas Sanity, composants, GROQ queries, structure projet).

### Couche 3 — Scaffolding (20 min)

1. `mkdir <project> && cd <project>`
2. Créer `package.json` avec les versions exactes de `references/package-template.json`
3. `pnpm install`
4. Créer la structure :
   ```
   src/
   ├── app/
   │   ├── layout.tsx
   │   ├── page.tsx
   │   ├── globals.css
   │   ├── studio/[[...tool]]/page.tsx
   │   └── api/
   ├── components/
   ├── lib/sanity/
   │   ├── client.ts
   │   ├── queries.ts
   │   └── schemas/
   └── types/
   ```
5. **Client Sanity** : toujours utiliser `"placeholder"` comme fallback projectId (jamais `""`)
6. Coder les composants, pages, schemas Sanity
7. `pnpm build` — vérifier que tout compile

### Couche 4 — Sanity CMS (10 min)

1. Créer le projet Sanity via API (si nouveau) :
   ```bash
   curl -X POST "https://api.sanity.io/v2021-06-07/projects" \
     -H "Authorization: Bearer $SANITY_TOKEN" \
     -d '{"displayName":"<name>"}'
   ```
2. Créer le dataset `production`
3. Créer un token editor via API
4. Seeder le contenu via script Python (voir `scripts/seed-sanity.py`)

### Couche 5 — Déploiement (5 min)

1. `git add -A && git commit && git push origin main`
2. Déclencher le deploy via **Vercel API REST** (pas CLI) :
   ```bash
   curl -X POST "https://api.vercel.com/v13/deployments" \
     -H "Authorization: Bearer $VERCEL_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"name":"<project>","project":"<project_id>","gitSource":{"type":"github","repoId":<id>,"ref":"main"},"target":"production"}'
   ```
3. Monitorer : polling `/v13/deployments/<id>` toutes les 10s
4. Vérifier : `curl -s -o /dev/null -w "%{http_code}" <url>`

### Couche 6 — Validation (5 min)

1. Vérifier homepage, signup, studio
2. Tester le formulaire
3. Vérifier que le contenu Sanity est chargé
4. Livrer les URLs au user

## Pièges connus — LIRE AVANT CHAQUE PROJET

| Piège | Solution |
|---|---|
| `projectId can only contain a-z, 0-9 and dashes` | Fallback `"placeholder"` dans client.ts, jamais `""` |
| `vercel env add` crée des vars encrypted | Utiliser API v10 avec `"type":"plain"` |
| `vercel deploy` timeout ou "Unexpected error" | Utiliser API REST v13 `/deployments` |
| Sanity v5 + React 18 = crash `useEffectEvent` | Rester sur Sanity v3.99.0 |
| GitHub PAT fine-grained sans `contents:write` | SSH deploy key avec write access |
| `vercel build` bloque indéfiniment | Ne jamais utiliser, toujours API |
| Sanity Studio crashe sur Vercel | Vérifier que `sanity.config.ts` est à la racine |
| Env vars non lues au build | Vérifier `target` inclut `production` |

## Credentials

| Service | Env var / Méthode | Notes |
|---|---|---|
| OpenAI | `OPENAI_API_KEY` | Pour conception produit (GPT) |
| Anthropic | `ANTHROPIC_API_KEY` | Pour specs techniques (Claude) |
| OpenRouter | `OPENROUTER_API_KEY` | Fallback Claude |
| Vercel | Token en mémoire Notion | API deploy + env vars |
| Sanity | Token robot par projet | Créer via API par projet |
| GitHub | SSH deploy key par repo | Créer par projet |

## Temps cible

| Phase | Durée |
|---|---|
| Pré-requis (GitHub + Vercel) | 5 min |
| Conception (GPT) | 3 min |
| Specs (Claude) | 3 min |
| Scaffolding + code | 20 min |
| Sanity CMS | 10 min |
| Deploy + validation | 10 min |
| **Total** | **~50 min** |

## Ressources

- `references/prompts.md` — Prompts GPT et Claude pour couches 1-2
- `references/package-template.json` — package.json avec versions exactes validées
- `references/version-matrix.md` — Matrice de compatibilité détaillée
- `scripts/seed-sanity.py` — Template de script de seeding Sanity
- `templates/sanity-client.ts` — Client Sanity avec fallback placeholder
- `templates/sanity-config.ts` — Configuration Sanity Studio v3
