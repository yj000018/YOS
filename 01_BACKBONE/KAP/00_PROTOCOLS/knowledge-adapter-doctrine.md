# Knowledge Adapter Doctrine

> **Module:** KAP — Knowledge Absorption Pipeline
> **Gate:** MPM-20260705-YOS-KAP-KNOWLEDGE-ADAPTER-CENSUS-AND-PROBE-GATE
> **Version:** v1.0.0
> **Status:** ACTIVE

---

## Article I — The Core Separation

```
KAP does not speak to LLMs.
KAP does not speak to provider brands.
KAP does not speak to consumer applications.

KAP speaks to Knowledge Adapters.
Knowledge Adapters speak to provider APIs, workspaces, repositories, memories, files, and research systems.
```

This separation is immutable. It ensures KAP remains provider-agnostic and survives API changes, provider migrations, and tool deprecations.

---

## Article II — The Adapter Contract

Every Knowledge Adapter MUST implement the canonical adapter contract (see `knowledge-adapter-contract.md`). No adapter may be used by KAP without a contract-compliant implementation or stub.

---

## Article III — Runtime Classification

All environments are classified by runtime type:

| Class | Definition | Examples |
|---|---|---|
| **Class A — API Runtime** | Programmatic access via authenticated API | OpenAI API, Anthropic API, Notion API, Mem0 API |
| **Class B — Workspace Runtime** | File system, CLI, or embedded runtime access | Manus workspace, Claude Code, Git repo, Google Drive export |
| **Class C — Consumer UI** | Human-operated browser/app interface | ChatGPT App, Claude.ai, Gemini App |

**Class C is descriptive only.** KAP architecture MUST prefer Class A and B. Class C adapters may be documented for completeness but MUST NOT be used as primary production adapters.

---

## Article IV — Adapter Taxonomy

KAP recognizes seven canonical adapter types:

| Type | Purpose | Examples |
|---|---|---|
| **Conversation Adapter** | Capture LLM sessions and message history | OpenAI API, Anthropic API, Gemini API |
| **Workspace Adapter** | Access file systems, CLIs, and embedded runtimes | Manus workspace, Claude Code, Codex runtime |
| **Research Adapter** | Retrieve research results, citations, evidence | Perplexity API, xAI API |
| **Repository Adapter** | Access version-controlled code and documents | Git (GitHub, GitLab), any VCS |
| **Memory Adapter** | Read/write persistent cross-session memory stores | Mem0, future memory backends |
| **File Adapter** | Access document stores, exports, and file corpora | Google Drive, local export corpus |
| **Evidence Adapter** | Retrieve structured evidence and citations | Perplexity (dual role), research APIs |

An adapter MAY implement multiple types (e.g., Perplexity = Research + Evidence).

---

## Article V — The Four Capture Modes

Every adapter MUST be evaluated against four capture modes:

| Mode | Definition |
|---|---|
| **Historical Backfill** | Retrieve past sessions/records up to a cursor or date |
| **Continuous Capture** | Detect and capture new sessions/records as they occur |
| **Checkpointing** | Save progress cursor to enable resume after interruption |
| **Finalization** | Detect and mark a session/record as complete and immutable |

An adapter that cannot support a mode MUST declare it `unsupported` — never silently skip it.

---

## Article VI — The History Distinction

Every adapter MUST explicitly distinguish between:

```
provider_api_history     — what the provider API exposes (may be limited)
consumer_app_history     — what the consumer app shows (may exceed API)
workspace_history        — what exists in a workspace/filesystem
exported_history         — what has been manually exported
```

**Never imply that API access automatically includes consumer app history.**

Example: OpenAI API exposes only conversations created via API. ChatGPT App conversations are NOT accessible via OpenAI API.

---

## Article VII — Trigger Signal Priority

When detecting new sessions or deltas, prefer signals in this order:

```
1. native message event (webhook/push)
2. native completion/archive event
3. API polling cursor
4. filesystem watcher
5. scheduled delta import
6. manual finalize marker
```

**Best available signal wins.**

---

## Article VIII — Finalization Signals

Accepted finalization signals (in order of reliability):

```
1. native completion event (most reliable)
2. explicit SESSION_FINALIZE event
3. workspace marker file
4. task completion signal
5. commit marker in repository
6. idle timeout (least reliable — use with caution)
7. full export import
8. manual finalize (always available as fallback)
```

---

## Article IX — Amendment

This doctrine may be amended only by a marathon gate with `guardian_required: true`. Sprint and run gates may not amend Articles I–VIII.
