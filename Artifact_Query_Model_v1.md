# Artifact Query Model v1

**Status:** Official | **Date:** 2026-06-12 | **Owner:** Chief Architect (Brahma)

## Context
Agents must query the Registry to find their work. This model defines the standard queries used by the roles.

## Standard Queries

### 1. Consumer Inbox Query
Used by any role to find work they need to review or act upon.
- **Filter:** `Consumer == [Role] AND Status == 'Ready For Review'`
- **Example:** Brahma queries: `Consumer == 'Brahma' AND Status == 'Ready For Review'`. He receives a list of Execution Plans from Ganesha.

### 2. Producer Rework Query
Used by any role to find work they submitted that was rejected.
- **Filter:** `Producer == [Role] AND Status == 'Rejected'`
- **Example:** Ganesha queries: `Producer == 'Ganesha' AND Status == 'Rejected'`. He finds Execution Plans rejected by Brahma.

### 3. Mission Status Query
Used by Lakshmi or the CEO to see the current bottleneck in a mission.
- **Filter:** `Mission ID == [ID] AND Status IN ['Draft', 'Ready For Review', 'Rejected']`

### 4. Downstream Block Query
Used by a Producer to check if their Accepted artifact has been acted upon.
- **Filter:** `Producer == [Role] AND Status == 'Accepted'`
- **Logic:** If an artifact stays 'Accepted' for too long, the Consumer is a bottleneck. Once the Consumer acts, the status changes to 'Consumed'.
