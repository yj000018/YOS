# Artifact Schema v1

**Status:** Official | **Date:** 2026-06-12 | **Owner:** Chief Architect (Brahma)

## Data Model

Every entry in the Artifact Registry MUST conform to the following schema:

| Field | Type | Description | Required |
| :--- | :--- | :--- | :--- |
| **Artifact ID** | String | Unique identifier (e.g., `ART-20260612-001`). | Yes |
| **Artifact Type** | Select | e.g., Strategy Brief, Execution Plan, Architecture Package. | Yes |
| **Mission ID** | String | The overarching mission this artifact belongs to. | Yes |
| **Producer** | Select | The Role that created the artifact (e.g., Krishna, Brahma). | Yes |
| **Consumer** | Select | The Role expected to consume the artifact. | Yes |
| **Status** | Select | Current state (Draft, Ready For Review, Accepted, etc.). | Yes |
| **Version** | Number | Incremental version number (starts at 1.0). | Yes |
| **Created Date** | Date | Timestamp of initial creation. | Yes |
| **Updated Date** | Date | Timestamp of last modification. | Yes |
| **Parent Artifact** | Relation | ID of the artifact that triggered this one. | No |
| **Child Artifact** | Relation | ID of the artifact(s) generated from this one. | No |
| **URI** | URL | Link to the actual content (Notion page, Git repo, S3 link). | Yes |
| **Acceptance Notes** | Text | Rationale or conditions upon acceptance. | No |
| **Rejection Notes** | Text | Specific reasons for rejection, required if Status = Rejected. | No |
