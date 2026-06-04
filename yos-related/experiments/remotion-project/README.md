# Bonjour ☀️ — Décryptage du message paternel

**Projet Remotion V1** · Y-OS Video Engine · Yannick

---

## Concept

Une intelligence artificielle mobilise toute la connaissance humaine — cryptographie, astrophysique, linguistique, histoire de l'art, cosmologie — pour décrypter un message reçu d'un père.

Le message est : `"Ich wünsche dir einen sonnigen Morgen!"`

La réponse est : **Bonjour ☀️**

---

## Structure du film — 13 séquences

| # | Séquence | Durée | Contenu |
|---|---|---|---|
| 01 | Prologue Cosmique | 25s | Particules, pulsation, transmission reçue |
| 02 | Le Message Apparaît | 25s | Phrase allemande monumentale, annotations |
| 03 | Appel à l'IA | 30s | Dialogue narrateur / IA, terminal |
| 04 | Langue Inventée du Père | 40s | Image réelle, scan, classification glyphes |
| 05 | Permutations Alphabétiques | 40s | Explosion de lettres, recombinaisons |
| 06 | Rotations Spatiales | 35s | 0° / 90° / 180° / 270°, morphing |
| 07 | L'IA Écrit du Code | 40s | Code en live, terminal, modules |
| 08 | Cryptographie & Histoire | 40s | Roues cryptographiques, scores analytiques |
| 09 | Hubble / Quasars / Pulsars | 45s | Carte stellaire, signaux, constellation |
| 10 | La Fréquence Clé | 35s | Pulsation dorée, métriques d'amour |
| 11 | Synthèse Totale | 30s | Toutes les couches, formule finale |
| 12 | Chute Finale | 35s | Fond blanc, **Bonjour ☀️** |
| 13 | Épilogue Making-of | 45s | Timeline 08:45→09:14, 30 min de conception |

**Durée totale : ~7 min 05s** · 12 735 frames @30fps

---

## Identité visuelle

- Palette : noir profond, bleu nuit, graphite, craie, cyan, ambre, jaune solaire
- Typographie : serif cinématique + mono terminal + annotations manuscrites
- Motion : zooms lents, explosions de lettres, rotations 3D, signaux spectraux
- Asset central : image réelle de la langue inventée du père

---

## Langues

- Voix off : **français** (4 voix : narrateur, IA centrale, IA secondaire, système)
- Sous-titres intégrés : **italien** (cinématographiques, position basse)
- Phrase source : **allemand**

---

## Architecture technique

```
src/
├── index.ts              # Entry point Remotion
├── Root.tsx              # Compositions + Series
├── sequences/
│   ├── Seq01_Prologue.tsx
│   ├── Seq02_Message.tsx
│   ├── Seq03_AppelIA.tsx
│   ├── Seq04_LangagePere.tsx
│   ├── Seq05_Permutations.tsx
│   ├── Seq06_Rotations.tsx
│   ├── Seq07_Code.tsx
│   ├── Seq08_Crypto.tsx
│   ├── Seq09_Cosmos.tsx
│   ├── Seq10_Frequence.tsx
│   ├── Seq11_Synthese.tsx
│   ├── Seq12_Chute.tsx
│   └── Seq13_Epilogue.tsx
├── components/
│   ├── Subtitle.tsx      # Sous-titres italiens
│   ├── LogLine.tsx       # Terminal typewriter
│   ├── Particles.tsx     # Particules cosmiques
│   └── ScanLine.tsx      # Effet scanning IA
└── utils/
    └── theme.ts          # Palette, polices, helpers
public/
└── assets/
    └── father-language.png  # Asset central — langue du père
```

---

## Commandes

```bash
# Studio Remotion (preview interactif)
npm start

# Render film complet
npm run render

# Render séquence individuelle
npx remotion render Seq04_LangagePere out/seq04.mp4
```

---

## Placeholders voix off

Chaque séquence contient un commentaire `[VOICE: ...]` indiquant :
- le personnage (Narrateur / IA centrale / IA secondaire / Système)
- le texte exact à enregistrer
- le ton attendu

---

## Genèse

Conçu le matin du 4 avril 2026, vers 8h45, au réveil.
En réaction à un message du père.
En ~30 minutes avec les IA.
Produit par Manus / Y-OS.
