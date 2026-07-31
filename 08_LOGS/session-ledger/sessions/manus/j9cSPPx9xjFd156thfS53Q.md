---
id: "j9cSPPx9xjFd156thfS53Q"
title: "[✓] Testing Instagram Creator Marketplace Connector and Features"
date: "2026-03-18"
importance: "3"
depth_score: "standard"
projects: ["Y-OS", "Instagram Creator Marketplace Connector"]
tags: ["instagram", "creator marketplace", "connector", "api integration", "testing", "meta"]
summary: ""
executive_summary: "The session aimed to test the Instagram Creator Marketplace connector. The assistant explored its available tools (listing pages and searching for creators) but was unable to fetch live creator data due to the absence of a linked Instagram Business Account. Despite this, the assistant successfully extracted the full schema and capabilities of the connector and provided a detailed capability brief."
context_and_intent: "The user wanted to test the Instagram Creator Marketplace connector, understand its features, see fetched data, and get a brief about its capabilities."
what_was_done: "The assistant explored the Meta Creators (Instagram Creator Marketplace) MCP connector, testing both the listing pages and searching for creators tools. It attempted to fetch live data but was blocked by account configuration issues. It then extracted the full schema and capabilities of the connector and compiled a detailed capability brief."
outputs_produced: [{"description": "A detailed brief outlining how the Meta Creators (Instagram Creator Marketplace) tools work, the extensive filtering options available (demographics, follower counts, interests, lookalikes), and the required implementation protocol.", "name": "Capability Brief", "type": "document"}]
key_decisions: []
lessons_learned: {"discoveries": ["Successfully extracted the full schema and capabilities of the Meta Creators (Instagram Creator Marketplace) connector.", "Compiled a structured capability brief detailing how the tools work, the extensive filtering options available (demographics, follower counts, interests, lookalikes), and the required implementation protocol."], "failed_or_suboptimal": ["Could not fetch live creator data due to the absence of an active Instagram Business Account linked to a Facebook Page.", "Bypassing the 'page_id' requirement for the search tool was not possible."], "worked_well": ["Explored both available tools: listing pages and searching for creators.", "Successfully extracted and documented the connector's schema and capabilities."]}
challenges_and_blockers: ["The current Meta account does not have an active Instagram Business Account linked to a Facebook Page, which is a strict requirement for fetching live creator data (the API returned 'No pages found').", "Attempting to bypass the requirement by querying the search tool directly was unsuccessful as Meta enforces the 'page_id' requirement."]
open_questions: []
next_steps: ["Link an active Instagram Business Account to a Facebook Page to enable fetching live creator data."]
url: "https://manus.im/app/task/j9cSPPx9xjFd156thfS53Q"
---

# [✓] Testing Instagram Creator Marketplace Connector and Features

| Field | Value |
|-------|-------|
| **Session ID** | `j9cSPPx9xjFd156thfS53Q` |
| **Date** | 2026-03-18 18:42 UTC |
| **Project** | — |
| **URL** | [https://manus.im/app/sessions/j9cSPPx9xjFd156thfS53Q](https://manus.im/app/sessions/j9cSPPx9xjFd156thfS53Q) |
| **Messages** | 1 user · 4 assistant · 7 total |

## Initial Prompt

Help me test the Instagram Creator Marketplace connector and show me how to use its feature (e.g. show any data you fetched with it). Give me a brief about its capabilities.

## First Response

I have explored the Meta Creators (Instagram Creator Marketplace) MCP connector. I tested both available tools: listing pages and searching for creators. 

During the live test, I found that the current Meta account does not have an active Instagram Business Account linked to a Facebook Page, which is a strict requirement for fetching live creator data (the API returns `No pages found`). I attempted to bypass this by querying the search tool directly, but Meta enforces the `page_id` requirement.

However, I successfully extracted the full schema and capabilities of the connector. I have compiled a structured capability brief detailing how the tools work, the extensive filtering options available (demographics, follower counts, interests, lookalikes), and the required implementation protocol.

Please find the detailed capability brief attached. Let me know if you'd like to link an account and try again, or if you need anything else!

## Conversation Summary

> **User:** Help me test the Instagram Creator Marketplace connector and show me how to use its feature (e.g. show any data you fetched with it). Give me a brief about its capabilities.

> **Manus:** I have explored the Meta Creators (Instagram Creator Marketplace) MCP connector. I tested both available tools: listing pages and searching for creators. 

During the live test, I found that the current Meta account does not have an active Instagram Business Account linked to a Facebook Page, which is a strict requirement for fetching live creator data (the API returns `No pages found`). I attempted to bypass this by querying the search tool directly, but Meta enforces the `page_id` requirement.

However, I successfully extracted the full schema and capabilities of the connector. I have compiled a structured capability brief detailing how the tools work, the extensive filtering options available (demographics, follower counts, interests, lookalikes), and the required implementation protoco...

> **Manus:** The `list_pages` call confirmed: no Instagram Business Account is linked to the connected Meta session — so `page_id` cannot be resolved dynamically. The `meta_creators_instagram_search` tool requires a valid `page_id` from a linked IG Business Account to execute. I'll now document the full test results and compile the capability brief based on the live schema introspection and API responses obtained.

## Full Verbatim

<details>
<summary>Expand full conversation (5 messages)</summary>

**[1773859445353] MANUS:** I have explored the Meta Creators (Instagram Creator Marketplace) MCP connector. I tested both available tools: listing pages and searching for creators. 

During the live test, I found that the current Meta account does not have an active Instagram Business Account linked to a Facebook Page, which is a strict requirement for fetching live creator data (the API returns `No pages found`). I attempted to bypass this by querying the search tool directly, but Meta enforces the `page_id` requirement.

However, I successfully extracted the full schema and capabilities of the connector. I have compiled a structured capability brief detailing how the tools work, the extensive filtering options available (demographics, follower counts, interests, lookalikes), and the required implementation protocol.

Please find the detailed capability brief attached. Let me know if you'd like to link an account and try again, or if you need anything else!
**[1773859405895] MANUS:** The `list_pages` call confirmed: no Instagram Business Account is linked to the connected Meta session — so `page_id` cannot be resolved dynamically. The `meta_creators_instagram_search` tool requires a valid `page_id` from a linked IG Business Account to execute. I'll now document the full test results and compile the capability brief based on the live schema introspection and API responses obtained.
**[1773859362811] MANUS:** No Instagram Business Account is linked to the connected Meta account — so `list_pages` returns empty. I'll now run the creator search tool with a broad query to test it independently, using a placeholder page_id (required field) to probe the API response structure.
**[1773859339614] MANUS:** On it. I'll explore the Instagram Creator Marketplace MCP connector, list its available tools, run live queries, and compile a structured capability brief with real fetched data.
**[1773859325880] USER:** Help me test the Instagram Creator Marketplace connector and show me how to use its feature (e.g. show any data you fetched with it). Give me a brief about its capabilities.



</details>