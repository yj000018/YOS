# Notion Artifact Registry — Schema Reference

**DB ID:** 8cd17557-340e-4346-9850-7291face328e  
**Data Source URL:** collection://4ae2fa35-d24f-4c44-be88-dbb808ea14cd  
**Data Source ID:** 4ae2fa35-d24f-4c44-be88-dbb808ea14cd  

## Fields

| Field | Type | Values |
| :--- | :--- | :--- |
| Name | title | free text |
| Status | status | Not started / In progress / Done |
| Artifact Type | select | Strategy Brief / Execution Plan / Architecture Package / Build Artifact / Build Report / Delivery Report / Learning Report |
| Producer | select | CEO / Krishna / Ganesha / Brahma / Hanuman / Saraswati / Lakshmi |
| Consumer | select | CEO / Krishna / Ganesha / Brahma / Hanuman / Saraswati / Lakshmi / System |
| Mission ID | text | free text |
| Version | text | free text |
| URI | url | free text |
| Acceptance Notes | text | free text |
| Rejection Notes | text | free text |

## Y-ORC Trigger Field Strategy

- **Trigger condition:** Status = "Not started" AND Consumer = "System" (or a specific worker)
- **Consumed state:** Status = "Done"
- **Capability field:** We will use "Acceptance Notes" as a temporary Capability field for MVP v1
  (or add a dedicated "Capability" text field via schema update)
- **Lineage:** URI field will store parent artifact URL

## Notes
- No "Capability" or "Parent Artifact" field exists yet — need to add via schema update
- Status options: Not started / In progress / Done (not "Ready For Execution" — must adapt)
