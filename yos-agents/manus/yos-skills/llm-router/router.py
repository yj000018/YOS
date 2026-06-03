#!/usr/bin/env python3
"""
LLM Router - Intelligent routing to optimal LLM based on task type
Author: Manus AI
"""

import os
import json
import sys
from typing import Dict, List, Optional, Tuple
from enum import Enum


class TaskCategory(Enum):
    """Categories of tasks for LLM routing"""
    REALTIME_SEARCH = "realtime_search"
    VISION_MULTIMODAL = "vision_multimodal"
    CODE_GENERATION = "code_generation"
    COMPLEX_REASONING = "complex_reasoning"
    CREATIVE_WRITING = "creative_writing"
    CONVERSATION = "conversation"
    DATA_ANALYSIS = "data_analysis"
    DEFAULT = "default"


class LLMModel(Enum):
    """Available LLM models"""
    PERPLEXITY = "perplexity"
    GEMINI = "gemini"
    GPT5 = "gpt5"
    CLAUDE_OPUS = "claude_opus"
    GROK = "grok"
    CLAUDE_SONNET = "claude_sonnet"


# Routing matrix: maps task categories to optimal LLM
ROUTING_MATRIX = {
    TaskCategory.REALTIME_SEARCH: (LLMModel.PERPLEXITY, "Perplexity sonar-pro", "Spécialisé recherche web temps réel avec citations"),
    TaskCategory.VISION_MULTIMODAL: (LLMModel.GEMINI, "Google Gemini 2.5 Flash", "Vision avancée, contexte long, génération d'images"),
    TaskCategory.CODE_GENERATION: (LLMModel.GPT5, "OpenAI GPT-5", "Leader raisonnement et programmation"),
    TaskCategory.COMPLEX_REASONING: (LLMModel.GPT5, "OpenAI GPT-5", "Raisonnement profond et logique complexe"),
    TaskCategory.CREATIVE_WRITING: (LLMModel.CLAUDE_OPUS, "Claude 3 Opus", "Contexte étendu, finesse d'écriture"),
    TaskCategory.CONVERSATION: (LLMModel.GROK, "Grok 4", "Approche conversationnelle, base unique"),
    TaskCategory.DATA_ANALYSIS: (LLMModel.GPT5, "OpenAI GPT-5", "Analyse quantitative et structuration"),
    TaskCategory.DEFAULT: (LLMModel.CLAUDE_SONNET, "Claude 3.7 Sonnet", "Équilibre performance/coût optimal"),
}


def analyze_intent(query: str) -> Tuple[TaskCategory, float]:
    """
    Analyze user query to determine task category and confidence score.
    
    Args:
        query: User's input query
        
    Returns:
        Tuple of (TaskCategory, confidence_score)
    """
    query_lower = query.lower()
    
    # Keywords for each category
    keywords = {
        TaskCategory.REALTIME_SEARCH: ["actualité", "news", "récent", "aujourd'hui", "recherche", "trouve", "what's happening"],
        TaskCategory.VISION_MULTIMODAL: ["image", "photo", "vision", "voir", "analyser image", "génère image", "dessine"],
        TaskCategory.CODE_GENERATION: ["code", "fonction", "script", "programme", "debug", "api", "développe", "implémente"],
        TaskCategory.COMPLEX_REASONING: ["analyse", "raisonne", "explique pourquoi", "logique", "démontre", "prouve"],
        TaskCategory.CREATIVE_WRITING: ["écris", "rédige", "histoire", "poème", "créatif", "imagine", "article"],
        TaskCategory.CONVERSATION: ["discute", "parle", "conversation", "chat", "qu'en penses-tu"],
        TaskCategory.DATA_ANALYSIS: ["données", "statistiques", "tableau", "graphique", "analyse data", "csv", "excel"],
    }
    
    # Calculate scores for each category
    scores = {}
    for category, kw_list in keywords.items():
        score = sum(1 for kw in kw_list if kw in query_lower)
        if score > 0:
            scores[category] = score
    
    # Return category with highest score, or DEFAULT
    if scores:
        best_category = max(scores, key=scores.get)
        confidence = min(scores[best_category] / 3.0, 1.0)  # Normalize to 0-1
        return best_category, confidence
    
    return TaskCategory.DEFAULT, 0.5


def get_recommended_llm(category: TaskCategory) -> Tuple[LLMModel, str, str]:
    """
    Get recommended LLM for a task category.
    
    Args:
        category: Detected task category
        
    Returns:
        Tuple of (LLMModel enum, model_name, justification)
    """
    return ROUTING_MATRIX.get(category, ROUTING_MATRIX[TaskCategory.DEFAULT])


def call_perplexity(query: str) -> str:
    """Call Perplexity API"""
    import requests
    
    api_key = os.getenv("SONAR_API_KEY")
    if not api_key:
        return "ERROR: SONAR_API_KEY not set"
    
    response = requests.post(
        "https://api.perplexity.ai/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "sonar-pro",
            "messages": [{"role": "user", "content": query}]
        }
    )
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"ERROR: {response.status_code} - {response.text}"


def call_gemini(query: str) -> str:
    """Call Google Gemini API"""
    from google import genai
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "ERROR: GEMINI_API_KEY not set"
    
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=query
    )
    
    return response.text


def call_gpt5(query: str) -> str:
    """Call OpenAI GPT-5 API"""
    from openai import OpenAI
    
    client = OpenAI()  # Uses OPENAI_API_KEY env var
    
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": query}]
    )
    
    return response.choices[0].message.content


def call_claude_opus(query: str) -> str:
    """Call Anthropic Claude Opus API"""
    from anthropic import Anthropic
    
    client = Anthropic()  # Uses ANTHROPIC_API_KEY env var
    
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4096,
        messages=[{"role": "user", "content": query}]
    )
    
    return response.content[0].text


def call_grok(query: str) -> str:
    """Call Grok API"""
    from xai_sdk import Client
    
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        return "ERROR: XAI_API_KEY not set"
    
    client = Client(api_key=api_key)
    
    response = client.chat.create(
        model="grok-4",
        messages=[{"role": "user", "content": query}]
    )
    
    return response.choices[0].message.content


def call_claude_sonnet(query: str) -> str:
    """Call Anthropic Claude Sonnet API"""
    from anthropic import Anthropic
    
    client = Anthropic()  # Uses ANTHROPIC_API_KEY env var
    
    response = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=4096,
        messages=[{"role": "user", "content": query}]
    )
    
    return response.content[0].text


# Map LLM models to their call functions
LLM_CALLERS = {
    LLMModel.PERPLEXITY: call_perplexity,
    LLMModel.GEMINI: call_gemini,
    LLMModel.GPT5: call_gpt5,
    LLMModel.CLAUDE_OPUS: call_claude_opus,
    LLMModel.GROK: call_grok,
    LLMModel.CLAUDE_SONNET: call_claude_sonnet,
}


def route_and_execute(query: str, model_override: Optional[str] = None) -> Dict:
    """
    Main routing function: analyze query, select LLM, and execute.
    
    Args:
        query: User's query
        model_override: Optional model name to override automatic selection
        
    Returns:
        Dict with routing info and response
    """
    # Analyze intent
    category, confidence = analyze_intent(query)
    
    # Get recommended LLM
    llm_model, model_name, justification = get_recommended_llm(category)
    
    # Override if specified
    if model_override:
        model_map = {
            "perplexity": LLMModel.PERPLEXITY,
            "gemini": LLMModel.GEMINI,
            "gpt5": LLMModel.GPT5,
            "opus": LLMModel.CLAUDE_OPUS,
            "grok": LLMModel.GROK,
            "sonnet": LLMModel.CLAUDE_SONNET,
        }
        llm_model = model_map.get(model_override.lower(), llm_model)
    
    # Execute call
    caller = LLM_CALLERS[llm_model]
    response = caller(query)
    
    return {
        "detected_category": category.value,
        "confidence": confidence,
        "selected_model": model_name,
        "justification": justification,
        "response": response
    }


def main():
    """CLI interface for testing"""
    if len(sys.argv) < 2:
        print("Usage: router.py <query> [model_override]")
        sys.exit(1)
    
    query = sys.argv[1]
    model_override = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = route_and_execute(query, model_override)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
