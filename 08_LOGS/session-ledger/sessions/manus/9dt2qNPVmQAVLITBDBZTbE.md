---
session_id: 9dt2qNPVmQAVLITBDBZTbE
title: "[✓] MCP Server Configuration Guidance - Notion SSE Integration"
date: 2026-03-31 21:11 UTC
url: https://manus.im/app/sessions/9dt2qNPVmQAVLITBDBZTbE
project_id: none
user_messages: 1
assistant_messages: 2
total_messages: 5
processed: true
---

# [✓] MCP Server Configuration Guidance - Notion SSE Integration

| Field | Value |
|-------|-------|
| **Session ID** | `9dt2qNPVmQAVLITBDBZTbE` |
| **Date** | 2026-03-31 21:11 UTC |
| **Project** | — |
| **URL** | [https://manus.im/app/sessions/9dt2qNPVmQAVLITBDBZTbE](https://manus.im/app/sessions/9dt2qNPVmQAVLITBDBZTbE) |
| **Messages** | 1 user · 2 assistant · 5 total |

## Initial Prompt

add mcp https://mcp.notion.com/sse

## First Response

**MCP Server Configuration — Notion**

Adding an MCP server (`https://mcp.notion.com/sse`) must be done from the **Manus settings interface**, not from within a session. Here is the procedure:

**Steps:**

1. Go to **Manus Settings** → **MCP Servers** (or equivalent integration panel)
2. Click **Add MCP Server**
3. Enter the SSE endpoint: `https://mcp.notion.com/sse`
4. Authenticate with your Notion account when prompted
5. Save and restart the session

**Note:** The `notion` MCP server is already configured and active in your current environment (visible in the system). If you are seeing a duplicate or want to update the endpoint, you will need to remove the existing entry first via the same settings panel.

If the issue is that the current `notion` MCP is not connecting correctly, let me know and I can run a diagnostic on it directly from this session.

## Conversation Summary

> **User:** add mcp https://mcp.notion.com/sse

> **Manus:** **MCP Server Configuration — Notion**

Adding an MCP server (`https://mcp.notion.com/sse`) must be done from the **Manus settings interface**, not from within a session. Here is the procedure:

**Steps:**

1. Go to **Manus Settings** → **MCP Servers** (or equivalent integration panel)
2. Click **Add MCP Server**
3. Enter the SSE endpoint: `https://mcp.notion.com/sse`
4. Authenticate with your Notion account when prompted
5. Save and restart the session

**Note:** The `notion` MCP server is already configured and active in your current environment (visible in the system). If you are seeing a duplicate or want to update the endpoint, you will need to remove the existing entry first via the same settings panel.

If the issue is that the current `notion` MCP is not connecting correctly, let me...

> **Manus:** Noted — but adding or configuring MCP servers is outside my execution scope. MCP server configuration is managed at the platform level, not from within a session.

## Full Verbatim

<details>
<summary>Expand full conversation (3 messages)</summary>

**[1774991531237] MANUS:** **MCP Server Configuration — Notion**

Adding an MCP server (`https://mcp.notion.com/sse`) must be done from the **Manus settings interface**, not from within a session. Here is the procedure:

**Steps:**

1. Go to **Manus Settings** → **MCP Servers** (or equivalent integration panel)
2. Click **Add MCP Server**
3. Enter the SSE endpoint: `https://mcp.notion.com/sse`
4. Authenticate with your Notion account when prompted
5. Save and restart the session

**Note:** The `notion` MCP server is already configured and active in your current environment (visible in the system). If you are seeing a duplicate or want to update the endpoint, you will need to remove the existing entry first via the same settings panel.

If the issue is that the current `notion` MCP is not connecting correctly, let me know and I can run a diagnostic on it directly from this session.
**[1774991520043] MANUS:** Noted — but adding or configuring MCP servers is outside my execution scope. MCP server configuration is managed at the platform level, not from within a session.
**[1774991510146] USER:** add mcp https://mcp.notion.com/sse



</details>
