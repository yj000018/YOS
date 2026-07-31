---
session_id: FeZeM7gpLl0uYBklTXrV0n
title: "[✓] Wrike MCP Connector OAuth Authentication Troubleshooting"
date: 2026-01-06 00:10 UTC
url: https://manus.im/app/sessions/FeZeM7gpLl0uYBklTXrV0n
project_id: none
user_messages: 2
assistant_messages: 6
total_messages: 15
processed: true
---

# [✓] Wrike MCP Connector OAuth Authentication Troubleshooting

| Field | Value |
|-------|-------|
| **Session ID** | `FeZeM7gpLl0uYBklTXrV0n` |
| **Date** | 2026-01-06 00:10 UTC |
| **Project** | — |
| **URL** | [https://manus.im/app/sessions/FeZeM7gpLl0uYBklTXrV0n](https://manus.im/app/sessions/FeZeM7gpLl0uYBklTXrV0n) |
| **Messages** | 2 user · 6 assistant · 15 total |

## Initial Prompt

Id yCKmO4Ib
Secret key rW8rI08jJsxbZvwCrXrgW2OYa5HXb8SfnQdKqyhaX8wPl4MQmTYnxOPauNW2KABs

## First Response

I'm consistently getting a 401 Unauthorized error when trying to connect to the Wrike MCP server. This indicates that the OAuth authentication is not properly configured or the token has not been authorized yet.

Based on what I can see from your screenshots and the error, here's what's happening:

**The Issue:**
The Wrike MCP connector is configured to use OAuth 2.0 authentication, but the OAuth flow hasn't been completed successfully. The connector is trying to authenticate but receiving a 401 error from Wrike's API.

**What needs to happen:**
The MCP connector needs to complete an OAuth authorization flow where:
1. You authorize the app in your browser
2. Wrike redirects back to the configured redirect URL
3. The MCP system exchanges the authorization code for an access token

**Possible solutions:**

1. **Check the redirect URL**: The redirect URL in your Wrike app is set to `http://localhost`. The MCP system might need a specific redirect URL to complete the OAuth flow. You may ne

## Conversation Summary

> **User:** Id yCKmO4Ib
Secret key rW8rI08jJsxbZvwCrXrgW2OYa5HXb8SfnQdKqyhaX8wPl4MQmTYnxOPauNW2KABs

> **User:** Help me test the Wrike connector and show me how to use its feature (e.g. show any data you fetched with it). Give me a brief about its capabilities.

> **Manus:** I'm consistently getting a 401 Unauthorized error when trying to connect to the Wrike MCP server. This indicates that the OAuth authentication is not properly configured or the token has not been authorized yet.

Based on what I can see from your screenshots and the error, here's what's happening:

**The Issue:**
The Wrike MCP connector is configured to use OAuth 2.0 authentication, but the OAuth flow hasn't been completed successfully. The connector is trying to authenticate but receiving a 401 error from Wrike's API.

**What needs to happen:**
The MCP connector needs to complete an OAuth authorization flow where:
1. You authorize the app in your browser
2. Wrike redirects back to the configured redirect URL
3. The MCP system exchanges the authorization code for an access token

**Possibl...

> **Manus:** Perfect! I can see you've set up a Wrike App API with OAuth credentials and also have a permanent access token available. The MCP connector is likely configured to use OAuth, but since you have a permanent access token, that might be an alternative approach.

However, looking at the screenshots, I notice the OAuth setup requires a redirect URL (currently set to `http://localhost`). The MCP connector needs a specific redirect URL to complete the OAuth flow.

Let me check if there's a way to configure the MCP connector to use the permanent access token instead, or if we need to adjust the OAuth settings. Let me try one more approach to see if the connector can be accessed now.

## Full Verbatim

<details>
<summary>Expand full conversation (8 messages)</summary>

**[1767658492559] MANUS:** I'm consistently getting a 401 Unauthorized error when trying to connect to the Wrike MCP server. This indicates that the OAuth authentication is not properly configured or the token has not been authorized yet.

Based on what I can see from your screenshots and the error, here's what's happening:

**The Issue:**
The Wrike MCP connector is configured to use OAuth 2.0 authentication, but the OAuth flow hasn't been completed successfully. The connector is trying to authenticate but receiving a 401 error from Wrike's API.

**What needs to happen:**
The MCP connector needs to complete an OAuth authorization flow where:
1. You authorize the app in your browser
2. Wrike redirects back to the configured redirect URL
3. The MCP system exchanges the authorization code for an access token

**Possible solutions:**

1. **Check the redirect URL**: The redirect URL in your Wrike app is set to `http://localhost`. The MCP system might need a specific redirect URL to complete the OAuth flow. You may ne...
**[1767658456162] MANUS:** Perfect! I can see you've set up a Wrike App API with OAuth credentials and also have a permanent access token available. The MCP connector is likely configured to use OAuth, but since you have a permanent access token, that might be an alternative approach.

However, looking at the screenshots, I notice the OAuth setup requires a redirect URL (currently set to `http://localhost`). The MCP connector needs a specific redirect URL to complete the OAuth flow.

Let me check if there's a way to configure the MCP connector to use the permanent access token instead, or if we need to adjust the OAuth settings. Let me try one more approach to see if the connector can be accessed now.
**[1767658331050] MANUS:** I'm still getting an OAuth authentication error (401 Unauthorized). The credentials you provided (Client ID and Secret Key) appear to be Wrike API credentials, but the MCP connector configuration needs to be set up differently.

The Wrike MCP server requires OAuth to be configured at the MCP server level. This typically involves:

1. **Adding the OAuth credentials to your MCP configuration file** where the Wrike server is defined
2. **Going through an OAuth authorization flow** in your browser to grant access

Could you check your MCP configuration for the Wrike server? The configuration should include the client ID and secret key you provided. If you need help setting this up, you may need to:

- Update your MCP settings/configuration file with these OAuth credentials
- Restart the MCP connection
- Complete any browser-based authorization if prompted

Alternatively, if there's a way for you to re-authorize or refresh the Wrike MCP connection in your MCP settings interface, that might ...
**[1767658319247] MANUS:** Thank you for providing the credentials! However, I should clarify that the Wrike MCP connector uses OAuth authentication, which is typically configured through the MCP server settings rather than through direct API credentials.

The OAuth flow should be handled automatically by the MCP system when I attempt to use the connector. Let me try accessing the Wrike connector again - it may trigger the OAuth authentication process automatically.
**[1767658315114] USER:** Id yCKmO4Ib
Secret key rW8rI08jJsxbZvwCrXrgW2OYa5HXb8SfnQdKqyhaX8wPl4MQmTYnxOPauNW2KABs
**[1767658221460] MANUS:** It looks like the Wrike MCP connector requires OAuth authentication. The authentication needs to be completed before I can access your Wrike workspace. 

Could you please check if you've completed the OAuth authorization for the Wrike connector in your MCP settings? You may need to:

1. Go to your MCP server configuration
2. Find the Wrike connector
3. Complete the OAuth authorization flow

Once the authorization is complete, I'll be able to test the connector and show you its capabilities. Would you like to authorize it now, or have you already done so?
**[1767658206535] MANUS:** I'll help you test the Wrike MCP connector and demonstrate its capabilities. Let me start by exploring the available tools and then fetch some data from your Wrike workspace.
**[1767658202987] USER:** Help me test the Wrike connector and show me how to use its feature (e.g. show any data you fetched with it). Give me a brief about its capabilities.



</details>
