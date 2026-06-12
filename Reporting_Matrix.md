# Reporting Relationships Matrix

**Status:** Official | **Date:** 2026-06-12 | **Owner:** CODO (Saraswati)

## Interaction Rules

| Role | Reports To | Gives Orders To | Receives Artifacts From | Delivers Artifacts To |
| :--- | :--- | :--- | :--- | :--- |
| **CSO (Krishna)** | CEO | Ganesha | CEO | Ganesha |
| **COO (Ganesha)** | CEO | Brahma, Hanuman | Krishna, Hanuman | Brahma, CEO |
| **Architect (Brahma)** | COO | Hanuman | Ganesha | Hanuman |
| **Developer (Hanuman)** | COO | None | Brahma | Ganesha |
| **CODO (Saraswati)** | CEO | All Agents (Rules) | All Agents (Logs) | System (Updates) |
| **ECO (Lakshmi)** | CEO | None (Observer) | All Agents (State) | CEO |

## Executive Proxy Exception
Lakshmi may give orders to any agent *only* when explicitly acting as an Executive Proxy for the CEO.
