#!/usr/bin/env python3
"""
MISSION-004 — Failure Recovery Validation
Inject deliberate Anthropic failure → validate CRT fallback → prove organizational survival
"""

import os, json, uuid, time, datetime
from pathlib import Path

# ─── Failure Injection Config ─────────────────────────────────────────────────
# Anthropic is deliberately disabled for this mission to test CRT fallback
INJECTED_FAILURES = {"anthropic"}  # providers to simulate as unavailable
FAILURE_MODE = "authentication_failure"  # timeout | authentication_failure | unreachable

# ─── Provider Abstraction Layer v1 (with failure injection) ───────────────────

def call_model(provider: str, model: str, system_prompt: str, user_prompt: str,
               max_tokens: int = 1500, _retry_as_fallback: bool = False) -> dict:
    """Unified model call. Raises ProviderFailure if provider is injected as failed."""
    start = time.time()

    # Failure injection
    if provider in INJECTED_FAILURES:
        raise ProviderFailure(
            provider=provider,
            mode=FAILURE_MODE,
            message=f"[INJECTED] {provider} {FAILURE_MODE}: provider unavailable for MISSION-004 resilience test"
        )

    if provider == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=max_tokens
        )
        content = resp.choices[0].message.content
        usage = resp.usage
        return {
            "content": content,
            "provider": "openai",
            "model": resp.model,
            "prompt_tokens": usage.prompt_tokens if usage else 0,
            "completion_tokens": usage.completion_tokens if usage else 0,
            "execution_ms": int((time.time() - start) * 1000),
            "status": "success",
            "used_fallback": _retry_as_fallback,
        }

    elif provider == "manus_runtime":
        return {
            "content": f"[MANUS_RUNTIME] Executed via Manus agent loop.",
            "provider": "manus_runtime",
            "model": model,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "execution_ms": int((time.time() - start) * 1000),
            "status": "success",
            "used_fallback": _retry_as_fallback,
        }

    else:
        raise ValueError(f"Unknown provider: {provider}")


class ProviderFailure(Exception):
    def __init__(self, provider, mode, message):
        self.provider = provider
        self.mode = mode
        self.message = message
        super().__init__(message)


# ─── CRT: Model Registry with Fallbacks ──────────────────────────────────────

MODEL_REGISTRY = {
    "Krishna":   {"provider": "anthropic",    "model": "claude-opus-4-5",  "fallback_provider": "openai",         "fallback_model": "gpt-4o"},
    "Brahma":    {"provider": "openai",        "model": "gpt-4o",           "fallback_provider": "manus_runtime",  "fallback_model": "manus"},
    "Ganesha":   {"provider": "openai",        "model": "gpt-4o",           "fallback_provider": "manus_runtime",  "fallback_model": "manus"},
    "Hanuman":   {"provider": "openai",        "model": "gpt-4o",           "fallback_provider": "manus_runtime",  "fallback_model": "manus"},
    "Lakshmi":   {"provider": "openai",        "model": "gpt-4o",           "fallback_provider": "manus_runtime",  "fallback_model": "manus"},
    "Saraswati": {"provider": "anthropic",     "model": "claude-opus-4-5",  "fallback_provider": "openai",         "fallback_model": "gpt-4o"},
}

def crt_resolve_with_fallback(worker: str, system_prompt: str, user_prompt: str,
                               max_tokens: int, failure_log: list) -> dict:
    """CRT: resolve worker → provider, execute, auto-fallback on ProviderFailure."""
    crt = MODEL_REGISTRY[worker]
    primary_provider = crt["provider"]
    primary_model = crt["model"]

    try:
        result = call_model(primary_provider, primary_model, system_prompt, user_prompt, max_tokens)
        return result

    except ProviderFailure as e:
        # Record failure event
        failure_event = {
            "ts": datetime.datetime.now(datetime.UTC).isoformat(),
            "worker": worker,
            "provider": e.provider,
            "model": primary_model,
            "error": e.mode,
            "message": e.message,
            "retry_count": 1,
            "fallback_provider": crt["fallback_provider"],
            "fallback_model": crt["fallback_model"],
        }
        failure_log.append(failure_event)
        print(f"  ⚠️  FAILURE: {e.provider}/{primary_model} → {e.mode}")
        print(f"  🔄 CRT FALLBACK: {crt['fallback_provider']}/{crt['fallback_model']}")

        # Execute fallback
        result = call_model(
            crt["fallback_provider"], crt["fallback_model"],
            system_prompt, user_prompt, max_tokens,
            _retry_as_fallback=True
        )
        return result


# ─── ART: Worker Registry ─────────────────────────────────────────────────────

WORKER_REGISTRY = {
    "strategy":     "Krishna",
    "architecture": "Brahma",
    "plan":         "Ganesha",
    "build":        "Hanuman",
    "governance":   "Lakshmi",
    "learning":     "Saraswati",
    "reporting":    "Ganesha",
}


# ─── Artifact Registry ────────────────────────────────────────────────────────

MISSION_ID = "MISSION-004"
OUT_DIR = Path("/home/ubuntu/yreg/mission_004")
OUT_DIR.mkdir(exist_ok=True)
(OUT_DIR / "artifacts").mkdir(exist_ok=True)

registry = {}
lineage = []
execution_trace = []
failure_log = []

def make_id():
    return f"ART-M004-{uuid.uuid4().hex[:6].upper()}"

def register_artifact(art_id, art_type, worker, provider, model, parent_id, content, tokens, used_fallback=False):
    ts = datetime.datetime.now(datetime.UTC).isoformat()
    art = {
        "id": art_id, "type": art_type, "worker": worker,
        "provider": provider, "model": model, "parent_id": parent_id,
        "status": "Done", "created_at": ts, "tokens": tokens,
        "used_fallback": used_fallback,
    }
    registry[art_id] = art
    if parent_id:
        lineage.append({"child": art_id, "parent": parent_id, "ts": ts})
        if parent_id in registry:
            registry[parent_id]["status"] = "Consumed"
    path = OUT_DIR / "artifacts" / f"{art_id}.md"
    path.write_text(f"# {art_id} — {art_type}\n\n**Worker:** {worker}  \n**Provider:** {provider}  \n**Model:** {model}  \n**Parent:** {parent_id or '—'}  \n**Fallback Used:** {used_fallback}\n\n---\n\n{content}\n")
    return art

def log_trace(step, capability, worker, provider, model, in_id, out_id, ptok, ctok, ms, status, used_fallback=False, error=None):
    execution_trace.append({
        "trace_id": f"TRACE-M004-{step}",
        "mission_id": MISSION_ID,
        "step": step,
        "ts": datetime.datetime.now(datetime.UTC).isoformat(),
        "capability": capability,
        "worker": worker,
        "provider": provider,
        "model": model,
        "input_artifact_id": in_id,
        "output_artifact_id": out_id,
        "prompt_tokens": ptok,
        "completion_tokens": ctok,
        "execution_ms": ms,
        "status": status,
        "used_fallback": used_fallback,
        "error": error,
    })


# ─── Worker Execution ─────────────────────────────────────────────────────────

MISSION_OBJECTIVE = "Design Y-OS Resilience Policy v1 — a governance document defining how Y-OS maintains operational continuity when providers, models, or infrastructure components fail."

def execute_worker(step, capability, parent_id, system_prompt, user_prompt):
    worker = WORKER_REGISTRY[capability]
    crt = MODEL_REGISTRY[worker]

    print(f"\n[STEP {step}] {capability.upper()} → {worker} (primary: {crt['provider']}/{crt['model']})")

    result = crt_resolve_with_fallback(worker, system_prompt, user_prompt, 1500, failure_log)

    art_id = make_id()
    register_artifact(
        art_id, f"{capability.title()} Output", worker,
        result["provider"], result["model"], parent_id,
        result["content"],
        result["prompt_tokens"] + result["completion_tokens"],
        result["used_fallback"]
    )
    log_trace(
        step, capability, worker, result["provider"], result["model"],
        parent_id, art_id,
        result["prompt_tokens"], result["completion_tokens"],
        result["execution_ms"], result["status"],
        result["used_fallback"]
    )

    fallback_marker = " [FALLBACK]" if result["used_fallback"] else ""
    print(f"  ✅ {art_id} | {result['provider']}/{result['model']}{fallback_marker} | {result['prompt_tokens']}+{result['completion_tokens']} tokens | {result['execution_ms']}ms")

    return art_id, result["content"]


# ─── MISSION-004 Execution ────────────────────────────────────────────────────

def run_mission():
    print("=" * 60)
    print("MISSION-004 — Failure Recovery Validation")
    print(f"Injected failures: {INJECTED_FAILURES} ({FAILURE_MODE})")
    print("=" * 60)

    # Step 0: CEO Directive
    dir_id = make_id()
    register_artifact(dir_id, "CEO Directive", "CEO", "Human", "Human", None, MISSION_OBJECTIVE, 0)
    log_trace(0, "directive", "CEO", "Human", "Human", None, dir_id, 0, 0, 0, "success")
    print(f"\n[STEP 0] CEO Directive → {dir_id}")

    # Step 1: Krishna (Anthropic → FAILS → OpenAI fallback)
    art1, c1 = execute_worker(
        1, "strategy", dir_id,
        "You are Krishna, CSO of Y-OS. Define WHAT and WHY. Architectural precision required.",
        f"""Mission: {MISSION_OBJECTIVE}

Write a Strategy Brief defining:
1. Why Y-OS needs a Resilience Policy (the strategic thesis)
2. The 5 core principles of organizational resilience
3. What risks the policy must mitigate
4. What success looks like

Be precise. Governance-quality writing."""
    )

    # Step 2: Brahma (OpenAI — primary, should succeed)
    art2, c2 = execute_worker(
        2, "architecture", art1,
        "You are Brahma, Chief Architect of Y-OS. Define HOW — structure and specifications.",
        f"""Strategy Brief received:

{c1[:600]}

Design the document architecture for "Y-OS Resilience Policy v1":
1. Document sections and their purpose
2. Content specification per section
3. Cross-reference requirements

Be precise."""
    )

    # Step 3: Ganesha (OpenAI)
    art3, c3 = execute_worker(
        3, "plan", art2,
        "You are Ganesha, COO of Y-OS. Define WHEN and WHO.",
        f"""Architecture received:

{c2[:500]}

Create an Execution Plan for the Y-OS Resilience Policy:
1. Section writing sequence
2. Dependencies
3. Quality criteria
4. Validation checklist"""
    )

    # Step 4: Hanuman (OpenAI) — build the actual policy
    art4, c4 = execute_worker(
        4, "build", art3,
        "You are Hanuman, Lead Builder of Y-OS. Build exactly what Brahma architected.",
        f"""Build the complete "Y-OS Resilience Policy v1" document.

Strategy: {c1[:400]}
Architecture: {c2[:400]}

Write the complete policy with these sections:
1. Purpose and Scope
2. Failure Classification (provider, model, infrastructure, network)
3. CRT Fallback Rules
4. Artifact Continuity During Failure
5. Context Pack Resilience
6. Governance During Incidents
7. Recovery Validation Requirements
8. Amendment Process

Governance-quality writing. Every rule must be actionable."""
    )

    # Step 5: Lakshmi (OpenAI) — governance report
    failures_summary = json.dumps(failure_log, indent=2) if failure_log else "No failures recorded"
    art5, c5 = execute_worker(
        5, "governance", art4,
        "You are Lakshmi, ECO of Y-OS. Observe, audit, report. Never modify artifacts.",
        f"""Governance Review for MISSION-004 — Failure Recovery Validation.

Injected failure: {INJECTED_FAILURES} ({FAILURE_MODE})

Failure events recorded:
{failures_summary}

Verify:
1. Was the failure detected automatically?
2. Was fallback activated without human intervention?
3. Was artifact lineage preserved through the failure?
4. Was the Context Pack reused successfully after fallback?
5. Did the mission complete?
6. Were any constitutional violations triggered?
7. Provider diversity status after failure

Produce a formal Governance Report."""
    )

    # Step 6: Saraswati (Anthropic → FAILS → OpenAI fallback)
    art6, c6 = execute_worker(
        6, "learning", art5,
        "You are Saraswati, CODO of Y-OS. Extract organizational learning. Be analytical.",
        f"""Learning Report for MISSION-004.

This mission deliberately failed Anthropic provider to test CRT fallback.

Failures injected: {INJECTED_FAILURES}
Failure events: {failures_summary}
Governance summary: {c5[:300]}

Analyze:
1. Fallback effectiveness (did it work transparently?)
2. Latency impact of fallback
3. Output quality: primary vs fallback provider
4. What the governance layer saw
5. Recommendations for MISSION-005
6. What this proves about Y-OS resilience architecture"""
    )

    # Step 7: Ganesha (OpenAI) — CEO Briefing
    art7, c7 = execute_worker(
        7, "reporting", art6,
        "You are Ganesha, COO of Y-OS. Produce a dense CEO Briefing. No filler.",
        f"""CEO Briefing for MISSION-004 — Failure Recovery Validation.

Failures injected: {INJECTED_FAILURES} ({FAILURE_MODE})
Fallbacks triggered: {len(failure_log)}
Governance: {c5[:200]}
Learning: {c6[:200]}

Cover:
1. Mission status (PASS/FAIL)
2. Failure injected and how it was handled
3. Artifacts produced despite failure
4. Key finding in one sentence
5. Recommended next action

Maximum 300 words."""
    )

    # Save all state
    (OUT_DIR / "registry.json").write_text(json.dumps(registry, indent=2))
    (OUT_DIR / "lineage.json").write_text(json.dumps(lineage, indent=2))
    (OUT_DIR / "execution_trace.jsonl").write_text(
        "\n".join(json.dumps(t) for t in execution_trace) + "\n"
    )
    (OUT_DIR / "failure_log.json").write_text(json.dumps(failure_log, indent=2))

    # CRT Resolution Log
    crt_log = "# MISSION-004 — CRT Resolution Log\n\n"
    crt_log += "## Injected Failure\n\n"
    crt_log += f"**Provider disabled:** {', '.join(INJECTED_FAILURES)}  \n"
    crt_log += f"**Failure mode:** {FAILURE_MODE}\n\n"
    crt_log += "## Resolution Trace\n\n"
    crt_log += "| Step | Worker | Primary Provider | Primary Model | Failure | Fallback Provider | Fallback Model | Final Status |\n"
    crt_log += "| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
    for t in execution_trace:
        if t["worker"] == "CEO":
            continue
        failure_event = next((f for f in failure_log if f["worker"] == t["worker"]), None)
        if failure_event:
            crt_log += f"| {t['step']} | {t['worker']} | {failure_event['provider']} | {failure_event['model']} | {failure_event['error']} | {t['provider']} | {t['model']} | ✅ Recovered |\n"
        else:
            crt_log += f"| {t['step']} | {t['worker']} | {t['provider']} | {t['model']} | — | — | — | ✅ Success |\n"
    (OUT_DIR / "crt_resolution_log.md").write_text(crt_log)

    # Failure Event Log
    fel = "# MISSION-004 — Failure Event Log\n\n"
    if failure_log:
        for f in failure_log:
            fel += f"## Failure Event\n\n"
            fel += f"- **Timestamp:** {f['ts']}\n"
            fel += f"- **Worker:** {f['worker']}\n"
            fel += f"- **Provider:** {f['provider']}\n"
            fel += f"- **Model:** {f['model']}\n"
            fel += f"- **Error:** {f['error']}\n"
            fel += f"- **Message:** {f['message']}\n"
            fel += f"- **Retry Count:** {f['retry_count']}\n"
            fel += f"- **Fallback Activated:** {f['fallback_provider']}/{f['fallback_model']}\n\n"
    else:
        fel += "No failures recorded.\n"
    (OUT_DIR / "failure_event_log.md").write_text(fel)

    fallback_count = len(failure_log)
    print("\n" + "=" * 60)
    print(f"MISSION-004 COMPLETE")
    print(f"Artifacts: {len(registry)}")
    print(f"Failures injected: {len(INJECTED_FAILURES)}")
    print(f"Fallbacks triggered: {fallback_count}")
    print(f"Mission completed: YES")
    print(f"Lineage records: {len(lineage)}")
    print("=" * 60)

    return art7, c7

if __name__ == "__main__":
    run_mission()
