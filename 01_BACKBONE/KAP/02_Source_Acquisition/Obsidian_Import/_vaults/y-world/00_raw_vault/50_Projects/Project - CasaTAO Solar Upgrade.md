---
type: project
project_name: CasaTAO Solar Upgrade
status: active
priority: high
domain: CasaTAO
created: 2026-05-29
review_date: 2026-06-05
---

# Project — CasaTAO Solar Upgrade

Upgrade the solar and battery storage system at [[CasaTAO]] in Sicily to achieve 100% off-grid sovereign energy.

## Objectives

- [x] Install 12 additional bifacial solar panels (500W each)
- [ ] Connect 3x Pylontech US5000 LiFePO4 batteries (14.4 kWh total capacity)
- [ ] Configure Victron Cerbo GX to expose energy metrics via MQTT to Home Assistant [[CasaTAO Dashboard]]
- [ ] Integrate local AI predictive charging model based on weather forecasts

## Linked Systems

- **Hardware**: [[Coral Edge TPU]] (local weather processing)
- **Monitoring**: [[CasaTAO Dashboard]]
- **Automation**: [[n8n Cognitive Automation]] for load shedding during low-sun days\n