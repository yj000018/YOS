# eYa AutoLive2D Pipeline

Fully automated pipeline: Portrait JPG → Live2D-ready `.stretch` file.

## Pipeline (4.1s end-to-end)

```
Portrait JPG
  → See-through API        (24 semantic layers)
  → Filter + Rename        (remove empty, fix names)
  → L/R Split              (8 bilateral layers → L + R)
  → DWPose ONNX CPU        (facial keypoints, 0.1s)
  → Build PSD              (18 layers, exact Stretchy names)
  → Stretchy Studio        (auto-rig → 41 params, 37 nodes)
  → .stretch export        (Live2D-ready)
  → Pushover notification  (deep link to Manus thread)
```

## Usage

```bash
python3 eya_autolive2d.py \
  --input portrait.jpg \
  --output ./output \
  --task-id MANUS_THREAD_ID
```

## Output

- `eya_output.stretch` — 37 nodes, 41 Live2D parameters
- `dwpose_keypoints.json` — facial keypoints (normalized)
- `eya_pipeline.psd` — 18-layer PSD (Stretchy-compatible names)

## Parameters (41)

Angle X/Y/Z, Eye L/R Open, Eye L/R Smile, Eyeball X/Y/Z/Form,
Brow L/R Form/Angle, Mouth Form/Open/Smile, Cheek, Breath,
Body Angle X/Y/Z, Arm L/R, Hair Front/Side/Back

## Layer Mapping (24 → 18 non-empty → 37 with L/R splits)

| See-through | → Stretchy | Op |
|---|---|---|
| back_hair | back hair | rename |
| ears | ears-l + ears-r | split |
| eyebrow | eyebrow-l + eyebrow-r | split |
| eyelash | eyelash-l + eyelash-r | split |
| eyewhite | eyewhite-l + eyewhite-r | split |
| irides | irides-l + irides-r | split |
| face, neck, nose, mouth, topwear | same | rename only |
| head | — | ignored |

## Dependencies

```bash
pip install psd-tools pillow numpy onnxruntime opencv-python requests
```

## Notifications

Uses `yos-notify` module (Pushover + Telegram).
Deep link: `tech.butterfly.app://app/{task_id}` → opens Manus iOS app directly.
