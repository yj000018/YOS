# yOS Voice - Guide Rapide

## Installation

Le skill est prêt à l'emploi. Aucune installation supplémentaire requise.

## Utilisation Rapide

### Dans Manus (Conversation)

Utilisez simplement les commandes vocales naturelles :

```
"Active le mode vocal"
"Lis-moi ce texte"
"Utilise la voix Inspiring Woman"
"Crée une voix : homme français, ton calme"
```

### En Ligne de Commande (Tests)

```bash
# Parler un texte
python3 /home/ubuntu/skills/yos-voice/scripts/voice_conversation.py speak "Bonjour, ceci est un test"

# Parler avec une voix spécifique
python3 /home/ubuntu/skills/yos-voice/scripts/voice_conversation.py speak "Bonjour" "Inspiring Woman"

# Lire un fichier
python3 /home/ubuntu/skills/yos-voice/scripts/voice_conversation.py read /path/to/document.txt

# Créer une voix personnalisée
python3 /home/ubuntu/skills/yos-voice/scripts/voice_conversation.py create "voix masculine grave et calme"

# Lister les voix disponibles
python3 /home/ubuntu/skills/yos-voice/scripts/voice_conversation.py list
```

## Voix Recommandées pour yOS

- **Conversations générales** : `Conversational English Guy`
- **Concepts yOS** : `Literature Professor`
- **Contenu inspirant** : `Inspiring Woman`
- **Philosophie** : `Brooding Intellectual Man`
- **Lectures longues** : `Campfire Narrator`

## Configuration

Les préférences sont stockées dans :
```
/home/ubuntu/yos_memory/profile/voice_preferences.json
```

Structure :
```json
{
  "default_voice": "Conversational English Guy",
  "auto_select": true,
  "speed": 1.0,
  "context_voices": {
    "yos": "Literature Professor",
    "philosophy": "Brooding Intellectual Man",
    "inspiration": "Inspiring Woman"
  }
}
```

## Exemples

### Exemple 1 : Test Simple

```bash
cd /home/ubuntu/skills/yos-voice/scripts
python3 voice_conversation.py speak "Bonjour Yannick, bienvenue dans yOS Voice"
```

### Exemple 2 : Lecture de Document

```bash
# Créer un document test
echo "yOS est une architecture conceptuelle pour une nouvelle société." > /tmp/test_yos.txt

# Le lire avec voix appropriée (auto-détection du contexte yOS)
python3 voice_conversation.py read /tmp/test_yos.txt
```

### Exemple 3 : Voix Personnalisée

```bash
# Créer une voix pour yOS
python3 voice_conversation.py create "voix masculine française, ton sage et inspirant, chaleureux"

# Suivre les instructions pour sauvegarder comme "yOS Sage"
```

## Dépannage

### Pas de son
- Vérifier le volume système
- Vérifier les permissions audio du navigateur
- Tester avec : `python3 voice_conversation.py speak "test"`

### Erreur MCP
- Vérifier que le serveur Hume est configuré : `manus-mcp-cli tool list --server hume`
- Vérifier la connexion internet

### Voix non trouvée
- Lister les voix disponibles : `python3 voice_conversation.py list`
- Utiliser un nom exact de la liste

## Documentation Complète

Voir `SKILL.md` pour la documentation complète avec tous les workflows et commandes avancées.

---

**Créé par** : Manus AI  
**Date** : 2026-01-31  
**Version** : 1.0
