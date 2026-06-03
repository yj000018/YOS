---
name: memoriser
description: Generates a standardized yOS Memory Package from any content (LLM session, document, image, note, link, transcript) and pushes it to the yOS Memory Inbox in Notion. Use when the user asks to "mémoriser", "sauvegarder dans yOS", "envoyer à la mémoire", or wants to preserve valuable content for the long-term memory system.
---

# Skill: Mémoriser (yOS Memory Intake)

The **Skill “Mémoriser”** is the standard yOS mechanism for pushing valuable content from any external or native interface into the **yOS Memory Inbox**.

It solves memory fragmentation by creating a standard exit path for all content, ensuring yOS (and not individual LLMs or apps) owns the memory.

## 1. When to Use

Trigger this skill when the user provides content and says:
- "Mémorise cette session"
- "Mémorise ceci dans yOS"
- "Envoie ceci à yOS Memory Inbox"
- "Fais un checkout mémoire de cette conversation"
- Or any variation indicating a desire to save content to long-term memory.

Supported content types: LLM sessions, PDFs, screenshots, images, YouTube links, web pages, voice notes, WhatsApp/Telegram exports, Figma exports, Notion/Tana notes, transcripts, or copied text.

## 2. Workflow

When triggered, execute these steps in order:

### Step 1: Analyze the Content
Read the provided content. Depending on the type:
- **Text/Session**: Extract key decisions, insights, and actions.
- **Image**: Describe it, extract visible text, identify relevant objects/diagrams, generate insights.
- **PDF**: Extract title, summarize key sections, identify document type.
- **Video/Audio**: Transcribe (if needed/possible), summarize, extract key ideas.

*Rule: Ignore irrelevant speech fragments (e.g., casual comments to pets, background noise) when explicitly identifiable.*

### Step 2: Generate the yOS Memory Package
Format the analysis into the standardized Markdown structure. See `/home/ubuntu/skills/memoriser/templates/memory_package.md` for the exact format.

*Rules for Generation:*
- Prioritize structured extraction over generic summaries.
- Preserve the raw source whenever available.
- Identify project, tags, and source type when possible.
- Mark uncertainty clearly (Confidence: Low/Medium/High).
- Never assume missing facts.
- Separate durable memory from temporary noise.

### Step 3: Push to yOS Memory Inbox (Notion)
Use the `manus-mcp-cli` with the `notion` server to create a new page in the yOS Memory Inbox database.

**Database ID:** `938332ffed1d4965849908df442bfa1c`

Map the generated package to the Notion properties:
- **Title**: A clear, concise title.
- **Status**: `Inbox`
- **Source Type**: Choose the closest match (e.g., `LLM Session`, `Text`, `Image`, `PDF`, `Link`, etc.)
- **Source App**: Choose the closest match (e.g., `Manus`, `ChatGPT`, `Web`, etc.)
- **Confidence**: `Low`, `Medium`, or `High`
- **Reinject Priority**: Assess importance (`None`, `Low`, `Medium`, `High`, `Critical`)
- **Content**: Pass the full Markdown package as the page content string.

*Command Example:*
Use the `notion-create-pages` tool via MCP. Note that the `content` field must be a string containing the full Markdown package.

### Step 4: Confirm to User
Inform the user that the content has been successfully memorized and provide a link to the Notion page if available.
