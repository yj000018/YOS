#!/usr/bin/env python3
"""
add_necklace.py — Composite necklace onto eYa neck layer using PIL
"""
from PIL import Image
import numpy as np

CANVAS = 768
NECK_CENTER_X = 379
NECK_TOP_Y = 407
NECK_WIDTH = 272

# Load necklace (already transparent background removed by generation)
necklace = Image.open("/home/ubuntu/eya_pipeline/necklace_raw.png").convert("RGBA")

# Remove green chroma key background (the generation used #00FF00 green bg)
import cv2
arr = np.array(necklace)
# Convert to HSV for green detection
rgb = arr[:,:,:3]
hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
# Green hue range in HSV: H=40-80 (out of 180), S>50, V>50
green_mask = cv2.inRange(hsv, np.array([35, 40, 40]), np.array([85, 255, 255]))
# Feather the mask edges
kernel = np.ones((3,3), np.uint8)
green_mask = cv2.dilate(green_mask, kernel, iterations=1)
alpha_new = np.where(green_mask > 0, 0, 255).astype(np.uint8)
arr[:,:,3] = alpha_new
necklace = Image.fromarray(arr, "RGBA")

# Crop to necklace bounding box (remove empty space)
bbox = necklace.getbbox()
necklace = necklace.crop(bbox)

# Scale necklace to fit neck width — necklace chain should be ~neck width
# Neck is 272px wide, necklace chain arc should match that
target_w = int(NECK_WIDTH * 1.05)  # just slightly wider than neck
scale = target_w / necklace.width
target_h = int(necklace.height * scale)
necklace = necklace.resize((target_w, target_h), Image.LANCZOS)

# Position: center horizontally, chain sits at base of neck (y=516 = topwear top)
# The necklace chain top arc should be at ~y=510 (just above topwear)
COLLAR_Y = 516  # top of topwear = where collar/necklace sits
x = NECK_CENTER_X - target_w // 2
y = COLLAR_Y - int(target_h * 0.25)  # chain arc at collar level, pendant hangs below

# Create neckwear layer (768x768 transparent)
neckwear = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
neckwear.paste(necklace, (x, y), necklace)
neckwear.save("/home/ubuntu/eya_pipeline/neckwear_layer.png")
print(f"✅ Neckwear layer saved: {neckwear.size}")
print(f"   Necklace placed at x={x}, y={y}, size={target_w}x{target_h}")

# Preview: composite on top of existing layers
base = Image.open("/home/ubuntu/eya-psd-correct/face.png").convert("RGBA")
neck = Image.open("/home/ubuntu/eya-psd-correct/neck.png").convert("RGBA")
topwear = Image.open("/home/ubuntu/eya-psd-correct/topwear.png").convert("RGBA")
back_hair = Image.open("/home/ubuntu/eya-psd-correct/back_hair.png").convert("RGBA")
front_hair = Image.open("/home/ubuntu/eya-psd-correct/front_hair.png").convert("RGBA")

preview = Image.new("RGBA", (CANVAS, CANVAS), (240, 230, 220, 255))
for layer in [back_hair, topwear, neck, base, neckwear, front_hair]:
    preview = Image.alpha_composite(preview, layer)

preview.convert("RGB").save("/home/ubuntu/eya_pipeline/eya_with_necklace_preview.jpg", quality=92)
print(f"✅ Preview saved: eya_with_necklace_preview.jpg")
