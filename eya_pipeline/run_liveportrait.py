"""
run_liveportrait.py — CPU retargeting test on eYa portrait.
Uses GradioPipeline.execute_image_retargeting() directly.
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
    source=SOURCE,
    driving=SOURCE,  # placeholder, not used in retargeting
    output_dir=OUT_DIR,
    flag_force_cpu=True,
    flag_eye_retargeting=True,
    flag_lip_retargeting=True,
)

print("Loading GradioPipeline...")
t0 = time.time()
pipeline = GradioPipeline(inference_cfg=inf_cfg, crop_cfg=crop_cfg, args=args)
print(f"Loaded in {time.time()-t0:.1f}s")

# Initialize source image — required before retargeting
print("Initializing source image...")
src_eye_ratio, src_lip_ratio = pipeline.init_retargeting_image(
    retargeting_source_scale=2.5,
    source_eye_ratio=0.0,
    source_lip_ratio=0.0,
    input_image=SOURCE,
)
print(f"Source: eye_ratio={src_eye_ratio} lip_ratio={src_lip_ratio}")

TESTS = [
    # (eye_ratio, lip_ratio, pitch, yaw, roll, mov_x, mov_y, mov_z,
    #  lip_v0, lip_v1, lip_v2, lip_v3, smile, wink, eyebrow, eyeball_x, eyeball_y,
    #  scale, name)
    (0.0, 0.3,  0, 0, 0,  0, 0, 0,  0, 0, 0, 0,  0.8, 0, 0, 0, 0,  2.5, "smile"),
    (0.6, 0.4,  0, 0, 0,  0, 0, 0,  0, 0, 0, 0,  0.0, 0, 0, 0, 0,  2.5, "surprised"),
    (0.0, 0.0,  0, 0, 0,  0, 0, 0,  0, 0, 0, 0, -0.5, 0, 0, 0, 0,  2.5, "sad"),
]

for test in TESTS:
    *params, name = test
    eye_r, lip_r, pitch, yaw, roll, mx, my, mz, lv0, lv1, lv2, lv3, smile, wink, eyebrow, ex, ey, scale = params
    print(f"\n[{name}] eye={eye_r} lip={lip_r} smile={smile}...")
    t0 = time.time()
    try:
        result_img, paste_back = pipeline.execute_image_retargeting(
            input_eye_ratio=eye_r,
            input_lip_ratio=lip_r,
            input_head_pitch_variation=pitch,
            input_head_yaw_variation=yaw,
            input_head_roll_variation=roll,
            mov_x=mx, mov_y=my, mov_z=mz,
            lip_variation_zero=lv0,
            lip_variation_one=lv1,
            lip_variation_two=lv2,
            lip_variation_three=lv3,
            smile=smile,
            wink=wink,
            eyebrow=eyebrow,
            eyeball_direction_x=ex,
            eyeball_direction_y=ey,
            input_image=SOURCE,
            retargeting_source_scale=scale,
            flag_stitching_retargeting_input=True,
            flag_do_crop_input_retargeting_image=True,
        )
        elapsed = time.time() - t0
        print(f"  Done in {elapsed:.1f}s")
        # Save result
        if paste_back is not None:
            out_path = os.path.join(OUT_DIR, f"eya_lp_{name}.jpg")
            cv2.imwrite(out_path, cv2.cvtColor(paste_back, cv2.COLOR_RGB2BGR))
            print(f"  Saved: {out_path}")
        elif result_img is not None:
            out_path = os.path.join(OUT_DIR, f"eya_lp_{name}.jpg")
            cv2.imwrite(out_path, cv2.cvtColor(result_img, cv2.COLOR_RGB2BGR))
            print(f"  Saved: {out_path}")
    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback; traceback.print_exc()

print("\n✅ Done. Results in:", OUT_DIR)
