# ERT — Execution Routing Table

## Purpose
The Execution Routing Table (ERT) is the definitive decision matrix for Y-OS execution nodes. It dictates *where* and *how* to execute tasks based on constraints like Cloudflare blocking, required session states, hardware dependencies, and execution speed.

This document replaces ad-hoc decision-making with a deterministic routing logic.

---

## 1. Execution Nodes (The Fleet)

| Node | Environment | Best For | Limitations |
|---|---|---|---|
| **Manus Sandbox** | Ephemeral Ubuntu VM (512MB RAM) | Orchestration, LLM calling, Git operations, text processing, lightweight Python scripts | Ephemeral (data lost on restart), no persistent heavy binaries, easily blocked by Cloudflare (datacenter IP) |
| **Cloud Computer (CC)** | Persistent GCP VM (1GB RAM) | Cron jobs, background batches, headless Playwright, data pipelines (KAP) | Low RAM (OOM on heavy tasks like n8n), headless only, datacenter IP |
| **Mac Physical (Yannick)** | macOS (GUI active) | Authenticated web access (CDP), Keychain access, native Mac apps, bypassing Cloudflare | Requires Yannick to open the Mac, not 24/7 |
| **N100 Lambda** | Physical MiniPC (Ubuntu, 8-16GB RAM) | 24/7 heavy services (Docker, n8n, Home Assistant, databases) | (Pending full integration) |

---

## 2. Web Access Routing (The Hierarchy)

When a task requires accessing web data or interacting with web services, strictly follow this hierarchy:

| Priority | Method | Execution Node | Speed | When to Use |
|---|---|---|---|---|
| **1️⃣ Direct API** | `requests` / `httpx` | Sandbox or CC | ~50ms | Public APIs, documented endpoints, services with official tokens (e.g., GitHub, Raindrop). |
| **2️⃣ CDP (Chrome DevTools Protocol)** | WebSocket → `fetch()` | Mac Physical | ~100ms | Sites behind Cloudflare, services requiring complex auth (cookies/Keychain), when a real browser session is needed (e.g., ChatGPT API). |
| **3️⃣ Headless Playwright** | `playwright` (Chromium) | Cloud Computer | ~1-2s | Scraping static/light dynamic sites without strict anti-bot measures, taking screenshots. |
| **4️⃣ Headful Playwright** | `playwright` (UI rendered) | Sandbox | ~2-5s | Complex SPAs requiring visual interaction, but only if CDP is unavailable and anti-bot measures are low. |

### Why CDP is the "Holy Grail" for Protected Sites:
CDP injects JavaScript (`fetch()`) directly into the context of a real, running browser (like Brave on the Mac).
- **Bypasses Cloudflare natively**: Uses the Mac's residential IP and a genuine TLS fingerprint.
- **Accesses httpOnly cookies**: Inherits the active session (e.g., ChatGPT login) without needing to extract or decrypt cookies manually.
- **Speed**: Bypasses HTML rendering overhead, returning raw JSON payloads.

---

## 3. Specific Workarounds & Playbooks

### Scenario A: ChatGPT / OpenAI API Access
- **Constraint**: Strictly protected by Cloudflare, requires complex auth tokens stored in macOS Keychain.
- **Routing**: **Mac Physical + CDP** (or Cookie Extraction to CC).
- **Playbook**:
  1. Ensure Brave is running on the Mac.
  2. If using CDP: Launch Brave via `osascript` with `--remote-debugging-port=9222`. Connect via WebSocket from the Sandbox/CC and execute `fetch('/api/auth/session')` to get the Bearer token, then query `/backend-api/conversations`.
  3. If using Cookie Extraction: Run extraction script on Mac (via `osascript` to access Keychain), send cookies to CC, CC uses cookies to get Bearer token.

### Scenario B: Scheduled Background Tasks (Cron)
- **Constraint**: Must run autonomously, 24/7, without Yannick's intervention.
- **Routing**: **Cloud Computer (CC)**.
- **Playbook**:
  - Deploy Python scripts (e.g., `delta_manus.py`) to `/home/ubuntu/yos/ledger/`.
  - Schedule via `crontab`.
  - Output pushed directly to GitHub `yj000018/YOS`.

### Scenario C: Heavy Automation / Local Network Services
- **Constraint**: Requires high RAM, persistent database, or local network access.
- **Routing**: **N100 Lambda**.
- **Playbook**:
  - Deploy via Docker Compose (n8n, Home Assistant).

### Scenario D: Standard Web Scraping (No Anti-Bot)
- **Constraint**: Needs to render JS but isn't aggressively blocking bots.
- **Routing**: **Cloud Computer (Headless Playwright)**.
- **Playbook**:
  - Execute scripts in `/home/ubuntu/yos/playwright/`.

---

## 4. Decision Matrix Summary

*If I need to...*

*   **Call a public API (e.g., GitHub)** ➔ Sandbox (`requests`)
*   **Run a nightly sync script** ➔ CC (Cron + Python)
*   **Extract data from ChatGPT** ➔ Mac (CDP or Cookie extract) ➔ CC (Processing)
*   **Scrape a standard website** ➔ CC (Headless Playwright)
*   **Run a complex n8n workflow** ➔ N100 Lambda
*   **Render an Excalidraw diagram** ➔ CC (`build_native_excalidraw.py`)

## 5. Mac Access Protocol (Zero Friction)
When routing a task to the Mac Physical node:
1.  **Check Mount**: Is `/mnt/desktop/` available? If yes, execute directly.
2.  **Fallback SSH**: Use `sshpass -p '    ' ssh yannickjolliet@bore.pub -p 22847`.
3.  **User Prompt (Last Resort)**: Only if the above fail, ask Yannick to "Ouvre Manus Desktop sur ton Mac". Never ask him to type terminal commands.
