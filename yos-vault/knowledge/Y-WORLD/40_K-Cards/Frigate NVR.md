---
type: k-card
domain: AI-Systems
tags: [nvr, local-ai, security, frigate, smart-home]
created: 2026-05-29
status: active
---

# Frigate NVR

**Frigate** is an open-source, local network video recorder (NVR) that uses real-time AI object detection to turn dumb IP cameras into intelligent sensors.

## Integration in Y-WORLD

Frigate is deployed as a Docker container on the local MiniPCs at [[CasaTAO]] and [[ARC Anandaz]].

- **Hardware Acceleration**: Leverages the [[Coral Edge TPU]] for ultra-fast object detection (person, car, dog, package).
- **Home Assistant Sync**: Sends real-time MQTT events to trigger local automations [[n8n Cognitive Automation]].
- **Cognitive Integration**: Critical security events are piped directly to the [[Manus Control Surface]] for human operator review.\n