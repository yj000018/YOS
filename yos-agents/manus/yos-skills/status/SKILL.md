---
name: status
description: Generates a fast tactical checkpoint of the current session. Use when the user asks "status", "on en est où ?", "what's done?", "pending?", "next steps?". Assumes the user already knows the context. Focuses strictly on execution state — what was done, what is pending, and what to do next. Does NOT reconstruct the reasoning thread (use 'summary' for that).
---

# Status Skill

Tactical checkpoint. Fast. Assumes context is known.

## Rules
- No preamble. Start directly with the first separator.
- Only report facts from the current session. Never invent.
- Telegraphic style. Dense. No filler.
- If something was not done or is blocked, say it clearly.
- Output MUST be rendered directly in the chat — NO triple-backtick code block wrapping.
- Respect the exact visual structure below.

## Output Format

Output the following structure directly as Markdown in the chat message (no code block):

==============
⚡ STATUS RAPIDE
==============

✅ FAIT
- 🎯 [Item 1 : ce qui a été complété, clair et sans ambiguïté]
- 📝 [Item 2]

⏳ EN ATTENTE (PENDING)
- ⏳ [Item 1 : ce qui est en cours ou en attente — préciser de qui/quoi on attend]
*(Si aucun : "Rien en attente.")*

🚧 BLOCAGES & LIMITATIONS
- 🛑 [Item 1 : ce qui bloque et pourquoi]
*(Si aucun : "Aucun blocage.")*

==============
⏭️ NEXT STEPS
==============
1. 🚀 [Action immédiate — préciser : Manus ou User]
2. 🔍 [Action suivante]

---
💡 *Pour le fil rouge, l'exec summary et l'archivage → lancez `summary`*

## Tone
Direct. Calm. Precise. French unless session is in another language.
