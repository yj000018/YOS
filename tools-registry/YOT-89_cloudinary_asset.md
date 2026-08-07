---
tool_id: YOT-89
tool_name: "Cloudinary Asset"
tool_type: "MCP Connector"
category: "Media Asset Management"
status: "Production"
pricing: "Freemium"
source_type: "Officiel"
source_url: "https://cloudinary.com/documentation"
auth_credentials: "OAuth MCP"
tags: ["media", "assets", "images", "video", "cloudinary"]
created_date: "2026-08-07"
---
# 🟢 YOT-89 — Cloudinary Asset
| Champ | Valeur |
| :--- | :--- |
| **Type** | MCP Connector |
| **Catégorie** | Media Asset Management |
| **Statut** | Production |
| **Pricing** | Freemium |
| **Source** | Officiel |
| **Auth** | OAuth MCP |
| **URL** | https://cloudinary.com/documentation |
## Business Value
Cloudinary Asset provides robust media management capabilities to the Y-OS ecosystem, enabling seamless uploading, transformation, and organization of images and videos. It accelerates content delivery and optimizes media workflows directly from the agentic environment.
## Capabilities
- Upload images, videos, and raw files to Cloudinary.
- Apply on-the-fly transformations (resizing, cropping, format conversion).
- Search and retrieve media assets using advanced querying.
- Organize assets with tags and folders.
## Dependencies
- Cloudinary account (Freemium or paid).
- OAuth MCP authentication configured in Y-OS.
## Known Limits & Bugs
- Free tier has limits on storage, bandwidth, and monthly transformations.
- Large video uploads may require chunking or hit timeout limits depending on the network.
## Workarounds & Lessons
- Always specify transformation parameters during retrieval to save bandwidth and processing time.
- Use tags consistently during upload to ensure assets are easily searchable later.
