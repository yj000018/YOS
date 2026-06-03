#!/usr/bin/env python3
"""
yOS Voice - Conversation Vocale Interactive
Utilise Hume AI TTS pour générer des réponses vocales naturelles
"""

import json
import subprocess
import sys
from pathlib import Path

# Configuration
DEFAULT_VOICE = "Conversational English Guy"
VOICE_PREFERENCES_FILE = Path("/home/ubuntu/yos_memory/profile/voice_preferences.json")

# Mapping contexte → voix recommandée
CONTEXT_VOICE_MAP = {
    "yos": "Literature Professor",
    "philosophy": "Brooding Intellectual Man",
    "inspiration": "Inspiring Woman",
    "technical": "Deep Male Conversational Voice",
    "meditation": "Serene Assistant",
    "narrative": "Campfire Narrator",
    "general": "Conversational English Guy"
}


def load_voice_preferences():
    """Charge les préférences vocales de l'utilisateur"""
    if VOICE_PREFERENCES_FILE.exists():
        with open(VOICE_PREFERENCES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "default_voice": DEFAULT_VOICE,
        "context_voices": CONTEXT_VOICE_MAP.copy(),
        "auto_select": True,
        "speed": 1.0
    }


def save_voice_preferences(prefs):
    """Sauvegarde les préférences vocales"""
    VOICE_PREFERENCES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(VOICE_PREFERENCES_FILE, 'w', encoding='utf-8') as f:
        json.dump(prefs, f, indent=2, ensure_ascii=False)


def detect_context(text):
    """Détecte le contexte de la conversation pour sélection de voix"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ["yos", "société", "architecture sociétale"]):
        return "yos"
    elif any(word in text_lower for word in ["philosophie", "conscience", "éveil"]):
        return "philosophy"
    elif any(word in text_lower for word in ["inspire", "motivation", "transformation"]):
        return "inspiration"
    elif any(word in text_lower for word in ["code", "technique", "algorithme", "système"]):
        return "technical"
    elif any(word in text_lower for word in ["méditation", "calme", "sérénité"]):
        return "meditation"
    elif any(word in text_lower for word in ["histoire", "raconte", "narratif"]):
        return "narrative"
    else:
        return "general"


def select_voice(text, preferences):
    """Sélectionne la voix appropriée selon le contexte"""
    if not preferences.get("auto_select", True):
        return preferences.get("default_voice", DEFAULT_VOICE)
    
    context = detect_context(text)
    return preferences["context_voices"].get(context, preferences["default_voice"])


def speak_with_hume(text, voice_name=None, speed=1.0, continuation_of=None, description=None):
    """
    Génère et joue la parole avec Hume TTS
    
    Args:
        text: Texte à vocaliser
        voice_name: Nom de la voix à utiliser
        speed: Vitesse de parole (0.5 à 2.0)
        continuation_of: ID de génération précédente pour continuité
        description: Instructions tonales supplémentaires
    
    Returns:
        generation_id: ID de la génération pour continuité future
    """
    # Construction de l'input JSON
    input_data = {
        "utterances": [
            {
                "text": text
            }
        ]
    }
    
    # Ajout de la voix si spécifiée
    if voice_name:
        input_data["voiceName"] = voice_name
        input_data["provider"] = "HUME_AI"
    
    # Ajout de la vitesse si différente de 1.0
    if speed != 1.0:
        input_data["utterances"][0]["speed"] = speed
    
    # Ajout de la description tonale si fournie
    if description:
        input_data["utterances"][0]["description"] = description
    
    # Ajout de la continuation si fournie
    if continuation_of:
        input_data["continuationOf"] = continuation_of
    
    # Appel Hume TTS via MCP
    cmd = [
        "manus-mcp-cli", "tool", "call", "tts",
        "--server", "hume",
        "--input", json.dumps(input_data)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Parse du résultat pour extraire le generation_id
        # Le résultat contient le generation_id pour continuité
        result_data = json.loads(result.stdout)
        generation_id = result_data.get("generation_id")
        
        return generation_id
    
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la génération vocale: {e.stderr}", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        print(f"❌ Erreur de parsing du résultat Hume", file=sys.stderr)
        return None


def read_long_text(text, voice_name=None, speed=1.0, segment_size=5):
    """
    Lit un texte long en segments avec continuité vocale
    
    Args:
        text: Texte complet à lire
        voice_name: Voix à utiliser
        speed: Vitesse de lecture
        segment_size: Nombre de paragraphes par segment
    """
    # Découpage en paragraphes
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    print(f"📖 Lecture de {len(paragraphs)} paragraphes avec voix '{voice_name}'")
    
    generation_id = None
    
    # Lecture par segments
    for i in range(0, len(paragraphs), segment_size):
        segment = '\n\n'.join(paragraphs[i:i+segment_size])
        
        print(f"🔊 Segment {i//segment_size + 1}/{(len(paragraphs)-1)//segment_size + 1}")
        
        # Génération avec continuité
        generation_id = speak_with_hume(
            text=segment,
            voice_name=voice_name,
            speed=speed,
            continuation_of=generation_id
        )
        
        if not generation_id:
            print("⚠️ Erreur lors de la lecture, arrêt.")
            break
    
    print("✅ Lecture terminée")


def create_custom_voice(description, sample_text=None):
    """
    Crée une voix personnalisée selon une description
    
    Args:
        description: Description de la voix souhaitée
        sample_text: Texte d'échantillon (optionnel)
    
    Returns:
        generation_id: ID de la génération pour sauvegarde
    """
    if not sample_text:
        # Texte d'échantillon par défaut
        sample_text = "Bonjour, voici un échantillon de ma voix. Comment trouvez-vous cette intonation ?"
    
    print(f"🎨 Création de voix : {description}")
    print(f"🎤 Échantillon : {sample_text}")
    
    # Génération avec description (modelVersion 1 requis)
    input_data = {
        "utterances": [
            {
                "text": sample_text,
                "description": description
            }
        ],
        "modelVersion": "1"
    }
    
    cmd = [
        "manus-mcp-cli", "tool", "call", "tts",
        "--server", "hume",
        "--input", json.dumps(input_data)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        result_data = json.loads(result.stdout)
        generation_id = result_data.get("generation_id")
        
        print("✅ Voix générée. Écoutez l'échantillon.")
        print(f"💾 Generation ID: {generation_id}")
        print("Pour sauvegarder cette voix, utilisez: save_voice(generation_id, 'nom_voix')")
        
        return generation_id
    
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la création de voix: {e.stderr}", file=sys.stderr)
        return None


def save_voice(generation_id, voice_name):
    """
    Sauvegarde une voix générée dans la bibliothèque
    
    Args:
        generation_id: ID de la génération à sauvegarder
        voice_name: Nom à donner à la voix
    """
    cmd = [
        "manus-mcp-cli", "tool", "call", "save_voice",
        "--server", "hume",
        "--input", json.dumps({
            "generationId": generation_id,
            "name": voice_name
        })
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ Voix '{voice_name}' sauvegardée dans votre bibliothèque")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la sauvegarde: {e.stderr}", file=sys.stderr)
        return False


def list_voices():
    """Liste toutes les voix disponibles"""
    cmd = [
        "manus-mcp-cli", "tool", "call", "list_voices",
        "--server", "hume",
        "--input", json.dumps({"provider": "HUME_AI"})
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur: {e.stderr}", file=sys.stderr)


def main():
    """Fonction principale pour tests"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python voice_conversation.py speak <texte> [voix]")
        print("  python voice_conversation.py read <fichier> [voix]")
        print("  python voice_conversation.py create <description>")
        print("  python voice_conversation.py list")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "speak":
        if len(sys.argv) < 3:
            print("❌ Texte requis")
            sys.exit(1)
        
        text = sys.argv[2]
        voice = sys.argv[3] if len(sys.argv) > 3 else None
        
        prefs = load_voice_preferences()
        if not voice:
            voice = select_voice(text, prefs)
        
        print(f"🔊 Parole avec voix: {voice}")
        speak_with_hume(text, voice_name=voice, speed=prefs.get("speed", 1.0))
    
    elif command == "read":
        if len(sys.argv) < 3:
            print("❌ Fichier requis")
            sys.exit(1)
        
        file_path = Path(sys.argv[2])
        if not file_path.exists():
            print(f"❌ Fichier non trouvé: {file_path}")
            sys.exit(1)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        voice = sys.argv[3] if len(sys.argv) > 3 else None
        prefs = load_voice_preferences()
        
        if not voice:
            voice = select_voice(text, prefs)
        
        read_long_text(text, voice_name=voice, speed=prefs.get("speed", 1.0))
    
    elif command == "create":
        if len(sys.argv) < 3:
            print("❌ Description requise")
            sys.exit(1)
        
        description = sys.argv[2]
        generation_id = create_custom_voice(description)
        
        if generation_id:
            save_choice = input("Sauvegarder cette voix ? (o/n): ")
            if save_choice.lower() == 'o':
                voice_name = input("Nom de la voix: ")
                save_voice(generation_id, voice_name)
    
    elif command == "list":
        list_voices()
    
    else:
        print(f"❌ Commande inconnue: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
