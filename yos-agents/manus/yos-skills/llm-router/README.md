# LLM Router Skill

## Vue d'ensemble

Système de routage intelligent qui analyse chaque requête utilisateur et sélectionne automatiquement le LLM le plus adapté parmi les modèles disponibles via API.

## Architecture

```
┌─────────────────┐
│ Requête User    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Analyse Intent  │ ← router.py::analyze_intent()
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Matrice Routing │ ← ROUTING_MATRIX
└────────┬────────┘
         │
         ▼
    ┌────┴────┐
    │ Mode ?  │
    └────┬────┘
         │
    ┌────┴────────────┐
    │                 │
    ▼                 ▼
┌─────────┐    ┌──────────────┐
│  auto   │    │  semi-auto   │
└────┬────┘    └──────┬───────┘
     │                │
     │                ▼
     │         ┌──────────────┐
     │         │ Confirmation │
     │         └──────┬───────┘
     │                │
     └────────┬───────┘
              │
              ▼
     ┌────────────────┐
     │ Exécution API  │
     └────────┬───────┘
              │
              ▼
     ┌────────────────┐
     │   Réponse      │
     └────────────────┘
```

## Matrice de routage

| Catégorie | LLM | Justification |
|-----------|-----|---------------|
| `realtime_search` | Perplexity sonar-pro | Recherche web temps réel avec citations |
| `vision_multimodal` | Gemini 2.5 Flash | Vision avancée, génération d'images |
| `code_generation` | GPT-5 | Leader raisonnement et programmation |
| `complex_reasoning` | GPT-5 | Logique complexe et déduction |
| `creative_writing` | Claude 3 Opus | Contexte long, finesse littéraire |
| `conversation` | Grok 4 | Approche conversationnelle unique |
| `data_analysis` | GPT-5 | Analyse quantitative structurée |
| `default` | Claude 3.7 Sonnet | Équilibre optimal performance/coût |

## Modes de fonctionnement

### Semi-auto (défaut)

Manus analyse la requête, propose un LLM avec justification, et attend confirmation :

```
Détection : requête de type [code_generation]
Recommandation : GPT-5 (leader raisonnement et programmation)
Confirmer ? [oui/non/autre modèle]
```

### Auto

Routage et exécution directs sans confirmation. Activation :

```
"Passe le routeur LLM en mode automatique"
```

## Utilisation

### Via Manus (intégré)

Aucune action requise. Le routeur s'active automatiquement sur chaque nouvelle requête.

### Via CLI (test)

```bash
# Routage automatique
python3 /home/ubuntu/skills/llm-router/router.py "Quelle est l'actualité en IA ?"

# Override manuel
python3 /home/ubuntu/skills/llm-router/router.py "Écris un poème" grok
```

### Sortie JSON

```json
{
  "detected_category": "realtime_search",
  "confidence": 0.67,
  "selected_model": "Perplexity sonar-pro",
  "justification": "Spécialisé recherche web temps réel avec citations",
  "response": "..."
}
```

## Configuration

Fichier : `/home/ubuntu/skills/llm-router/config.json`

```json
{
  "mode": "semi-auto",
  "description": "Mode de fonctionnement du routeur LLM"
}
```

Modification :

```bash
# Passer en mode auto
echo '{"mode": "auto"}' > /home/ubuntu/skills/llm-router/config.json
```

## Commandes utilisateur

| Commande | Action |
|----------|--------|
| "Mode routeur auto" | Active le mode automatique |
| "Mode routeur semi-auto" | Active la confirmation (défaut) |
| "Utilise [modèle] pour cette requête" | Override ponctuel |
| "Pourquoi ce modèle ?" | Affiche la justification du choix |

## Dépendances

Packages Python requis :

```bash
sudo pip3 install requests google-genai openai anthropic xai-sdk
```

Variables d'environnement (déjà configurées) :

- `SONAR_API_KEY` (Perplexity)
- `GEMINI_API_KEY` (Google)
- `OPENAI_API_KEY` (OpenAI)
- `XAI_API_KEY` (Grok)
- `ANTHROPIC_API_KEY` (Claude)

## Extension

### Ajouter une catégorie

1. Ajouter dans `TaskCategory` enum
2. Définir keywords dans `analyze_intent()`
3. Ajouter mapping dans `ROUTING_MATRIX`

### Ajouter un LLM

1. Ajouter dans `LLMModel` enum
2. Créer fonction `call_<model>()`
3. Ajouter dans `LLM_CALLERS`
4. Mettre à jour `ROUTING_MATRIX`

## Métriques

Le routeur peut logger les décisions pour analyse :

```python
# À implémenter
log_routing_decision(category, model, confidence, user_override)
```

## Gouvernance

**Propriétaire** : Yannick (Y-OS)  
**Créé** : 2026-02-08  
**Version** : 1.0  
**Statut** : Opérationnel
