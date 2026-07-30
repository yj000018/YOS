---
session_id: 7y07A8G6RtivnjGw8VEeEV
title: "[✓] Where to Define Secrets in Manus Environment"
date: 2026-01-06 00:43 UTC
url: https://manus.im/app/sessions/7y07A8G6RtivnjGw8VEeEV
project_id: none
user_messages: 9
assistant_messages: 12
total_messages: 37
processed: true
---

# [✓] Where to Define Secrets in Manus Environment

| Field | Value |
|-------|-------|
| **Session ID** | `7y07A8G6RtivnjGw8VEeEV` |
| **Date** | 2026-01-06 00:43 UTC |
| **Project** | — |
| **URL** | [https://manus.im/app/sessions/7y07A8G6RtivnjGw8VEeEV](https://manus.im/app/sessions/7y07A8G6RtivnjGw8VEeEV) |
| **Messages** | 9 user · 12 assistant · 37 total |

## Initial Prompt

echo $openai_api_key

## First Response

✅ **Result:**

```
[REDACTED:api-key]
```

Your OpenAI API key is available and ready to use!

## Conversation Summary

> **User:** echo $openai_api_key

> **User:** echo $USERNAME

> **User:** Y

> **Manus:** ✅ **Result:**

```
[REDACTED:api-key]
```

Your OpenAI API key is available and ready to use!

> **Manus:** I'll execute that command for you now.

## Full Verbatim

<details>
<summary>Expand full conversation (21 messages)</summary>

**[1767660665956] MANUS:** ✅ **Result:**

```
[REDACTED:api-key]
```

Your OpenAI API key is available and ready to use!
**[1767660663336] MANUS:** I'll execute that command for you now.
**[1767660662224] USER:** echo $openai_api_key
**[1767660650878] MANUS:** ✅ **Result:**

```
Yannick Jolliet
```

Your USERNAME secret is active and working correctly!
**[1767660648234] MANUS:** I'll execute that command for you now.
**[1767660646651] USER:** echo $USERNAME
**[1767660627929] MANUS:** ✅ **Success!** Your USERNAME secret has been set up.

**What was done:**
- Executed: `export USERNAME="Yannick Jolliet"`
- Verified: The environment variable is now accessible and contains the correct value

**How to use it:**

You can now access this secret in your code and commands:

```bash
# In shell commands
echo $USERNAME
# Output: Yannick Jolliet

# In Python
import os
username = os.getenv('USERNAME')
print(username)  # Output: Yannick Jolliet
```

**Important Note:**
This environment variable is set for the current shell session. If you need it to persist across multiple sessions or scripts, I can create a `.env` file or a configuration file that loads automatically. Just let me know!
**[1767660613784] MANUS:** Understood! I'll execute the command now.
**[1767660612759] USER:** Y
**[1767660570010] MANUS:** Great question! Based on the Manus platform architecture, here's how you can access terminal/shell functionality:

**Direct Shell Access:**

You don't have a traditional terminal window in the web interface itself. Instead, the Manus platform is designed so that **I (the AI agent) execute shell commands on your behalf** using the shell tool.

**How it works:**

1. **You tell me what you want to do** (e.g., "export USERNAME='Yannick Jolliet'")
2. **I execute it in the sandbox** using my shell tool
3. **You get the results back**

**Example:**

If you want to run `export USERNAME="Yannick Jolliet"`, just ask me and I'll do it immediately. For instance:

- "Set the USERNAME environment variable to Yannick Jolliet"
- "Run: export USERNAME='Yannick Jolliet'"
- "Execute this command: [your command here]"

**For this specific request:**

Would you like me to now execute `export USERNAME="Yannick Jolliet"` in the sandbox? I can do that right away, and then verify it's set correctly by checking...
**[1767660566063] USER:** How to access to a terminal/shell interface in the Manus web platform
**[1767660564422] MANUS:** Perfect! I'll set up the USERNAME secret for you now.
**[1767660562497] USER:** export USERNAME="Yannick Jolliet"
**[1767660506490] MANUS:** Good question! The `export USERNAME="Yannick Jolliet"` command is a **shell/terminal command**, not something you enter in the web interface.

**Where to enter it:**

You have two options:

**Option 1: Through Me (Recommended)**
Simply tell me to set it up, and I'll execute the command in the sandbox shell for you. For example, you could say:
- "Set up the USERNAME secret as Yannick Jolliet"
- "Create a .env file with my secrets"

I can then use the shell tool to execute these commands and make the secret available for your tasks.

**Option 2: Direct Shell Access**
If you have direct access to a terminal/shell interface in the Manus web platform, you could paste the command there. However, this depends on whether your Manus interface provides a terminal/shell window.

**What I recommend:**

Since you're asking, let me set this up for you right now. Would you like me to:

1. **Set USERNAME as an environment variable** (temporary, for this session only)
2. **Create a `.env` file** with y...
**[1767660502620] USER:** Where in the web interfsce do I enter
export USERNAME="Yannick Jolliet"
**[1767660416502] MANUS:** You're absolutely right! The two existing secrets (OpenAI and OpenRouter) were pre-configured at the platform level before your session started. Since you cannot share your secrets with the Manus help team, here's how you can define and use new secrets **locally within your sandbox session**:

**Option 1: Set as Environment Variables (Temporary)**

```bash
export USERNAME="Yannick Jolliet"
```

Then access it in your code:
```bash
echo $USERNAME
```

**Option 2: Store in a Local Configuration File (Persistent)**

Create a `.env` file in your project directory:

```bash
USERNAME=Yannick Jolliet
API_KEY_SECRET=your_secret_value
ANOTHER_SECRET=another_value
```

Then load it in Python:
```python
from dotenv import load_dotenv
import os

load_dotenv()
username = os.getenv('USERNAME')
```

**Option 3: Create a Secure Config File**

```bash
# Create a config file with restricted permissions
cat > ~/.secrets.conf << 'EOF'
USERNAME=Yannick Jolliet
SECRET_API_KEY=your_secret_value
EOF

chmod 60...
**[1767660412410] USER:** My secrets are secrets, cant inform manus help team... 2 secrets (openai, openrouter) have been defined, so how ??
**[1767660358138] MANUS:** I appreciate you wanting to define a new secret, but I need to clarify the process:

**Current Limitation:**
I cannot directly define or add new secrets to your Manus environment. Secrets and API credentials are managed at the platform level and must be configured through the official Manus support channel.

**How to Add New Secrets:**

To define new secrets like your username, please submit a request at **https://help.manus.im** with the following information:

- **Secret Name:** UserName
- **Secret Value:** Yannick Jolliet
- **Service/Purpose:** (Brief description of what this secret will be used for)

The Manus support team will securely add this to your environment configuration, and it will then be available as an environment variable (e.g., `$USERNAME` or similar) in your sandbox.

**Alternatively, for this session:**

If you need to use this value immediately within this task, I can store it in a local file or environment variable within the sandbox. Would you like me to:

1. Cr...
**[1767660353313] USER:** Define new secret: UserName = Yannick Jolliet
**[1767660243320] MANUS:** Based on the system configuration, secrets and environment variables for accessing external services are pre-configured and available in your sandbox environment. Here's how they work:

**Available Secrets:**

Currently, two services have pre-configured API keys available as environment variables:

1. **OpenRouter** (`OPENROUTER_API_KEY`)
   - For unified access to a wide range of AI models
   - Main endpoint: `https://openrouter.ai/api/v1/chat/completions`
   - Supports OpenAI-compatible schemas

2. **OpenAI** (`OPENAI_API_KEY`)
   - Access to OpenAI and third-party LLMs via OpenAI-compatible API
   - Pre-configured for direct use with the OpenAI Python client

**How to Use Secrets:**

You can access these environment variables directly in your code or shell commands:

```bash
# In shell commands
echo $OPENROUTER_API_KEY
echo $OPENAI_API_KEY

# In Python
import os
api_key = os.getenv('OPENROUTER_API_KEY')
```

**Important Notes:**

- These secrets are automatically injected into the s...
**[1767660236895] USER:** Where to define secrets



</details>
