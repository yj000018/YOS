#!/usr/bin/env python3
"""
Inject DWPose keypoints into a Stretchy Studio .stretch file.
The .stretch file is a ZIP containing project.json + texture PNGs.
We update the joint positions in project.json with DWPose keypoints.
"""

import json
import zipfile
import shutil
from pathlib import Path

HEURISTIC_STRETCH = "/home/ubuntu/eya_pipeline/output/eya_heuristic.stretch"
DWPOSE_KEYPOINTS  = "/home/ubuntu/eya_pipeline/dwpose_keypoints.json"
OUTPUT_STRETCH    = "/home/ubuntu/eya_pipeline/output/eya_dwpose.stretch"

def load_keypoints(path: str) -> dict:
    with open(path) as f:
        data = json.load(f)
    return data["joints_stretchy"]  # normalized [0..1] coords

def inspect_stretch(path: str):
    """Show what's inside the .stretch ZIP."""
    with zipfile.ZipFile(path, 'r') as z:
        print("Contents:", z.namelist())
        if "project.json" in z.namelist():
            with z.open("project.json") as f:
                proj = json.load(f)
            print("project.json keys:", list(proj.keys()))
            return proj
    return None

def find_joint_fields(obj, path="", results=None):
    """Recursively find joint/bone position fields in project.json."""
    if results is None:
        results = []
    
    if isinstance(obj, dict):
        # Look for fields that look like joint positions
        keys = set(obj.keys())
        if ("x" in keys and "y" in keys) and len(keys) <= 5:
            results.append((path, obj))
        for k, v in obj.items():
            find_joint_fields(v, f"{path}.{k}", results)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            find_joint_fields(v, f"{path}[{i}]", results)
    
    return results

def update_joints_in_project(proj: dict, joints: dict) -> dict:
    """
    Update joint positions in project.json with DWPose keypoints.
    
    Stretchy Studio stores joints in various locations depending on version.
    We look for 'joints', 'bones', 'armature', 'skeleton' keys.
    """
    import copy
    proj_updated = copy.deepcopy(proj)
    
    # Map DWPose joint names to Stretchy Studio bone names
    # Based on Stretchy Studio's armature structure
    JOINT_MAP = {
        "head":      ["head", "Head", "HEAD"],
        "eyeL":      ["eyeL", "eye_l", "eye-l", "leftEye", "EyeL"],
        "eyeR":      ["eyeR", "eye_r", "eye-r", "rightEye", "EyeR"],
        "earL":      ["earL", "ear_l", "ear-l", "leftEar"],
        "earR":      ["earR", "ear_r", "ear-r", "rightEar"],
        "neck":      ["neck", "Neck", "NECK"],
        "shoulderL": ["shoulderL", "shoulder_l", "leftShoulder"],
        "shoulderR": ["shoulderR", "shoulder_r", "rightShoulder"],
    }
    
    updated_count = 0
    
    def update_recursive(obj, path=""):
        nonlocal updated_count
        if isinstance(obj, dict):
            # Check if this looks like a joint object with a name
            name = obj.get("name", obj.get("id", obj.get("tag", "")))
            if name:
                for dw_joint, aliases in JOINT_MAP.items():
                    if dw_joint in joints and name in aliases:
                        kp = joints[dw_joint]
                        if "x" in obj and "y" in obj:
                            old_x, old_y = obj["x"], obj["y"]
                            obj["x"] = kp["x"]
                            obj["y"] = kp["y"]
                            print(f"  Updated {name}: ({old_x:.3f},{old_y:.3f}) → ({kp['x']:.3f},{kp['y']:.3f})")
                            updated_count += 1
            
            for k, v in obj.items():
                update_recursive(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                update_recursive(v, f"{path}[{i}]")
    
    update_recursive(proj_updated)
    print(f"Total joints updated: {updated_count}")
    return proj_updated, updated_count

def create_dwpose_stretch(heuristic_path: str, joints: dict, output_path: str):
    """Create a new .stretch file with DWPose joint positions."""
    
    # Copy the heuristic .stretch as base
    shutil.copy2(heuristic_path, output_path)
    
    # Open and modify project.json
    with zipfile.ZipFile(heuristic_path, 'r') as z_in:
        files = z_in.namelist()
        print(f"Files in .stretch: {files}")
        
        if "project.json" not in files:
            print("ERROR: project.json not found in .stretch file")
            return False
        
        with z_in.open("project.json") as f:
            proj = json.load(f)
        
        # Show structure
        print(f"\nproject.json top-level keys: {list(proj.keys())}")
        
        # Find all position-like objects
        positions = find_joint_fields(proj)
        print(f"\nFound {len(positions)} position-like objects:")
        for path, obj in positions[:20]:
            print(f"  {path}: {obj}")
        
        # Try to update joints
        proj_updated, n_updated = update_joints_in_project(proj, joints)
        
        if n_updated == 0:
            print("\nNo joints updated via name matching. Trying direct structure inspection...")
            # Show more of the structure for debugging
            for key in proj.keys():
                val = proj[key]
                if isinstance(val, (dict, list)):
                    print(f"\n{key}: {json.dumps(val, indent=2)[:500]}")
        
        # Write updated project.json back to ZIP
        import io
        proj_bytes = json.dumps(proj_updated, indent=2).encode('utf-8')
        
        # Rewrite ZIP with updated project.json
        import tempfile
        tmp_path = output_path + ".tmp"
        with zipfile.ZipFile(heuristic_path, 'r') as z_in:
            with zipfile.ZipFile(tmp_path, 'w', zipfile.ZIP_DEFLATED) as z_out:
                for item in z_in.namelist():
                    if item == "project.json":
                        z_out.writestr("project.json", proj_bytes)
                    else:
                        z_out.writestr(item, z_in.read(item))
        
        import os
        os.replace(tmp_path, output_path)
        print(f"\nDWPose .stretch saved: {output_path}")
        return True

def main():
    print("=== Inject DWPose Keypoints into Stretchy Studio ===\n")
    
    # Load DWPose keypoints
    joints = load_keypoints(DWPOSE_KEYPOINTS)
    print(f"DWPose joints loaded ({len(joints)}):")
    for name, j in joints.items():
        print(f"  {name:15s} x={j['x']:.3f} y={j['y']:.3f} score={j['score']:.3f}")
    
    print(f"\nInspecting heuristic .stretch file...")
    proj = inspect_stretch(HEURISTIC_STRETCH)
    
    print(f"\nCreating DWPose .stretch file...")
    Path(OUTPUT_STRETCH).parent.mkdir(parents=True, exist_ok=True)
    success = create_dwpose_stretch(HEURISTIC_STRETCH, joints, OUTPUT_STRETCH)
    
    if success:
        import os
        size = os.path.getsize(OUTPUT_STRETCH)
        print(f"\n✅ DWPose .stretch created: {OUTPUT_STRETCH} ({size/1024:.0f} KB)")
    else:
        print("\n❌ Failed to create DWPose .stretch")

if __name__ == "__main__":
    main()
