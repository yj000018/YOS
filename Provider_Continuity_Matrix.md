# Provider Continuity Matrix

**Mission:** CCV-001  
**Date:** 2026-06-13  
**Status:** Draft

## Objective
Assess the context continuity capabilities of major LLM providers to determine their suitability for Y-OS workers.

## Assessment Matrix

| Provider | Conversation Reuse | API Persistence | Context Window | Memory Support | Lock-in Risk | Y-OS Suitability |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **OpenAI** (GPT-4o) | Threads via Assistants API | High (stateful threads) | 128k | Vector store integration | High | High for complex, multi-step tasks. Stateful threads reduce context pack overhead but increase lock-in. |
| **Anthropic** (Claude 3.5) | Stateless API (requires full history send) | Low (stateless) | 200k | Prompt caching | Low | Very High. Large context window and prompt caching make it ideal for injecting large Y-OS Context Packs statelessly. |
| **Google** (Gemini 1.5) | Stateless API | Low (stateless) | 1M - 2M | Context caching | Low | High for tasks requiring massive context (e.g., reading entire Y-OS codebase or massive artifacts). |
| **Manus** (Internal) | Agentic sessions | Medium | Variable | Internal workspace | Medium | High for execution and orchestration. |
| **Local / OS** (Llama 3, etc.) | Stateless | Low | 8k - 128k | None built-in | None | Medium. Good for simple, privacy-sensitive tasks, but context window limits full Context Pack injection. |

## Analysis & Cost Implications

1. **Stateful vs. Stateless:** OpenAI's Assistants API offers stateful threads, reducing the need to resend the Context Pack every time. However, this creates vendor lock-in. Anthropic and Gemini are stateless, requiring the full Context Pack per invocation, but prompt/context caching significantly reduces costs and latency for repeated context.
2. **Context Window:** Y-OS Context Packs (Canonical + Mission + Artifact) will grow. Claude's 200k and Gemini's 1M+ windows are critical for ensuring no context is truncated.
3. **Recommendation for Y-OS:** Y-OS must remain provider-agnostic. Therefore, Y-OS must rely on **stateless Context Packs** injected into every fresh session. Prompt caching (Anthropic/Gemini) should be utilized to mitigate costs, rather than relying on stateful APIs (OpenAI Threads) which violate the principle that the Artifact Registry is the sole source of truth.
