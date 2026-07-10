// eYa AutoLive2D — Stretchy Studio Full Pipeline Script
// Version: 0.2
// Generated: 2026-07-09 08:00:47

(async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));

  // ── Step: load_psd ──────────────────────────
  console.log('STEP: load_psd');
  (async () => {
    const resp = await fetch('/eya_correct.psd');
    const blob = await resp.blob();
    const fname = '/eya_correct.psd'.split('/').pop();
    const file = new File([blob], fname, { type: 'application/octet-stream' });
    const input = document.querySelector("input[type='file']");
    if (!input) { console.error('INPUT NOT FOUND: input[type='file']'); return; }
    const dt = new DataTransfer();
    dt.items.add(file);
    Object.defineProperty(input, 'files', { value: dt.files, writable: false });
    input.dispatchEvent(new Event('change', { bubbles: true }));
    console.log('FILE INJECTED:', fname, file.size, 'bytes');
  })();
  await sleep(2000);

  // ── Step: click_continue ──────────────────────────
  console.log('STEP: click_continue');
  const btns = Array.from(document.querySelectorAll('button'));
  const btn = btns.find(b => b.textContent.includes('Continue'));
  if (btn) {
    btn.click();
    console.log('CLICKED:', 'Continue');
  } else {
    console.error('BUTTON NOT FOUND: Continue');
    console.log('Available buttons:', btns.map(b => b.textContent.trim()).join(' | '));
  }
  await sleep(1500);

  // ── Step: click_next_reorder ──────────────────────────
  console.log('STEP: click_next_reorder');
  const btns = Array.from(document.querySelectorAll('button'));
  const btn = btns.find(b => b.textContent.includes('Next: Adjust Joints →'));
  if (btn) {
    btn.click();
    console.log('CLICKED:', 'Next: Adjust Joints →');
  } else {
    console.error('BUTTON NOT FOUND: Next: Adjust Joints →');
    console.log('Available buttons:', btns.map(b => b.textContent.trim()).join(' | '));
  }
  await sleep(2000);

  // ── Step: click_next_params ──────────────────────────
  console.log('STEP: click_next_params');
  const btns = Array.from(document.querySelectorAll('button'));
  const btn = btns.find(b => b.textContent.includes('Next: Setup Parameters →'));
  if (btn) {
    btn.click();
    console.log('CLICKED:', 'Next: Setup Parameters →');
  } else {
    console.error('BUTTON NOT FOUND: Next: Setup Parameters →');
    console.log('Available buttons:', btns.map(b => b.textContent.trim()).join(' | '));
  }
  await sleep(3000);

  // ── Step: click_done ──────────────────────────
  console.log('STEP: click_done');
  const btns = Array.from(document.querySelectorAll('button'));
  const btn = btns.find(b => b.textContent.includes('Done'));
  if (btn) {
    btn.click();
    console.log('CLICKED:', 'Done');
  } else {
    console.error('BUTTON NOT FOUND: Done');
    console.log('Available buttons:', btns.map(b => b.textContent.trim()).join(' | '));
  }
  await sleep(2000);

  console.log('PIPELINE COMPLETE');
})();