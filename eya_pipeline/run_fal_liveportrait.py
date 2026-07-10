"""
run_fal_liveportrait.py — eYa smile+wink via fal.ai LivePortrait GPU
fal.ai endpoint: fal-ai/live-portrait
"""
import fal_client
import os, requests, json

# Upload eYa portrait to get a public URL
print("Uploading eYa portrait to fal.ai...")
portrait_url = fal_client.upload_file("/home/ubuntu/eya_pipeline/eya_portrait.jpg")
print(f"Portrait URL: {portrait_url}")

# fal.ai LivePortrait retargeting
# Params: source_image_url, driving params (eye_open, smile, etc.)
# Using image retargeting mode for smile + wink

print("\n=== Job 1: Warm Smile ===")
result_smile = fal_client.run(
    "fal-ai/live-portrait",
    arguments={
        "image_url": portrait_url,
        "retargeting_input": {
            "eye_open": 0.34,
            "lip_open": 0.3,
            "smile": 0.85,
        }
    }
)
print(json.dumps(result_smile, indent=2))

print("\n=== Job 2: Wink + Head Tilt ===")
result_wink = fal_client.run(
    "fal-ai/live-portrait",
    arguments={
        "image_url": portrait_url,
        "retargeting_input": {
            "eye_open": 0.34,
            "lip_open": 0.25,
            "smile": 0.9,
            "eye_open_left": 0.05,  # left eye nearly closed = wink
        }
    }
)
print(json.dumps(result_wink, indent=2))
