#!/usr/bin/env python3
"""
Visual comparison: Heuristic rig vs DWPose keypoints on eYa portrait.
Generates a side-by-side comparison image.
"""

import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

PORTRAIT = "/home/ubuntu/eya_pipeline/eya_portrait.jpg"
DWPOSE_JSON = "/home/ubuntu/eya_pipeline/dwpose_keypoints.json"
OUTPUT = "/home/ubuntu/eya_pipeline/output/rig_comparison.jpg"

# Canvas size: 768x768 (Stretchy Studio canvas)
CANVAS_W = 768
CANVAS_H = 768

# Heuristic joint positions (extracted from project.json canvas coords)
# These are the bbox-based positions Stretchy Studio computed
# Canvas is 768x768, coords in pixels
HEURISTIC_JOINTS = {
    # Approximated from the bbox centers of each layer in the 768x768 canvas
    "head":      {"x": 384, "y": 280, "label": "head (nose)"},
    "eyeL":      {"x": 460, "y": 230, "label": "eye-l"},
    "eyeR":      {"x": 310, "y": 230, "label": "eye-r"},
    "earL":      {"x": 555, "y": 260, "label": "ear-l"},
    "earR":      {"x": 215, "y": 260, "label": "ear-r"},
    "neck":      {"x": 384, "y": 520, "label": "neck"},
    "shoulderL": {"x": 580, "y": 620, "label": "shoulder-l"},
    "shoulderR": {"x": 190, "y": 620, "label": "shoulder-r"},
}

def load_portrait_resized(path: str, target_w: int, target_h: int) -> Image.Image:
    img = Image.open(path).convert("RGB")
    return img.resize((target_w, target_h), Image.LANCZOS)

def draw_joints(img: Image.Image, joints: dict, color: tuple, label_color: tuple) -> Image.Image:
    draw = ImageDraw.Draw(img)
    
    # Draw skeleton connections
    connections = [
        ("eyeL", "eyeR"),
        ("eyeL", "earL"),
        ("eyeR", "earR"),
        ("eyeL", "head"),
        ("eyeR", "head"),
        ("head", "neck"),
        ("neck", "shoulderL"),
        ("neck", "shoulderR"),
        ("shoulderL", "shoulderR"),
    ]
    
    for a, b in connections:
        if a in joints and b in joints:
            x1, y1 = int(joints[a]["x"]), int(joints[a]["y"])
            x2, y2 = int(joints[b]["x"]), int(joints[b]["y"])
            draw.line([(x1, y1), (x2, y2)], fill=color, width=2)
    
    # Draw joint circles
    for name, j in joints.items():
        x, y = int(j["x"]), int(j["y"])
        r = 8
        draw.ellipse([(x-r, y-r), (x+r, y+r)], fill=color, outline=(255,255,255), width=2)
        label = j.get("label", name)
        draw.text((x+10, y-8), label, fill=label_color)
    
    return img

def main():
    # Load portrait
    portrait = load_portrait_resized(PORTRAIT, CANVAS_W, CANVAS_H)
    
    # Load DWPose keypoints (normalized → pixel coords)
    with open(DWPOSE_JSON) as f:
        dw_data = json.load(f)
    
    dw_joints_norm = dw_data["joints_stretchy"]
    
    # Convert normalized to canvas pixels
    dw_joints = {}
    for name, j in dw_joints_norm.items():
        dw_joints[name] = {
            "x": j["x"] * CANVAS_W,
            "y": j["y"] * CANVAS_H,
            "label": name,
            "score": j["score"]
        }
    
    # Create side-by-side comparison
    W = CANVAS_W * 2 + 20  # 20px gap
    H = CANVAS_H + 80       # 80px for title
    comparison = Image.new("RGB", (W, H), (30, 30, 30))
    
    # Left panel: Heuristic
    left = portrait.copy()
    left = draw_joints(left, HEURISTIC_JOINTS, (255, 165, 0), (255, 220, 100))  # orange
    comparison.paste(left, (0, 80))
    
    # Right panel: DWPose
    right = portrait.copy()
    right = draw_joints(right, dw_joints, (0, 200, 255), (150, 230, 255))  # cyan
    comparison.paste(right, (CANVAS_W + 20, 80))
    
    # Titles
    draw = ImageDraw.Draw(comparison)
    draw.rectangle([(0, 0), (W, 75)], fill=(20, 20, 20))
    draw.text((CANVAS_W//2 - 120, 10), "HEURISTIC (bbox)", fill=(255, 165, 0))
    draw.text((CANVAS_W//2 - 60, 35), "Stretchy Studio default", fill=(180, 180, 180))
    draw.text((CANVAS_W + 20 + CANVAS_W//2 - 100, 10), "DWPose (ONNX CPU)", fill=(0, 200, 255))
    draw.text((CANVAS_W + 20 + CANVAS_W//2 - 80, 35), "0.1s inference", fill=(180, 180, 180))
    
    # Separator
    draw.line([(CANVAS_W + 10, 0), (CANVAS_W + 10, H)], fill=(80, 80, 80), width=2)
    
    # Save
    Path(OUTPUT).parent.mkdir(parents=True, exist_ok=True)
    comparison.save(OUTPUT, quality=90)
    print(f"Comparison saved: {OUTPUT}")
    
    # Print DWPose keypoints summary
    print(f"\nDWPose keypoints (canvas coords {CANVAS_W}x{CANVAS_H}):")
    for name, j in dw_joints.items():
        print(f"  {name:15s} x={j['x']:.0f} y={j['y']:.0f} score={j['score']:.3f}")
    
    print(f"\nHeuristic joints (estimated from bbox):")
    for name, j in HEURISTIC_JOINTS.items():
        print(f"  {name:15s} x={j['x']:.0f} y={j['y']:.0f}")

if __name__ == "__main__":
    main()
