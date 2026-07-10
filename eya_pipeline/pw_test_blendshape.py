"""
pw_test_blendshape.py v3 — Inject project directly into Zustand store via JS.
Bypasses the UI file dialog entirely.
"""
import asyncio, os, json, base64
from playwright.async_api import async_playwright

STRETCH_URL = "http://localhost:8771/"
STRETCH_FILE = "/home/ubuntu/eya_pipeline/output/eya_test_blendshape.stretch"
OUT_DIR = "/home/ubuntu/eya_pipeline/output/pw_frames"
os.makedirs(OUT_DIR, exist_ok=True)

# Read the stretch file and encode as base64 for JS injection
with open(STRETCH_FILE, 'rb') as f:
    stretch_b64 = base64.b64encode(f.read()).decode()

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage',
                  '--enable-webgl', '--use-gl=swiftshader', '--ignore-gpu-blocklist']
        )
        ctx = await browser.new_context(viewport={'width': 1400, 'height': 900})
        page = await ctx.new_page()

        page.on("console", lambda msg: print(f"  [JS] {msg.text[:120]}") if msg.type in ('error', 'log') else None)

        print("1. Loading Stretchy Studio...")
        await page.goto(STRETCH_URL, wait_until='networkidle', timeout=20000)
        await page.wait_for_timeout(3000)

        print("2. Injecting project via JS...")
        # Inject JSZip if not available, then load the stretch file
        result = await page.evaluate(f"""
            async () => {{
                // Decode base64 stretch file
                const b64 = "{stretch_b64}";
                const binary = atob(b64);
                const bytes = new Uint8Array(binary.length);
                for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
                const blob = new Blob([bytes], {{type: 'application/zip'}});
                const file = new File([blob], 'eya_test_blendshape.stretch');
                
                // Find the loadProject function from the module system
                // Stretchy uses Vite — modules are accessible via import()
                try {{
                    const mod = await import('/src/io/projectFile.js');
                    const project = await mod.loadProject(file);
                    
                    // Find projectStore and load the project
                    // Zustand stores are not directly exposed, but we can find them
                    // via React DevTools fiber or by checking all window properties
                    let storeFound = false;
                    for (const key of Object.getOwnPropertyNames(window)) {{
                        try {{
                            const val = window[key];
                            if (val && typeof val.getState === 'function') {{
                                const state = val.getState();
                                if (state.project && state.loadProject) {{
                                    state.loadProject(project.projectData);
                                    storeFound = true;
                                    return 'project_loaded_via_store_' + key;
                                }}
                            }}
                        }} catch(e) {{}}
                    }}
                    return storeFound ? 'loaded' : 'store_not_found_but_project_parsed';
                }} catch(e) {{
                    return 'error: ' + e.message;
                }}
            }}
        """)
        print(f"   JS result: {result}")
        await page.wait_for_timeout(3000)
        await page.screenshot(path=f"{OUT_DIR}/02_after_inject.png")
        print("   Screenshot: 02_after_inject.png")

        # Alternative: use the file input directly but handle the dialog properly
        if 'error' in str(result) or 'not_found' in str(result):
            print("3. Fallback: using file input with dialog bypass...")
            # Click open button
            toolbar_btns = await page.locator('header button, [role="toolbar"] button').all()
            if len(toolbar_btns) >= 3:
                await toolbar_btns[2].click()
                await page.wait_for_timeout(1000)

            # Upload file
            file_input = page.locator('input[type="file"]').first
            if await file_input.count() > 0:
                await file_input.set_input_files(STRETCH_FILE)
                await page.wait_for_timeout(1000)

            # Close dialog via JS (bypass click interception)
            await page.evaluate("""
                () => {
                    // Close all Radix dialogs by setting their state
                    document.querySelectorAll('[data-state="open"][role="dialog"]').forEach(d => {
                        // Trigger close event
                        d.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', bubbles: true}));
                    });
                    // Also remove backdrop
                    document.querySelectorAll('[data-state="open"][aria-hidden="true"]').forEach(el => {
                        el.setAttribute('data-state', 'closed');
                        el.style.display = 'none';
                    });
                }
            """)
            await page.wait_for_timeout(2000)
            await page.screenshot(path=f"{OUT_DIR}/03_dialog_closed.png")
            print("   Screenshot: 03_dialog_closed.png")

        # Switch to Animation mode
        print("4. Switching to Animation mode...")
        await page.evaluate("""
            () => {
                // Find and click Animation button by text content
                const btns = document.querySelectorAll('button');
                for (const btn of btns) {
                    if (btn.textContent.trim() === 'Animation') {
                        btn.click();
                        return 'clicked';
                    }
                }
                return 'not_found';
            }
        """)
        await page.wait_for_timeout(1000)
        await page.screenshot(path=f"{OUT_DIR}/04_animation_mode.png")
        print("   Screenshot: 04_animation_mode.png")

        # Select the test animation
        print("5. Selecting eYa BIG SMILE TEST animation...")
        await page.evaluate("""
            () => {
                const els = document.querySelectorAll('*');
                for (const el of els) {
                    if (el.textContent.trim() === 'eYa BIG SMILE TEST' && el.children.length === 0) {
                        el.click();
                        return 'clicked';
                    }
                }
                // Try parent elements
                for (const el of els) {
                    if (el.textContent.includes('eYa BIG SMILE TEST') && el.tagName !== 'BODY' && el.tagName !== 'HTML') {
                        el.click();
                        return 'clicked_parent: ' + el.tagName + '.' + el.className.slice(0,30);
                    }
                }
                return 'not_found';
            }
        """)
        await page.wait_for_timeout(1000)
        await page.screenshot(path=f"{OUT_DIR}/05_anim_selected.png")
        print("   Screenshot: 05_anim_selected.png")

        # Set currentTime via Zustand store using React fiber
        print("6. Capturing frames...")
        for frame_ms, label in [(0, 't0_rest'), (1000, 't1000_peak'), (2000, 't2000_end')]:
            result = await page.evaluate(f"""
                () => {{
                    // Method 1: Find Zustand store via React fiber
                    const canvas = document.querySelector('canvas');
                    if (canvas) {{
                        const fiberKey = Object.keys(canvas).find(k => k.startsWith('__reactFiber'));
                        if (fiberKey) {{
                            let fiber = canvas[fiberKey];
                            while (fiber) {{
                                if (fiber.memoizedState) {{
                                    // Walk the hooks chain
                                    let hook = fiber.memoizedState;
                                    while (hook) {{
                                        if (hook.queue && hook.memoizedState && 
                                            typeof hook.memoizedState.currentTime === 'number') {{
                                            // This might be the animation store
                                            break;
                                        }}
                                        hook = hook.next;
                                    }}
                                }}
                                fiber = fiber.return;
                            }}
                        }}
                    }}
                    
                    // Method 2: Use window.__ZUSTAND__ if available
                    if (window.__ZUSTAND__) {{
                        for (const store of Object.values(window.__ZUSTAND__)) {{
                            if (typeof store.getState().currentTime === 'number') {{
                                store.setState({{ currentTime: {frame_ms}, isPlaying: false }});
                                return 'set_via_zustand';
                            }}
                        }}
                    }}
                    
                    // Method 3: Find via all window properties
                    for (const key of Object.getOwnPropertyNames(window)) {{
                        try {{
                            const val = window[key];
                            if (val && typeof val === 'object' && typeof val.getState === 'function') {{
                                const state = val.getState();
                                if (typeof state.currentTime === 'number') {{
                                    val.setState({{ currentTime: {frame_ms}, isPlaying: false }});
                                    return 'set_via_window.' + key;
                                }}
                            }}
                        }} catch(e) {{}}
                    }}
                    return 'store_not_found';
                }}
            """)
            print(f"   [{label}] store: {result}")
            await page.wait_for_timeout(500)
            await page.screenshot(path=f"{OUT_DIR}/06_{label}.png")
            print(f"   Screenshot: 06_{label}.png")

        await browser.close()
        print(f"\n✅ Done. Frames in {OUT_DIR}")

asyncio.run(main())
