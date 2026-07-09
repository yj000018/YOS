#!/usr/bin/env python3
"""
DWPose inference using ONNX Runtime (CPU) — no browser WASM needed.
Extracts body keypoints from a portrait image and outputs joint positions
compatible with Stretchy Studio's rigging format.

Model: dw-ll_ucoco_384.onnx (DWPose whole-body pose estimation)
Input: 384x384 RGB image
Output: 133 keypoints (body + face + hands)
"""

import numpy as np
import cv2
import json
import time
from pathlib import Path

ONNX_MODEL = "/home/ubuntu/stretchy-studio/public/dw-ll_ucoco_384.onnx"
INPUT_IMAGE = "/home/ubuntu/eya_pipeline/eya_portrait.jpg"
OUTPUT_JSON = "/home/ubuntu/eya_pipeline/dwpose_keypoints.json"

# DWPose keypoint indices (COCO WholeBody 133)
KP = {
    "nose":          0,
    "left_eye":      1,
    "right_eye":     2,
    "left_ear":      3,
    "right_ear":     4,
    "left_shoulder": 5,
    "right_shoulder":6,
    "left_elbow":    7,
    "right_elbow":   8,
    "left_wrist":    9,
    "right_wrist":   10,
    "left_hip":      11,
    "right_hip":     12,
    "neck":          17,  # virtual neck (midpoint shoulders)
}

def preprocess(img_path: str, input_h: int = 384, input_w: int = 288):
    """Load and preprocess image for DWPose. Model expects [batch, 3, 384, 288]."""
    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {img_path}")
    
    orig_h, orig_w = img.shape[:2]
    
    # Resize to model input size (W=288, H=384)
    img_resized = cv2.resize(img, (input_w, input_h))
    img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
    
    # Normalize: mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std  = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    img_norm = (img_rgb.astype(np.float32) / 255.0 - mean) / std
    
    # HWC -> NCHW
    img_tensor = img_norm.transpose(2, 0, 1)[np.newaxis, ...]
    
    return img_tensor, orig_w, orig_h, input_w, input_h

def run_inference(model_path: str, img_tensor: np.ndarray):
    """Run DWPose ONNX model inference."""
    import onnxruntime as ort
    
    print(f"Loading model: {model_path}")
    t0 = time.time()
    
    sess = ort.InferenceSession(
        model_path,
        providers=["CPUExecutionProvider"]
    )
    
    input_name = sess.get_inputs()[0].name
    print(f"Model loaded in {time.time()-t0:.1f}s. Running inference...")
    
    t1 = time.time()
    outputs = sess.run(None, {input_name: img_tensor})
    elapsed = time.time() - t1
    print(f"Inference done in {elapsed:.1f}s")
    
    return outputs, elapsed

def extract_keypoints(outputs, orig_w: int, orig_h: int,
                       input_w: int = 288, input_h: int = 384):
    """
    Extract keypoint coordinates from SimCC model output.
    DWPose SimCC output:
      simcc_x: [1, 133, W*2]  — x coordinate distribution
      simcc_y: [1, 133, H*2]  — y coordinate distribution
    """
    simcc_x, simcc_y = outputs[0], outputs[1]
    print(f"simcc_x shape: {simcc_x.shape}, simcc_y shape: {simcc_y.shape}")
    
    # SimCC: argmax gives position in upsampled space (x2 resolution)
    simcc_split_ratio = 2.0
    kps_x = np.argmax(simcc_x[0], axis=-1)  # [133]
    kps_y = np.argmax(simcc_y[0], axis=-1)  # [133]
    
    # Confidence = max value of distribution
    scores_x = simcc_x[0].max(axis=-1)  # [133]
    scores_y = simcc_y[0].max(axis=-1)  # [133]
    scores = (scores_x + scores_y) / 2
    
    # Convert from SimCC space to pixel space
    # SimCC x range: [0, input_w * simcc_split_ratio]
    # SimCC y range: [0, input_h * simcc_split_ratio]
    scale_x = orig_w / (input_w * simcc_split_ratio)
    scale_y = orig_h / (input_h * simcc_split_ratio)
    
    keypoints = {}
    for name, idx in KP.items():
        if idx < len(kps_x):
            x = float(kps_x[idx]) * scale_x
            y = float(kps_y[idx]) * scale_y
            score = float(scores[idx])
            keypoints[name] = {"x": x, "y": y, "score": score}
    
    # Compute virtual neck as midpoint of shoulders
    if "left_shoulder" in keypoints and "right_shoulder" in keypoints:
        ls = keypoints["left_shoulder"]
        rs = keypoints["right_shoulder"]
        keypoints["neck"] = {
            "x": (ls["x"] + rs["x"]) / 2,
            "y": (ls["y"] + rs["y"]) / 2,
            "score": min(ls["score"], rs["score"])
        }
    
    return keypoints

def keypoints_to_stretchy_joints(keypoints: dict, img_w: int, img_h: int) -> dict:
    """
    Convert DWPose keypoints to Stretchy Studio joint format.
    Stretchy expects normalized coordinates [0..1] with origin top-left.
    """
    def norm(kp):
        return {
            "x": kp["x"] / img_w,
            "y": kp["y"] / img_h,
            "score": kp["score"]
        }
    
    joints = {}
    
    # Map DWPose keypoints to Stretchy Studio joint names
    mapping = {
        "head":       "nose",
        "eyeL":       "left_eye",
        "eyeR":       "right_eye",
        "earL":       "left_ear",
        "earR":       "right_ear",
        "neck":       "neck",
        "shoulderL":  "left_shoulder",
        "shoulderR":  "right_shoulder",
    }
    
    for joint_name, kp_name in mapping.items():
        if kp_name in keypoints and keypoints[kp_name]["score"] > 0.1:
            joints[joint_name] = norm(keypoints[kp_name])
    
    return joints

def visualize_keypoints(img_path: str, keypoints: dict, output_path: str):
    """Draw keypoints on image for visual validation."""
    img = cv2.imread(img_path)
    
    colors = {
        "nose": (0, 255, 0),
        "left_eye": (255, 0, 0), "right_eye": (255, 0, 0),
        "left_ear": (0, 0, 255), "right_ear": (0, 0, 255),
        "neck": (255, 255, 0),
        "left_shoulder": (0, 255, 255), "right_shoulder": (0, 255, 255),
    }
    
    for name, kp in keypoints.items():
        if kp["score"] > 0.1:
            x, y = int(kp["x"]), int(kp["y"])
            color = colors.get(name, (128, 128, 128))
            cv2.circle(img, (x, y), 8, color, -1)
            cv2.putText(img, name[:6], (x+5, y-5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
    
    cv2.imwrite(output_path, img)
    print(f"Visualization saved: {output_path}")

def main():
    # Find input image
    candidates = [
        "/home/ubuntu/eya_pipeline/eya_portrait.jpg",
        "/home/ubuntu/eya_pipeline/eya_portrait.png",
        "/home/ubuntu/eya_pipeline/input/portrait.jpg",
    ]
    img_path = None
    for c in candidates:
        if Path(c).exists():
            img_path = c
            break
    
    if not img_path:
        # Use the original portrait from the project files
        import glob
        portraits = glob.glob("/home/ubuntu/projects/eya-97fb1a5c/*.jpg") + \
                   glob.glob("/home/ubuntu/projects/eya-97fb1a5c/*.png")
        if portraits:
            img_path = portraits[0]
        else:
            print("ERROR: No portrait image found")
            return
    
    print(f"Input image: {img_path}")
    
    # Preprocess
    img_tensor, orig_w, orig_h, input_w, input_h = preprocess(img_path)
    print(f"Image size: {orig_w}x{orig_h} → model input: {input_w}x{input_h}")
    
    # Run inference
    outputs, elapsed = run_inference(ONNX_MODEL, img_tensor)
    
    # Extract keypoints
    keypoints = extract_keypoints(outputs, orig_w, orig_h, input_w, input_h)
    
    # Convert to Stretchy Studio format
    joints = keypoints_to_stretchy_joints(keypoints, orig_w, orig_h)
    
    # Save results
    result = {
        "source": "DWPose ONNX Runtime (CPU)",
        "model": "dw-ll_ucoco_384.onnx",
        "inference_time_sec": round(elapsed, 2),
        "image_size": {"w": orig_w, "h": orig_h},
        "keypoints_raw": keypoints,
        "joints_stretchy": joints
    }
    
    Path(OUTPUT_JSON).parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nKeypoints saved: {OUTPUT_JSON}")
    
    # Visualize
    viz_path = OUTPUT_JSON.replace(".json", "_viz.jpg")
    visualize_keypoints(img_path, keypoints, viz_path)
    
    # Summary
    print(f"\n=== DWPose Results ===")
    print(f"Inference time: {elapsed:.1f}s")
    print(f"Keypoints detected ({len(keypoints)}):")
    for name, kp in sorted(keypoints.items(), key=lambda x: -x[1]["score"]):
        print(f"  {name:20s} x={kp['x']:.0f} y={kp['y']:.0f} score={kp['score']:.3f}")
    
    print(f"\nStretchy Studio joints ({len(joints)}):")
    for name, j in joints.items():
        print(f"  {name:15s} x={j['x']:.3f} y={j['y']:.3f} score={j['score']:.3f}")

if __name__ == "__main__":
    main()
