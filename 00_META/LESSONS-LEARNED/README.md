# Y-OS Lessons Learned Registry
> **Source of truth:** `yj000018/YOS · 00_META/LESSONS-LEARNED/`
> **Format:** One YAML file per session or domain. Index in this README.

---

## How to use

**Write a LL:**
```
00_META/LESSONS-LEARNED/YYYY-MM-DD_<topic>.yaml
```

**Find a LL (Mem0 — cross-session):**
```python
memory.search("chatgpt pipeline", user_id="yannick", limit=5)
```

**Find a LL (GitHub — structured):**
- Tool-specific → `02_AGENTS/<tool>/TOOL-FACT-SHEET.md`
- Infrastructure → `AGENTS.md` on Cloud Computer
- Cross-domain → this registry

---

## Index

| File | Date | Domain | Key topics |
|---|---|---|---|
| [2026-07-30_chatgpt-pipeline.yaml](2026-07-30_chatgpt-pipeline.yaml) | 2026-07-30 | ChatGPT API · macOS · SSH | Brave cookies, Keychain, AES decrypt, Cloudflare bypass |

---

## Dispatch Rules

| LL type | Primary destination | Secondary |
|---|---|---|
| Tool-specific (API, auth, endpoints) | `02_AGENTS/<tool>/TOOL-FACT-SHEET.md` | Mem0 + this registry |
| Infrastructure (SSH, Mac, CC) | `AGENTS.md` on Cloud Computer | Mem0 |
| Architecture / Y-OS rules | `00_META/YOS-CONSTITUTION.md` or `CANON/` | Mem0 |
| Cross-session operational | Mem0 (`memory.search()`) | This registry |

---

*LL Registry v1.0 — 2026-07-30*
