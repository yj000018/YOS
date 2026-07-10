"""
test_liveportrait.py
Test LivePortrait retargeting on eYa portrait via HuggingFace Space API.
Uses /gpu_wrapped_execute_image endpoint (retargeting mode).
"""
from gradio_client import Client, handle_file
import os, time

SOURCE = "/home/ubuntu/eya_pipeline/eya_portrait.jpg"
OUT_DIR = "/home/ubuntu/eya_pipeline/output/liveportrait"
os.makedirs(OUT_DIR, exist_ok=True)

# Try alternative spaces that may have more GPU quota
SPACES = [
    "KlingTeam/LivePortrait",
    "cleardusk/LivePortrait",
    "fffiloni/LivePortrait",
]

print("Connecting to HuggingFace Space...")
client = None
for space in SPACES:
    try:
        c = Client(space, verbose=False)
        client = c
        print(f"  Connected: {space}")
        break
    except Exception as e:
        print(f"  {space}: {e}")
if client is None:
    raise RuntimeError("No space available")

# Test 1: smile — open mouth slightly + eyes open
print("\n[1/3] Testing: smile (lip open 0.3, eyes open 0.0)...")
t0 = time.time()
result = client.predict(
    param_0=0.0,          # target eyes-open ratio (0=neutral)
    param_1=0.3,          # target lip-open ratio (0.3=slight smile/open)
    param_2=handle_file(SOURCE),  # source image
    param_3=True,         # do crop
    api_name="/gpu_wrapped_execute_image"
)
print(f"  Done in {time.time()-t0:.1f}s → {result}")
# result is (output_image_path, paste_back_image_path)
if isinstance(result, (list, tuple)) and len(result) >= 1:
    import shutil
    out = result[0] if isinstance(result[0], str) else str(result[0])
    dst = os.path.join(OUT_DIR, "eya_lp_smile.jpg")
    shutil.copy(out, dst)
    print(f"  Saved: {dst}")

# Test 2: wide eyes (surprised)
print("\n[2/3] Testing: surprised (eyes open 0.8, lip open 0.4)...")
t0 = time.time()
result2 = client.predict(
    param_0=0.8,
    param_1=0.4,
    param_2=handle_file(SOURCE),
    param_3=True,
    api_name="/gpu_wrapped_execute_image"
)
print(f"  Done in {time.time()-t0:.1f}s → {result2}")
if isinstance(result2, (list, tuple)) and len(result2) >= 1:
    out = result2[0] if isinstance(result2[0], str) else str(result2[0])
    dst = os.path.join(OUT_DIR, "eya_lp_surprised.jpg")
    shutil.copy(out, dst)
    print(f"  Saved: {dst}")

# Test 3: closed eyes (sleepy/shy)
print("\n[3/3] Testing: eyes closed (eyes open -0.5, lip 0.0)...")
t0 = time.time()
result3 = client.predict(
    param_0=-0.5,
    param_1=0.0,
    param_2=handle_file(SOURCE),
    param_3=True,
    api_name="/gpu_wrapped_execute_image"
)
print(f"  Done in {time.time()-t0:.1f}s → {result3}")
if isinstance(result3, (list, tuple)) and len(result3) >= 1:
    out = result3[0] if isinstance(result3[0], str) else str(result3[0])
    dst = os.path.join(OUT_DIR, "eya_lp_eyes_closed.jpg")
    shutil.copy(out, dst)
    print(f"  Saved: {dst}")

print("\n✅ LivePortrait test complete. Results in:", OUT_DIR)
