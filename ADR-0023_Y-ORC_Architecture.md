# ADR-0023: Y-ORC Architecture

**Date:** 2026-06-13  
**Status:** Accepted  
**Owner:** Chief Architect (Brahma)  

## Purpose
Define how work moves through Y-OS and establish the execution coordination layer on top of the Control Plane.

## Decision
Y-ORC becomes the orchestration layer responsible for triggering execution based on registered state.

## Consequences
*   **Lakshmi remains read-only.**
*   **Control Plane remains governance.**
*   **Y-ORC becomes execution coordination.**
*   **Agents become pluggable workers.**
