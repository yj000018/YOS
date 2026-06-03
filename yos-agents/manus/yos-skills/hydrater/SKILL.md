---
name: hydrater
description: Retrieves relevant memory context from Notion (yOS Memory) and generates a standardized Context Injection Package for use in current or external sessions. Use when the user asks to "hydrater", "récupérer le contexte", "charger la mémoire", or needs background information on a project, tag, or session to continue working intelligently.
---

# Skill: Hydrater (yOS Memory Retrieval)

The **Skill “Hydrater”** is the standard yOS mechanism for retrieving and injecting relevant memory context into an active conversation, external LLM session, native app, or Manus workflow.

It is the counterpart of the "Mémoriser" skill. It allows any LLM or interface to benefit from yOS memory without owning the memory itself.

## 1. When to Use

Trigger this skill when the user says:
- "Hydrate this session with the [Project] context."
- "Hydrate with everything relevant to [Tag]."
- "Hydrate from the session about [Topic]."
- "Hydrate automatically based on the current conversation."
- "Hydrate with relevant YOUniverse context about Yannick."
- Or any variation using the word "Hydrater" or requesting context injection.

## 2. Hydration Modes

Determine the appropriate hydration mode based on the user's request or the current task complexity:

- **Light Hydration** (500–1,000 words): Quick sessions. Includes project summary, key constraints, and active goal.
- **Standard Hydration** (1,000–2,500 words): Normal working sessions. Includes project synthesis, recent relevant logs, decisions, open questions, and next recommended actions.
- **Deep Hydration** (2,500–6,000+ words): Complex work continuation. Includes project synthesis, selected session summaries, relevant raw excerpts, contradictions, and unresolved design choices.
- **Verbatim Hydration**: Precise continuation from a prior conversation. Includes full/partial verbatim, timestamp, executive summary, and continuation instructions.

## 3. Workflow

When triggered, execute these steps in order:

### Step 1: Analyze the Request and Identify Search Parameters
Determine what the user needs context for (Project, Tag, Session, or Automatic/Current Conversation).
Identify the target interface (e.g., Manus, ChatGPT native, Gemini native) to format the output appropriately.

### Step 2: Query yOS Memory (Notion)
Use the `manus-mcp-cli` with the `notion` server to search for relevant entries in the Notion Memory Repository.
Search across:
- Project Synthesis pages
- Session Logs
- Global YOUniverse profile (only if explicitly requested or highly relevant)

*Rule: Retrieve only context relevant to the current task. Avoid overloading the target LLM.*

### Step 3: Synthesize and Generate the Context Package
Read the retrieved Notion pages and extract the most relevant information based on the chosen Hydration Mode.
Format the extracted information into the standardized **yOS Context Injection Package** Markdown structure.
See `/home/ubuntu/skills/hydrater/templates/context_package.md` for the exact format.

*Rules for Generation:*
- Prefer synthesis over raw verbatim unless precision is needed (Verbatim mode).
- State confidence in retrieved relevance.
- Preserve uncertainty and clearly separate project memory from global YOUniverse memory.
- Avoid injecting private/personal data unless strictly relevant to the task.

### Step 4: Deliver the Context Package
Provide the generated Markdown context block to the user.
If the target interface is an external native app (e.g., ChatGPT native), provide it as a paste-ready code block so the user can easily copy and inject it.
If the target interface is Manus, inject the context directly into your own working memory and acknowledge the hydration.
