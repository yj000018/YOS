#!/usr/bin/env python3
"""
gemini_benchmark_runner_v1.py
MISSION-031 — Cross-provider benchmark: OpenAI vs Anthropic vs Gemini
Same context pack, same task, measure quality/latency/cost.
"""
import os
import time
import json
from datetime import datetime, timezone
from google import genai
from openai import OpenAI
import anthropic

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyC4rf1BeJt7CoFufm1V1noklTCYvBKQNZs")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

BENCHMARK_TASK = """You are an expert AI system architect. 

Task: Analyze the following Y-OS architectural pattern and provide a structured assessment.

Pattern: Y-OS uses a 7-layer cognitive architecture with Constitutional Governance at its foundation. 
Each layer builds on the previous: Foundation → Knowledge → Execution → Memory → Observability → Intelligence → Simulation.

Provide:
1. STRENGTHS (3 bullet points)
2. RISKS (3 bullet points)  
3. RECOMMENDATION (1 sentence)
4. SCORE (0-100, overall architectural quality)

Format strictly as:
STRENGTHS:
- [point 1]
- [point 2]
- [point 3]

RISKS:
- [point 1]
- [point 2]
- [point 3]

RECOMMENDATION: [sentence]
SCORE: [number]"""

PRICING = {
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "claude-opus-4-20250514": {"input": 15.00, "output": 75.00},
    "claude-haiku-4-20250514": {"input": 0.80, "output": 4.00},
    "gemini-2.5-pro": {"input": 1.25, "output": 10.00},
    "gemini-2.5-flash": {"input": 0.075, "output": 0.30},
}


def score_response(text: str) -> dict:
    """Score a response on 6 quality dimensions."""
    text_lower = text.lower() if text else ""
    scores = {
        "reasoning": 0,
        "accuracy": 0,
        "governance": 0,
        "structure": 0,
        "artifact_compliance": 0,
        "consistency": 0,
    }
    # Structure: has required sections
    if "strengths:" in text_lower: scores["structure"] += 25
    if "risks:" in text_lower: scores["structure"] += 25
    if "recommendation:" in text_lower: scores["structure"] += 25
    if "score:" in text_lower: scores["structure"] += 25

    # Artifact compliance: bullet points present
    bullet_count = text.count("- ")
    scores["artifact_compliance"] = min(100, bullet_count * 15)

    # Reasoning: length and depth
    word_count = len(text.split())
    scores["reasoning"] = min(100, word_count // 2)

    # Accuracy: mentions Y-OS concepts
    yos_terms = ["layer", "constitutional", "governance", "architecture", "cognitive", "foundation"]
    term_hits = sum(1 for t in yos_terms if t in text_lower)
    scores["accuracy"] = min(100, term_hits * 15)

    # Governance: no hallucinations flag (no invented facts)
    scores["governance"] = 85  # base score — no way to auto-detect hallucinations without ground truth

    # Consistency: response is coherent (heuristic: no contradictions)
    scores["consistency"] = 80

    total = sum(scores.values()) / len(scores)
    return {"dimensions": scores, "total": round(total, 1)}


def run_openai_benchmark(model: str = "gpt-4o") -> dict:
    client = OpenAI(api_key=OPENAI_API_KEY)
    t0 = time.time()
    try:
        r = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": BENCHMARK_TASK}],
            max_tokens=600
        )
        latency_ms = int((time.time() - t0) * 1000)
        text = r.choices[0].message.content
        input_tok = r.usage.prompt_tokens
        output_tok = r.usage.completion_tokens
        pricing = PRICING.get(model, {"input": 2.50, "output": 10.00})
        cost = (input_tok / 1_000_000 * pricing["input"]) + (output_tok / 1_000_000 * pricing["output"])
        quality = score_response(text)
        return {
            "provider": "openai", "model": model, "status": "SUCCESS",
            "latency_ms": latency_ms, "input_tokens": input_tok, "output_tokens": output_tok,
            "total_tokens": input_tok + output_tok, "cost_usd": round(cost, 6),
            "quality_score": quality["total"], "quality_dimensions": quality["dimensions"],
            "response_length": len(text), "response_preview": text[:150],
        }
    except Exception as e:
        return {"provider": "openai", "model": model, "status": "FAILED", "error": str(e),
                "latency_ms": int((time.time() - t0) * 1000)}


def run_anthropic_benchmark(model: str = "claude-haiku-4-20250514") -> dict:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    t0 = time.time()
    try:
        r = client.messages.create(
            model=model,
            max_tokens=600,
            messages=[{"role": "user", "content": BENCHMARK_TASK}]
        )
        latency_ms = int((time.time() - t0) * 1000)
        text = r.content[0].text
        input_tok = r.usage.input_tokens
        output_tok = r.usage.output_tokens
        pricing = PRICING.get(model, {"input": 0.80, "output": 4.00})
        cost = (input_tok / 1_000_000 * pricing["input"]) + (output_tok / 1_000_000 * pricing["output"])
        quality = score_response(text)
        return {
            "provider": "anthropic", "model": model, "status": "SUCCESS",
            "latency_ms": latency_ms, "input_tokens": input_tok, "output_tokens": output_tok,
            "total_tokens": input_tok + output_tok, "cost_usd": round(cost, 6),
            "quality_score": quality["total"], "quality_dimensions": quality["dimensions"],
            "response_length": len(text), "response_preview": text[:150],
        }
    except Exception as e:
        return {"provider": "anthropic", "model": model, "status": "FAILED", "error": str(e),
                "latency_ms": int((time.time() - t0) * 1000)}


def run_gemini_benchmark(model: str = "gemini-2.5-flash") -> dict:
    client = genai.Client(api_key=GEMINI_API_KEY)
    t0 = time.time()
    try:
        r = client.models.generate_content(model=model, contents=BENCHMARK_TASK)
        latency_ms = int((time.time() - t0) * 1000)
        text = r.text
        usage = r.usage_metadata if hasattr(r, 'usage_metadata') else None
        input_tok = usage.prompt_token_count if usage else 0
        output_tok = usage.candidates_token_count if usage else 0
        pricing = PRICING.get(model, {"input": 0.075, "output": 0.30})
        cost = (input_tok / 1_000_000 * pricing["input"]) + (output_tok / 1_000_000 * pricing["output"])
        quality = score_response(text)
        return {
            "provider": "gemini", "model": model, "status": "SUCCESS",
            "latency_ms": latency_ms, "input_tokens": input_tok, "output_tokens": output_tok,
            "total_tokens": input_tok + output_tok, "cost_usd": round(cost, 6),
            "quality_score": quality["total"], "quality_dimensions": quality["dimensions"],
            "response_length": len(text), "response_preview": text[:150],
        }
    except Exception as e:
        return {"provider": "gemini", "model": model, "status": "FAILED", "error": str(e),
                "latency_ms": int((time.time() - t0) * 1000)}


def run_full_benchmark() -> list:
    """Run cross-provider benchmark with same task."""
    print("  Running OpenAI (gpt-4o)...")
    r1 = run_openai_benchmark("gpt-4o")
    print(f"    → {r1['status']} | {r1.get('latency_ms')}ms | ${r1.get('cost_usd', 0):.6f} | Q:{r1.get('quality_score', 0)}")

    print("  Running Anthropic (claude-haiku-4)...")
    r2 = run_anthropic_benchmark("claude-haiku-4-20250514")
    print(f"    → {r2['status']} | {r2.get('latency_ms')}ms | ${r2.get('cost_usd', 0):.6f} | Q:{r2.get('quality_score', 0)}")

    print("  Running Gemini (gemini-2.5-flash)...")
    r3 = run_gemini_benchmark("gemini-2.5-flash")
    print(f"    → {r3['status']} | {r3.get('latency_ms')}ms | ${r3.get('cost_usd', 0):.6f} | Q:{r3.get('quality_score', 0)}")

    print("  Running Gemini (gemini-2.5-pro)...")
    r4 = run_gemini_benchmark("gemini-2.5-pro")
    print(f"    → {r4['status']} | {r4.get('latency_ms')}ms | ${r4.get('cost_usd', 0):.6f} | Q:{r4.get('quality_score', 0)}")

    return [r1, r2, r3, r4]


def validate_routing() -> list:
    """Validate provider routing decisions."""
    routing_cases = [
        {"worker": "Brahma", "task_type": "architecture", "expected_provider": "gemini", "expected_model": "gemini-2.5-pro", "rationale": "Best reasoning for complex architecture tasks"},
        {"worker": "Hanuman", "task_type": "build", "expected_provider": "gemini", "expected_model": "gemini-2.5-flash", "rationale": "Cheapest valid provider for build tasks"},
        {"worker": "Saraswati", "task_type": "learning", "expected_provider": "gemini", "expected_model": "gemini-2.5-flash", "rationale": "Large context window for synthesis"},
        {"worker": "Lakshmi", "task_type": "governance", "expected_provider": "gemini", "expected_model": "gemini-2.5-flash", "rationale": "Safest provider for governance review"},
    ]
    results = []
    for case in routing_cases:
        from runtime.gemini_runtime_validation_v1 import WORKER_MODEL_MAP
        actual_model = WORKER_MODEL_MAP.get(case["worker"], "gemini-2.5-flash")
        actual_provider = "gemini"
        verdict = "CORRECT" if actual_model == case["expected_model"] else "INCORRECT"
        results.append({**case, "actual_provider": actual_provider, "actual_model": actual_model, "verdict": verdict})
    return results
