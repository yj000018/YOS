"""
run_liveportrait_all.py — Generate all 10 eYa expressions via LivePortrait retargeting.
"""
import os, sys, time, cv2
sys.path.insert(0, '/home/ubuntu/LivePortrait')
os.environ['CUDA_VISIBLE_DEVICES'] = ''
import warnings; warnings.filterwarnings('ignore')

from src.config.argument_config import ArgumentConfig
from src.config.inference_config import InferenceConfig
from src.config.crop_config import CropConfig
from src.gradio_pipeline import GradioPipeline

SOURCE = '/home/ubuntu/eya_pipeline/eya_portrait.jpg'
OUT_DIR = '/home/ubuntu/eya_pipeline/output/liveportrait'
os.makedirs(OUT_DIR, exist_ok=True)

inf_cfg = InferenceConfig(flag_use_half_precision=False, flag_force_cpu=True)
crop_cfg = CropConfig(flag_force_cpu=True)
args = ArgumentConfig(
    source=SOURCE, driving=SOURCE, output_dir=OUT_DIR,
    flag_force_cpu=True, flag_eye_retargeting=True, flag_lip_retargeting=True,
)

print("Loading pipeline...")
pipeline = GradioPipeline(inference_cfg=inf_cfg, crop_cfg=crop_cfg, args=args)

print("Initializing source image...")
src_eye, src_lip = pipeline.init_retargeting_image(
    retargeting_source_scale=2.5, source_eye_ratio=0.0, source_lip_ratio=0.0,
    input_image=SOURCE,
)
print(f"Source ratios: eye={src_eye} lip={src_lip}")

# 10 expressions: (eye_ratio, lip_ratio, pitch, yaw, roll, mx, my, mz,
#                  lv0, lv1, lv2, lv3, smile, wink, eyebrow, ex, ey, scale, name)
EXPRESSIONS = [
    # eye,  lip,   p,  y,  r,  mx, my, mz, lv0,lv1,lv2,lv3, smile, wink, brow,  ex,  ey,  sc,  name
    (0.0,  0.3,   0,  0,  0,   0,  0,  0,   0,  0,  0,  0,  0.8,   0,    0,    0,   0,  2.5, "smile"),
    (0.0,  0.5,   0,  0,  0,   0,  0,  0,   0,  0,  0,  0,  1.0,   0,    0,    0,   0,  2.5, "big_smile"),
    (0.0,  0.0,   0,  0,  0,   0,  0,  0,   0,  0,  0,  0, -0.5,   0,    0,    0,   0,  2.5, "sad"),
    (0.6,  0.4,   0,  0,  0,   0,  0,  0,   0,  0,  0,  0,  0.0,   0,    0,    0,   0,  2.5, "surprised"),
    (0.0,  0.0,   0,  0,  0,   0,  0,  0,   0,  0,  0,  0, -0.3,   0,   -0.5,  0,   0,  2.5, "angry"),
    (-0.3, 0.0,   0,  0,  0,   0,  0,  0,   0,  0,  0,  0,  0.0,   0,    0,    0,   0,  2.5, "blink"),
    (-0.3, 0.0,   0,  0,  0,   0,  0,  0,   0,  0,  0,  0,  0.3,   0.5,  0,    0,   0,  2.5, "wink"),
    (0.0,  0.0,   0,  0,  0,   0,  0,  0,   0,  0,  0,  0,  0.0,   0,    0,    0,   0,  2.5, "neutral"),
    (0.0,  0.0,   0,  5,  0,   0,  0,  0,   0,  0,  0,  0,  0.1,   0,    0.3,  0,   0,  2.5, "thinking"),
    (0.0,  0.1,   0,  0,  0,   0,  0,  0,   0,  0,  0,  0,  0.4,   0,    0,    0,   0,  2.5, "shy"),
]

results = []
total_t = time.time()
for expr in EXPRESSIONS:
    *params, name = expr
    eye_r, lip_r, pitch, yaw, roll, mx, my, mz, lv0, lv1, lv2, lv3, smile, wink, eyebrow, ex, ey, scale = params
    print(f"  [{name}]...", end=" ", flush=True)
    t0 = time.time()
    try:
        result_img, paste_back = pipeline.execute_image_retargeting(
            input_eye_ratio=eye_r, input_lip_ratio=lip_r,
            input_head_pitch_variation=pitch, input_head_yaw_variation=yaw,
            input_head_roll_variation=roll, mov_x=mx, mov_y=my, mov_z=mz,
            lip_variation_zero=lv0, lip_variation_one=lv1,
            lip_variation_two=lv2, lip_variation_three=lv3,
            smile=smile, wink=wink, eyebrow=eyebrow,
            eyeball_direction_x=ex, eyeball_direction_y=ey,
            input_image=SOURCE, retargeting_source_scale=scale,
            flag_stitching_retargeting_input=True,
            flag_do_crop_input_retargeting_image=True,
        )
        elapsed = time.time() - t0
        img = paste_back if paste_back is not None else result_img
        out_path = os.path.join(OUT_DIR, f"eya_lp_{name}.jpg")
        cv2.imwrite(out_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        print(f"✅ {elapsed:.1f}s → {out_path}")
        results.append((name, True, elapsed, out_path))
    except Exception as e:
        print(f"❌ {e}")
        results.append((name, False, 0, str(e)))

print(f"\n✅ {sum(1 for r in results if r[1])}/{len(results)} expressions in {time.time()-total_t:.0f}s")
print("Output:", OUT_DIR)
