# eYa AutoLive2D — Pipeline Clarity Document

## Le flux complet en 3 étapes

```
[Portrait JPG]
      │
      ▼ ÉTAPE 1: See-through (HuggingFace API)
      │  → Génère TOUJOURS 24 layers fixes (liste prédéfinie)
      │  → Beaucoup sont VIDES pour eYa (elle n'a pas de queue, ailes, etc.)
      │
      ▼ FILTRE: Garder seulement les layers avec pixels réels
      │
      ▼ ÉTAPE 2: Renommage (colle Python)
      │  → Mapper les noms See-through → noms Stretchy Studio
      │  → Reconstruire le PSD avec les bons noms
      │
      ▼ ÉTAPE 3: Stretchy Studio (local WebGL)
         → Auto-rig → 40+ paramètres Live2D
         → Export .stretch + animations
```

---

## ÉTAPE 1 — See-through : les 24 layers fixes

See-through génère TOUJOURS ces 24 catégories (liste fixe, indépendante du personnage) :

| # | Nom See-through | Pixels eYa | Statut |
|---|----------------|------------|--------|
| 00 | back_hair | 133 199 (22.6%) | ✅ PLEIN |
| 01 | bottomwear | 0 | ❌ VIDE |
| 02 | ears | 12 627 (2.1%) | ✅ PRÉSENT |
| 03 | earwear | 2 726 (0.5%) | ⚠️ SPARSE |
| 04 | eyebrow | 3 891 (0.7%) | ✅ PRÉSENT |
| 05 | eyelash | 6 081 (1.0%) | ✅ PRÉSENT |
| 06 | eyewear | 0 | ❌ VIDE |
| 07 | eyewhite | 3 912 (0.7%) | ✅ PRÉSENT |
| 08 | face | 106 832 (18.1%) | ✅ PLEIN |
| 09 | footwear | 0 | ❌ VIDE |
| 10 | front_hair | 116 988 (19.8%) | ✅ PLEIN |
| 11 | handwear | 0 | ❌ VIDE |
| 12 | head | 113 930 (19.3%) | ✅ PLEIN |
| 13 | headwear | 0 | ❌ VIDE |
| 14 | irides | 2 303 (0.4%) | ⚠️ SPARSE |
| 15 | legwear | 0 | ❌ VIDE |
| 16 | mouth | 4 406 (0.7%) | ✅ PRÉSENT |
| 17 | neck | 67 185 (11.4%) | ✅ PLEIN |
| 18 | neckwear | 0 | ❌ VIDE |
| 19 | nose | 8 971 (1.5%) | ✅ PRÉSENT |
| 20 | objects | 0 | ❌ VIDE |
| 21 | tail | 0 | ❌ VIDE |
| 22 | topwear | 87 787 (14.9%) | ✅ PLEIN |
| 23 | wings | 0 | ❌ VIDE |

**Résultat : 12 layers non-vides sur 24**

---

## ÉTAPE 2 — Mapping See-through → Stretchy Studio

See-through et Stretchy Studio utilisent des conventions différentes.
Le mapping est fait manuellement dans le script Python :

| See-through (nom fichier) | Stretchy Studio (nom layer PSD) | Action |
|--------------------------|----------------------------------|--------|
| 00_back_hair | `back hair` | Renommer (underscore → espace) |
| 02_ears | `ears-l` + `ears-r` | Split + miroir horizontal |
| 04_eyebrow | `eyebrow-l` + `eyebrow-r` | Split + miroir |
| 05_eyelash | `eyelash-l` + `eyelash-r` | Split + miroir |
| 07_eyewhite | `eyewhite-l` + `eyewhite-r` | Split + miroir |
| 08_face | `face` | Renommer |
| 10_front_hair | `front hair` | Renommer |
| 12_head | *(non utilisé — déjà dans face)* | Ignorer |
| 14_irides | `irides-l` + `irides-r` | Split + miroir |
| 16_mouth | `mouth` | Renommer |
| 17_neck | `neck` | Renommer |
| 19_nose | `nose` | Renommer |
| 22_topwear | `topwear` | Renommer |

**Résultat : 17 layers dans le PSD final (12 originaux + 5 miroirs)**

---

## ÉTAPE 3 — Stretchy Studio : KNOWN_TAGS attendus

Liste complète des noms que Stretchy Studio reconnaît (armatureOrganizer.js) :

```
back hair, front hair, headwear, face
irides, irides-l, irides-r
eyebrow, eyebrow-l, eyebrow-r
eyewhite, eyewhite-l, eyewhite-r
eyelash, eyelash-l, eyelash-r
eyewear, ears, ears-l, ears-r, earwear
nose, mouth, neck, neckwear, topwear
handwear, handwear-l, handwear-r
bottomwear
legwear, legwear-l, legwear-r
footwear, footwear-l, footwear-r
tail, wings, objects
```

**Total : 31 tags possibles**
**Pour eYa : 17 layers matchent (tous les tags présents dans le PSD)**

---

## Clarification des chiffres historiques

| Moment | Chiffre | Explication |
|--------|---------|-------------|
| See-through output | 24 | Liste fixe de catégories (toujours 24) |
| Layers non-vides | 12 | Layers avec pixels réels pour eYa |
| PSD v1 (mauvais noms) | 12/31 matchés | Noms avec underscores non reconnus |
| PSD v2 (bons noms) | 17/31 matchés | 12 originaux + 5 miroirs L/R |
| Paramètres Live2D | 40+ | Générés par Stretchy Studio après rig |

---

## Pipeline automatisé final (script Python unique)

```python
# ÉTAPE 1: See-through API
layers = seethrough_api(portrait_jpg)  # → 24 layers

# ÉTAPE 2: Filtrer les vides
non_empty = [l for l in layers if l.pixel_count > threshold]

# ÉTAPE 3: Mapper les noms
MAPPING = {
    'back_hair': 'back hair',
    'ears': ['ears-l', 'ears-r'],  # split + mirror
    'eyebrow': ['eyebrow-l', 'eyebrow-r'],
    'eyelash': ['eyelash-l', 'eyelash-r'],
    'eyewhite': ['eyewhite-l', 'eyewhite-r'],
    'face': 'face',
    'front_hair': 'front hair',
    'irides': ['irides-l', 'irides-r'],
    'mouth': 'mouth',
    'neck': 'neck',
    'nose': 'nose',
    'topwear': 'topwear',
}

# ÉTAPE 4: Construire le PSD
psd = build_psd(mapped_layers)  # → eya_stretchy.psd

# ÉTAPE 5: Charger dans Stretchy Studio
# (manuel via browser OU automatisé via Playwright)
```
