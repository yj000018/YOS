---
name: yos-voice
description: Conversations vocales interactives avec Hume AI TTS pour yOS. Permet de parler avec Manus et recevoir des réponses vocales naturelles et expressives.
tags: [yOS, voice, hume, conversation, accessibility, Manus]
---

# yOS Voice - Conversations Vocales avec Hume AI

Ce skill active les conversations vocales interactives dans Manus en utilisant Hume AI TTS pour générer des réponses vocales naturelles et expressives.

## Vue d'Ensemble

**yOS Voice** combine :
- 🎤 **Reconnaissance vocale** (Web Speech API du navigateur)
- 🧠 **Traitement Manus** (compréhension et génération de réponse)
- 🔊 **Synthèse vocale Hume AI** (voix naturelles et expressives)

## Capacités

### Voix Disponibles

Hume AI offre **100+ voix** de haute qualité, incluant :

**Voix Conversationnelles** (recommandées pour yOS) :
- `Conversational English Guy` - Voix masculine anglaise naturelle
- `Demure Conversationalist` - Voix calme et posée
- `Warm Female Assistant Voice` - Voix féminine chaleureuse d'assistante
- `Deep Male Conversational Voice` - Voix masculine profonde conversationnelle
- `Serene Assistant` - Voix sereine et apaisante
- `Soft Male Conversationalist` - Voix masculine douce
- `Comforting Male Conversationalist` - Voix masculine réconfortante

**Voix Inspirantes** (pour contenu motivant) :
- `Inspiring Man` - Voix masculine inspirante
- `Inspiring Woman` - Voix féminine inspirante
- `Inspiring Older Guy` - Voix masculine mature inspirante

**Voix Narratives** (pour lectures longues) :
- `Nature Documentary Narrator` - Narrateur de documentaire nature
- `Campfire Narrator` - Narrateur de feu de camp
- `English Children's Book Narrator` - Narrateur de livres pour enfants

**Voix Spécialisées** :
- `Literature Professor` - Professeur de littérature
- `Brooding Intellectual Man` - Intellectuel pensif
- `Caring Mother` - Mère bienveillante
- `Wise Wizard` - Sage magicien

### Fonctionnalités Clés

1. **Mode Conversation Continue** : Échanges vocaux fluides
2. **Voix Contextuelle** : Sélection automatique selon le type de contenu
3. **Voix Personnalisée** : Création et sauvegarde de voix sur mesure
4. **Lecture de Documents** : Vocalisation de textes longs
5. **Réponses Expressives** : Intonation et émotion adaptées au contexte

## Commandes Disponibles

### Activation du Mode Vocal

**Commande** : `"Active le mode vocal"` ou `"Conversation vocale"`

**Comportement** :
1. Active la reconnaissance vocale du navigateur
2. Vous parlez, Manus transcrit et traite
3. Manus génère une réponse vocale via Hume
4. Cycle continue jusqu'à désactivation

**Exemple** :
```
User: "Active le mode vocal"
Manus: 🎤 Mode vocal activé. Parlez maintenant...
User: [parle] "Parle-moi de yOS"
Manus: [répond vocalement avec Hume TTS]
```

### Lecture Vocale

**Commande** : `"Lis-moi [texte]"` ou `"Vocalise ce texte"`

**Comportement** :
- Prend le texte fourni
- Le vocalise avec Hume TTS
- Utilise une voix appropriée au contenu

**Exemple** :
```
User: "Lis-moi ce document sur l'architecture sociétale"
Manus: [vocalise le document avec voix "Literature Professor"]
```

### Changement de Voix

**Commande** : `"Change de voix : [nom de voix]"` ou `"Utilise la voix [nom]"`

**Comportement** :
- Change la voix active pour les prochaines réponses
- Sauvegarde la préférence dans le profil yOS

**Exemple** :
```
User: "Utilise la voix Inspiring Woman"
Manus: ✅ Voix changée : Inspiring Woman
[Prochaines réponses utilisent cette voix]
```

### Création de Voix Personnalisée

**Commande** : `"Crée une voix : [description]"`

**Comportement** :
1. Génère une voix selon votre description
2. Vous fait écouter un échantillon
3. Itère selon vos retours
4. Sauvegarde la voix finale dans votre bibliothèque

**Exemple** :
```
User: "Crée une voix : homme français, ton calme et philosophique, légèrement grave"
Manus: 🎨 Création de voix en cours...
[Génère et fait écouter]
Manus: "Voici un échantillon. Souhaitez-vous des ajustements ?"
User: "Un peu plus grave"
Manus: [Ajuste et régénère]
User: "Parfait, sauvegarde-la comme 'Philosophe'"
Manus: ✅ Voix 'Philosophe' sauvegardée dans votre bibliothèque
```

### Liste des Voix

**Commande** : `"Liste les voix disponibles"` ou `"Quelles voix as-tu ?"`

**Comportement** :
- Affiche toutes les voix Hume disponibles
- Indique votre voix active actuelle
- Montre vos voix personnalisées

### Lecture Longue

**Commande** : `"Lis-moi ce document en entier"` ou `"Audiobook mode"`

**Comportement** :
1. Détecte les chapitres/sections
2. Lit de manière continue
3. Utilise `continuationOf` pour cohérence vocale
4. Permet pause/reprise

**Exemple** :
```
User: "Lis-moi ce document de 20 pages sur yOS"
Manus: 📖 Mode lecture longue activé
[Lit le document en continu avec pauses naturelles]
[Vous pouvez dire "Pause", "Continue", "Arrête"]
```

## Workflows Détaillés

### Workflow 1 : Conversation Vocale Interactive

```
1. User: "Active le mode vocal"
   ↓
2. Manus active la reconnaissance vocale browser
   ↓
3. User parle (micro)
   ↓
4. Browser transcrit en texte (STT)
   ↓
5. Manus traite la demande
   ↓
6. Manus génère réponse (texte)
   ↓
7. Manus appelle Hume TTS avec:
   - text: réponse générée
   - voiceName: voix sélectionnée
   - description: instructions tonales si nécessaire
   ↓
8. Hume génère audio et le joue
   ↓
9. Retour à l'étape 3 (écoute)
```

### Workflow 2 : Lecture de Document

```
1. User: "Lis-moi [document]"
   ↓
2. Manus charge le document
   ↓
3. Manus détecte le type de contenu
   ↓
4. Manus sélectionne voix appropriée:
   - Technique → Literature Professor
   - Inspirant → Inspiring Man/Woman
   - Narratif → Campfire Narrator
   ↓
5. Manus découpe en segments (3-5 paragraphes)
   ↓
6. Pour chaque segment:
   - Appel Hume TTS avec continuationOf
   - Lecture audio
   ↓
7. Fin de document
```

### Workflow 3 : Création de Voix Personnalisée

```
1. User: "Crée une voix : [description]"
   ↓
2. Manus parse la description
   ↓
3. Manus génère un texte d'échantillon approprié
   ↓
4. Manus appelle Hume TTS avec:
   - description: description utilisateur
   - text: échantillon
   - modelVersion: "1" (pour génération sans voix)
   ↓
5. Hume génère et joue l'échantillon
   ↓
6. Manus demande feedback
   ↓
7. Si ajustements nécessaires:
   - Manus ajuste la description
   - Retour à l'étape 4
   ↓
8. Si satisfait:
   - Manus sauvegarde avec save_voice
   - Voix disponible pour usage futur
```

## Sélection Automatique de Voix

Le skill sélectionne automatiquement la voix appropriée selon le contexte :

| Type de Contenu | Voix Recommandée | Raison |
|------------------|------------------|--------|
| **Conversation générale** | `Conversational English Guy` | Naturelle et accessible |
| **Concepts yOS** | `Literature Professor` | Autorité et clarté |
| **Contenu inspirant** | `Inspiring Woman` | Motivation et énergie |
| **Lecture longue** | `Campfire Narrator` | Engagement narratif |
| **Contenu technique** | `Deep Male Conversational Voice` | Clarté et professionnalisme |
| **Méditation/Réflexion** | `Serene Assistant` | Calme et apaisement |
| **Contenu philosophique** | `Brooding Intellectual Man` | Profondeur et réflexion |

**Configuration** : Vous pouvez définir vos préférences dans le profil yOS.

## Configuration

### Voix par Défaut

Définir votre voix préférée :

```
User: "Définis [voix] comme voix par défaut"
→ Sauvegardé dans /home/ubuntu/yos_memory/profile/preferences.json
```

### Voix Contextuelle

Activer/désactiver la sélection automatique :

```
User: "Active la sélection automatique de voix"
User: "Désactive la sélection automatique de voix"
```

### Vitesse de Parole

Ajuster la vitesse (0.5 à 2.0) :

```
User: "Parle plus lentement" → speed: 0.8
User: "Parle plus vite" → speed: 1.3
User: "Vitesse normale" → speed: 1.0
```

## Intégration avec yOS

### Chargement Automatique du Contexte

Quand le mode vocal est activé pour une conversation sur yOS :
1. Le contexte yOS est chargé automatiquement
2. Les réponses sont adaptées au framework yOS
3. La voix utilisée reflète le ton de yOS (inspirant, philosophique)

### Stockage en Mémoire

Les insights importants mentionnés vocalement peuvent être stockés :

```
User: [en vocal] "Stocke cette idée en mémoire yOS"
Manus: ✅ Idée stockée : [résumé de l'idée]
```

### Archivage de Conversations Vocales

Les conversations vocales sont automatiquement transcrites et peuvent être archivées :

```
User: "Archive cette conversation vocale"
Manus: ✅ Conversation transcrite et archivée dans yOS Memory
```

## Commandes Avancées

### Mode Performance vs Dictation

**Performance** (création de contenu audio) :
- Travail par petits segments
- Feedback après chaque génération
- Itération pour qualité optimale

```
User: "Mode performance : crée un audiobook de ce texte"
```

**Dictation** (lecture pour soi) :
- Travail par gros segments (3-5 paragraphes)
- Continuation automatique sans feedback
- Optimisé pour vitesse

```
User: "Lis-moi ce document en mode dictation"
```

### Contrôles Pendant la Lecture

Pendant qu'une lecture est en cours :

- `"Pause"` - Met en pause
- `"Continue"` - Reprend
- `"Arrête"` - Arrête complètement
- `"Plus lent"` - Réduit la vitesse
- `"Plus vite"` - Augmente la vitesse
- `"Répète"` - Rejoue le dernier segment

### Export Audio

Sauvegarder l'audio généré :

```
User: "Sauvegarde cette réponse vocale"
Manus: ✅ Audio sauvegardé : /home/ubuntu/yos_voice_outputs/response_[timestamp].wav
```

## Exemples d'Usage

### Exemple 1 : Brainstorming Vocal sur yOS

```
User: "Active le mode vocal"
Manus: 🎤 Mode vocal activé

User: [parle] "Parlons de l'architecture sociétale de yOS"
Manus: [répond vocalement] "L'architecture sociétale de yOS repose sur quatre piliers fondamentaux..."

User: [parle] "Comment intégrer la conscience collective ?"
Manus: [répond vocalement] "La conscience collective dans yOS peut être intégrée à travers..."

User: [parle] "Stocke ces idées en mémoire"
Manus: ✅ Idées stockées dans le projet yOS
```

### Exemple 2 : Lecture de Document

```
User: "Lis-moi le document 'Principes fondateurs de yOS'"
Manus: 📖 Lecture en cours avec voix "Literature Professor"
[Lit le document en entier avec intonation appropriée]
Manus: ✅ Lecture terminée
```

### Exemple 3 : Création de Voix pour yOS

```
User: "Crée une voix pour yOS : voix masculine, ton sage et inspirant, avec une touche de chaleur humaine"
Manus: 🎨 Création de voix en cours...
[Génère et fait écouter]
Manus: "Voici la voix. Qu'en pensez-vous ?"
User: "Parfait ! Sauvegarde-la comme 'yOS Sage'"
Manus: ✅ Voix 'yOS Sage' sauvegardée
User: "Utilise cette voix par défaut pour les conversations yOS"
Manus: ✅ 'yOS Sage' définie comme voix par défaut pour yOS
```

## Notes Techniques

### Latence

**Latence typique** : 2-4 secondes entre votre question et le début de la réponse vocale

**Décomposition** :
- STT (browser) : ~0.5s
- Traitement Manus : ~1-2s
- Hume TTS : ~1-2s

**Optimisations** :
- Utilisation de `continuationOf` pour réduire la latence sur les segments suivants
- Pré-chargement des voix fréquemment utilisées

### Qualité Audio

- **Format** : WAV 48kHz 16-bit mono
- **Qualité** : Haute fidélité, voix naturelles
- **Expressivité** : Intonation, pauses, émotion adaptées

### Limitations

- ⚠️ **Pas de détection émotionnelle** (contrairement à Hume EVI complet)
- ⚠️ **Pas de speech-to-speech natif** (3 étapes : STT → traitement → TTS)
- ⚠️ **Nécessite connexion internet** pour Hume API
- ⚠️ **Latence supérieure** à ChatGPT Advanced Voice Mode (~2-4s vs ~1s)

### Évolution Future

**Court terme** :
- Optimisation de la latence
- Plus de voix personnalisées yOS
- Meilleure sélection contextuelle

**Moyen terme** :
- Migration vers Hume EVI (speech-to-speech natif)
- Détection émotionnelle
- Latence réduite (<1s)

## Dépannage

### Problème : Pas de son

**Solutions** :
1. Vérifier les permissions micro/haut-parleurs du navigateur
2. Vérifier le volume système
3. Tester avec `"Lis-moi bonjour"`

### Problème : Reconnaissance vocale ne fonctionne pas

**Solutions** :
1. Vérifier que le navigateur supporte Web Speech API (Chrome, Edge)
2. Autoriser l'accès au microphone
3. Parler clairement et attendre le signal d'écoute

### Problème : Voix robotique ou de mauvaise qualité

**Solutions** :
1. Changer de voix : `"Utilise la voix [autre voix]"`
2. Créer une voix personnalisée avec plus de détails
3. Vérifier la connexion internet (qualité de streaming)

## Bonnes Pratiques

1. **Parlez clairement** : Articulez bien pour une meilleure transcription
2. **Phrases courtes** : Plus facile à traiter et à répondre
3. **Contexte explicite** : Mentionnez "yOS" si pertinent
4. **Feedback régulier** : Dites si la voix ou le ton ne convient pas
5. **Pauses naturelles** : Laissez Manus finir de parler avant de répondre

## Ressources

- **Documentation Hume TTS** : https://dev.hume.ai/docs/text-to-speech-tts/overview
- **Liste complète des voix** : Commande `"Liste les voix disponibles"`
- **Exemples audio** : `/home/ubuntu/skills/yos-voice/examples/`

---

**Tags** : yOS, voice, hume, conversation, TTS, accessibility, Manus

**Créé par** : Manus AI  
**Date** : 2026-01-31  
**Version** : 1.0
