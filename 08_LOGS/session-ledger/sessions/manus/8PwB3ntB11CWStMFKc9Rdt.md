---
id: "8PwB3ntB11CWStMFKc9Rdt"
title: "[✓] Testing Hugging Face Connector and 3D AI Model Comparison"
date: "2026-01-02"
importance: "3"
depth_score: "standard"
projects: ["Y-OS"]
tags: ["hugging face", "3d", "ai", "generative ai", "model comparison", "connector", "testing"]
summary: ""
executive_summary: "The session aimed to test the Hugging Face connector and compare 3D AI models. Due to connectivity issues with Hugging Face Spaces, the assistant provided direct links to popular 3D generation models (Microsoft TRELLIS, Tencent Hunyuan3D-2) and pre-uploaded the user's image to a CDN for direct use as a workaround."
context_and_intent: "The user inquired about available 3D AI models from Hugging Face, likely for generating a 3D model from an image (implied 'castle image'). The session also served to test the Hugging Face connector."
what_was_done: "The assistant identified connectivity issues with Hugging Face Spaces, uploaded the user's image to a CDN, and provided direct links to two popular 3D generation models (Microsoft TRELLIS and Tencent Hunyuan3D-2) on Hugging Face, along with instructions and the CDN image URL for each."
outputs_produced: [{"description": "Direct link to the Microsoft TRELLIS 3D generation model on Hugging Face Spaces.", "name": "Microsoft TRELLIS Hugging Face Space Link", "type": "URL"}, {"description": "Direct link to the Tencent Hunyuan3D-2 3D generation model on Hugging Face Spaces.", "name": "Tencent Hunyuan3D-2 Hugging Face Space Link", "type": "URL"}, {"description": "CDN link for the user's uploaded castle image, to be used with the 3D generation models.", "name": "User Image on CDN", "type": "URL"}]
key_decisions: ["The assistant decided to bypass the direct connector issues by providing manual links to Hugging Face Spaces.", "The assistant pre-uploaded the user's image to a CDN to facilitate direct use with the external models."]
lessons_learned: {"discoveries": ["Hugging Face Spaces, especially popular ones, can experience heavy load, leading to connectivity issues and timeouts."], "failed_or_suboptimal": ["The direct Hugging Face connector or integration failed to function as intended due to external service connectivity problems."], "worked_well": ["Providing direct links to external services and pre-uploading user assets to a CDN proved to be an effective workaround for external service connectivity issues.", "The assistant quickly identified the problem and offered a practical, actionable solution."]}
challenges_and_blockers: ["Hugging Face Spaces experienced connectivity issues and timeouts.", "Popular 3D generation services on Hugging Face were under heavy load."]
open_questions: ["Was the 'castle image' explicitly provided by the user in a prior, unshown prompt, or was it inferred by the assistant?"]
next_steps: ["The user needs to manually visit the provided Hugging Face Space links and generate the 3D models using the CDN image URL.", "Further investigation into the robustness and error handling of the Hugging Face connector might be beneficial."]
url: "https://manus.im/app/task/8PwB3ntB11CWStMFKc9Rdt"
---

# [✓] Testing Hugging Face Connector and 3D AI Model Comparison

| Field | Value |
|-------|-------|
| **Session ID** | `8PwB3ntB11CWStMFKc9Rdt` |
| **Date** | 2026-01-02 05:49 UTC |
| **Project** | — |
| **URL** | [https://manus.im/app/sessions/8PwB3ntB11CWStMFKc9Rdt](https://manus.im/app/sessions/8PwB3ntB11CWStMFKc9Rdt) |
| **Messages** | 4 user · 9 assistant · 21 total |

## Initial Prompt

Is available models from hugging face

## First Response

I apologize for the difficulties. The Hugging Face Spaces are experiencing connectivity issues and timeouts. This is a common problem when these popular 3D generation services are under heavy load.

Let me provide you with a comprehensive solution:

## **Direct Access Links to Generate Your Castle 3D Model:**

I've uploaded your castle image to a CDN. Here are the direct links to the top 3 models where you can generate the 3D models yourself:

### **1. Microsoft TRELLIS (Most Popular - 19.2M downloads)**
- **Link:** https://huggingface.co/spaces/trellis-community/TRELLIS
- **Your image URL:** https://files.manuscdn.com/user_upload_by_module/session_file/310419663032381833/eyokpwlMSDKKXqpm.png
- **Instructions:** Upload the image, adjust settings if needed, and click generate

### **2. Tencent Hunyuan3D-2 (High Quality - 2.7M downloads)**  
- **Link:** https://huggingface.co/spaces/tencent/Hunyuan3D-2
- **Your image URL:** https://files.manuscdn.com/user_upload_by_module/session_file/31

## Conversation Summary

> **User:** Is available models from hugging face

> **User:** Create 3d model of the  castle shown on photo. Select 3 top most appellate mmodels and generate 3 3d outputs I can visualise here

> **User:** Compare best ai models for 3d

> **Manus:** I apologize for the difficulties. The Hugging Face Spaces are experiencing connectivity issues and timeouts. This is a common problem when these popular 3D generation services are under heavy load.

Let me provide you with a comprehensive solution:

## **Direct Access Links to Generate Your Castle 3D Model:**

I've uploaded your castle image to a CDN. Here are the direct links to the top 3 models where you can generate the 3D models yourself:

### **1. Microsoft TRELLIS (Most Popular - 19.2M downloads)**
- **Link:** https://huggingface.co/spaces/trellis-community/TRELLIS
- **Your image URL:** https://files.manuscdn.com/user_upload_by_module/session_file/310419663032381833/eyokpwlMSDKKXqpm.png
- **Instructions:** Upload the image, adjust settings if needed, and click generate

### **2. Tenc...

> **Manus:** I'm experiencing timeout issues connecting to the Hugging Face Spaces. The spaces appear to be experiencing high load or connectivity issues. Let me try a different approach - I'll attempt to use the Hunyuan3D model and also try the Microsoft TRELLIS space.

## Full Verbatim

<details>
<summary>Expand full conversation (13 messages)</summary>

**[1767336164717] MANUS:** I apologize for the difficulties. The Hugging Face Spaces are experiencing connectivity issues and timeouts. This is a common problem when these popular 3D generation services are under heavy load.

Let me provide you with a comprehensive solution:

## **Direct Access Links to Generate Your Castle 3D Model:**

I've uploaded your castle image to a CDN. Here are the direct links to the top 3 models where you can generate the 3D models yourself:

### **1. Microsoft TRELLIS (Most Popular - 19.2M downloads)**
- **Link:** https://huggingface.co/spaces/trellis-community/TRELLIS
- **Your image URL:** https://files.manuscdn.com/user_upload_by_module/session_file/310419663032381833/eyokpwlMSDKKXqpm.png
- **Instructions:** Upload the image, adjust settings if needed, and click generate

### **2. Tencent Hunyuan3D-2 (High Quality - 2.7M downloads)**  
- **Link:** https://huggingface.co/spaces/tencent/Hunyuan3D-2
- **Your image URL:** https://files.manuscdn.com/user_upload_by_module/session_file/31...
**[1767336086503] MANUS:** I'm experiencing timeout issues connecting to the Hugging Face Spaces. The spaces appear to be experiencing high load or connectivity issues. Let me try a different approach - I'll attempt to use the Hunyuan3D model and also try the Microsoft TRELLIS space.
**[1767335969744] MANUS:** Yes! The Hugging Face models are available. Let me check if I can use the Hugging Face Spaces through the MCP connector or access them programmatically. I'll try to generate 3D models using the available Hugging Face infrastructure.
**[1767335965691] USER:** Is available models from hugging face
**[1767335858639] MANUS:** I understand you want to generate 3D models using the top AI models. However, I'm facing some challenges:

1. **Browser access issues**: The web-based interfaces are not loading properly
2. **API limitations**: These advanced 3D generation models typically require specialized API keys or cloud infrastructure that I don't currently have access to
3. **Local installation**: Installing these models locally would require significant GPU resources and dependencies

**Alternative solutions I can offer:**

1. **Guide you to use the tools yourself**: I can provide you with direct links and instructions to use these tools:
   - TRELLIS: https://huggingface.co/spaces/trellis-community/TRELLIS
   - Hunyuan3D-2: https://huggingface.co/spaces/tencent/Hunyuan3D-2
   - VGGT: https://huggingface.co/spaces/facebook/vggt

2. **Use simpler 3D reconstruction**: I could try using basic photogrammetry or depth estimation techniques, though the quality won't match the specialized models

3. **Provide a compa...
**[1767335824359] MANUS:** I apologize, but I'm encountering technical difficulties accessing the browser-based 3D generation tools. Let me try an alternative approach by using Python libraries to access these models programmatically. I'll install and use the available 3D generation tools directly.
**[1767335789893] MANUS:** I'll help you create 3D models of the Château d'Annecy using the top 3 image-to-3D models. Based on my research, the best models for this task are:

1. **Microsoft TRELLIS** - 19.2M downloads, excellent for high-quality 3D asset generation
2. **Tencent Hunyuan3D-2** - 2.7M downloads, great for detailed textured 3D assets
3. **Facebook VGGT-1B** - 2.5M downloads, specialized in scene reconstruction

Let me generate 3D models using these three models.
**[1767335784054] USER:** Create 3d model of the  castle shown on photo. Select 3 top most appellate mmodels and generate 3 3d outputs I can visualise here
**[1767335591370] MANUS:** I'll help you compare the best AI models for 3D generation. Let me search for the latest 3D AI models on Hugging Face and gather information about their capabilities.
**[1767335588426] USER:** Compare best ai models for 3d
**[1767333090270] MANUS:** I have completed the demonstration of the Hugging Face connector. The attached report provides a comprehensive overview of its capabilities, along with practical examples of how to use its various features. I hope this helps you in your future projects!
**[1767332992569] MANUS:** I'll help you test the Hugging Face connector and demonstrate its capabilities. Let me start by exploring the available tools and then show you practical examples of how to use them.
**[1767332990607] USER:** Help me test the Hugging Face connector and show me how to use its feature (e.g. show any data you fetched with it). Give me a brief about its capabilities.



</details>