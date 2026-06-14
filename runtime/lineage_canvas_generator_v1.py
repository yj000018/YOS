#!/usr/bin/env python3
"""
Module 6: Lineage Canvas Generator v1 — Y-OS MISSION-022A
Generates Mission_Lineage_Recovery.canvas
"""
from __future__ import annotations
import json
from pathlib import Path


# Confidence → Obsidian canvas color
CONF_COLOR = {
    "HIGH": "3",    # green
    "MEDIUM": "4",  # yellow
    "LOW": "6",     # red
}


def generate_lineage_canvas(registry: dict, output_path: Path) -> None:
    nodes = []
    edges = []
    edge_count = 0

    # Layout: missions in rows of 5
    items = sorted(registry.items(), key=lambda x: x[1]["mission_num"])
    cols = 5
    col_w = 220
    row_h = 300

    mission_positions: dict[str, tuple[float, float]] = {}

    for i, (m_id, m_data) in enumerate(items):
        col = i % cols
        row = i // cols
        x = col * col_w - (cols * col_w // 2)
        y = row * row_h - 200

        mission_positions[m_id] = (x, y)
        color = "3" if m_data["lineage_complete"] else "6"
        short_id = m_id.replace("MISSION-", "M-").split("_")[0]
        label = f"{short_id}\n{'✅' if m_data['lineage_complete'] else '⚠️'}\n{len(m_data['adr_links'])} ADRs"

        nodes.append({
            "id": f"m_{i}",
            "x": x, "y": y,
            "width": 180, "height": 80,
            "type": "text",
            "text": label,
            "color": color,
        })

    # Add ADR nodes (unique targets)
    adr_nodes: dict[str, dict] = {}
    adr_y = max(row_h * ((len(items) // cols) + 1), 400)
    adr_x_start = -(len(set(
        e["target"] for m in registry.values() for e in m["adr_links"]
    )) * 180 // 2)

    all_adr_targets = list(set(
        e["target"] for m in registry.values() for e in m["adr_links"]
    ))[:15]  # cap at 15 for readability

    for j, adr_id in enumerate(sorted(all_adr_targets)):
        ax = adr_x_start + j * 180
        short_adr = adr_id[:20]
        adr_nodes[adr_id] = {
            "id": f"adr_{j}",
            "x": ax, "y": adr_y,
            "width": 160, "height": 60,
            "type": "text",
            "text": short_adr,
            "color": "4",
        }
        nodes.append(adr_nodes[adr_id])

    # Add edges from missions to ADRs
    for i, (m_id, m_data) in enumerate(items):
        m_node_id = f"m_{i}"
        for adr_edge in m_data["adr_links"][:3]:  # max 3 per mission for readability
            adr_target = adr_edge["target"]
            if adr_target in adr_nodes:
                conf_band = adr_edge.get("band", "MEDIUM")
                label = f"{adr_edge['rel']}\n{adr_edge['confidence']:.2f}"
                edges.append({
                    "id": f"e_{edge_count}",
                    "fromNode": m_node_id,
                    "toNode": adr_nodes[adr_target]["id"],
                    "fromSide": "bottom",
                    "toSide": "top",
                    "label": label,
                    "color": CONF_COLOR.get(conf_band, "4"),
                })
                edge_count += 1

    # Add sequential dependency edges between missions
    for i in range(1, len(items)):
        edges.append({
            "id": f"dep_{i}",
            "fromNode": f"m_{i-1}",
            "toNode": f"m_{i}",
            "fromSide": "right",
            "toSide": "left",
            "label": "depends_on",
            "color": "3",
        })

    canvas = {"nodes": nodes, "edges": edges}
    output_path.write_text(json.dumps(canvas, indent=2), encoding="utf-8")
