#!/bin/bash
# Script de test pour yOS Voice

echo "🎤 Test du Skill yOS Voice"
echo "=========================="
echo ""

SCRIPT_DIR="/home/ubuntu/skills/yos-voice/scripts"

# Test 1 : Parole simple
echo "Test 1: Parole simple avec voix conversationnelle"
python3 $SCRIPT_DIR/voice_conversation.py speak "Bonjour, ceci est un test de yOS Voice" "Conversational English Guy"
echo "✅ Test 1 terminé"
echo ""

# Test 2: Parole avec contexte yOS (auto-sélection de voix)
echo "Test 2: Contexte yOS (auto-sélection Literature Professor)"
python3 $SCRIPT_DIR/voice_conversation.py speak "yOS est une architecture conceptuelle pour une nouvelle société et une humanité éclairée"
echo "✅ Test 2 terminé"
echo ""

# Test 3: Liste des voix
echo "Test 3: Liste des voix disponibles"
python3 $SCRIPT_DIR/voice_conversation.py list | head -20
echo "... (liste tronquée)"
echo "✅ Test 3 terminé"
echo ""

echo "🎉 Tous les tests sont terminés !"
echo ""
echo "Pour tester la lecture de document:"
echo "  python3 $SCRIPT_DIR/voice_conversation.py read /chemin/vers/document.txt"
echo ""
echo "Pour créer une voix personnalisée:"
echo "  python3 $SCRIPT_DIR/voice_conversation.py create 'votre description'"
