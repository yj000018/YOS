# Capability Roadmap: ECO (Lakshmi)

**Status:** Official | **Date:** 2026-06-12 | **Owner:** CODO (Saraswati)

## Current Capabilities (v1 - Active)
1. **Artifact Parsing:** Ability to read and extract metadata from Markdown artifacts in Notion/Git.
2. **Dashboard Generation:** Generating static Markdown or simple HTML dashboards representing organizational state.
3. **Anomaly Detection:** Basic threshold monitoring (e.g., time-in-state, token limits).

## Near-Term Expansion (v1.5 - Next 3 Months)
1. **Automated Polling:** Integrating with Y-ORC to receive webhook events on artifact state changes, rather than manual polling.
2. **Cost API Integration:** Direct integration with LLM provider APIs to pull real-time cost data per agent session.
3. **Interactive Dashboards:** Upgrading the ECO Dashboard to a React/Next.js web application (built by Hanuman) with live data feeds.

## Long-Term Vision (v2.0 - Predictive Coordination)
1. **Predictive Bottlenecking:** Using historical data to predict which missions are likely to fail or exceed budget before the build phase begins.
2. **Automated Triage:** Automatically resolving low-level open loops based on predefined CEO preferences.
3. **Semantic Search:** Allowing the CEO to query Lakshmi via natural language to find specific data across the entire history of Y-OS artifacts.
