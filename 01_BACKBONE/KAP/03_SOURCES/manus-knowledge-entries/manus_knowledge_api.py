#!/usr/bin/env python3
"""
Script de création des 27 Knowledge entries UPPERCASE via l'API Manus.
Nécessite le token session_id passé en argument ou via variable d'environnement.
Usage: python3 create_27_km.py <session_token>
"""
import json
import requests
import sys
import time

API_BASE = "https://api.manus.im"

def create_knowledge(token, name, content):
    resp = requests.post(
        f"{API_BASE}/knowledge.v1.KnowledgeService/CreateKnowledge",
        headers={
            "content-type": "application/json",
            "authorization": f"Bearer {token}"
        },
        json={"name": name, "content": content},
        timeout=30
    )
    return resp.status_code, resp.json()

def list_knowledge(token):
    resp = requests.post(
        f"{API_BASE}/knowledge.v1.KnowledgeService/ListKnowledge",
        headers={
            "content-type": "application/json",
            "authorization": f"Bearer {token}"
        },
        json={"limit": 200, "offset": 0},
        timeout=30
    )
    return resp.json()

def delete_knowledge(token, uid):
    resp = requests.post(
        f"{API_BASE}/knowledge.v1.KnowledgeService/DeleteKnowledge",
        headers={
            "content-type": "application/json",
            "authorization": f"Bearer {token}"
        },
        json={"knowledgeUid": uid},
        timeout=30
    )
    return resp.status_code

if __name__ == "__main__":
    token = sys.argv[1] if len(sys.argv) > 1 else None
    if not token:
        print("Usage: python3 create_27_km.py <session_token>")
        sys.exit(1)
    
    entries = json.load(open("/home/ubuntu/km_27_entries.json"))
    print(f"Creating {len(entries)} entries...")
    
    created, errors = 0, []
    for i, entry in enumerate(entries):
        name = entry["title"]
        content = entry["content"]
        status, data = create_knowledge(token, name, content)
        if status == 200:
            created += 1
            uid = data.get("knowledge", {}).get("uid", "?")
            print(f"[{i+1:2}/{len(entries)}] ✓ {name} (uid={uid})")
        else:
            errors.append({"name": name, "status": status, "error": data})
            print(f"[{i+1:2}/{len(entries)}] ✗ {name} — {status}: {data}")
        time.sleep(0.1)
    
    print(f"\n=== RESULT: {created}/{len(entries)} created, {len(errors)} errors ===")
    if errors:
        print("ERRORS:", json.dumps(errors, indent=2))
