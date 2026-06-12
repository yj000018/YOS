# Artifact State Machine v1

**Status:** Official | **Date:** 2026-06-12 | **Owner:** Chief Architect (Brahma)

## Supported States

1. **Draft:** The artifact is currently being written by the Producer.
2. **Ready For Review:** The Producer has finished and submitted the artifact to the Consumer for validation.
3. **Accepted:** The Consumer has validated the artifact against their requirements. It is now the official input for the next phase.
4. **Rejected:** The Consumer found the artifact lacking. `Rejection Notes` must be populated. The artifact is returned to the Producer.
5. **Consumed:** The Consumer has successfully used the artifact to produce the *next* artifact in the chain.
6. **Superseded:** A newer version of this artifact has been Accepted, rendering this version obsolete.
7. **Archived:** The overarching Mission is complete, and the artifact is moved to cold storage (Memory Layer).

## Valid State Transitions

- `Draft` → `Ready For Review`
- `Ready For Review` → `Accepted`
- `Ready For Review` → `Rejected`
- `Rejected` → `Draft` (Implicitly creates a new version)
- `Accepted` → `Consumed`
- `Accepted` → `Superseded`
- `Consumed` → `Archived`
- `Superseded` → `Archived`
