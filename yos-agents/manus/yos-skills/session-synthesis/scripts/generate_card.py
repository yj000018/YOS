#!/usr/bin/env python3.11
"""
LLM Memory Pipeline (LMP) — Manus instance
Phase 2 : Génération des fiches session via Claude 3.5 Sonnet

- Lit les verbatim exportés par 01_collect_sessions.py
- Pour chaque session : appelle Claude Sonnet avec prompt canonique
- Output : {uid}_card.json (fiche structurée) + {uid}_card.md (version lisible)
- Déduplication : skip si _card.json existe déjà
- Gestion sessions vides/triviales : fiche minimaliste auto-générée
"""

import json
import os
import time
from pathlib import Path
import anthropic

# ── Config ────────────────────────────────────────────────────────────────────
EXPORT_DIR = Path("/home/ubuntu/manus_pipeline/sessions_export")
CARDS_DIR = Path("/home/ubuntu/manus_pipeline/session_cards")
CARDS_DIR.mkdir(parents=True, exist_ok=True)

CLAUDE_MODEL = "claude-sonnet-4-20250514"
MIN_WORDS_FOR_LLM = 50  # Sessions < 50 mots → fiche minimaliste sans appel LLM
RATE_LIMIT_DELAY = 1.0  # seconds between Claude calls

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# ── Prompt système canonique ──────────────────────────────────────────────────

SYSTEM_PROMPT = """You are an expert knowledge architect specializing in extracting structured intelligence from AI conversation transcripts.

Your task: analyze a Manus AI session transcript and produce a structured session card in JSON format.

The session is a conversation between a user (Yannick Jolliet, cognitive systems architect, creator of yOS) and Manus (an autonomous AI agent). Sessions may be in French, English, or mixed.

OUTPUT FORMAT: Return ONLY a valid JSON object with exactly these fields:

{
  "title": "string — clean, descriptive title (English, max 80 chars)",
  "date": "string — ISO date YYYY-MM-DD from transcript or metadata",
  "language": "string — primary language: fr / en / mixed",
  "depth_score": "string — one of: minor / standard / substantial / landmark",
  "length_category": "string — one of: short / medium / long / xl",
  "project_hint": "string — most likely project: eia / yOS / VISUAL_REALITY / DOMUS / GEN5 / ODYSSEY / UNKNOWN",
  "themes": ["array of strings — key themes, concepts, tools, technologies mentioned"],
  "subthemes": ["array of strings — more specific sub-topics"],
  "executive_summary": "string — 3-5 sentences. What happened, why, net result. Dense, factual, no filler.",
  "context_and_intent": "string — Why this session was started. Initial question or goal. Prior state.",
  "what_was_done": "string — Chronological sequence of actions. Validated steps and confirmed decisions.",
  "outputs_produced": [
    {"type": "string", "name": "string", "description": "string"}
  ],
  "key_decisions": ["array of strings — explicit choices made, what was confirmed/rejected/deferred"],
  "lessons_learned": {
    "worked_well": ["array of strings"],
    "failed_or_suboptimal": ["array of strings"],
    "discoveries": ["array of strings"]
  },
  "challenges_and_blockers": ["array of strings — obstacles encountered, how resolved or not"],
  "open_questions": ["array of strings — unresolved uncertainties at session end"],
  "next_steps": ["array of strings — concrete actions identified but not executed"]
}

DEPTH SCORE GUIDE:
- minor: trivial session, test, single question, no real content
- standard: useful session with some value but no major decisions or outputs
- substantial: important session with decisions, outputs, or significant learning
- landmark: critical session — major architectural decisions, key outputs, paradigm shifts

PROJECT HINT GUIDE:
- eia: Yannick's wife's spiritual name, her website, personal projects related to her
- yOS: Yannick's cognitive operating system, AI infrastructure, Manus workflows, memory systems
- VISUAL_REALITY: photography, video, visual creative work
- DOMUS: home automation, smart home
- GEN5: generation 5 project (future society, next civilization concepts)
- ODYSSEY: journey/travel related project
- UNKNOWN: cannot determine

Be precise. Be dense. No filler. If a field has no content, use empty array [] or empty string "".
Output ONLY the JSON object, no markdown, no explanation."""


# ── Génération fiche minimaliste (sessions vides) ─────────────────────────────

def make_trivial_card(session_data: dict) -> dict:
    """Fiche minimaliste pour sessions quasi-vides (< MIN_WORDS_FOR_LLM mots)."""
    msgs = session_data.get("messages", [])
    content_preview = msgs[0].get("content", "") if msgs else ""
    return {
        "title": session_data.get("title", "Untitled"),
        "date": (session_data.get("created_at", "") or "")[:10],
        "language": "unknown",
        "depth_score": "minor",
        "length_category": "short",
        "project_hint": "UNKNOWN",
        "themes": [],
        "subthemes": [],
        "executive_summary": f"Trivial session. Content: '{content_preview[:200]}'",
        "context_and_intent": "",
        "what_was_done": "",
        "outputs_produced": [],
        "key_decisions": [],
        "lessons_learned": {"worked_well": [], "failed_or_suboptimal": [], "discoveries": []},
        "challenges_and_blockers": [],
        "open_questions": [],
        "next_steps": [],
        "_generated_by": "trivial_fallback",
    }


# ── Formatage verbatim pour Claude ───────────────────────────────────────────

def format_verbatim(session_data: dict) -> str:
    """Formate le verbatim pour injection dans le prompt Claude."""
    lines = []
    lines.append(f"SESSION TITLE: {session_data.get('title', 'Untitled')}")
    lines.append(f"DATE: {(session_data.get('created_at', '') or '')[:10]}")
    lines.append(f"TOTAL MESSAGES: {session_data.get('message_count', len(session_data.get('messages', [])))}")
    lines.append("")
    lines.append("--- TRANSCRIPT ---")
    lines.append("")

    for msg in session_data.get("messages", []):
        sender = msg.get("sender", "?").upper()
        content = msg.get("content", "").strip()
        if content:
            lines.append(f"[{sender}]")
            lines.append(content)
            lines.append("")

    return "\n".join(lines)


# ── Génération fiche via Claude ───────────────────────────────────────────────

def generate_card_with_claude(session_data: dict) -> dict:
    """Appelle Claude Sonnet pour générer la fiche structurée."""
    verbatim = format_verbatim(session_data)

    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Analyze this session and produce the structured JSON card:\n\n{verbatim}"
            }
        ]
    )

    raw = message.content[0].text.strip()

    # Nettoyer si Claude a ajouté des backticks
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    if raw.endswith("```"):
        raw = raw[:-3]

    card = json.loads(raw.strip())
    card["_generated_by"] = "claude-3-5-sonnet"
    card["_input_tokens"] = message.usage.input_tokens
    card["_output_tokens"] = message.usage.output_tokens
    card["_cost_usd"] = round(
        message.usage.input_tokens / 1_000_000 * 3.0 +
        message.usage.output_tokens / 1_000_000 * 15.0,
        6
    )
    return card


# ── Génération markdown lisible ───────────────────────────────────────────────

def card_to_markdown(card: dict, uid: str) -> str:
    """Convertit la fiche JSON en markdown structuré pour Notion."""
    lines = []

    depth_emoji = {"minor": "⚪", "standard": "🟡", "substantial": "🟢", "landmark": "⭐"}.get(card.get("depth_score", ""), "⚪")
    length_emoji = {"short": "S", "medium": "M", "long": "L", "xl": "XL"}.get(card.get("length_category", ""), "?")

    lines.append(f"# {card.get('title', 'Untitled')}")
    lines.append("")
    lines.append(f"**Date:** {card.get('date', '?')} | **Project:** {card.get('project_hint', '?')} | **Depth:** {depth_emoji} {card.get('depth_score', '?')} | **Length:** {length_emoji} | **Lang:** {card.get('language', '?')}")
    lines.append("")
    lines.append(f"**Themes:** {', '.join(card.get('themes', []))}")
    lines.append(f"**Subthemes:** {', '.join(card.get('subthemes', []))}")
    lines.append("")

    # Executive Summary — OPEN
    lines.append("## Executive Summary")
    lines.append(card.get("executive_summary", ""))
    lines.append("")

    # Context & Intent
    if card.get("context_and_intent"):
        lines.append("## Context & Intent")
        lines.append(card.get("context_and_intent", ""))
        lines.append("")

    # What Was Done
    if card.get("what_was_done"):
        lines.append("## What Was Done")
        lines.append(card.get("what_was_done", ""))
        lines.append("")

    # Outputs Produced
    outputs = card.get("outputs_produced", [])
    if outputs:
        lines.append("## Outputs Produced")
        for o in outputs:
            lines.append(f"- **[{o.get('type', '?')}]** {o.get('name', '?')} — {o.get('description', '')}")
        lines.append("")

    # Key Decisions
    decisions = card.get("key_decisions", [])
    if decisions:
        lines.append("## Key Decisions & Validations")
        for d in decisions:
            lines.append(f"- {d}")
        lines.append("")

    # Lessons Learned
    ll = card.get("lessons_learned", {})
    if any(ll.get(k) for k in ["worked_well", "failed_or_suboptimal", "discoveries"]):
        lines.append("## Lessons Learned")
        if ll.get("worked_well"):
            lines.append("**Worked well:**")
            for x in ll["worked_well"]:
                lines.append(f"- {x}")
        if ll.get("failed_or_suboptimal"):
            lines.append("**Failed / suboptimal:**")
            for x in ll["failed_or_suboptimal"]:
                lines.append(f"- {x}")
        if ll.get("discoveries"):
            lines.append("**Discoveries:**")
            for x in ll["discoveries"]:
                lines.append(f"- {x}")
        lines.append("")

    # Challenges
    challenges = card.get("challenges_and_blockers", [])
    if challenges:
        lines.append("## Challenges & Blockers")
        for c in challenges:
            lines.append(f"- {c}")
        lines.append("")

    # Open Questions
    oq = card.get("open_questions", [])
    if oq:
        lines.append("## Open Questions")
        for q in oq:
            lines.append(f"- {q}")
        lines.append("")

    # Next Steps — OPEN
    ns = card.get("next_steps", [])
    lines.append("## Next Steps")
    if ns:
        for s in ns:
            lines.append(f"- {s}")
    else:
        lines.append("_None identified._")
    lines.append("")

    lines.append("---")
    lines.append(f"_uid: {uid} | generated by: {card.get('_generated_by', '?')}_")

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────

def main(subset: list = None):
    print("=" * 60)
    print("LLM Memory Pipeline — Phase 2 : Generate Session Cards")
    print(f"Model: {CLAUDE_MODEL}")
    print("=" * 60)

    # Lister les sessions à traiter
    if subset:
        session_files = [EXPORT_DIR / f"{uid}.json" for uid in subset
                         if (EXPORT_DIR / f"{uid}.json").exists()]
    else:
        session_files = sorted(EXPORT_DIR.glob("*.json"))
        session_files = [f for f in session_files if f.name != "sessions_index.json"]

    print(f"\n→ {len(session_files)} sessions to process\n")

    stats = {"success_llm": 0, "success_trivial": 0, "skipped": 0, "error": 0}
    total_cost = 0.0

    for i, session_file in enumerate(session_files):
        uid = session_file.stem
        card_path = CARDS_DIR / f"{uid}_card.json"

        # Déduplication
        if card_path.exists():
            print(f"  [{i+1:3d}/{len(session_files)}] SKIP (exists): {uid[:12]}...")
            stats["skipped"] += 1
            continue

        try:
            session_data = json.load(open(session_file))
            title = session_data.get("title", "")[:55]
            wc = session_data.get("word_count",
                  sum(len(m.get("content","").split()) for m in session_data.get("messages",[])))

            # Sessions triviales : fiche minimaliste sans LLM
            if wc < MIN_WORDS_FOR_LLM:
                card = make_trivial_card(session_data)
                print(f"  [{i+1:3d}/{len(session_files)}] TRIVIAL ({wc}w): {title}")
                stats["success_trivial"] += 1
            else:
                card = generate_card_with_claude(session_data)
                cost = card.get("_cost_usd", 0)
                total_cost += cost
                print(f"  [{i+1:3d}/{len(session_files)}] ✓ Claude [{card.get('depth_score','?'):11s}] "
                      f"${cost:.4f} | {wc}w : {title}")
                stats["success_llm"] += 1
                time.sleep(RATE_LIMIT_DELAY)

            # Sauvegarder JSON
            with open(card_path, "w") as f:
                json.dump(card, f, ensure_ascii=False, indent=2)

            # Sauvegarder Markdown
            md_path = CARDS_DIR / f"{uid}_card.md"
            with open(md_path, "w") as f:
                f.write(card_to_markdown(card, uid))

        except json.JSONDecodeError as e:
            print(f"  [{i+1:3d}/{len(session_files)}] JSON ERROR {uid}: {e}")
            stats["error"] += 1
        except Exception as e:
            print(f"  [{i+1:3d}/{len(session_files)}] ERROR {uid}: {e}")
            stats["error"] += 1

    print("\n" + "=" * 60)
    print("SUMMARY")
    print(f"  Claude calls     : {stats['success_llm']}")
    print(f"  Trivial (no LLM) : {stats['success_trivial']}")
    print(f"  Skipped (exists) : {stats['skipped']}")
    print(f"  Errors           : {stats['error']}")
    print(f"  Total cost       : ${total_cost:.4f}")
    print(f"\nCards: {CARDS_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    TEST_UIDS = [
        "mWVysv0MBCNHRsi0n2etX7",
        "gTTBiSafWaj72Gr9fsOMhY",
        "8YCBdRxCMDYbhgQXx8v9VG",
        "vXs1WpNeEuH8ZJ4ybDExws",
        "eak6dAJxZKruhgQhMUhTHh",
    ]
    if "--test" in sys.argv:
        main(subset=TEST_UIDS)
    elif len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        main(subset=sys.argv[1:])
    else:
        main()
