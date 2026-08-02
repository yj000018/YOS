# GitHub - Y-OS Tool Fact Sheet

## Overview
**Category:** Dev
**Description:** Code hosting, CI/CD, PRs

## Authentication & Access
**Auth Method:** `api_key`
**Endpoint:** `https://api.github.com`
**Environment Variable:** `GITHUB_PAT`

### 1Password Integration
**1Password Item:** `GitHub PAT — yOS-GITHUB-MCP-2026-03`
*(1Password is the Single Source of Truth for all Y-OS secrets)*

## Multi-Platform LLM Access
How this tool is accessed across different AI platforms:

| Platform | Access Method |
|----------|---------------|
| **Manus** | `custom_api_editable + builtin` |
| **ChatGPT** | `oauth` |
| **Claude** | `api_key` |

## Notes
Custom API editable + builtin OAuth.
