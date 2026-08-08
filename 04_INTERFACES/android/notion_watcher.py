# TOKENS: Loaded from env vars NOTION_TOKEN and TELEGRAM_TOKEN (stored in /home/ubuntu/yos/.env on CC)
#!/usr/bin/env python3
"""
Y-OS Notion Watcher — Polling 5min
Détecte les tâches passées en "Done" dans la DB Action Items Notion
→ Envoie notif Telegram + log

DB Action Items: collection://1e0508b7-405c-4180-b39d-4f681735245c
DB Fleet:        collection://070971da-4ae4-4ace-96fc-5a9b2f5a930f
"""

import requests
import json
import os
from datetime import datetime, timezone

# Config
NOTION_TOKEN = "${NOTION_TOKEN}"
TELEGRAM_TOKEN = "${TELEGRAM_TOKEN}"
CHAT_ID = "223132272"
STATE_FILE = "/home/ubuntu/yos/android/notion_watcher_state.json"
LOG_FILE = "/home/ubuntu/yos/android/logs/notion_watcher.log"

# Notion DB IDs
ACTION_ITEMS_DB = "b8d00a1ef73a43909532a55c67b71e2a"
FLEET_DB = "ee6b6f120b06428d9b3e3d90eb877dab"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def log(msg):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def send_telegram(msg):
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"},
            timeout=10
        )
        return r.status_code == 200
    except Exception as e:
        log(f"Telegram error: {e}")
        return False

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"seen_done": []}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def query_action_items_done():
    """Query Notion DB for all items with Status = Done"""
    url = f"https://api.notion.com/v1/databases/{ACTION_ITEMS_DB}/query"
    payload = {
        "filter": {
            "property": "Status",
            "select": {"equals": "Done"}
        }
    }
    try:
        r = requests.post(url, headers=HEADERS, json=payload, timeout=15)
        if r.status_code == 200:
            return r.json().get("results", [])
        else:
            log(f"Notion query error: {r.status_code} {r.text[:100]}")
            return []
    except Exception as e:
        log(f"Notion request error: {e}")
        return []

def get_page_title(page):
    """Extract title from a Notion page"""
    try:
        title_prop = page.get("properties", {}).get("Name", {})
        title_arr = title_prop.get("title", [])
        if title_arr:
            return title_arr[0].get("plain_text", "Unknown")
    except:
        pass
    return "Unknown"

def get_page_priority(page):
    """Extract priority from a Notion page"""
    try:
        prio = page.get("properties", {}).get("Priority", {})
        sel = prio.get("select", {})
        if sel:
            return sel.get("name", "")
    except:
        pass
    return ""

def get_page_device(page):
    """Extract device from a Notion page"""
    try:
        device = page.get("properties", {}).get("Device", {})
        rich = device.get("rich_text", [])
        if rich:
            return rich[0].get("plain_text", "")
    except:
        pass
    return ""

def main():
    state = load_state()
    seen_done = set(state.get("seen_done", []))

    done_items = query_action_items_done()
    
    new_done = []
    for item in done_items:
        page_id = item["id"]
        if page_id not in seen_done:
            title = get_page_title(item)
            priority = get_page_priority(item)
            device = get_page_device(item)
            new_done.append({
                "id": page_id,
                "title": title,
                "priority": priority,
                "device": device
            })
            seen_done.add(page_id)

    if new_done:
        for task in new_done:
            device_str = f" [{task['device']}]" if task['device'] else ""
            prio_str = f" {task['priority']}" if task['priority'] else ""
            msg = f"✅ <b>Tâche complétée{device_str}</b>{prio_str}\n\n<code>{task['title']}</code>\n\n<i>Y-OS Notion Dashboard</i>"
            sent = send_telegram(msg)
            log(f"NEW DONE: {task['title']} (device={task['device']}, prio={task['priority']}) → Telegram: {sent}")

        # Save updated state
        state["seen_done"] = list(seen_done)
        state["last_check"] = datetime.now(timezone.utc).isoformat()
        save_state(state)
    else:
        # Update last check time silently
        state["last_check"] = datetime.now(timezone.utc).isoformat()
        save_state(state)

if __name__ == "__main__":
    main()
