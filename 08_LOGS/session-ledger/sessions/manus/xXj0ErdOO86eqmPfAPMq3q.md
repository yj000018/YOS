---
id: "xXj0ErdOO86eqmPfAPMq3q"
title: "[✓] Make Connector Authentication Testing and Setup Guidance"
date: "2026-01-04"
importance: "3"
depth_score: "standard"
projects: ["Y-OS", "Make Connector"]
tags: ["Make", "Connector", "Authentication", "Testing", "Setup", "Integration", "OAuth", "On demand scenarios"]
summary: "Testing and setting up the Make connector, troubleshooting an OAuth authentication issue, and guiding on 'On demand' scenarios."
executive_summary: "The user attempted to test the Make connector, but the assistant immediately encountered an OAuth authentication issue. The assistant identified that the connector was not authenticated and required pre-configured 'On demand' scenarios in Make. It then prompted the user for clarification on whether they needed guidance on setting up scenarios or just help with authentication."
context_and_intent: "The user wanted to test the Make connector, understand its features, see fetched data, and get a brief overview of its capabilities."
what_was_done: "The assistant attempted to use the Make connector but encountered an OAuth authentication error. It then diagnosed the problem, explained the prerequisites for the Make connector (pre-configured 'On demand' scenarios), and provided steps for the user to resolve the issue. It also asked a clarifying question to determine the user's next need."
outputs_produced: [{"description": "An explanation of the OAuth authentication issue, prerequisites for using the Make connector (on-demand scenarios), and a request for user action/clarification.", "name": "Authentication Issue Diagnosis and Setup Guidance", "type": "Textual Response"}]
key_decisions: []
lessons_learned: {"discoveries": ["The Make connector has a dependency on 'On demand' scenarios being pre-configured in the Make platform.", "Authentication issues can prevent any further interaction with the connector's features."], "failed_or_suboptimal": ["The assistant could not fulfill the user's request to test the connector or show data due to authentication and setup prerequisites.", "The initial prompt did not include enough context about the user's Make setup, leading to an immediate blocker."], "worked_well": ["The assistant quickly identified the root cause of the problem (authentication and scenario setup).", "The assistant provided clear instructions on how to resolve the issue and offered further guidance.", "The assistant asked a clarifying question to guide the next steps."]}
challenges_and_blockers: ["OAuth authentication issue with the Make connector.", "Make connector requires pre-configured 'On demand' scenarios to be set up in Make before it can be used."]
open_questions: ["Does the user have Make scenarios configured already?", "Does the user need guidance on setting up Make scenarios?", "Does the user need help specifically with authentication?"]
next_steps: ["User needs to check Make account connection in Manus settings.", "User needs to create at least one 'On demand' scenario in Make.", "User needs to respond to the assistant's clarifying question regarding scenario setup or authentication help."]
url: "https://manus.im/app/task/xXj0ErdOO86eqmPfAPMq3q"
---

# [✓] Make Connector Authentication Testing and Setup Guidance

| Field | Value |
|-------|-------|
| **Session ID** | `xXj0ErdOO86eqmPfAPMq3q` |
| **Date** | 2026-01-04 04:55 UTC |
| **Project** | — |
| **URL** | [https://manus.im/app/sessions/xXj0ErdOO86eqmPfAPMq3q](https://manus.im/app/sessions/xXj0ErdOO86eqmPfAPMq3q) |
| **Messages** | 1 user · 2 assistant · 5 total |

## Initial Prompt

Help me test the Make connector and show me how to use its feature (e.g. show any data you fetched with it). Give me a brief about its capabilities.

## First Response

I encountered an OAuth authentication issue with the Make connector. This typically means the connector needs to be authenticated first. 

Could you please check if you've:
1. Connected your Make account in the Manus settings
2. Created at least one "On demand" scenario in your Make platform

The Make connector requires pre-configured "On demand" scenarios to be set up in Make before it can be used. If you haven't set up any scenarios yet, you'll need to:
- Log into your Make account
- Create a scenario and set its trigger type to "On demand"
- Then the connector will be able to discover and run those scenarios

Would you like me to provide guidance on setting up Make scenarios, or do you already have scenarios configured and just need help with the authentication?

## Conversation Summary

> **User:** Help me test the Make connector and show me how to use its feature (e.g. show any data you fetched with it). Give me a brief about its capabilities.

> **Manus:** I encountered an OAuth authentication issue with the Make connector. This typically means the connector needs to be authenticated first. 

Could you please check if you've:
1. Connected your Make account in the Manus settings
2. Created at least one "On demand" scenario in your Make platform

The Make connector requires pre-configured "On demand" scenarios to be set up in Make before it can be used. If you haven't set up any scenarios yet, you'll need to:
- Log into your Make account
- Create a scenario and set its trigger type to "On demand"
- Then the connector will be able to discover and run those scenarios

Would you like me to provide guidance on setting up Make scenarios, or do you already have scenarios configured and just need help with the authentication?

> **Manus:** I'll help you test the Make connector and demonstrate its capabilities. Let me start by exploring the available tools through the Make MCP server.

## Full Verbatim

<details>
<summary>Expand full conversation (3 messages)</summary>

**[1767502522519] MANUS:** I encountered an OAuth authentication issue with the Make connector. This typically means the connector needs to be authenticated first. 

Could you please check if you've:
1. Connected your Make account in the Manus settings
2. Created at least one "On demand" scenario in your Make platform

The Make connector requires pre-configured "On demand" scenarios to be set up in Make before it can be used. If you haven't set up any scenarios yet, you'll need to:
- Log into your Make account
- Create a scenario and set its trigger type to "On demand"
- Then the connector will be able to discover and run those scenarios

Would you like me to provide guidance on setting up Make scenarios, or do you already have scenarios configured and just need help with the authentication?
**[1767502504447] MANUS:** I'll help you test the Make connector and demonstrate its capabilities. Let me start by exploring the available tools through the Make MCP server.
**[1767502500625] USER:** Help me test the Make connector and show me how to use its feature (e.g. show any data you fetched with it). Give me a brief about its capabilities.



</details>