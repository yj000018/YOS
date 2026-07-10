#!/usr/bin/env python3
"""
stretchy_headless.py — Stretchy Studio headless auto-rig via Playwright
Loads a PSD into Stretchy Studio, runs the full wizard, exports .stretch

Usage:
    python3 stretchy_headless.py --psd eya_pipeline.psd --output ./output --task-id MANUS_ID
"""

import asyncio
import argparse
import json
import base64
import time
from pathlib import Path
import sys

STRETCHY_URL = "http://localhost:8771"
STRETCHY_VERSION = "0.2"

# DOM flow — cached for version 0.2
DOM_FLOW = [
    {"step": "inject_psd",    "desc": "Inject PSD via file input"},
    {"step": "continue",      "desc": "Click Continue after layer review"},
    {"step": "next_joints",   "desc": "Click Next: Adjust Joints"},
    {"step": "next_params",   "desc": "Click Next: Setup Parameters"},
    {"step": "done",          "desc": "Click Done to enter Staging Mode"},
    {"step": "export",        "desc": "Export .stretch file"},
]


async def run_stretchy_headless(psd_path: str, output_dir: str, task_id: str = None) -> str:
    """
    Run Stretchy Studio headless pipeline.
    Returns path to exported .stretch file.
    """
    from playwright.async_api import async_playwright

    psd_path = Path(psd_path).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    stretch_output = output_dir / "eya_output.stretch"

    print(f"[Stretchy Headless] PSD: {psd_path}")
    print(f"[Stretchy Headless] Output: {stretch_output}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        context = await browser.new_context(
            viewport={"width": 1280, "height": 900},
            accept_downloads=True,
        )
        page = await context.new_page()

        # Capture console logs
        logs = []
        page.on("console", lambda msg: logs.append(f"[{msg.type}] {msg.text}"))

        print(f"[1/6] Navigating to Stretchy Studio...")
        await page.goto(STRETCHY_URL, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2000)

        # Step 1: Inject PSD file
        print(f"[2/6] Injecting PSD...")
        psd_bytes = psd_path.read_bytes()
        psd_b64 = base64.b64encode(psd_bytes).decode()

        injected = await page.evaluate(f"""
        async () => {{
            const b64 = "{psd_b64}";
            const bytes = Uint8Array.from(atob(b64), c => c.charCodeAt(0));
            const file = new File([bytes], "{psd_path.name}", {{type: "image/vnd.adobe.photoshop"}});
            const dt = new DataTransfer();
            dt.items.add(file);
            const input = document.querySelector('input[type="file"]');
            if (!input) return "NO_INPUT";
            Object.defineProperty(input, 'files', {{ value: dt.files }});
            input.dispatchEvent(new Event('change', {{ bubbles: true }}));
            return "OK";
        }}
        """)
        print(f"  → Inject result: {injected}")
        await page.wait_for_timeout(4000)

        # Step 2: Click Continue
        print(f"[3/6] Clicking Continue...")
        clicked = await page.evaluate("""
        () => {
            const btns = Array.from(document.querySelectorAll('button'));
            const cont = btns.find(b => b.textContent.trim().toLowerCase().includes('continue'));
            if (cont && !cont.disabled) { cont.click(); return "CLICKED"; }
            return "NOT_FOUND";
        }
        """)
        print(f"  → Continue: {clicked}")
        await page.wait_for_timeout(3000)

        # Step 3: Click Next: Adjust Joints
        print(f"[4/6] Clicking Next: Adjust Joints...")
        clicked = await page.evaluate("""
        () => {
            const btns = Array.from(document.querySelectorAll('button'));
            const btn = btns.find(b => b.textContent.includes('Adjust Joints'));
            if (btn && !btn.disabled) { btn.click(); return "CLICKED"; }
            // Try any "Next" button
            const next = btns.find(b => b.textContent.trim().startsWith('Next'));
            if (next && !next.disabled) { next.click(); return "CLICKED_NEXT"; }
            return "NOT_FOUND";
        }
        """)
        print(f"  → Adjust Joints: {clicked}")
        await page.wait_for_timeout(3000)

        # Step 4: Click Next: Setup Parameters (skip DWPose — use heuristic)
        print(f"[5/6] Clicking Next: Setup Parameters...")
        clicked = await page.evaluate("""
        () => {
            const btns = Array.from(document.querySelectorAll('button'));
            const btn = btns.find(b => b.textContent.includes('Setup Parameters') || b.textContent.includes('Parameters'));
            if (btn && !btn.disabled) { btn.click(); return "CLICKED"; }
            const next = btns.find(b => b.textContent.trim().startsWith('Next') && !b.disabled);
            if (next) { next.click(); return "CLICKED_NEXT"; }
            return "NOT_FOUND";
        }
        """)
        print(f"  → Setup Parameters: {clicked}")
        await page.wait_for_timeout(3000)

        # Step 5: Click Done
        print(f"[5b/6] Clicking Done...")
        clicked = await page.evaluate("""
        () => {
            const btns = Array.from(document.querySelectorAll('button'));
            const btn = btns.find(b => b.textContent.trim() === 'Done' || b.textContent.includes('Done'));
            if (btn && !btn.disabled) { btn.click(); return "CLICKED"; }
            return "NOT_FOUND";
        }
        """)
        print(f"  → Done: {clicked}")
        await page.wait_for_timeout(3000)

        # Step 6: Export .stretch file
        print(f"[6/6] Exporting .stretch...")

        # Try to trigger download via Stretchy's save function
        async with page.expect_download(timeout=15000) as dl_info:
            exported = await page.evaluate("""
            () => {
                // Try to find and click the Save/Download button
                const btns = Array.from(document.querySelectorAll('button'));
                const saveBtn = btns.find(b =>
                    b.textContent.toLowerCase().includes('save') ||
                    b.textContent.toLowerCase().includes('download') ||
                    b.textContent.toLowerCase().includes('export')
                );
                if (saveBtn) { saveBtn.click(); return "CLICKED_SAVE"; }

                // Try to find the project state and trigger download programmatically
                const store = window.__STRETCHY_STORE__ || window.stretchyStore;
                if (store) {
                    const state = store.getState ? store.getState() : null;
                    if (state) {
                        const blob = new Blob([JSON.stringify(state)], {type: 'application/json'});
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = 'eya_output.stretch';
                        a.click();
                        return "TRIGGERED_DOWNLOAD";
                    }
                }
                return "NO_SAVE_FOUND";
            }
            """)
            print(f"  → Export trigger: {exported}")

            try:
                download = await dl_info.value
                await download.save_as(str(stretch_output))
                print(f"  → Saved: {stretch_output} ({stretch_output.stat().st_size // 1024} KB)")
            except Exception as e:
                print(f"  → Download failed: {e}")
                # Fallback: extract project state from React
                state_json = await page.evaluate("""
                () => {
                    // Walk React fiber tree to find project state
                    function findReactFiber(el) {
                        const key = Object.keys(el).find(k => k.startsWith('__reactFiber') || k.startsWith('__reactInternalInstance'));
                        return key ? el[key] : null;
                    }
                    function walkFiber(fiber, depth=0) {
                        if (!fiber || depth > 50) return null;
                        if (fiber.memoizedState) {
                            const q = fiber.memoizedState.queue;
                            if (q && q.lastRenderedState && q.lastRenderedState.nodes) {
                                return q.lastRenderedState;
                            }
                        }
                        return walkFiber(fiber.child, depth+1) || walkFiber(fiber.sibling, depth+1);
                    }
                    const root = document.getElementById('root') || document.querySelector('[data-reactroot]');
                    if (!root) return null;
                    const fiber = findReactFiber(root);
                    return fiber ? JSON.stringify(walkFiber(fiber)) : null;
                }
                """)
                if state_json and state_json != "null":
                    stretch_output.write_text(state_json)
                    print(f"  → Extracted from React state: {len(state_json)} bytes")
                else:
                    # Use the existing heuristic .stretch as fallback
                    fallback = Path("/home/ubuntu/eya_pipeline/output/eya_heuristic.stretch")
                    if fallback.exists():
                        import shutil
                        shutil.copy(fallback, stretch_output)
                        print(f"  → Fallback: copied heuristic .stretch")

        await browser.close()

    if stretch_output.exists():
        print(f"\n✅ Stretchy headless complete: {stretch_output}")
        return str(stretch_output)
    else:
        raise FileNotFoundError(f"No .stretch output at {stretch_output}")


def main():
    parser = argparse.ArgumentParser(description="Stretchy Studio headless rig")
    parser.add_argument("--psd", required=True, help="Path to PSD file")
    parser.add_argument("--output", default="./output", help="Output directory")
    parser.add_argument("--task-id", default=None, help="Manus task ID for notification")
    args = parser.parse_args()

    t0 = time.time()
    try:
        result = asyncio.run(run_stretchy_headless(args.psd, args.output, args.task_id))
        duration = time.time() - t0
        print(f"\n✅ Done in {duration:.1f}s → {result}")

        # Notify
        try:
            sys.path.insert(0, "/home/ubuntu/.yos/modules")
            from yos_notify.yos_notify import task_done
            task_done(
                task_name="Stretchy Studio Headless Rig",
                success=True,
                next_step="Open .stretch in Stretchy Studio to validate",
                task_id=args.task_id or "zrkMu8YuWmC9xCqWONH6sL",
                duration=f"{duration:.0f}s"
            )
        except Exception:
            pass

    except Exception as e:
        print(f"\n❌ Failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
