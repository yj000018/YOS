# Dropbox - Y-OS Tool Fact Sheet

## Overview
**Category:** Storage
**Description:** Cloud file storage

## Authentication & Access
**Auth Method:** `oauth`
**Endpoint:** `https://api.dropboxapi.com/2`
**Environment Variable:** `DROPBOX_ACCESS_TOKEN`

### 1Password Integration
**1Password Item:** `Dropbox`
*(1Password is the Single Source of Truth for all Y-OS secrets)*

## Multi-Platform LLM Access
How this tool is accessed across different AI platforms:

| Platform | Access Method |
|----------|---------------|
| **Manus** | `custom_api + mcp_token` |
| **ChatGPT** | `oauth` |
| **Claude** | `oauth` |

## Notes
Custom API + MCP Dropbox. OAuth principal.
