#!/usr/bin/env python3
"""
delta_raindrop.py — Pipeline delta automatique pour les bookmarks Raindrop
Détecte les nouveaux bookmarks depuis la dernière cutoff et les pousse dans GitHub YOS

Architecture: cron 03:00 UTC sur le Cloud Computer
Auteur: Y-OS pipeline (session 2026-07-31)
"""

import json
import os
import time
import base64
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# ─── CONFIG ───────────────────────────────────────────────────────────────────
BASE_DIR = Path("/home/ubuntu/yos/ledger")
STATE_FILE = BASE_DIR / "state_raindrop.json"
OUTPUT_DIR = BASE_DIR / "bookmarks_raindrop"
LOG_FILE = BASE_DIR / "logs" / "delta_raindrop.log"

RAINDROP_TOKEN = open(BASE_DIR / ".raindrop_token").read().strip()
GITHUB_PAT = open(BASE_DIR / ".github_pat").read().strip()
GITHUB_REPO = "yj000018/YOS"
GITHUB_BRANCH = "main"
GITHUB_PATH_PREFIX = "08_LOGS/raindrop-bookmarks"

GEMINI_API_KEY = open(BASE_DIR / ".gemini_key").read().strip() if (BASE_DIR / ".gemini_key").exists() else os.environ.get("GEMINI_API_KEY", "")

# ─── LOGGING ──────────────────────────────────────────────────────────────────
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def log(msg):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

# ─── STATE ────────────────────────────────────────────────────────────────────
def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    # Cutoff initiale : 2026-07-31 (date du premier run)
    return {
        "last_cutoff": "2026-07-31T00:00:00.000Z",
        "total_processed": 0,
        "last_run": None
    }

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))

# ─── RAINDROP API ─────────────────────────────────────────────────────────────
def raindrop_get(path, params=None):
    url = f"https://api.raindrop.io/rest/v1{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {RAINDROP_TOKEN}",
        "Content-Type": "application/json"
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

def fetch_new_bookmarks(since_iso):
    """Récupère tous les bookmarks créés après since_iso"""
    bookmarks = []
    page = 0
    per_page = 50
    since_dt = datetime.fromisoformat(since_iso.replace("Z", "+00:00"))
    
    while True:
        data = raindrop_get("/raindrops/0", {
            "sort": "-created",
            "perpage": per_page,
            "page": page
        })
        items = data.get("items", [])
        if not items:
            break
        
        new_in_page = 0
        for item in items:
            created_str = item.get("created", "")
            if not created_str:
                continue
            created_dt = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
            if created_dt > since_dt:
                bookmarks.append(item)
                new_in_page += 1
            else:
                # Les items sont triés par -created, donc on peut arrêter
                return bookmarks
        
        if new_in_page < per_page:
            break
        page += 1
        time.sleep(0.2)
    
    return bookmarks

# ─── GEMINI ENRICHMENT ────────────────────────────────────────────────────────
def enrich_bookmark_gemini(bookmark):
    """Enrichit un bookmark avec tags sémantiques et résumé via Gemini"""
    if not GEMINI_API_KEY:
        return {"summary": "", "semantic_tags": [], "category": ""}
    
    title = bookmark.get("title", "")
    link = bookmark.get("link", "")
    excerpt = bookmark.get("excerpt", "")[:500]
    existing_tags = bookmark.get("tags", [])
    
    prompt = f"""Analyze this bookmark and return JSON only:
Title: {title}
URL: {link}
Excerpt: {excerpt}
Existing tags: {existing_tags}

Return exactly:
{{"summary": "1 sentence description", "semantic_tags": ["tag1", "tag2", "tag3"], "category": "one of: AI/Tech/Design/Science/Business/Personal/Other"}}"""
    
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 300, "temperature": 0.1}
    }).encode()
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            resp = json.loads(r.read())
        text = resp["candidates"][0]["content"]["parts"][0]["text"]
        # Extraire le JSON
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(text[start:end])
    except Exception as e:
        log(f"  Gemini error: {e}")
    
    return {"summary": "", "semantic_tags": [], "category": ""}

# ─── FACT SHEET GENERATION ────────────────────────────────────────────────────
def generate_bookmark_md(bookmark, enrichment):
    bid = bookmark.get("_id", "")
    title = bookmark.get("title", "Untitled")
    link = bookmark.get("link", "")
    created = bookmark.get("created", "")[:10]  # YYYY-MM-DD
    tags = bookmark.get("tags", [])
    excerpt = bookmark.get("excerpt", "")
    collection_id = bookmark.get("collection", {}).get("$id", "")
    note = bookmark.get("note", "")
    
    # Enrichissement Gemini
    summary = enrichment.get("summary", "")
    semantic_tags = enrichment.get("semantic_tags", [])
    category = enrichment.get("category", "")
    
    # Fusionner tags existants + sémantiques
    all_tags = list(set(tags + semantic_tags))
    
    front_matter = f"""---
id: {bid}
title: "{title.replace('"', "'")}"
date: "{created}"
url: "{link}"
collection_id: {collection_id}
tags: {json.dumps(all_tags)}
category: "{category}"
summary: "{summary.replace('"', "'")}"
source: "raindrop"
---"""
    
    content_parts = [front_matter, "", f"# {title}", ""]
    
    if summary:
        content_parts += [f"> {summary}", ""]
    
    content_parts += [
        "## Metadata",
        "",
        f"| Field | Value |",
        f"|---|---|",
        f"| URL | [{link[:80]}]({link}) |",
        f"| Date | {created} |",
        f"| Tags | {', '.join(tags) if tags else '—'} |",
        f"| Category | {category or '—'} |",
        ""
    ]
    
    if excerpt:
        content_parts += ["## Excerpt", "", excerpt, ""]
    
    if note:
        content_parts += ["## Note", "", note, ""]
    
    if semantic_tags:
        content_parts += [f"## Semantic Tags", "", ", ".join(f"`{t}`" for t in semantic_tags), ""]
    
    return "\n".join(content_parts)

# ─── GITHUB PUSH ──────────────────────────────────────────────────────────────
def github_api(method, path, data=None):
    url = f"https://api.github.com{path}"
    payload = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=payload, method=method, headers={
        "Authorization": f"token {GITHUB_PAT}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
        "User-Agent": "Y-OS-delta-raindrop"
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read()), r.status
    except urllib.error.HTTPError as e:
        return json.loads(e.read()), e.code

def push_bookmarks_to_github(bookmarks_md):
    """Push tous les bookmarks en un seul commit atomique"""
    if not bookmarks_md:
        return True
    
    log(f"  Pushing {len(bookmarks_md)} bookmarks to GitHub...")
    
    # 1. Récupérer le SHA du dernier commit sur main
    ref_data, _ = github_api("GET", f"/repos/{GITHUB_REPO}/git/ref/heads/{GITHUB_BRANCH}")
    base_sha = ref_data["object"]["sha"]
    
    # 2. Récupérer le tree SHA
    commit_data, _ = github_api("GET", f"/repos/{GITHUB_REPO}/git/commits/{base_sha}")
    tree_sha = commit_data["tree"]["sha"]
    
    # 3. Créer les blobs
    tree_items = []
    for filename, content in bookmarks_md.items():
        blob_data, _ = github_api("POST", f"/repos/{GITHUB_REPO}/git/blobs", {
            "content": base64.b64encode(content.encode()).decode(),
            "encoding": "base64"
        })
        tree_items.append({
            "path": f"{GITHUB_PATH_PREFIX}/{filename}",
            "mode": "100644",
            "type": "blob",
            "sha": blob_data["sha"]
        })
        time.sleep(0.05)
    
    # 4. Créer le nouveau tree
    new_tree, _ = github_api("POST", f"/repos/{GITHUB_REPO}/git/trees", {
        "base_tree": tree_sha,
        "tree": tree_items
    })
    
    # 5. Créer le commit
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    new_commit, _ = github_api("POST", f"/repos/{GITHUB_REPO}/git/commits", {
        "message": f"feat(raindrop): delta {len(bookmarks_md)} bookmarks [{now}]",
        "tree": new_tree["sha"],
        "parents": [base_sha]
    })
    
    # 6. Mettre à jour la ref
    github_api("PATCH", f"/repos/{GITHUB_REPO}/git/refs/heads/{GITHUB_BRANCH}", {
        "sha": new_commit["sha"],
        "force": False
    })
    
    log(f"  ✅ Pushed: {new_commit['sha'][:8]}")
    return True

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    log("=" * 60)
    log("delta_raindrop.py — START")
    
    state = load_state()
    cutoff = state["last_cutoff"]
    log(f"Cutoff: {cutoff}")
    
    # 1. Fetch new bookmarks
    log("Fetching new bookmarks from Raindrop API...")
    try:
        new_bookmarks = fetch_new_bookmarks(cutoff)
    except Exception as e:
        log(f"❌ Raindrop API error: {e}")
        return
    
    log(f"Found {len(new_bookmarks)} new bookmarks")
    
    if not new_bookmarks:
        log("Nothing to do.")
        state["last_run"] = datetime.now(timezone.utc).isoformat()
        save_state(state)
        return
    
    # 2. Enrich + generate MD
    bookmarks_md = {}
    errors = 0
    
    for i, bookmark in enumerate(new_bookmarks):
        bid = bookmark.get("_id", "")
        title = bookmark.get("title", "?")[:50]
        log(f"  [{i+1}/{len(new_bookmarks)}] {bid} — {title}")
        
        try:
            enrichment = enrich_bookmark_gemini(bookmark)
            md_content = generate_bookmark_md(bookmark, enrichment)
            filename = f"{bid}.md"
            bookmarks_md[filename] = md_content
            
            # Sauvegarder localement aussi
            (OUTPUT_DIR / filename).write_text(md_content)
        except Exception as e:
            log(f"    ❌ Error: {e}")
            errors += 1
        
        time.sleep(0.3)  # Rate limit Gemini
    
    # 3. Push to GitHub
    try:
        push_bookmarks_to_github(bookmarks_md)
    except Exception as e:
        log(f"❌ GitHub push error: {e}")
    
    # 4. Update state
    # Nouvelle cutoff = date du bookmark le plus récent
    if new_bookmarks:
        latest = max(b.get("created", "") for b in new_bookmarks)
        state["last_cutoff"] = latest
    state["total_processed"] = state.get("total_processed", 0) + len(new_bookmarks)
    state["last_run"] = datetime.now(timezone.utc).isoformat()
    save_state(state)
    
    log(f"DONE — {len(new_bookmarks)} processed, {errors} errors")
    log("=" * 60)

if __name__ == "__main__":
    main()
