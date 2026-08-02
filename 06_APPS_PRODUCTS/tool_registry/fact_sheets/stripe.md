# Stripe - Y-OS Tool Fact Sheet

## Overview
**Category:** Finance
**Description:** Payment processing

## Authentication & Access
**Auth Method:** `api_key`
**Endpoint:** `https://api.stripe.com/v1`
**Environment Variable:** `STRIPE_SECRET_KEY`

### 1Password Integration
**1Password Item:** `Stripe (Y-media)`
*(1Password is the Single Source of Truth for all Y-OS secrets)*

## Multi-Platform LLM Access
How this tool is accessed across different AI platforms:

| Platform | Access Method |
|----------|---------------|
| **Manus** | `custom_api + mcp_token` |
| **ChatGPT** | `api_key` |
| **Claude** | `api_key` |

## Notes
Custom API + MCP Stripe.
