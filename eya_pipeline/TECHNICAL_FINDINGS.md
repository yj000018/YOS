# eYa Pipeline — Technical Findings

## Stretchy Studio Warp Deformer — Root Cause Analysis

### Warp Grid Structure
MouthWarp: col=2, row=2, gridX=338, gridY=440, gridW=160, gridH=82
- Grid points: 3×3 = 9 control points (col+1 × row+1)
- Mouth layer vertices: 95 vertices, ALL inside bbox [338-498, 440-522] ✅

### Why Expressions Show No Movement
The warp deformer uses BILINEAR interpolation:
- gridPts[ri*(col+1)+ci] where col=2, row=2
- So gridPts needs indices 0..8 (3×3 grid) ✅ — our keyframes have 9 vertices

**BUT**: The renderer code (CanvasViewport.jsx line 722-769) reads:
```js
const gridPts = wdOv?.mesh_verts;  // from our keyframe value
const { col=2, row=2, gridX, gridY, gridW, gridH } = wd;
// bilinear: p00 = gridPts[ri*(col+1)+ci]
```

Our keyframes have ABSOLUTE positions of the 9 grid control points.
The neutral positions (t=0) ARE the rest positions.
At peak (t=500ms), we DISPLACE them.

**The issue**: The mouth layer vertices are at y=[450-512] but gridY=440.
The bilinear formula: t = (py - gridY) / gridH = (450-440)/82 = 0.12
So ri = floor(0.12 * 2) = 0 → uses row 0 only.

Most vertices are in the TOP row of the grid (ri=0).
Our deltas for row 0 (top) of MouthWarp:
- v0=(338,440), v1=(418,440), v2=(498,440) → neutral top row
- At peak: v0=(-18,-14) delta → (320, 426)

**This SHOULD work** — the bilinear interpolation should deform the mouth vertices.

### Hypothesis: The issue may be that editor.stretchy.studio loads the FILE but doesn't re-run the rig
When you open a .stretch file in the cloud editor, it may load the project.json but the warp deformer nodes need to be "active" — i.e., the renderer needs to recognize them as warpDeformer type and process them.

**Check**: Does our generated file have type="warpDeformer" on the warp nodes?

## LivePortrait Status
- Models downloaded: ✅ (~2GB in /home/ubuntu/LivePortrait/pretrained_weights/)
- Pipeline loads in 7.0s on CPU ✅
- Method available: `execute` (not `execute_image`)
- Need to check `execute` signature for retargeting params

## GitHub
- Repo: yj000018/YOS
- Latest commit: d1ab647 (expressions_v2 recalibrated)
- Module path: 03_AUTOMATIONS/modules/eya-autolive2d/

## Key Node IDs (eya_heuristic.stretch)
- MouthWarp: wqb5nmv (col=2,row=2, gridX=338,gridY=440,gridW=160,gridH=82)
- EyeLWarp: ihl34zg (col=2,row=2, gridX=453,gridY=306,gridW=106,gridH=74)
- EyeRWarp: 3zdcal0 (col=2,row=2, gridX=310,gridY=285,gridW=119,gridH=76)
- EyebrowLWarp: f16aiwn (col=2,row=2, gridX=456,gridY=279,gridW=120,gridH=55)
- EyebrowRWarp: swpfcoe (col=2,row=2, gridX=306,gridY=254,gridW=136,gridH=69)
- FaceWarp: 0z3f78q (col=5,row=5, gridX=131,gridY=38,gridW=552,gridH=641)
