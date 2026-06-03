# Matrice de compatibilité — Versions validées

## Combinaison stable (testée et déployée)

| Package | Version | Contrainte |
|---|---|---|
| react | 18.3.1 | Exact — Sanity v3 incompatible React 19 |
| react-dom | 18.3.1 | Doit matcher react |
| next | 14.2.x | App Router stable, pas de breaking changes |
| sanity | 3.99.0 | Dernière v3 — v5 requiert `useEffectEvent` |
| next-sanity | 9.x | Compatible Sanity v3 + Next 14 |
| @sanity/client | 6.21.x | Client API stable |
| @sanity/vision | 3.x | Doit matcher Sanity major |
| @sanity/visual-editing | 2.1.x | Visual editing overlay |
| @sanity/image-url | 1.0.x | URL builder pour images |
| styled-components | 6.x | Requis par Sanity Studio |
| typescript | 5.x | Standard |
| tailwindcss | 3.x | Pas encore Tailwind 4 |

## Incompatibilités connues

| Combinaison | Erreur | Solution |
|---|---|---|
| Sanity v5 + React 18 | `useEffectEvent is not a function` | Rester sur Sanity v3.99 |
| Sanity v5 + React 19 stable | `useEffectEvent is not a function` | React 19 stable n'a pas `useEffectEvent` |
| Next 15 + Sanity v3 | Warnings async params | Fonctionne mais warnings |
| Next 16 + React 19 | Breaking changes multiples | Éviter |
| next-sanity 10+ | Requiert Sanity v5 | Rester sur next-sanity 9 |

## Vérification rapide

```bash
# Après pnpm install, vérifier les versions
node -e "
const p = require('./package.json');
const deps = {...p.dependencies, ...p.devDependencies};
['react','next','sanity','next-sanity'].forEach(k => {
  const v = require(k + '/package.json').version;
  console.log(k + ': ' + v);
});
"
```

## Mise à jour future

Quand Sanity v5 sera compatible React 19 stable (avec `useEffectEvent` exporté) :
1. Mettre à jour cette matrice
2. Tester la combinaison complète
3. Mettre à jour `package-template.json`
4. Mettre à jour `SKILL.md`
