---
type: k-card
domain: AI-Systems
tags: [hardware, local-ai, coral, tpu, computer-vision]
created: 2026-05-29
status: active
---

# Coral Edge TPU

The **Google Coral Edge TPU** is a low-power, high-performance hardware accelerator designed to run machine learning models locally on the edge.

## Role in Y-WORLD

The Coral Edge TPU is integrated into the local server infrastructure of both [[CasaTAO]] (Sicile) and [[ARC Anandaz]] (Suisse).

- **Local Object Detection**: Accelerates [[Frigate NVR]] local video processing.
- **Privacy-First Processing**: Ensures zero camera feeds leave the local network.
- **Low Power Consumption**: Draws only 2W per TPU, making it ideal for solar-powered setups [[CasaTAO Dashboard]].

## System Mapping

```
[Local IP Cameras] ──> [Frigate NVR] ──> [Coral Edge TPU (Local Inference)] ──> [Home Assistant]
                                                                                      │
                                                                                      └──> [[Y-OS]] (Notification)
```\n