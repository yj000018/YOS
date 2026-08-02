# ERT — Execution Routing Table & Protocol

> **What it is:** A deterministic decision engine for Y-OS. For any task, the ERT tells you *which node executes it*, *which method to use*, and *what to do when the preferred path is blocked*.
>
> **How to use it:** Read the task type → follow the hierarchy → apply the relevant playbook. No improvisation.
>
> **How to maintain it:** Every new LL (Lesson Learned) that changes a routing decision MUST update this document. It is the living source of truth for execution strategy.

---

## 1. Execution Nodes

| Node | Type | Persistence | RAM | Primary Role |
|---|---|---|---|---|
| **Mac Physical** | macOS (Yannick's machine) | Permanent | 16GB+ | Authenticated web access (CDP), Keychain, native Mac apps, residential IP |
| **Cloud Computer (CC)** | GCP VM (Ubuntu) | Persistent | 1GB | Cron jobs, background pipelines, headless Playwright, data batches |
| **N100 Lambda** | Physical MiniPC (Ubuntu) | Persistent | 8-16GB | Heavy 24/7 services: Docker, n8n, Home Assistant, databases |
| **Manus Sandbox** | Ephemeral Ubuntu VM | Session-only | 512MB | Orchestration, LLM calls, Git operations, text/code generation |

---

## 2. Web Access Hierarchy (IMMUABLE)

Three methods, in strict priority order. No exceptions.

| Priority | Method | Node | Speed | When |
|---|---|---|---|---|
| **1️⃣ Direct API** | `requests` / `httpx` | Sandbox or CC | ~50ms | Public or documented API with a token (GitHub, Raindrop, Fireflies, etc.) |
| **2️⃣ CDP** | WebSocket → JS `fetch()` in live browser | **Mac Physical** | ~100ms | Cloudflare-protected sites, httpOnly cookies, active session required (ChatGPT, Claude, etc.) |
| **3️⃣ Playwright** | Browser automation (headless or headful) | CC (headless) / Sandbox (headful) | 1-5s | Last resort: no API, CDP unavailable, site not aggressively blocking bots |

### The "cookies_fresh.json" Pattern — Not a 4th Method

Storing extracted cookies in a file is a **cache optimization of CDP**, not a separate method. The flow is:

```
CDP (Mac) → extract cookies → store as cookies_fresh.json on CC → reuse for ~8h
```

**Critical limitation:** Bearer tokens from ChatGPT expire in ~8h. A stale `cookies_fresh.json` will cause silent auth failures in cron jobs. The correct approach for cron pipelines is to **re-extract cookies at runtime** via CDP before each significant batch, not to rely on a cached file.

### Why CDP is the Canonical Solution for Cloudflare

CDP injects `fetch()` directly into a live, authenticated browser (Brave on the Mac). Cloudflare sees:
- A real residential IP (Mac's network)
- A genuine TLS fingerprint (Brave's)
- Valid httpOnly session cookies (from the Keychain-loaded profile)

This is indistinguishable from a human user. It is 30-50x faster than Playwright because it bypasses HTML rendering entirely and returns raw JSON.

---

## 3. Execution Routing by Task Type

| Task | Preferred Node | Method | Fallback |
|---|---|---|---|
| Call public API (GitHub, Raindrop) | Sandbox or CC | Direct API | — |
| Extract ChatGPT conversations | Mac + CC | CDP → Bearer token → `/backend-api` | cookies_fresh.json (max 8h) |
| Nightly sync pipeline (delta_*.py) | CC (cron) | Direct API or stored cookies | Alert if auth fails |
| Scrape standard website (no Cloudflare) | CC | Headless Playwright | — |
| Interact with complex SPA (Manus, Notion) | Sandbox | Headful Playwright | — |
| Run 24/7 service (n8n, HA) | N100 Lambda | Docker | — |
| Render diagram (Excalidraw, Mermaid) | CC | Python script | Sandbox |
| Generate text/code/LLM output | Sandbox | LLM API | — |

---

## 4. Mac Access Protocol (Zero Friction)

When a task requires the Mac Physical node:

1. **Check mount first:** `cat /proc/mounts | grep desktop` → if `/mnt/desktop/` is active, act directly and silently.
2. **SSH fallback:** `ssh -i ~/.ssh/manus_mac -p 22847 yannickjolliet@bore.pub` (password: 4 spaces).
3. **User prompt (last resort only):** "Ouvre Manus Desktop sur ton Mac." Never ask Yannick to type a terminal command.

**Trigger phrase to Yannick:** "Pour cette tâche j'ai besoin du Mac ouvert (CDP / Keychain). Ouvre-le quand tu peux, je continue dès que le tunnel est actif."

---

## 5. Platform Capability Matrix

This matrix answers: *"What can I do from each platform/client?"*

| Capability | Mac Physical | Cloud Computer | N100 Lambda | Manus Sandbox | iOS/Android (web) | iOS/Android (native app) |
|---|---|---|---|---|---|---|
| **Run Python scripts** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Persistent cron jobs** | ⚠️ (sleep risk) | ✅ | ✅ | ❌ | ❌ | ❌ |
| **Keychain / credential access** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **CDP (live browser injection)** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Residential IP** | ✅ | ❌ (datacenter) | ✅ (home network) | ❌ (datacenter) | ✅ | ✅ |
| **Cloudflare bypass (native)** | ✅ | ❌ | ✅ | ❌ | ✅ | ✅ |
| **Headless Playwright** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Headful browser (real session)** | ✅ | ❌ | ❌ | ⚠️ (limited) | ✅ (web browser) | ✅ (app) |
| **Docker / heavy services** | ⚠️ (not ideal) | ❌ (OOM) | ✅ | ❌ | ❌ | ❌ |
| **File system access** | ✅ | ✅ | ✅ | ✅ (ephemeral) | ❌ | ⚠️ (sandboxed) |
| **GitHub push** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Manus API access** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **ChatGPT API (authenticated)** | ✅ (CDP) | ⚠️ (cached cookies) | ❌ | ❌ | ✅ (web session) | ✅ (app session) |

---

## 6. Maintenance Protocol

This document is a **living artifact**. Update it when:
- A new execution node is added (e.g., N100 fully integrated).
- A new workaround is validated (add to Section 3).
- A platform capability changes (e.g., Cloudflare updates anti-bot rules).
- A new LL (Lesson Learned) contradicts an existing routing decision.

**Location:** `00_META/ERT.md` in GitHub `yj000018/YOS`.
**Reference in AGENTS.md:** Règle Canon #3.
**Last updated:** 2026-08-02
