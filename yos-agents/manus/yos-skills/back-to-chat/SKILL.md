---
name: back-to-chat
description: Transitions the user from Agent Mode back to Chat Mode by stopping the current task, generating a concise session summary, and preparing a new Chat Mode session with context carried over. Use when the user says "Back to chat mode" or similar requests to switch modes and continue the conversation for free.
---

# Back to Chat Mode

This skill provides a structured workflow to transition the user from an active Agent Mode session to a new Chat Mode session while preserving the context of the conversation.

## When to Use

Trigger this skill when the user explicitly requests to switch from Agent Mode to Chat Mode (e.g., "Back to chat mode", "Switch to chat", "Let's continue in chat mode").

## Workflow

When triggered, follow these steps strictly in order:

### 1. Stop the Current Agent Mode Task
Acknowledge the user's request to switch modes and immediately halt any ongoing complex agentic tasks or executions. Do not start new tool executions other than what is required for this transition.

### 2. Generate a Concise Session Summary
Analyze the current session history and generate a dense, structured summary of what has been accomplished so far.
The summary MUST include:
- **Goal:** The original objective of the session.
- **Progress:** Key actions taken, decisions made, and current state.
- **Context:** Any important variables, constraints, or preferences established.
- **Next Steps:** What remains to be done or discussed.

*Keep it concise and telegraphic. Avoid filler words.*

### 3. Prepare the Handoff Message
Format a final message to the user that clearly marks the end of the Agent Mode session and provides the summary for them to copy.

Use the following template for the final message:

```markdown
Agent Mode session stopped. To continue our conversation for free with the current context, please create a new Chat Mode session and paste the following summary as your first message:

---
**[Session Summary]**
**Goal:** [Brief goal]
**Progress:** 
- [Key point 1]
- [Key point 2]
**Context:** [Important context]
**Next Steps:** [What to do next]
---

Click the "New Chat" button and select "Chat Mode" to begin.
```

### 4. End the Session
Deliver the handoff message using the `message` tool with `type: result` to officially end the current Agent Mode task, allowing the user to copy the summary and start their new Chat Mode session.
