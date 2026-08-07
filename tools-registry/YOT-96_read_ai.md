---
tool_id: YOT-96
tool_name: "Read AI"
tool_type: "MCP Connector"
category: "Meeting Intelligence"
status: "Production"
pricing: "Paid"
source_type: "Officiel"
source_url: "https://www.read.ai/"
auth_credentials: "OAuth MCP"
tags: ["meeting", "transcription", "summary", "intelligence"]
created_date: "2026-08-07"
---
# 🟢 YOT-96 — Read AI
| Champ | Valeur |
| :--- | :--- |
| **Type** | MCP Connector |
| **Catégorie** | Meeting Intelligence |
| **Statut** | Production |
| **Pricing** | Paid |
| **Source** | Officiel |
| **Auth** | OAuth MCP |
| **URL** | https://www.read.ai/ |
## Business Value
Read AI provides automated meeting intelligence by capturing transcripts, generating summaries, and extracting actionable insights across various meeting platforms. It enhances team productivity by ensuring no critical information or action item is lost during discussions.
## Capabilities
- Search meeting history and metadata
- Retrieve full meeting transcripts with speaker identification
- Extract action items and key questions
- Access meeting recording download links
- Fetch chapter summaries
## Dependencies
- Read AI account with appropriate subscription plan
- OAuth authentication via MCP
- Integration with meeting platforms (Zoom, Teams, Meet, etc.)
## Known Limits & Bugs
- Meeting IDs must use the ULID format for retrieval.
- Transcription accuracy may vary depending on audio quality and speaker accents.
- Processing time for summaries and action items may take a few minutes after the meeting ends.
## Workarounds & Lessons
- Always verify the ULID format when querying specific meetings to avoid retrieval errors.
- For long meetings, rely on chapter summaries to quickly navigate to relevant sections before downloading the full transcript.
