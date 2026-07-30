# ChatGPT — Tool Fact Sheet
> **Last updated:** 2026-07-30 | **Status:** Validated ✅

---

## Identity

| Field | Value |
|---|---|
| **Tool** | ChatGPT (OpenAI) |
| **Account type** | Business (Team/Enterprise) |
| **Primary browser** | Brave (`~/Library/Application Support/BraveSoftware/Brave-Browser/Default/Cookies`) |
| **Base URL** | `https://chatgpt.com` |
| **API base** | `https://chatgpt.com/backend-api` |

---

## Access Pipeline (Validated 2026-07-30)

**Problem:** Cloudflare Managed Challenge blocks all direct HTTP requests from servers (TLS fingerprinting + JS challenge). Cookies expire in 30min (`__cf_bm`).

**Solution:** Extract live cookies from Brave Mac session → inject as Bearer token.

```
Brave Mac (session active)
  → Keychain macOS (via Terminal GUI / osascript — NOT SSH headless)
    → AES-128-CBC decrypt (PBKDF2 + offset 32)
      → SSH bore.pub:22847 → Cloud Computer
        → GET /api/auth/session → accessToken (Bearer)
          → GET /backend-api/conversations?offset=N&limit=100&order=updated
            → paginate until items=[]
```

**1-command execution (from Cloud Computer):**
```bash
bash /home/ubuntu/yos/tools/refresh_chatgpt_cookies.sh
```

---

## API Reference

| Endpoint | Method | Auth | Notes |
|---|---|---|---|
| `/api/auth/session` | GET | cookies | Returns `accessToken` (Bearer JWT) |
| `/backend-api/conversations` | GET | Bearer + cookies | `?offset=N&limit=100&order=updated` |
| `/backend-api/conversation/{id}` | GET | Bearer + cookies | Full conversation with messages |

---

## Lessons Learned (LL)

### ❌ Anti-patterns — Never do these

| Anti-pattern | Why |
|---|---|
| Propose native ChatGPT export | **Business account = DISABLED** — never suggest this |
| HTTP direct from server | Cloudflare 403 — TLS fingerprinting blocks all non-browser requests |
| Chrome Remote Debugging via SSH | Chrome Updater intercepts launch, port never opens |
| `security find-generic-password` via SSH | rc=36 `errSecInteractionNotAllowed` — Keychain blocked headless |
| Playwright CDP cookie injection | `__cf_bm` expires in 30min — stale by the time it's used |

### ✅ Validated patterns

| Pattern | Detail |
|---|---|
| **Keychain access** | Only via `osascript → tell application "Terminal" to do script "..."` (GUI context) |
| **AES decrypt offset** | After decryption, **skip first 32 bytes** (Chrome/Brave metadata prefix) |
| **AES parameters** | PBKDF2-HMAC-SHA1(keychain_pw, `saltysalt`, 1003, dklen=16) · IV = `b' ' * 16` |
| **session-token** | Split across cookies `.0` + `.1` → concatenate before sending |
| **Timestamps** | API returns ISO 8601 strings (`2026-07-29T21:54:43Z`), not Unix floats |
| **Pagination** | `total` can exceed 1000 — paginate with offset until `items=[]` |
| **Browser** | **Brave** (not Chrome) — different Keychain service name |

---

## Scripts (Cloud Computer — persistent)

| Script | Path | Purpose |
|---|---|---|
| Cookie extractor | `/home/ubuntu/yos/tools/extract_mac_chrome_cookies.py` | Brave + Chrome, AES decrypt, offset 32 |
| Ingestion | `/home/ubuntu/yos/ledger/ingest_chatgpt_cookies.py` | Bearer token auto, ISO timestamps, pagination |
| Pipeline master | `/home/ubuntu/yos/tools/refresh_chatgpt_cookies.sh` | End-to-end in 1 command |
| Ledger output | `/home/ubuntu/yos/data/master_ledger.csv` | 3060+ conversations |

---

## Credentials & Access

| Item | Value | Storage |
|---|---|---|
| Mac SSH | `bore.pub:22847` · user `yannickjolliet` | AGENTS.md CC |
| Mac password | 4 spaces `    ` | AGENTS.md CC (never hardcode in scripts) |
| SSH key | `~/.ssh/manus_mac` (sandbox ephemeral — regenerate each session) | Sandbox |
| Brave Keychain service | `Brave` (vs `Chrome Safe Storage` for Chrome) | macOS Keychain |

---

## Ingestion Stats

| Date | Conversations | Method |
|---|---|---|
| 2026-07-30 | 3060 | Brave cookies pipeline v1 |

---

*ChatGPT Tool Fact Sheet — yj000018/YOS · 02_AGENTS/chatgpt/*
