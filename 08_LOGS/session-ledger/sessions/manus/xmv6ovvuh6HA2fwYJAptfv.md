---
id: "xmv6ovvuh6HA2fwYJAptfv"
title: "[✓] Testing Notion Connector and Exploring Its Features"
date: "2026-02-27"
importance: "2"
depth_score: "standard"
projects: ["Y-OS", "Notion Connector"]
tags: ["notion", "connector", "testing", "integration", "api", "features", "demo"]
summary: "Successful testing and exploration of the Notion connector's core functionalities, including live data read/write operations."
executive_summary: "The session successfully tested the Notion connector, confirming its core functionalities and generating a detailed capability brief with live data demonstrations."
context_and_intent: "The user wanted to test the Notion connector, understand its features, see data fetched, and receive a brief about its capabilities."
what_was_done: "Manus AI connected to the user's Notion workspace, tested all core functionalities of the Notion connector, performed live read/write operations, and compiled a detailed capability brief with live data demonstrations. A test page was created in the user's workspace during the process."
outputs_produced: [{"description": "A document outlining the Notion connector's features, the full list of available tools, and the results of live read/write operations performed.", "name": "Capability Brief with Live Data Demonstrations", "type": "Document"}]
key_decisions: []
lessons_learned: {"discoveries": ["The Notion connector supports core functionalities including read/write operations."], "failed_or_suboptimal": [], "worked_well": ["The connection to the Notion workspace was successful.", "Core functionalities of the Notion connector were tested.", "Live read/write operations were performed and demonstrated.", "A detailed capability brief was compiled and provided."]}
challenges_and_blockers: []
open_questions: ["Does the user want the test page created in their Notion workspace to be deleted?"]
next_steps: ["The user needs to decide whether to proceed with deleting the test page created in their Notion workspace."]
url: "https://manus.im/app/task/xmv6ovvuh6HA2fwYJAptfv"
---

# [✓] Testing Notion Connector and Exploring Its Features

| Field | Value |
|-------|-------|
| **Session ID** | `xmv6ovvuh6HA2fwYJAptfv` |
| **Date** | 2026-02-27 08:27 UTC |
| **Project** | — |
| **URL** | [https://manus.im/app/sessions/xmv6ovvuh6HA2fwYJAptfv](https://manus.im/app/sessions/xmv6ovvuh6HA2fwYJAptfv) |
| **Messages** | 3 user · 4 assistant · 11 total |

## Initial Prompt

OK

## First Response

Connection to your Notion workspace is successful. I have tested all core functionalities and compiled a detailed capability brief with live data demonstrations.

The attached document outlines the connector’s features, including the full list of available tools and the results of the live read/write operations I performed.

Let me know if you want me to proceed with deleting the test page created in your workspace.

## Conversation Summary

> **User:** OK

> **User:** I

> **User:** Help me test the Notion connector and show me how to use its feature (e.g. show any data you fetched with it). Give me a brief about its capabilities.

> **Manus:** Connection to your Notion workspace is successful. I have tested all core functionalities and compiled a detailed capability brief with live data demonstrations.

The attached document outlines the connector’s features, including the full list of available tools and the results of the live read/write operations I performed.

Let me know if you want me to proceed with deleting the test page created in your workspace.

> **Manus:** Retrying live connection to Notion workspace now.

## Full Verbatim

<details>
<summary>Expand full conversation (7 messages)</summary>

**[1772182909238] MANUS:** Connection to your Notion workspace is successful. I have tested all core functionalities and compiled a detailed capability brief with live data demonstrations.

The attached document outlines the connector’s features, including the full list of available tools and the results of the live read/write operations I performed.

Let me know if you want me to proceed with deleting the test page created in your workspace.
**[1772182809645] MANUS:** Retrying live connection to Notion workspace now.
**[1772182807616] USER:** OK
**[1772182804636] USER:** I
**[1772180872957] MANUS:** The Notion MCP connector is installed and exposes **12 tools** (full list below), but the live call returned a **401 Unauthorized** — the API token stored in the MCP config is invalid or expired.

To proceed with the live data demo, I need you to reconnect the Notion integration:

1. Go to your Manus integrations settings
2. Disconnect and reconnect the Notion MCP server (this will refresh the OAuth token)
3. Let me know once done — I'll immediately re-run the live fetch

---

**Alternatively**, if you want I can show you a full capability brief now based on the tool discovery (no live data), and we run the live demo once the token is refreshed. Your call.
**[1772180839621] MANUS:** On it. I'll probe the Notion MCP connector, fetch live data from your workspace, and produce a structured capability brief.
**[1772180835529] USER:** Help me test the Notion connector and show me how to use its feature (e.g. show any data you fetched with it). Give me a brief about its capabilities.



</details>