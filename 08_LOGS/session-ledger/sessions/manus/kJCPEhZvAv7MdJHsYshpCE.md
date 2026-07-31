---
id: "kJCPEhZvAv7MdJHsYshpCE"
title: "[✓] Manus to Notion Session Export PoC - Multi-mode Export System"
date: "2026-03-16"
importance: "3"
depth_score: "standard"
projects: ["Manus", "Notion", "Manus to Notion Exporter"]
tags: ["PoC", "Export System", "Multi-mode Export", "Verbatim"]
summary: ""
executive_summary: "A Proof of Concept (PoC) for a Manus to Notion Session Exporter has been successfully completed. The full-stack application features a server-side API proxy, Swiss Blueprint UI, and three distinct export modes: Verbatim, Synthesis (AI-powered summary), and Project Pages (auto-clustering and aggregation). The system passed 10 unit tests and is TypeScript error-free, ready for use with specified API keys."
context_and_intent: "The intent was to build a Proof of Concept (PoC) module to export Manus AI sessions to Notion. This PoC aimed to support multi-mode exports: verbatim, synthetic summaries, and aggregated project pages for related sessions."
what_was_done: "A full-stack application was built to export Manus sessions to Notion. This included developing server-side API proxies to handle CORS, implementing a Swiss Blueprint UI, and creating three distinct export modes: Verbatim (raw transcript), Synthesis (AI-generated summary using Gemini for key points, todos, decisions, and challenges), and Project Pages (auto-clustering of related sessions into a single aggregated Notion page). The development included 10 unit tests, all of which passed, and the codebase was free of TypeScript errors."
outputs_produced: [{"description": "A full-stack application designed to export Manus AI sessions to Notion, featuring a server-side API proxy, Swiss Blueprint UI, and three export modes.", "name": "Manus → Notion Session Exporter", "type": "Full-stack application"}, {"description": "An export mode that transfers the full session transcript, message by message, without any AI processing.", "name": "Verbatim Export Mode", "type": "Feature"}, {"description": "An export mode that uses Gemini AI to extract and summarize key points, todos, decisions, and challenges from sessions.", "name": "Synthesis Export Mode", "type": "Feature"}, {"description": "An export mode that automatically clusters related sessions and creates a single Notion page with an aggregation/summary of these sessions.", "name": "Project Pages Export Mode", "type": "Feature"}]
key_decisions: ["Implement three distinct export modes: Verbatim, Synthesis, and Project Pages.", "Utilize Gemini for AI-powered synthesis.", "Develop a full-stack application with server-side API proxies to handle CORS."]
lessons_learned: {"discoveries": ["Successfully implemented a full-stack application with server-side API proxies to avoid CORS issues.", "Developed three distinct and functional export modes catering to different user needs.", "Demonstrated the feasibility of integrating Manus sessions with Notion using AI for summarization and aggregation."], "failed_or_suboptimal": [], "worked_well": ["The PoC was completed successfully, delivering a functional application.", "All 10 unit tests passed, indicating robust code.", "No TypeScript errors were encountered, ensuring type safety and maintainability."]}
challenges_and_blockers: []
open_questions: []
next_steps: ["Provide Manus API Key from manus.im → Settings → API Keys", "Provide Notion Token from notion.so/my-integrations → your integration", "Provide Gemini API Key from aistudio.google.com"]
url: "https://manus.im/app/task/kJCPEhZvAv7MdJHsYshpCE"
---

# [✓] Manus to Notion Session Export PoC - Multi-mode Export System

| Field | Value |
|-------|-------|
| **Session ID** | `kJCPEhZvAv7MdJHsYshpCE` |
| **Date** | 2026-03-16 01:30 UTC |
| **Project** | — |
| **URL** | [https://manus.im/app/sessions/kJCPEhZvAv7MdJHsYshpCE](https://manus.im/app/sessions/kJCPEhZvAv7MdJHsYshpCE) |
| **Messages** | 7 user · 15 assistant · 37 total |

## Initial Prompt

Build module to export sessions from manus to Notion
Mini PoC to select sessions and have them exported
- as verbatim
- as a synthetic summary with key points and todo decision challenges etc
- identify common sessions to a project and create a Peojext Page with aggregation / summary of the different related sesisons

## First Response

**Manus → Notion Session Exporter — PoC complete.**

Full-stack app with server-side API proxies (no CORS), Swiss Blueprint UI, and three export modes. 10 unit tests passing, no TypeScript errors.

**To use it:**

| Credential | Where to get it |
|---|---|
| Manus API Key | manus.im → Settings → API Keys |
| Notion Token | notion.so/my-integrations → your integration → copy `secret_...` |
| Notion DB ID | Pre-filled: `211da186743d4521b1f1e05eb9c93321` |
| Gemini API Key | aistudio.google.com → Get API key (free tier sufficient) |

**Three export modes:**
- **Verbatim** — full transcript, every message, no AI
- **Synthesis** — Gemini extracts key points, todos, decisions, challenges
- **Project Pages** — auto-clusters related sessions, creates one aggregated Notion page per project with links to individual sessions

**Next steps to consider:**
1. **Scheduled export** — add a cron trigger to auto-export new completed sessions daily to Notion without manual intervention
2. **Tag/label ses

## Conversation Summary

> **User:** Build module to export sessions from manus to Notion
Mini PoC to select sessions and have them exported
- as verbatim
- as a synthetic summary with key points and todo decision challenges etc
- identify common sessions to a project and create a Peojext Page with aggregation / summary of the different related sesisons

> **User:** Do 1 for me

> **User:** Notion integration token?

> **Manus:** **Manus → Notion Session Exporter — PoC complete.**

Full-stack app with server-side API proxies (no CORS), Swiss Blueprint UI, and three export modes. 10 unit tests passing, no TypeScript errors.

**To use it:**

| Credential | Where to get it |
|---|---|
| Manus API Key | manus.im → Settings → API Keys |
| Notion Token | notion.so/my-integrations → your integration → copy `secret_...` |
| Notion DB ID | Pre-filled: `211da186743d4521b1f1e05eb9c93321` |
| Gemini API Key | aistudio.google.com → Get API key (free tier sufficient) |

**Three export modes:**
- **Verbatim** — full transcript, every message, no AI
- **Synthesis** — Gemini extracts key points, todos, decisions, challenges
- **Project Pages** — auto-clusters related sessions, creates one aggregated Notion page per project with lin...

> **Manus:** Server running, no TypeScript errors. Writing unit tests now, then saving checkpoint.

## Full Verbatim

<details>
<summary>Expand full conversation (22 messages)</summary>

**[1773626298826] MANUS:** **Manus → Notion Session Exporter — PoC complete.**

Full-stack app with server-side API proxies (no CORS), Swiss Blueprint UI, and three export modes. 10 unit tests passing, no TypeScript errors.

**To use it:**

| Credential | Where to get it |
|---|---|
| Manus API Key | manus.im → Settings → API Keys |
| Notion Token | notion.so/my-integrations → your integration → copy `secret_...` |
| Notion DB ID | Pre-filled: `211da186743d4521b1f1e05eb9c93321` |
| Gemini API Key | aistudio.google.com → Get API key (free tier sufficient) |

**Three export modes:**
- **Verbatim** — full transcript, every message, no AI
- **Synthesis** — Gemini extracts key points, todos, decisions, challenges
- **Project Pages** — auto-clusters related sessions, creates one aggregated Notion page per project with links to individual sessions

**Next steps to consider:**
1. **Scheduled export** — add a cron trigger to auto-export new completed sessions daily to Notion without manual intervention
2. **Tag/label ses...
**[1773626187422] MANUS:** Server running, no TypeScript errors. Writing unit tests now, then saving checkpoint.
**[1773626021898] MANUS:** App is live and rendering correctly. Now adding the CORS proxy layer for the Manus API (browser can't call it directly), then polishing and saving checkpoint.
**[1773625745116] MANUS:** Design chosen: **Architectural Blueprint** — Swiss/Constructivist grid. Off-white base, deep navy structure, electric indigo accent. IBM Plex Sans + Mono. Asymmetric 3-column layout: credentials rail | session grid | export drawer. Building now.
**[1773625692024] MANUS:** Solid scope. Building the PoC now. Let me plan the full module before executing.
**[1773625687060] USER:** Build module to export sessions from manus to Notion
Mini PoC to select sessions and have them exported
- as verbatim
- as a synthetic summary with key points and todo decision challenges etc
- identify common sessions to a project and create a Peojext Page with aggregation / summary of the different related sesisons
**[1773624942160] MANUS:** Notion sent a verification code to **yannick.jolliet@gmail.com**. Please share the code so I can complete the login and retrieve the integration token.
**[1773624907990] MANUS:** Navigating to notion.so/my-integrations to find the Notion MCP token.
**[1773624903927] USER:** Do 1 for me
**[1773624850050] MANUS:** The Notion integration token used by this MCP connection is an internal credential managed by the Manus platform — it is not exposed to me programmatically, so I cannot retrieve or display it directly.

**Two options to get your token:**

**Option 1 — Use the existing Manus MCP integration token**
Go to: `https://www.notion.so/my-integrations` → find the integration named **"Notion MCP"** → click it → copy the **Internal Integration Token** (starts with `secret_...`).

**Option 2 — Create a dedicated integration for the export app**
1. Go to `https://www.notion.so/my-integrations`
2. Click **"New integration"**
3. Name it (e.g., `Manus Export`)
4. Select your workspace
5. Submit → copy the token (`secret_...`)
6. Then share the **Manus Tasks Export** database with it: open the DB in Notion → **...** menu → **Connections** → add your integration

Option 2 is cleaner — dedicated token, scoped only to this database.
**[1773624841882] USER:** Notion integration token?
**[1773624799488] MANUS:** Here is everything you need to proceed with the batch export app:

---

## Notion Database — "Manus Tasks Export"

| Field | Value |
|---|---|
| **Database URL** | https://www.notion.so/211da186743d4521b1f1e05eb9c93321 |
| **Database ID** | `211da186-743d-4521-b1f1-e05eb9c93321` |
| **Data Source ID** | `549b9299-700d-4461-af6d-20e96b1621b6` |

## Schema Confirmed

| Property | Type | Options |
|---|---|---|
| **Name** | Title | — |
| **Status** | Select | completed (green), pending (yellow), running (blue), failed (red) |
| **Created** | Date | — |
| **Manus ID** | Rich Text | — |

---

## What's done

1. **Database created** — all 4 properties match the app spec exactly.
2. **Integration access** — the database was created via the Notion MCP integration, which already has full read/write access to it. No additional sharing step needed.

## What you still need to do manually

3. **Manus API key** — the Manus dashboard requires a logged-in session. Navigate to: `https://manus.im` → Set...
**[1773624787925] USER:** Db id
**[1773624781030] MANUS:** Your message seems incomplete — "D. If" was cut off. Could you complete it? What would you like me to do?
**[1773624778332] USER:** D. If
**[1773624744796] MANUS:** The Notion MCP does not expose a direct "share with integration" tool — sharing is managed via the Notion UI or Notion API directly. The database was created via the Notion MCP integration which already has access to it (it created it). Now navigating to the Manus dashboard to retrieve the API key.
**[1773624726262] MANUS:** Database confirmed. Now sharing with the Notion MCP integration (bot ID: 30135e21-8cf8-811e-ac0e-0027bd8d4b62) and navigating to the Manus dashboard for the API key.
**[1773624701757] MANUS:** Database created. Extracting DB ID and proceeding to share with integration + fetch Manus API key.
**[1773624666918] MANUS:** Understood. Executing all 3 steps: create Notion DB with correct properties, share it with your integration, and retrieve your Manus API key. Starting now.
**[1773624664208] USER:** Do this for me

Create a Notion database with properties: Name (title), Status (select), Created (date), and Manus ID (rich text)
2.	Share that database with your Notion integration
3.	Get your Manus API key from the Manus dashboard
**[1773624642717] MANUS:** Got it. Building the interactive batch export app — Manus tasks → Notion. Let me plan and execute.
**[1773624639139] USER:** Do this for me as asked
I've created an interactive app to export batch chats from Manus to Notion. The app features:

**Setup Section:**
- Manus API key input (get from Manus Settings → API Keys)
- Notion integration token input (create at notion.so/my-integrations)
- Notion database ID input (from your database URL)

**Fetch Options:**
- Configurable number of tasks to fetch (1-100)
- Status filter (all, completed, pending, running, failed)
- Fetches tasks from Manus API v1

**Task Selection:**
- Displays all fetched tasks with titles, status, creation date, and IDs
- Checkboxes to select which tasks to export
- Select All / Deselect All buttons for convenience

**Export Process:**
- Batch exports selected tasks to your Notion database
- Progress bar showing export status
- Creates Notion pages with: Name, Status, Created date, and Manus ID properties

**Note:** Before using this app, you'll need to:
1. Create a Notion database with properties: Name (title), Status (select), Created ...



</details>