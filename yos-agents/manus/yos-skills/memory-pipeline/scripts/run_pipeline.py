#!/usr/bin/env python3.11
"""
LLM Memory Pipeline (LMP) — Full Run
Phases 1+2 : Collecte verbatim (351 sessions) + Génération fiches Claude
Rapport de progression tous les 75 sessions ou sur demande
"""

import json
import os
import sys
import time
import requests
import anthropic
from pathlib import Path
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────────────
EXPORT_DIR = Path("/home/ubuntu/manus_pipeline/sessions_export")
CARDS_DIR = Path("/home/ubuntu/manus_pipeline/session_cards")
LOG_FILE = Path("/home/ubuntu/manus_pipeline/run_full.log")
PROGRESS_FILE = Path("/home/ubuntu/manus_pipeline/progress.json")

EXPORT_DIR.mkdir(parents=True, exist_ok=True)
CARDS_DIR.mkdir(parents=True, exist_ok=True)

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Inlhbm5pY2suam9sbGlldEBnbWFpbC5jb20iLCJleHAiOjE3ODM0MzEwOTMsImlhdCI6MTc3NTY1NTA5MywianRpIjoiY3dUOUxoOEtzNmNacEwzakVSaHozQyIsIm5hbWUiOiJZYW5uaWNrIEpvbGxpZXQiLCJvcmlnaW5hbF91c2VyX2lkIjoiIiwidGVhbV91aWQiOiIiLCJ0eXBlIjoidXNlciIsInVzZXJfaWQiOiIzMTA0MTk2NjMwMzIzODE4MzMifQ.88v6mbthCgzJQwUAc1-_wKYo-8uSdQ_qkro7C2cYVuM"
API_HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "connect-protocol-version": "1",
    "x-client-id": "SH6GDQiPhdFcHsaqh7U4Rm"
}

CLAUDE_MODEL = "claude-sonnet-4-20250514"
MIN_WORDS_FOR_LLM = 50
RATE_LIMIT_DELAY = 1.2
MILESTONE_EVERY = 75

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# ── Logging ───────────────────────────────────────────────────────────────────
def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

# ── Phase 1 : Collecte ────────────────────────────────────────────────────────
def fetch_all_sessions():
    all_sessions = []
    offset = 0
    while True:
        r = requests.post(
            "https://api.manus.im/session.v1.SessionService/ListSessions",
            headers=API_HEADERS,
            json={"pageSize": 100, "offset": offset},
            timeout=30
        )
        data = r.json()
        batch = data.get("sessions", [])
        all_sessions.extend(batch)
        if not data.get("hasNext") or not batch:
            break
        offset += len(batch)
    return all_sessions

def fetch_session_verbatim(uid):
    """Récupère le verbatim complet d'une session (tous segments)."""
    all_messages = []
    segment = 0
    while True:
        url = f"https://api.manus.im/session.v1.SessionService/getSessionV2?uid={uid}&segment={segment}"
        r = requests.get(url, headers=API_HEADERS, timeout=30)
        if r.status_code != 200:
            break
        data = r.json()
        events = data.get("events", [])
        if not events:
            break
        for ev in events:
            ev_type = ev.get("type", "")
            if ev_type in ("chat", "message"):
                role = ev.get("role", ev.get("sender", ""))
                content = ""
                if isinstance(ev.get("content"), str):
                    content = ev["content"]
                elif isinstance(ev.get("content"), list):
                    for block in ev["content"]:
                        if isinstance(block, dict) and block.get("type") == "text":
                            content += block.get("text", "")
                elif isinstance(ev.get("message"), dict):
                    content = ev["message"].get("content", "")
                if content.strip():
                    all_messages.append({"sender": role, "content": content.strip()})
        if not data.get("hasNextSegment"):
            break
        segment += 1
    return all_messages, segment + 1

def collect_session(session_meta):
    uid = session_meta["uid"]
    out_path = EXPORT_DIR / f"{uid}.json"
    if out_path.exists():
        existing = json.load(open(out_path))
        wc = existing.get("word_count", 0)
        return "skip", wc

    try:
        messages, seg_count = fetch_session_verbatim(uid)
        wc = sum(len(m["content"].split()) for m in messages)
        data = {
            "uid": uid,
            "title": session_meta.get("title", ""),
            "created_at": session_meta.get("createdAt", session_meta.get("created_at", "")),
            "updated_at": session_meta.get("updatedAt", session_meta.get("updated_at", "")),
            "status": session_meta.get("status", ""),
            "message_count": len(messages),
            "word_count": wc,
            "segment_count": seg_count,
            "messages": messages
        }
        with open(out_path, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return "ok", wc
    except Exception as e:
        return "error", str(e)

# ── Phase 2 : Génération fiches ───────────────────────────────────────────────
SYSTEM_PROMPT = """You are an expert knowledge architect specializing in extracting structured intelligence from AI conversation transcripts.

Your task: analyze a Manus AI session transcript and produce a structured session card in JSON format.

The session is a conversation between a user (Yannick Jolliet, cognitive systems architect, creator of yOS) and Manus (an autonomous AI agent). Sessions may be in French, English, or mixed.

OUTPUT FORMAT: Return ONLY a valid JSON object with exactly these fields:

{
  "title": "string — clean, descriptive title (English, max 80 chars)",
  "date": "string — ISO date YYYY-MM-DD",
  "language": "string — fr / en / mixed",
  "depth_score": "string — minor / standard / substantial / landmark",
  "length_category": "string — short / medium / long / xl",
  "project_hint": "string — eia / yOS / VISUAL_REALITY / DOMUS / GEN5 / ODYSSEY / UNKNOWN",
  "themes": ["array of strings"],
  "subthemes": ["array of strings"],
  "executive_summary": "string — 3-5 sentences, dense, factual",
  "context_and_intent": "string",
  "what_was_done": "string",
  "outputs_produced": [{"type": "string", "name": "string", "description": "string"}],
  "key_decisions": ["array of strings"],
  "lessons_learned": {
    "worked_well": ["array"],
    "failed_or_suboptimal": ["array"],
    "discoveries": ["array"]
  },
  "challenges_and_blockers": ["array of strings"],
  "open_questions": ["array of strings"],
  "next_steps": ["array of strings"]
}

DEPTH SCORE: minor=trivial/test, standard=useful, substantial=decisions+outputs, landmark=critical/architectural
PROJECT HINT: eia=wife's projects, yOS=cognitive OS/AI infra, VISUAL_REALITY=photo/video, DOMUS=home automation, GEN5=future society, ODYSSEY=journey/travel, UNKNOWN=unclear

Output ONLY the JSON object, no markdown, no explanation."""

def make_trivial_card(session_data):
    msgs = session_data.get("messages", [])
    preview = msgs[0].get("content", "")[:200] if msgs else ""
    return {
        "title": session_data.get("title", "Untitled"),
        "date": (session_data.get("created_at", "") or "")[:10],
        "language": "unknown", "depth_score": "minor", "length_category": "short",
        "project_hint": "UNKNOWN", "themes": [], "subthemes": [],
        "executive_summary": f"Trivial session. Content: '{preview}'",
        "context_and_intent": "", "what_was_done": "", "outputs_produced": [],
        "key_decisions": [],
        "lessons_learned": {"worked_well": [], "failed_or_suboptimal": [], "discoveries": []},
        "challenges_and_blockers": [], "open_questions": [], "next_steps": [],
        "_generated_by": "trivial_fallback"
    }

def format_verbatim(session_data):
    lines = [
        f"SESSION TITLE: {session_data.get('title', 'Untitled')}",
        f"DATE: {(session_data.get('created_at', '') or '')[:10]}",
        f"TOTAL MESSAGES: {session_data.get('message_count', len(session_data.get('messages', [])))}",
        "", "--- TRANSCRIPT ---", ""
    ]
    for msg in session_data.get("messages", []):
        content = msg.get("content", "").strip()
        if content:
            lines.append(f"[{msg.get('sender', '?').upper()}]")
            lines.append(content)
            lines.append("")
    return "\n".join(lines)

def generate_card(session_data):
    verbatim = format_verbatim(session_data)
    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"Analyze this session:\n\n{verbatim}"}]
    )
    raw = message.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    if raw.endswith("```"):
        raw = raw[:-3]
    card = json.loads(raw.strip())
    card["_generated_by"] = CLAUDE_MODEL
    card["_input_tokens"] = message.usage.input_tokens
    card["_output_tokens"] = message.usage.output_tokens
    card["_cost_usd"] = round(
        message.usage.input_tokens / 1_000_000 * 3.0 +
        message.usage.output_tokens / 1_000_000 * 15.0, 6
    )
    return card

def card_to_markdown(card, uid):
    depth_emoji = {"minor": "⚪", "standard": "🟡", "substantial": "🟢", "landmark": "⭐"}.get(card.get("depth_score", ""), "⚪")
    lines = [
        f"# {card.get('title', 'Untitled')}",
        "",
        f"**Date:** {card.get('date','?')} | **Project:** {card.get('project_hint','?')} | **Depth:** {depth_emoji} {card.get('depth_score','?')} | **Length:** {card.get('length_category','?')} | **Lang:** {card.get('language','?')}",
        "",
        f"**Themes:** {', '.join(card.get('themes', []))}",
        f"**Subthemes:** {', '.join(card.get('subthemes', []))}",
        "",
        "## Executive Summary",
        card.get("executive_summary", ""),
        "",
    ]
    for section, key in [
        ("## Context & Intent", "context_and_intent"),
        ("## What Was Done", "what_was_done"),
    ]:
        if card.get(key):
            lines += [section, card[key], ""]

    outputs = card.get("outputs_produced", [])
    if outputs:
        lines += ["## Outputs Produced"]
        for o in outputs:
            lines.append(f"- **[{o.get('type','?')}]** {o.get('name','?')} — {o.get('description','')}")
        lines.append("")

    decisions = card.get("key_decisions", [])
    if decisions:
        lines += ["## Key Decisions & Validations"]
        for d in decisions:
            lines.append(f"- {d}")
        lines.append("")

    ll = card.get("lessons_learned", {})
    if any(ll.get(k) for k in ["worked_well", "failed_or_suboptimal", "discoveries"]):
        lines += ["## Lessons Learned"]
        for label, key in [("**Worked well:**", "worked_well"), ("**Failed / suboptimal:**", "failed_or_suboptimal"), ("**Discoveries:**", "discoveries")]:
            if ll.get(key):
                lines.append(label)
                for x in ll[key]:
                    lines.append(f"- {x}")
        lines.append("")

    for section, key in [
        ("## Challenges & Blockers", "challenges_and_blockers"),
        ("## Open Questions", "open_questions"),
    ]:
        items = card.get(key, [])
        if items:
            lines += [section]
            for x in items:
                lines.append(f"- {x}")
            lines.append("")

    lines += ["## Next Steps"]
    ns = card.get("next_steps", [])
    if ns:
        for s in ns:
            lines.append(f"- {s}")
    else:
        lines.append("_None identified._")
    lines += ["", "---", f"_uid: {uid} | generated by: {card.get('_generated_by','?')}_"]
    return "\n".join(lines)

# ── Rapport de progression ────────────────────────────────────────────────────
def print_milestone(processed, total, stats, start_time):
    elapsed = time.time() - start_time
    rate = processed / elapsed * 60 if elapsed > 0 else 0
    remaining = total - processed
    eta_min = remaining / rate if rate > 0 else 0
    log(f"""
{'='*65}
MILESTONE — {processed}/{total} sessions processed
{'='*65}
  ✅ Claude cards    : {stats['llm']}
  ⚪ Trivial (no LLM): {stats['trivial']}
  ⏭️  Skipped (exists): {stats['skipped']}
  ❌ Errors          : {stats['errors']}
  💰 Cost so far     : ${stats['cost']:.4f}
  ⏱️  Elapsed         : {elapsed/60:.1f} min
  🚀 Rate            : {rate:.1f} sessions/min
  ⏳ ETA remaining   : {eta_min:.0f} min
{'='*65}
""")

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    start_time = time.time()
    log("=" * 65)
    log("LLM Memory Pipeline — FULL RUN")
    log(f"Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("=" * 65)

    # Phase 1 : Fetch all session metadata
    log("→ Fetching 351 session metadata...")
    all_sessions = fetch_all_sessions()
    log(f"  ✓ {len(all_sessions)} sessions found")

    stats = {"llm": 0, "trivial": 0, "skipped": 0, "errors": 0, "cost": 0.0}
    processed = 0

    for i, session_meta in enumerate(all_sessions):
        uid = session_meta["uid"]
        title = session_meta.get("title", "")[:50]
        card_path = CARDS_DIR / f"{uid}_card.json"

        # Skip si fiche déjà générée
        if card_path.exists():
            stats["skipped"] += 1
            processed += 1
            if processed % MILESTONE_EVERY == 0:
                print_milestone(processed, len(all_sessions), stats, start_time)
            continue

        # Phase 1 : Collecter verbatim si pas encore fait
        collect_status, collect_info = collect_session(session_meta)
        if collect_status == "error":
            log(f"  [{i+1:3d}] COLLECT ERROR {uid[:12]}: {collect_info}")
            stats["errors"] += 1
            processed += 1
            continue

        # Phase 2 : Générer fiche
        try:
            session_data = json.load(open(EXPORT_DIR / f"{uid}.json"))
            wc = session_data.get("word_count", 0)

            if wc < MIN_WORDS_FOR_LLM:
                card = make_trivial_card(session_data)
                stats["trivial"] += 1
                log(f"  [{i+1:3d}/{len(all_sessions)}] ⚪ TRIVIAL  ({wc:4d}w) : {title}")
            else:
                card = generate_card(session_data)
                cost = card.get("_cost_usd", 0)
                stats["cost"] += cost
                stats["llm"] += 1
                depth = card.get("depth_score", "?")
                log(f"  [{i+1:3d}/{len(all_sessions)}] ✅ {depth:11s} ${cost:.4f} {wc:5d}w : {title}")
                time.sleep(RATE_LIMIT_DELAY)

            # Sauvegarder JSON + Markdown
            with open(card_path, "w") as f:
                json.dump(card, f, ensure_ascii=False, indent=2)
            with open(CARDS_DIR / f"{uid}_card.md", "w") as f:
                f.write(card_to_markdown(card, uid))

        except json.JSONDecodeError as e:
            log(f"  [{i+1:3d}] JSON ERROR {uid[:12]}: {e}")
            stats["errors"] += 1
        except Exception as e:
            log(f"  [{i+1:3d}] ERROR {uid[:12]}: {e}")
            stats["errors"] += 1

        processed += 1

        # Milestone report
        if processed % MILESTONE_EVERY == 0:
            print_milestone(processed, len(all_sessions), stats, start_time)

        # Sauvegarder état
        with open(PROGRESS_FILE, "w") as f:
            json.dump({
                "processed": processed,
                "total": len(all_sessions),
                "stats": stats,
                "last_uid": uid,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)

    # Rapport final
    elapsed = time.time() - start_time
    log(f"""
{'='*65}
FINAL REPORT — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*65}
  Total sessions     : {len(all_sessions)}
  ✅ Claude cards    : {stats['llm']}
  ⚪ Trivial (no LLM): {stats['trivial']}
  ⏭️  Skipped (exists): {stats['skipped']}
  ❌ Errors          : {stats['errors']}
  💰 Total cost      : ${stats['cost']:.4f}
  ⏱️  Total time      : {elapsed/60:.1f} min
  📁 Cards dir       : {CARDS_DIR}
  📋 Log             : {LOG_FILE}
{'='*65}
""")

if __name__ == "__main__":
    main()
