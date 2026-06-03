#!/usr/bin/env python3.11
"""
LLM Memory Pipeline — Phase 3: Archive to Notion
Pousse les 325 fiches session dans "🗃️ Manus Memory — Sessions"
Data source ID: 0720db9b-5e1d-41a2-bd0c-6721fe0dab94
"""

import json
import os
import time
import subprocess
import glob
from pathlib import Path
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────────────
CARDS_DIR = Path("/home/ubuntu/manus_pipeline/session_cards")
EXPORT_DIR = Path("/home/ubuntu/manus_pipeline/sessions_export")
LOG_FILE = Path("/home/ubuntu/manus_pipeline/archive_notion.log")
ARCHIVED_FILE = Path("/home/ubuntu/manus_pipeline/archived_uids.json")

DATA_SOURCE_ID = "0720db9b-5e1d-41a2-bd0c-6721fe0dab94"
RATE_LIMIT_DELAY = 0.5  # seconds between Notion API calls

VALID_PROJECTS = {"eia", "yOS", "VISUAL_REALITY", "DOMUS", "GEN5", "ODYSSEY", "UNKNOWN"}
VALID_DEPTHS   = {"landmark", "substantial", "standard", "minor"}
VALID_LENGTHS  = {"xl", "long", "medium", "short"}
VALID_LANGS    = {"fr", "en", "mixed"}

# ── Logging ───────────────────────────────────────────────────────────────────
def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

# ── Archived state ────────────────────────────────────────────────────────────
def load_archived():
    if ARCHIVED_FILE.exists():
        return set(json.load(open(ARCHIVED_FILE)))
    return set()

def save_archived(s):
    with open(ARCHIVED_FILE, "w") as f:
        json.dump(list(s), f)

# ── Format page content ───────────────────────────────────────────────────────
def format_content(card, uid):
    lines = []

    # Executive Summary (always visible)
    es = card.get("executive_summary", "").strip()
    if es:
        lines += ["## Executive Summary", es, ""]

    # Context & Intent
    ctx = card.get("context_and_intent", "").strip()
    if ctx:
        lines += ["## Context & Intent", ctx, ""]

    # What Was Done
    done = card.get("what_was_done", "").strip()
    if done:
        lines += ["## What Was Done", done, ""]

    # Outputs Produced
    outputs = card.get("outputs_produced", [])
    if outputs:
        lines.append("## Outputs Produced")
        for o in (outputs if isinstance(outputs, list) else []):
            if isinstance(o, dict):
                lines.append(f"- **[{o.get('type','?')}]** {o.get('name','?')} — {o.get('description','')}")
            else:
                lines.append(f"- {o}")
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
    if isinstance(ll, dict) and any(ll.get(k) for k in ["worked_well", "failed_or_suboptimal", "discoveries"]):
        lines.append("## Lessons Learned")
        for label, key in [("Worked well", "worked_well"), ("Failed / suboptimal", "failed_or_suboptimal"), ("Discoveries", "discoveries")]:
            items = ll.get(key, [])
            if items:
                lines.append(f"**{label}:**")
                for x in items:
                    lines.append(f"- {x}")
        lines.append("")
    elif isinstance(ll, str) and ll.strip():
        lines += ["## Lessons Learned", ll, ""]

    # Challenges
    challenges = card.get("challenges_and_blockers", [])
    if challenges:
        lines.append("## Challenges & Blockers")
        for c in (challenges if isinstance(challenges, list) else [challenges]):
            lines.append(f"- {c}")
        lines.append("")

    # Open Questions
    oq = card.get("open_questions", [])
    if oq:
        lines.append("## Open Questions")
        for q in (oq if isinstance(oq, list) else [oq]):
            lines.append(f"- {q}")
        lines.append("")

    # Next Steps (always visible)
    ns = card.get("next_steps", [])
    lines.append("## Next Steps")
    if ns:
        for s in (ns if isinstance(ns, list) else [ns]):
            lines.append(f"- {s}")
    else:
        lines.append("_None identified._")
    lines.append("")

    # Footer
    cost = card.get("_cost_usd", 0)
    model = card.get("_generated_by", "claude")
    lines += ["---", f"_UID: `{uid}` | Model: {model} | Cost: ${cost:.4f}_"]

    return "\n".join(lines)

# ── MCP call ──────────────────────────────────────────────────────────────────
def mcp_create_page(properties, content, icon="📝"):
    input_data = {
        "parent": {"data_source_id": DATA_SOURCE_ID},
        "pages": [{
            "icon": icon,
            "properties": properties,
            "content": content
        }]
    }
    input_json = json.dumps(input_data)
    result = subprocess.run(
        ["manus-mcp-cli", "tool", "call", "notion-create-pages",
         "--server", "notion", "--input", input_json],
        capture_output=True, text=True, timeout=45
    )
    # Get latest result file
    files = sorted(glob.glob("/home/ubuntu/.mcp/tool-results/*.json"), key=os.path.getmtime, reverse=True)
    if files:
        try:
            r = json.load(open(files[0]))
            if "error" in str(r).lower() and "result" not in r:
                return False, str(r)
            return True, r
        except:
            pass
    return False, result.stdout + result.stderr

# ── Archive one session ───────────────────────────────────────────────────────
def archive_session(card_path, archived_set):
    uid = card_path.stem.replace("_card", "")

    if uid in archived_set:
        return "skip", None

    try:
        card = json.load(open(card_path))
    except Exception as e:
        return "error_load", str(e)

    title   = (card.get("title") or "Untitled")[:200]
    project = card.get("project_hint", "UNKNOWN")
    depth   = card.get("depth_score", "minor")
    length  = card.get("length_category", "short")
    lang    = card.get("language", "fr")
    themes  = ", ".join(card.get("themes", []))[:500]
    subth   = ", ".join(card.get("subthemes", []))[:500]
    date_s  = (card.get("date") or "")[:10]

    # Sanitize select values
    project = project if project in VALID_PROJECTS else "UNKNOWN"
    depth   = depth   if depth   in VALID_DEPTHS   else "minor"
    length  = length  if length  in VALID_LENGTHS  else "short"
    lang    = lang    if lang    in VALID_LANGS     else "fr"

    # Icon by depth
    icon = {"landmark": "⭐", "substantial": "🟢", "standard": "🔵", "minor": "⚪"}.get(depth, "📝")

    properties = {
        "Title":    title,
        "Project":  project,
        "Depth":    depth,
        "Length":   length,
        "Language": lang,
        "Themes":   themes,
        "Subthemes": subth,
        "UID":      uid,
        "Archived": "__YES__",
    }
    if date_s and len(date_s) == 10:
        properties["date:Date:start"]       = date_s
        properties["date:Date:is_datetime"] = 0

    content = format_content(card, uid)

    ok, result = mcp_create_page(properties, content, icon)
    if ok:
        archived_set.add(uid)
        return "ok", depth
    else:
        return "error_api", str(result)[:200]

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    log("=" * 65)
    log("Manus Memory — Archive to Notion")
    log(f"Data source: {DATA_SOURCE_ID}")
    log("=" * 65)

    archived_set = load_archived()
    log(f"Already archived: {len(archived_set)}")

    card_files = sorted(CARDS_DIR.glob("*_card.json"))
    total = len(card_files)
    log(f"Total cards: {total}")

    stats = {"ok": 0, "skip": 0, "error": 0}

    for i, card_path in enumerate(card_files):
        status, info = archive_session(card_path, archived_set)

        if status == "ok":
            stats["ok"] += 1
            card = json.load(open(card_path))
            title = card.get("title", "?")[:55]
            log(f"  [{i+1:3d}/{total}] ✅ {info:11s} : {title}")
            time.sleep(RATE_LIMIT_DELAY)
        elif status == "skip":
            stats["skip"] += 1
        else:
            stats["error"] += 1
            uid = card_path.stem.replace("_card", "")[:12]
            log(f"  [{i+1:3d}/{total}] ❌ {status:12s} : {uid} — {info}")
            time.sleep(RATE_LIMIT_DELAY)

        if (i + 1) % 25 == 0:
            save_archived(archived_set)
            log(f"  --- [{i+1}/{total}] ✅{stats['ok']} ⏭️{stats['skip']} ❌{stats['error']} ---")

    save_archived(archived_set)

    log(f"""
{'='*65}
ARCHIVE COMPLETE — {datetime.now().strftime('%Y-%m-%d %H:%M')}
  ✅ Archived : {stats['ok']}
  ⏭️  Skipped  : {stats['skip']}
  ❌ Errors   : {stats['error']}
  🔗 Notion   : https://notion.so/{DATA_SOURCE_ID.replace('-','')}
{'='*65}
""")

if __name__ == "__main__":
    main()
