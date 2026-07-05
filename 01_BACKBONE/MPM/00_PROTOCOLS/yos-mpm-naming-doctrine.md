# yOS MPM — Naming Doctrine

> KAP Runtime Pack — Canonical Naming Reference
> Version: 1.1.0 — Patch: DOCTRINE-PATCH-2026-07-04 — Patch: YOS-MPM-NAMING-PATCH-2026-07-04
> JSON source of truth: `mpm-frontmatter-schema.json`

---

## 1. Canonical System Name

| Level | Value |
| :--- | :--- |
| **System name** | `yOS MPM` |
| **Full name** | `yOS MPM — Mega Prompt Manager` |
| **Technical description** | Inter-LLM Prompt Runtime & Relay System |
| **Deprecated label** | ~~KAP Inter-LLM Prompt Runtime~~ (technical description only, not primary name) |

**Canonical definition:**

> yOS MPM is the Mega Prompt Manager: the yOS subsystem that creates, stores, routes, executes, tracks, and reviews Mega Prompts across Manus, ChatGPT, Claude, Gemini, Perplexity, and other LLMs.

---

## 2. Packet Code Table

| Packet Code | Full Name | Target LLM | Primary Use |
| :--- | :--- | :--- | :--- |
| `MP` | Mega Prompt (generic) | Generic / unspecified | Fallback or abstract Mega Prompt |
| `MPM` | Mega Prompt Manus | Manus | Execution, Git/files, long-run, multi-thread |
| `MPC` | Mega Prompt Claude | Claude | Deep critique, writing, long analysis |
| `MPX` | Mega Prompt ChatGPT | ChatGPT | Architecture, Architect & Guardian review, prompt generation |
| `MPG` | Mega Prompt Gemini | Gemini | Google/multimodal/large-context work |
| `MPP` | Mega Prompt Perplexity | Perplexity | Web research and cited external research |

**Deprecated:**

| Deprecated Code | Replacement |
| :--- | :--- |
| ~~`MPA` (Mega Prompt Any)~~ | `MP` (Mega Prompt generic) |

`MPA` must not be used going forward unless explicitly marked as `DEPRECATED_LEGACY`.

---

## 3. Disambiguation Rule

The term "MPM" is intentionally ambiguous at two levels:

| Context | Meaning |
| :--- | :--- |
| `yOS MPM` | The **global system** — Mega Prompt Manager |
| `MPM` (packet code) | A **Manus-specific packet** — Mega Prompt Manus |

When ambiguity is possible, use:
- `yOS MPM system` — to refer to the global system
- `MPM/Manus packet` — to refer to the Manus-specific packet type

---

## 4. Adapter File Naming Convention

| Packet Code | Adapter File | Legacy Alias |
| :--- | :--- | :--- |
| `MPM` | `mpm-manus-adapter.md` | `mpm-manus-fetch-and-run-protocol.md` (kept) |
| `MPC` | `mpc-claude-adapter.md` | `mpm-claude-adapter.md` (kept as alias) |
| `MPX` | `mpx-chatgpt-adapter.md` | `mpm-chatgpt-guardian-review-protocol.md` (kept as alias) |
| `MPG` | `mpg-gemini-adapter.md` | — |
| `MPP` | `mpp-perplexity-adapter.md` | — |
| `MP` | `mp-generic-adapter.md` | `mpm-generic-llm-adapter.md` (kept as alias) |

Legacy adapter files are preserved. New canonical files are the primary reference.

---

## 5. JSON-First Rule (Preserved)

> JSON = canonical machine source
> MD = generated human-readable view

Never manually edit MD views as source of truth. Update JSON first, then regenerate or patch the MD view.
