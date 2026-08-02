# Notion - Y-OS Tool Fact Sheet

## Overview
**Category:** Productivity
**Description:** Workspace, databases, pages

## Authentication & Access
**Auth Method:** `api_key`
**Endpoint:** `https://api.notion.com/v1`
**Environment Variable:** `NOTION_API_KEY`

### 1Password Integration
**1Password Item:** `Notion API Key`
*(1Password is the Single Source of Truth for all Y-OS secrets)*

## Multi-Platform LLM Access
How this tool is accessed across different AI platforms:

| Platform | Access Method |
|----------|---------------|
| **Manus** | `custom_api + mcp_token` |
| **ChatGPT** | `oauth + api_key` |
| **Claude** | `api_key` |

## Notes
Custom API + MCP Notion. ChatGPT via OAuth ou API key.
