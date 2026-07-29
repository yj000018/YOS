#!/usr/bin/env python3
"""
Raindrop AI Tagger — Y-OS
Token: 98422e2a-e0bd-4e35-be68-9277f52caaac
App: Raindrop to yOS | Client ID: 6a0da56f9a8b8816ae48f3f4
"""

import requests
import json
import time
import re
from openai import OpenAI

RAINDROP_TOKEN = "98422e2a-e0bd-4e35-be68-9277f52caaac"
RAINDROP_BASE = "https://api.raindrop.io/rest/v1"
MODEL = "claude-haiku-4-5"  # Fast + reliable for bulk tagging

PREFERRED_TAGS = [
    "ai", "technology", "finance", "music", "youtube", "wellness", "science",
    "diy", "lifestyle", "shopping", "design", "art", "travel", "productivity",
    "startup", "business", "health", "education", "programming", "news",
    "video", "tool", "research", "social", "food", "sport", "politics",
    "environment", "philosophy", "psychology", "inspiration"
]

llm = OpenAI()

def get_untagged_bookmarks(limit=150):
    r = requests.get(
        f"{RAINDROP_BASE}/raindrops/0",
        headers={"Authorization": f"Bearer {RAINDROP_TOKEN}"},
        params={"search": "notag:true", "perpage": limit, "page": 0},
        timeout=15
    )
    data = r.json()
    return data.get("items", []), data.get("count", 0)

def domain_fallback_tags(url, title):
    """Assign tags based on URL/title patterns when LLM fails."""
    url_lower = url.lower()
    title_lower = title.lower()
    
    if "youtube.com" in url_lower or "youtu.be" in url_lower:
        return ["youtube", "video"]
    if "github.com" in url_lower:
        return ["programming", "technology"]
    if "medium.com" in url_lower or "substack.com" in url_lower:
        return ["article", "education"]
    if "amazon" in url_lower:
        return ["shopping"]
    if "twitter.com" in url_lower or "x.com" in url_lower:
        return ["social"]
    if "linkedin.com" in url_lower:
        return ["business", "social"]
    if "google.com/search" in url_lower or "google search" in title_lower:
        return ["search"]
    if any(w in title_lower for w in ["ai", "gpt", "llm", "machine learning", "neural"]):
        return ["ai", "technology"]
    if any(w in title_lower for w in ["finance", "invest", "stock", "crypto", "bitcoin"]):
        return ["finance"]
    if any(w in title_lower for w in ["health", "médecin", "santé", "wellness"]):
        return ["health", "wellness"]
    if any(w in title_lower for w in ["design", "ui", "ux", "figma"]):
        return ["design"]
    if any(w in title_lower for w in ["music", "musique", "song", "album"]):
        return ["music"]
    return ["web"]

def analyze_chunk_with_llm(chunk):
    """Analyze a chunk of bookmarks with LLM."""
    items_text = []
    for i, bm in enumerate(chunk):
        title = (bm.get("title") or "").strip()[:80] or "(no title)"
        url = bm.get("link", "")
        try:
            domain = url.split("/")[2] if url.startswith("http") else url[:40]
        except:
            domain = url[:40]
        items_text.append(f"{i+1}. {title} | {domain}")
    
    items_str = "\n".join(items_text)
    preferred_str = ", ".join(PREFERRED_TAGS)
    
    prompt = f"""Tag these bookmarks. Preferred tags: {preferred_str}

Rules: lowercase, 1-3 tags each, single words or hyphenated.

{items_str}

JSON only: [{{"index":1,"tags":["tag1","tag2"]}}]"""

    resp = llm.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=1500
    )
    
    content = resp.choices[0].message.content
    if content is None:
        raise ValueError("LLM returned None content")
    
    content = content.strip()
    
    # Extract JSON array
    match = re.search(r'\[.*\]', content, re.DOTALL)
    if match:
        content = match.group(0)
    
    return json.loads(content)

def apply_tags(bookmark_id, tags):
    r = requests.put(
        f"{RAINDROP_BASE}/raindrop/{bookmark_id}",
        headers={
            "Authorization": f"Bearer {RAINDROP_TOKEN}",
            "Content-Type": "application/json"
        },
        json={"tags": tags},
        timeout=10
    )
    return r.json()

def process_batch(batch_num):
    print(f"\n{'='*60}")
    print(f"LOT {batch_num} — Fetch signets non tagués...")
    
    bookmarks, total = get_untagged_bookmarks(150)
    
    if not bookmarks:
        print(f"  ✅ Aucun signet non tagué. Total: {total}")
        return 0, total
    
    print(f"  Récupérés: {len(bookmarks)} | Total restants: {total}")
    
    # Build tag assignments
    assignments = {}  # idx -> tags
    chunk_size = 50
    
    for chunk_start in range(0, len(bookmarks), chunk_size):
        chunk = bookmarks[chunk_start:chunk_start + chunk_size]
        chunk_num = chunk_start // chunk_size + 1
        total_chunks = (len(bookmarks) - 1) // chunk_size + 1
        print(f"  LLM chunk {chunk_num}/{total_chunks} ({len(chunk)} signets)...", end=" ", flush=True)
        
        try:
            tag_data = analyze_chunk_with_llm(chunk)
            for item in tag_data:
                idx = chunk_start + item["index"] - 1
                assignments[idx] = item.get("tags", [])
            print(f"OK ({len(tag_data)} tagués)")
        except Exception as e:
            print(f"FALLBACK ({e})")
            for i, bm in enumerate(chunk):
                idx = chunk_start + i
                assignments[idx] = domain_fallback_tags(
                    bm.get("link", ""), 
                    bm.get("title", "")
                )
        
        time.sleep(0.2)
    
    # Apply tags
    print(f"  Application tags...", end=" ", flush=True)
    tagged = 0
    errors = 0
    
    for idx, tags in assignments.items():
        if idx >= len(bookmarks):
            continue
        
        bm = bookmarks[idx]
        clean_tags = [t.lower().strip().replace(" ", "-") for t in tags if t][:3]
        if not clean_tags:
            clean_tags = domain_fallback_tags(bm.get("link",""), bm.get("title",""))
        
        result = apply_tags(bm["_id"], clean_tags)
        if result.get("result"):
            tagged += 1
        else:
            errors += 1
        
        time.sleep(0.03)
    
    print(f"{tagged} OK, {errors} erreurs")
    return tagged, max(0, total - tagged)

def main():
    print("🏷️  RAINDROP AI TAGGER — Y-OS")
    
    # Verify
    r = requests.get(f"{RAINDROP_BASE}/user", headers={"Authorization": f"Bearer {RAINDROP_TOKEN}"})
    user = r.json()
    if not user.get("result"):
        print(f"❌ Auth failed: {user}")
        return
    print(f"✅ {user['user']['email']} | Modèle: {MODEL}")
    
    _, initial = get_untagged_bookmarks(1)
    print(f"📊 Non tagués au départ: {initial}")
    
    total_tagged = 0
    last_batch = 0
    
    for batch_num in range(1, 11):
        last_batch = batch_num
        tagged, remaining = process_batch(batch_num)
        total_tagged += tagged
        
        print(f"  → Total tagués: {total_tagged} | Restants: ~{remaining}")
        
        if tagged == 0:
            print("✅ Terminé — plus rien à tagger.")
            break
        
        time.sleep(0.5)
    
    print(f"\n{'='*60}")
    print(f"🏁 RAPPORT FINAL")
    print(f"   Tagués ce run : {total_tagged}")
    print(f"   Lots traités  : {last_batch}")
    print(f"   Restants est. : {max(0, initial - total_tagged)}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
