import asyncio, os, base64
from playwright.async_api import async_playwright

STRETCH_URL = "http://localhost:8771/"
STRETCH_FILE = "/home/ubuntu/eya_pipeline/output/eya_test_blendshape.stretch"
OUT_DIR = "/home/ubuntu/eya_pipeline/output/pw_frames2"
os.makedirs(OUT_DIR, exist_ok=True)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage',
                  '--enable-webgl', '--use-gl=swiftshader', '--ignore-gpu-blocklist']
        )
        ctx = await browser.new_context(viewport={'width': 1400, 'height': 900})
        page = await ctx.new_page()

        print("Loading Stretchy...")
        await page.goto(STRETCH_URL, wait_until='networkidle', timeout=20000)
        await page.wait_for_timeout(2000)

        # Open file
        toolbar_btns = await page.locator('header button').all()
        if len(toolbar_btns) >= 3:
            await toolbar_btns[2].click()
            await page.wait_for_timeout(800)

        file_input = page.locator('input[type="file"]').first
        if await file_input.count() > 0:
            await file_input.set_input_files(STRETCH_FILE)
            await page.wait_for_timeout(800)

        # Close dialog via Escape
        await page.keyboard.press('Escape')
        await page.wait_for_timeout(2000)

        # Switch to Animation
        await page.evaluate("""
            () => {
                for (const btn of document.querySelectorAll('button')) {
                    if (btn.textContent.trim() === 'Animation') { btn.click(); return; }
                }
            }
        """)
        await page.wait_for_timeout(500)

        # Select animation
        await page.evaluate("""
            () => {
                for (const el of document.querySelectorAll('*')) {
                    if (el.children.length === 0 && el.textContent.includes('eYa BIG SMILE TEST')) {
                        el.click(); return 'clicked';
                    }
                }
            }
        """)
        await page.wait_for_timeout(500)

        # Screenshot at rest (frame 0)
        await page.screenshot(path=f"{OUT_DIR}/01_rest_frame0.png")
        print("Screenshot: 01_rest_frame0.png")

        # Click on the timeline at ~50% (frame 24, peak of animation)
        # From previous screenshot: timeline row is at y≈819, x range ≈ 375-1040
        # Frame 24 of 48 = 50% = x ≈ 375 + (1040-375)*0.5 = 375 + 332 = 707
        await page.mouse.click(707, 819)
        await page.wait_for_timeout(300)
        await page.screenshot(path=f"{OUT_DIR}/02_peak_frame24.png")
        print("Screenshot: 02_peak_frame24.png")

        # Click at 25% (frame 12)
        await page.mouse.click(540, 819)
        await page.wait_for_timeout(300)
        await page.screenshot(path=f"{OUT_DIR}/03_frame12.png")
        print("Screenshot: 03_frame12.png")

        # Click at 75% (frame 36)
        await page.mouse.click(875, 819)
        await page.wait_for_timeout(300)
        await page.screenshot(path=f"{OUT_DIR}/04_frame36.png")
        print("Screenshot: 04_frame36.png")

        # Now try Play button and capture during playback
        play_btn = page.locator('[aria-label="Play"], button[title="Play"]').first
        if await play_btn.count() == 0:
            # Find by position — play button is the triangle icon in timeline controls
            await page.mouse.click(282, 772)  # Play button position from prev screenshot
        else:
            await play_btn.click()
        
        # Capture frames during playback
        for i, delay in enumerate([200, 400, 600, 800, 1000]):
            await page.wait_for_timeout(200)
            await page.screenshot(path=f"{OUT_DIR}/05_playing_{i:02d}.png")
        
        print(f"\n✅ Frames saved to {OUT_DIR}")
        await browser.close()

asyncio.run(main())
