---
name: fransai-basic
description: Traduit tout contenu français classique en Fransai Basic — orthographe simplifiée et grammaire allégée selon les 27 règles O1-O15 + G1-G12. Utiliser quand l'utilisateur demande de "traduire en fransai basic", "simplifier en fransai", "appliquer les règles Fransai Basic", ou veut démontrer la force simplificatrice du système. Produit le texte transformé avec comptage de caractères et gain mesuré en pourcentage.
---

# Fransai Basic — Skill de traduction

## Contexte

Fransai Basic simplifie le français en 27 règles : 15 orthographiques (O1-O15) + 12 grammaticales (G1-G12). Objectif : −30% de volume textuel, apprentissage réduit de 8-10 ans à 2-4 ans.

Règles complètes avec exemples détaillés : lire `/home/ubuntu/skills/fransai-basic/references/regles.md`

## Workflow

### 1. Analyser le texte source

Mesurer : nombre de caractères, mots, niveau CECRL estimé (A2/B1/B2/C1/C2).

### 2. Appliquer les règles O (orthographe) en premier

| Règle | Principe | Avant → Après |
|-------|----------|---------------|
| O1 | Supprimer lettres muettes finales | `enfants` → `anfan` |
| O2 | Consonnes doubles → simple | `belle` → `bel` |
| O3 | `ph` → `f` | `philosophie` → `filosofie` |
| O4 | `ch` (son /k/) → `k` | `orchestre` → `orkestr` |
| O5 | `qu` → `k` | `question` → `kestion` |
| O6 | `eau`/`au` → `o` | `beau` → `bo` |
| O7 | `ai`/`ei` → `e` | `maison` → `mezon` |
| O8 | `ou` → `u` (son /u/) | `toujours` → `tujur` |
| O9 | Supprimer accents inutiles | `été` → `ete` |
| O10 | `ç` → `s` | `garçon` → `garson` |
| O11 | `x` final muet → supprimer | `voix` → `voa` |
| O12 | `y` intérieur → `i` | `pays` → `pei` |
| O13 | `h` muet initial → supprimer | `homme` → `om` |
| O14 | `gn` → `ny` | `montagne` → `montany` |
| O15 | `-tion` → `-sion` | `nation` → `nasion` |

### 3. Appliquer les règles G (grammaire) ensuite

| Règle | Principe | Avant → Après |
|-------|----------|---------------|
| G1 | Participe passé invariable avec "avoir" | `mangées` → `manje` |
| G2 | Pluriel : `-s` uniquement (pas `-x`) | `choux` → `chou-s` |
| G3 | Féminin : invariable (pas `-e` muet) | `petite` → `petit` |
| G4 | Subjonctif → indicatif présent | `qu'il vienne` → `ki il vien` |
| G5 | Conditionnel passé 2e forme → conditionnel présent | `eussions adopté` → `auron adopte` |
| G6 | `quoique`/`quoi que` → `mem si` | `quoique difficile` → `mem si difisil` |
| G7 | `davantage`/`d'avantage` → `plu` | `davantage de temps` → `plu de tan` |
| G8 | `quelque`/`quel que` → `kelke`/`kel ke` | `quelque chose` → `kelke choz` |
| G9 | Pluriels composés : accord simplifié | `chefs-d'œuvre` → `chef-d'oeuvr-s` |
| G10 | Négation : supprimer `ne` | `je ne sais pas` → `je se pa` |
| G11 | Formules de politesse → formes courtes | `Veuillez agréer...` → `Kordialman` |
| G12 | Locutions verbales complexes → verbes simples | `il y a lieu de procéder à` → `il fo fer` |

### 4. Produire la sortie

Format obligatoire :

```
## Texte original
[texte source]
Caractères : X | Mots : Y | Niveau : C2/B1/etc.

---

## Version Fransai Basic
[texte transformé]
Caractères : X' | Mots : Y' | Gain : −Z%

---

## Cas notables transformés
| Expression originale | Fransai Basic | Gain |
|---------------------|---------------|------|
| [expression 1]      | [version]     | −X%  |
```

## Expressions pré-transformées (référence rapide)

| Français standard | Fransai Basic | Gain |
|-------------------|---------------|------|
| Nonobstant les dispositions susmentionnées | Malgre la regl en vigu | −77% |
| En ce qui concerne la question posée | Sur se kestion | −63% |
| Il convient de noter que | Not ke | −77% |
| Dans le cadre de cette réforme | Dan set reform | −55% |
| Conformément aux dispositions en vigueur | Selon la regl | −69% |
| Il y a lieu de procéder à | Il fo | −85% |
| À toutes fins utiles | Pour info | −59% |
| En vue de | Pour | −60% |
| Suite à votre demande | Apre votr demand | −23% |
| Veuillez agréer l'expression de mes sentiments distingués | Kordialman | −82% |
| Anticonstitutionnellement (25 lettres) | Antikonstitusionelman | −16% |
| Chrysanthèmes | Krizantem | −27% |
| Prestidigitateurs professionnels | Prestijitatr profasionel | −28% |

## Options de sortie

- **Standard** : texte transformé + tableau des cas notables
- **Format superposé** : tableau 2 colonnes (FRANÇAIS STANDARD | FRANSAI BASIC), une ligne par groupe de mots — demander explicitement
- **Comparatif complet** : texte original intégral + texte simplifié intégral + tableau des cas + statistiques globales

## Règles de priorité

1. Fidélité phonétique > économie de caractères
2. Ne pas transformer les noms propres, acronymes, termes techniques sans équivalent
3. Conserver la ponctuation originale
4. En cas d'ambiguïté : appliquer la règle la plus proche et signaler l'incertitude entre parenthèses
