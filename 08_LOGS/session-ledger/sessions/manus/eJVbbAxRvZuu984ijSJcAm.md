---
session_id: eJVbbAxRvZuu984ijSJcAm
title: "[✓] n8n Multilingual Message Translation Workflow Creation"
date: 2025-06-28 15:13 UTC
url: https://manus.im/app/sessions/eJVbbAxRvZuu984ijSJcAm
project_id: none
user_messages: 5
assistant_messages: 6
total_messages: 39
processed: true
---

# [✓] n8n Multilingual Message Translation Workflow Creation

| Field | Value |
|-------|-------|
| **Session ID** | `eJVbbAxRvZuu984ijSJcAm` |
| **Date** | 2025-06-28 15:13 UTC |
| **Project** | — |
| **URL** | [https://manus.im/app/sessions/eJVbbAxRvZuu984ijSJcAm](https://manus.im/app/sessions/eJVbbAxRvZuu984ijSJcAm) |
| **Messages** | 5 user · 6 assistant · 39 total |

## Initial Prompt

So make this JSON file that I can simply copy-paste into n8n and I will copy-paste and just make the links to the right tools and run it it should be completely operational as it is look if it's not difficult with WhatsApp, do it with Telegram if you can do both it's even better

## First Response

🎉 Your n8n translation workflow is complete and ready to use! I've created a comprehensive solution that handles both WhatsApp and Telegram messages with dual translation (DeepL + OpenAI) for optimal accuracy.

**What you're getting:**
✅ Complete n8n workflow JSON file (ready to copy-paste)
✅ Detailed setup guide with step-by-step instructions
✅ Validation confirmed - all 18 nodes and connections are properly configured
✅ Supports both WhatsApp and Telegram
✅ Intelligent language detection and complexity assessment
✅ Dual translation approach (DeepL + AI) with optimized combination
✅ Professional response formatting with original message context

The workflow will only translate messages that are:
1. Not in French or English
2. Complex enough to warrant translation (based on your language skills)

Simply import the JSON, configure your API credentials, and you're ready to go!

## Conversation Summary

> **User:** So make this JSON file that I can simply copy-paste into n8n and I will copy-paste and just make the links to the right tools and run it it should be completely operational as it is look if it's not difficult with WhatsApp, do it with Telegram if you can do both it's even better

> **User:** And then you deliver this translation together with the original text and the sender and date, time it was sent to my WhatsApp account or directly to the discussion group if it was coming from a group, but being clear that this is an automatic translation of the message above that everybody can understand what it is.

> **User:** The translation phase should use DeepL or any AI LLM tool, you choose what is the most appropriate explaining why, and in case of doubt or pros and cons of both approaches you make two branches and you translate by both tools, one LLM, open AI or another one, one DeepL, and then if you translate it twice then you combine both translations into one summary aggregated, meaningful, optimised translation, taking into account these two.

> **Manus:** 🎉 Your n8n translation workflow is complete and ready to use! I've created a comprehensive solution that handles both WhatsApp and Telegram messages with dual translation (DeepL + OpenAI) for optimal accuracy.

**What you're getting:**
✅ Complete n8n workflow JSON file (ready to copy-paste)
✅ Detailed setup guide with step-by-step instructions
✅ Validation confirmed - all 18 nodes and connections are properly configured
✅ Supports both WhatsApp and Telegram
✅ Intelligent language detection and complexity assessment
✅ Dual translation approach (DeepL + AI) with optimized combination
✅ Professional response formatting with original message context

The workflow will only translate messages that are:
1. Not in French or English
2. Complex enough to warrant translation (based on your language ...

> **Manus:** Understood! I'll create a complete, ready-to-use n8n workflow JSON file that you can simply copy-paste and configure. I'll include both WhatsApp and Telegram triggers so you have maximum flexibility. The workflow will be fully operational once you add your API credentials.

## Full Verbatim

<details>
<summary>Expand full conversation (11 messages)</summary>

**[1751124028922] MANUS:** 🎉 Your n8n translation workflow is complete and ready to use! I've created a comprehensive solution that handles both WhatsApp and Telegram messages with dual translation (DeepL + OpenAI) for optimal accuracy.

**What you're getting:**
✅ Complete n8n workflow JSON file (ready to copy-paste)
✅ Detailed setup guide with step-by-step instructions
✅ Validation confirmed - all 18 nodes and connections are properly configured
✅ Supports both WhatsApp and Telegram
✅ Intelligent language detection and complexity assessment
✅ Dual translation approach (DeepL + AI) with optimized combination
✅ Professional response formatting with original message context

The workflow will only translate messages that are:
1. Not in French or English
2. Complex enough to warrant translation (based on your language skills)

Simply import the JSON, configure your API credentials, and you're ready to go!
**[1751123881901] MANUS:** Understood! I'll create a complete, ready-to-use n8n workflow JSON file that you can simply copy-paste and configure. I'll include both WhatsApp and Telegram triggers so you have maximum flexibility. The workflow will be fully operational once you add your API credentials.
**[1751123877586] USER:** So make this JSON file that I can simply copy-paste into n8n and I will copy-paste and just make the links to the right tools and run it it should be completely operational as it is look if it's not difficult with WhatsApp, do it with Telegram if you can do both it's even better
**[1751123849835] MANUS:** Perfect! I'll add the delivery mechanism to send the translation back to the original chat (whether individual or group) with clear formatting that includes the original message, sender info, timestamp, and a clear indication that it's an automatic translation. This will make it transparent and useful for everyone in the conversation.
**[1751123845757] USER:** And then you deliver this translation together with the original text and the sender and date, time it was sent to my WhatsApp account or directly to the discussion group if it was coming from a group, but being clear that this is an automatic translation of the message above that everybody can understand what it is.
**[1751123825835] MANUS:** Excellent suggestion! I'll implement a dual translation approach using both DeepL and OpenAI, then combine them into an optimized final translation. This will provide the best accuracy by leveraging DeepL's specialized translation capabilities and OpenAI's contextual understanding. Let me update the workflow design accordingly.
**[1751123821694] USER:** The translation phase should use DeepL or any AI LLM tool, you choose what is the most appropriate explaining why, and in case of doubt or pros and cons of both approaches you make two branches and you translate by both tools, one LLM, open AI or another one, one DeepL, and then if you translate it twice then you combine both translations into one summary aggregated, meaningful, optimised translation, taking into account these two.
**[1751123765849] MANUS:** Perfect! I understand the additional requirement. The workflow should assess if the message is understandable even with basic language skills (like simple vocabulary, short phrases, or context from previous messages) and only proceed with translation if it's truly complex or unclear. I'll incorporate this logic into the workflow.
**[1751123761636] USER:** so if it's very understandable by me with my basic command of Italian medium command and my extremely basic command of German but no other languages I know then if it's understandable because it's short it's simple it's reusing the vocabulary of the previous text message then do not translate and stop the workflow here and do nothing otherwise move on with the workflow to the translation phase
**[1751123603560] MANUS:** Understood, I will create the n8n workflow for you.
**[1751123597037] USER:** I want to have an n8n workflow that you create automatically, give me the JSON file completely validated and without any error and all dependencies and links correctly set up to achieve the following whenever I receive a WhatsApp message or a Telegram message, check the language of the message using AI or any other system, but I think AI is good, and if the language is not French or not English, it's any other language, then proceed with the translation workflow. The first assessment of the workflow is to check whether the message is obvious and anyone can understand its signification, even me, with very basic comment of the language. If it's just a kind of a yes, okay, I'm late, absolutely agree with you, or a short sentence which is part.



</details>
