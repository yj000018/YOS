"""
gen_eya_sequence.py — eYa smile → coquettish wink sequence.
Full holistic face: smile, head tilt, left-eye wink, eyebrow lift.
24fps, 90 frames (~3.75s).
"""
import sys, os
sys.path.insert(0, '/home/ubuntu/LivePortrait')

import numpy as np
from src.gradio_pipeline import GradioPipeline
from src.config.argument_config import ArgumentConfig
from src.config.inference_config import InferenceConfig
from src.config.crop_config import CropConfig
from PIL import Image

PORTRAIT = '/home/ubuntu/eya_pipeline/eya_portrait.jpg'
OUT_DIR  = '/home/ubuntu/eya_pipeline/output/sequence'
os.makedirs(OUT_DIR, exist_ok=True)

# ─── Init pipeline ─────────────────────────────────────────────────────────
args = ArgumentConfig(
    source=PORTRAIT,
    driving=PORTRAIT,   # dummy — we use retargeting mode
    flag_force_cpu=True,
    flag_do_crop=True,
    flag_pasteback=True,
)
inf_cfg  = InferenceConfig(flag_force_cpu=True)
crop_cfg = CropConfig()
pipeline = GradioPipeline(inference_cfg=inf_cfg, crop_cfg=crop_cfg, args=args)

# Init retargeting — get source eye/lip ratios
SCALE = 2.3
print("Initialising retargeting...")
src_eye, src_lip = pipeline.init_retargeting_image(
    retargeting_source_scale=SCALE,
    source_eye_ratio=0.0,
    source_lip_ratio=0.0,
    input_image=PORTRAIT
)
print(f"  Source eye_ratio={src_eye}  lip_ratio={src_lip}")

# ─── Easing ─────────────────────────────────────────────────────────────────
def ease_in_out(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)

def lerp(a, b, t):
    return a + (b - a) * ease_in_out(t)

def phase_t(frame, f_start, f_end):
    if frame <= f_start: return 0.0
    if frame >= f_end:   return 1.0
    return (frame - f_start) / (f_end - f_start)

# ─── Motion design ──────────────────────────────────────────────────────────
# Phases:
# 0-5:   neutral hold
# 5-30:  smile builds warmly (Duchenne: eyes soften, cheeks rise)
# 30-50: smile peak — warm, genuine
# 50-60: head starts tilting right, eyebrow lifts slightly
# 60-72: LEFT eye winks, head tilt peaks, smile widens a touch
# 72-82: wink releases, head returns
# 82-90: settle into warm smile

FPS = 24
TOTAL = 90

def get_params(f):
    # ── smile ──────────────────────────────────────────────────────────────
    smile = 0.0
    if f < 5:
        smile = 0.0
    elif f < 30:
        smile = lerp(0.0, 0.8, phase_t(f, 5, 30))
    elif f < 50:
        smile = 0.8
    elif f < 65:
        smile = lerp(0.8, 0.92, phase_t(f, 50, 65))
    elif f < 82:
        smile = lerp(0.92, 0.78, phase_t(f, 65, 82))
    else:
        smile = lerp(0.78, 0.80, phase_t(f, 82, 90))

    # ── eye open ratio (both eyes soften with smile = Duchenne) ───────────
    # src_eye ≈ 0.34 (eYa's natural ratio)
    # Duchenne smile: eyes squint slightly → ratio drops to ~0.28
    eye_base = src_eye
    eye_squint = lerp(src_eye, src_eye * 0.82, phase_t(f, 10, 40))  # both eyes soften
    
    # Left eye wink
    eye_l = eye_squint
    if f >= 58:
        if f < 68:
            eye_l = lerp(eye_squint, 0.0, phase_t(f, 58, 68))   # close
        elif f < 76:
            eye_l = lerp(0.0, eye_squint, phase_t(f, 68, 76))   # open
        else:
            eye_l = eye_squint
    
    # Right eye stays open (slightly squinted from smile)
    eye_r = eye_squint

    # ── lip open (slight parting with big smile) ───────────────────────────
    lip = src_lip
    if f >= 25:
        lip = lerp(src_lip, src_lip + 0.04, phase_t(f, 25, 45))
    if f >= 65:
        lip = lerp(src_lip + 0.04, src_lip + 0.02, phase_t(f, 65, 82))

    # ── head roll (tilt right = coquettish) ───────────────────────────────
    roll = 0.0
    if f >= 50:
        if f < 65:
            roll = lerp(0.0, 12.0, phase_t(f, 50, 65))
        elif f < 80:
            roll = lerp(12.0, 3.0, phase_t(f, 65, 80))
        else:
            roll = lerp(3.0, 0.0, phase_t(f, 80, 90))

    # ── head pitch (slight down-tilt = intimate/coy) ──────────────────────
    pitch = 0.0
    if f >= 50:
        if f < 65:
            pitch = lerp(0.0, -4.0, phase_t(f, 50, 65))
        elif f < 80:
            pitch = lerp(-4.0, -1.0, phase_t(f, 65, 80))
        else:
            pitch = lerp(-1.0, 0.0, phase_t(f, 80, 90))

    # ── eyebrow (lifts slightly during wink prep) ─────────────────────────
    eyebrow = 0.0
    if f >= 52:
        if f < 65:
            eyebrow = lerp(0.0, 0.3, phase_t(f, 52, 65))
        elif f < 78:
            eyebrow = lerp(0.3, 0.0, phase_t(f, 65, 78))

    # ── eyeball direction (slight upward look = coy) ──────────────────────
    eyeball_y = 0.0
    if f >= 55:
        if f < 68:
            eyeball_y = lerp(0.0, -0.1, phase_t(f, 55, 68))
        elif f < 80:
            eyeball_y = lerp(-0.1, 0.0, phase_t(f, 68, 80))

    return {
        'eye_l': round(eye_l, 3),
        'eye_r': round(eye_r, 3),
        'lip':   round(lip, 3),
        'smile': round(smile, 3),
        'roll':  round(roll, 2),
        'pitch': round(pitch, 2),
        'eyebrow': round(eyebrow, 3),
        'eyeball_y': round(eyeball_y, 3),
    }

# ─── Generate frames ─────────────────────────────────────────────────────────
print(f"\nGenerating {TOTAL} frames...")
frame_paths = []

for f in range(TOTAL):
    p = get_params(f)
    
    result = pipeline.execute_image_retargeting(
        input_eye_ratio=p['eye_l'],           # left eye (winks)
        input_lip_ratio=p['lip'],
        input_head_pitch_variation=p['pitch'],
        input_head_yaw_variation=0.0,
        input_head_roll_variation=p['roll'],
        mov_x=0.0,
        mov_y=0.0,
        mov_z=0.0,
        lip_variation_zero=0.0,
        lip_variation_one=0.0,
        lip_variation_two=0.0,
        lip_variation_three=0.0,
        smile=p['smile'],
        wink=0.0,                             # not using wink param — using eye_ratio instead
        eyebrow=p['eyebrow'],
        eyeball_direction_x=0.0,
        eyeball_direction_y=p['eyeball_y'],
        input_image=PORTRAIT,
        retargeting_source_scale=SCALE,
        flag_stitching_retargeting_input=True,
        flag_do_crop_input_retargeting_image=True,
    )
    
    if result is not None:
        if isinstance(result, np.ndarray):
            img = Image.fromarray(result)
        elif isinstance(result, (list, tuple)):
            img = result[0] if isinstance(result[0], Image.Image) else Image.fromarray(result[0])
        else:
            img = result
        
        path = f"{OUT_DIR}/frame_{f:04d}.png"
        img.save(path)
        frame_paths.append(path)
        
        if f % 15 == 0:
            print(f"  f{f:3d}  smile={p['smile']:.2f}  eye_l={p['eye_l']:.3f}  roll={p['roll']:.1f}°  eyebrow={p['eyebrow']:.2f}")

print(f"\n✅ {len(frame_paths)} frames → {OUT_DIR}")
