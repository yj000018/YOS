#!/usr/bin/env python3.11
"""
LLM Memory Pipeline (LMP) — Manus instance
Phase 1 : Collecte complète des sessions

- Récupère les N sessions via API (pagination offset, toutes les pages)
- Pour chaque session : concatène TOUS les segments, extrait verbatim propre (user + agent)
- Déduplication : skip si uid déjà exporté dans sessions_export/
- Sauvegarde : sessions_export/{uid}.json + sessions_index.json
"""

import json
import os
import time
import requests
from pathlib import Path
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────────────
TOKEN = os.environ.get("MANUS_TOKEN", (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    ".eyJlbWFpbCI6Inlhbm5pY2suam9sbGlldEBnbWFpbC5jb20iLCJleHAiOjE3ODM0MzEwOTMsImlhdCI6MTc3NTY1NTA5MywianRpIjoiY3dUOUxoOEtzNmNacEwzakVSaHozQyIsIm5hbWUiOiJZYW5uaWNrIEpvbGxpZXQiLCJvcmlnaW5hbF91c2VyX2lkIjoiIiwidGVhbV91aWQiOiIiLCJ0eXBlIjoidXNlciIsInVzZXJfaWQiOiIzMTA0MTk2NjMwMzIzODE4MzMifQ"
    ".88v6mbthCgzJQwUAc1-_wKYo-8uSdQ_qkro7C2cYVuM"
))
BASE_URL = "https://api.manus.im"
EXPORT_DIR = Path("/home/ubuntu/manus_pipeline/sessions_export")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "connect-protocol-version": "1",
    "x-client-id": "SH6GDQiPhdFcHsaqh7U4Rm",
}
HEADERS_GET = {k: v for k, v in HEADERS.items() if k != "Content-Type"}

PAGE_SIZE = 100
RATE_LIMIT_DELAY = 0.4  # seconds between session content requests


# ── Pagination : récupère TOUTES les sessions ─────────────────────────────────

def list_all_sessions() -> list:
    """Récupère toutes les sessions via pagination offset jusqu'à épuisement."""
    all_sessions = []
    offset = 0
    total_reported = None

    while True:
        resp = requests.post(
            f"{BASE_URL}/session.v1.SessionService/ListSessions",
            headers=HEADERS,
            json={"pageSize": PAGE_SIZE, "offset": offset},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()

        sessions = data.get("sessions", [])
        has_next = data.get("hasNext", False)

        if total_reported is None:
            total_reported = data.get("total", "?")
            print(f"  API reports total: {total_reported} sessions")

        all_sessions.extend(sessions)
        print(f"  Batch offset={offset:4d} → {len(sessions):3d} sessions  (cumul: {len(all_sessions)})")

        if not has_next or len(sessions) == 0:
            break

        offset += PAGE_SIZE
        time.sleep(0.2)

    print(f"  ✓ Collected {len(all_sessions)} sessions (API total: {total_reported})")
    return all_sessions


# ── Extraction verbatim : TOUS les segments concaténés ───────────────────────

def extract_verbatim(session_data: dict) -> list:
    """
    Extrait les messages user + agent depuis TOUS les segments.
    Les segments sont concaténés dans l'ordre chronologique.
    Filtre : type=chat, sender in (user, assistant, agent), content non vide.
    """
    messages = []
    segments = session_data.get("segments", [])

    for seg_idx, seg in enumerate(segments):
        events = seg.get("events", [])
        for e in events:
            # Garder uniquement les vrais messages de chat
            if e.get("type") != "chat":
                continue
            sender = e.get("sender", "")
            if sender not in ("user", "assistant", "agent"):
                continue

            content = e.get("content", "")
            if not content:
                continue

            # Normaliser : content peut être str ou list de dicts
            if isinstance(content, list):
                parts = []
                for item in content:
                    if isinstance(item, dict):
                        text = item.get("text") or item.get("content") or ""
                        if text:
                            parts.append(str(text))
                    elif isinstance(item, str) and item.strip():
                        parts.append(item)
                content = "\n".join(parts)

            content = content.strip()
            if not content:
                continue

            # Normaliser sender label
            sender_label = "USER" if sender == "user" else "MANUS"

            messages.append({
                "sender": sender_label,
                "timestamp": e.get("timestamp"),
                "segment": seg_idx,
                "content": content,
            })

    return messages


# ── Fetch contenu d'une session ───────────────────────────────────────────────

def fetch_session_content(uid: str) -> dict | None:
    """
    Récupère le contenu complet d'une session.
    Retourne None si 403 (privé/inaccessible).
    """
    resp = requests.get(
        f"{BASE_URL}/api/chat/getSessionV2",
        headers=HEADERS_GET,
        params={"sessionId": uid, "getFirstSegment": "false"},
        timeout=30,
    )
    if resp.status_code == 403:
        return None
    resp.raise_for_status()
    return resp.json().get("data", {})


# ── Calcul stats verbatim ─────────────────────────────────────────────────────

def compute_stats(messages: list) -> dict:
    word_count = sum(len(m["content"].split()) for m in messages)
    # Estimation tokens : ~1.3 tokens/word (français/anglais mixte)
    token_estimate = int(word_count * 1.3)
    user_msgs = sum(1 for m in messages if m["sender"] == "USER")
    agent_msgs = sum(1 for m in messages if m["sender"] == "MANUS")

    # Catégorie longueur
    if word_count < 500:
        length_cat = "short"
    elif word_count < 2000:
        length_cat = "medium"
    elif word_count < 6000:
        length_cat = "long"
    else:
        length_cat = "xl"

    return {
        "word_count": word_count,
        "token_estimate": token_estimate,
        "message_count": len(messages),
        "user_messages": user_msgs,
        "agent_messages": agent_msgs,
        "length_category": length_cat,
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main(subset: list = None):
    """
    subset : liste de UIDs à traiter (pour tests). None = toutes les sessions.
    """
    print("=" * 60)
    print("LLM Memory Pipeline — Phase 1 : Collect")
    print(f"Export dir : {EXPORT_DIR}")
    print("=" * 60)

    # 1. Liste complète
    print("\n→ Fetching session list...")
    all_sessions = list_all_sessions()

    # Filtrer sur subset si fourni
    if subset:
        all_sessions = [s for s in all_sessions if s["uid"] in subset]
        print(f"  Subset mode: {len(all_sessions)} sessions selected")

    # 2. Sauvegarder l'index
    index = []
    for s in all_sessions:
        index.append({
            "uid": s["uid"],
            "title": s.get("title", ""),
            "created_at": s.get("createdAt", ""),
            "updated_at": s.get("updatedAt", ""),
            "status": s.get("status", ""),
            "last_message_preview": s.get("lastDisplayMessage", "")[:200],
        })

    index_path = EXPORT_DIR / "sessions_index.json"
    with open(index_path, "w") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"\n✓ Index saved: {index_path} ({len(index)} entries)")

    # 3. Collecter le verbatim de chaque session
    print(f"\n→ Fetching verbatim for {len(all_sessions)} sessions...\n")
    stats = {"success": 0, "skipped_existing": 0, "skipped_private": 0, "error": 0}
    total_words = 0
    total_tokens = 0

    for i, session in enumerate(all_sessions):
        uid = session["uid"]
        title = session.get("title", "")[:60]
        out_path = EXPORT_DIR / f"{uid}.json"

        # Déduplication : skip si déjà exporté
        if out_path.exists():
            print(f"  [{i+1:3d}/{len(all_sessions)}] SKIP (exists) : {title}")
            stats["skipped_existing"] += 1
            continue

        try:
            content = fetch_session_content(uid)

            if content is None:
                print(f"  [{i+1:3d}/{len(all_sessions)}] SKIP (private): {title}")
                stats["skipped_private"] += 1
                continue

            messages = extract_verbatim(content)
            s = compute_stats(messages)
            total_words += s["word_count"]
            total_tokens += s["token_estimate"]

            segment_count = len(content.get("segments", []))

            export = {
                "uid": uid,
                "title": session.get("title", ""),
                "created_at": session.get("createdAt", ""),
                "updated_at": session.get("updatedAt", ""),
                "status": session.get("status", ""),
                "segment_count": segment_count,
                "stats": s,
                "messages": messages,
            }

            with open(out_path, "w") as f:
                json.dump(export, f, ensure_ascii=False, indent=2)

            print(f"  [{i+1:3d}/{len(all_sessions)}] ✓ [{s['length_category']:6s}] "
                  f"{s['word_count']:5d}w / {s['token_estimate']:6d}t / "
                  f"{segment_count}seg / {s['message_count']}msg : {title}")
            stats["success"] += 1

        except Exception as e:
            print(f"  [{i+1:3d}/{len(all_sessions)}] ERROR {uid}: {e}")
            stats["error"] += 1

        time.sleep(RATE_LIMIT_DELAY)

    # 4. Résumé
    print("\n" + "=" * 60)
    print("SUMMARY")
    print(f"  Success          : {stats['success']}")
    print(f"  Skipped (exists) : {stats['skipped_existing']}")
    print(f"  Skipped (private): {stats['skipped_private']}")
    print(f"  Errors           : {stats['error']}")
    print(f"  Total words      : {total_words:,}")
    print(f"  Total tokens est.: {total_tokens:,}")
    print(f"  Claude cost est. : ${total_tokens / 1_000_000 * 3:.2f} (input only, Sonnet)")
    print(f"\nExport: {EXPORT_DIR}")
    print("=" * 60)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    # Mode test : passer des UIDs en arguments
    # python3.11 01_collect_sessions.py --test
    # python3.11 01_collect_sessions.py uid1 uid2 uid3
    if "--test" in sys.argv:
        # 5 sessions représentatives choisies manuellement
        TEST_UIDS = [
            "mWVysv0MBCNHRsi0n2etX7",  # What Does 1 2 3 OK-GO Mean? — short conceptual
            "gTTBiSafWaj72Gr9fsOMhY",  # Create a Skill for Switching to Chat Mode — with output
            "8YCBdRxCMDYbhgQXx8v9VG",  # LLM Knowledge Distillation Pipeline — long technical
            "vXs1WpNeEuH8ZJ4ybDExws",  # Cette session — contenu connu
            "eak6dAJxZKruhgQhMUhTHh",  # Journey — project focused
        ]
        main(subset=TEST_UIDS)
    elif len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        main(subset=sys.argv[1:])
    else:
        main()
