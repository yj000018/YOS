// ==UserScript==
// @name         yOS Memory Panel
// @namespace    https://yos.ai
// @version      1.1.0
// @description  Floating yOS panel — Mémoriser & Hydrater on any page, CSP-safe
// @author       Yannick Jolliet / Y-OS
// @match        *://*/*
// @grant        GM_xmlhttpRequest
// @grant        GM_setValue
// @grant        GM_getValue
// @grant        GM_addStyle
// @connect      yos-voice-vision.vercel.app
// @run-at       document-idle
// ==/UserScript==

(function () {
  'use strict';

  // ─── Config ────────────────────────────────────────────────────────────────
  const VIVI_BASE = 'https://yos-voice-vision.vercel.app';
  const INTAKE_URL = VIVI_BASE + '/api/intake';
  const CONTEXT_URL = VIVI_BASE + '/api/context-builder';

  // ─── State ─────────────────────────────────────────────────────────────────
  let panelVisible = false;
  let isProcessing = false;

  // ─── Shadow DOM host — bypasses page CSP entirely ─────────────────────────
  const host = document.createElement('div');
  host.id = 'yos-panel-host';
  host.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:2147483647;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;';

  // Use Shadow DOM so the panel's styles are fully isolated from the page CSP
  const shadow = host.attachShadow({ mode: 'open' });

  // ─── Inject styles into Shadow DOM (not the page — bypasses CSP) ──────────
  const styleEl = document.createElement('style');
  styleEl.textContent = `
    * { box-sizing: border-box; margin: 0; padding: 0; }

    #toggle {
      width: 48px; height: 48px; border-radius: 50%;
      background: linear-gradient(135deg, #0f1117 0%, #1a1f2e 100%);
      border: 1px solid rgba(79,110,247,0.4);
      cursor: pointer; display: flex; align-items: center; justify-content: center;
      box-shadow: 0 4px 20px rgba(79,110,247,0.3), 0 0 0 1px rgba(255,255,255,0.05);
      transition: all 0.2s; font-size: 20px; user-select: none;
    }
    #toggle:hover { border-color: rgba(79,110,247,0.8); box-shadow: 0 4px 24px rgba(79,110,247,0.5); transform: scale(1.05); }

    #menu {
      position: absolute; bottom: 58px; right: 0;
      background: #0f1117; border: 1px solid rgba(255,255,255,0.1);
      border-radius: 16px; padding: 12px; min-width: 230px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.6);
      display: none; flex-direction: column; gap: 8px;
    }
    #menu.open { display: flex; animation: fadein 0.15s ease; }

    @keyframes fadein { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:translateY(0); } }

    .header {
      display: flex; align-items: center; gap: 8px;
      padding: 4px 4px 8px; border-bottom: 1px solid rgba(255,255,255,0.06); margin-bottom: 4px;
    }
    .dot { width: 6px; height: 6px; border-radius: 50%; background: #4f6ef7; }
    .title { color: rgba(255,255,255,0.9); font-size: 12px; font-weight: 600; letter-spacing: 0.05em; }
    .url-label { color: rgba(255,255,255,0.3); font-size: 10px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 190px; }

    .btn {
      display: flex; align-items: center; gap: 10px;
      padding: 10px 12px; border-radius: 10px;
      border: 1px solid rgba(255,255,255,0.08);
      background: rgba(255,255,255,0.03);
      cursor: pointer; transition: all 0.15s;
      color: rgba(255,255,255,0.85); font-size: 13px; font-weight: 500;
      width: 100%; text-align: left;
    }
    .btn:hover { background: rgba(255,255,255,0.07); border-color: rgba(255,255,255,0.15); }
    .btn.mem:hover { background: rgba(79,110,247,0.15); border-color: rgba(79,110,247,0.3); }
    .btn.hyd:hover { background: rgba(34,211,238,0.1); border-color: rgba(34,211,238,0.25); }
    .btn.vivi:hover { background: rgba(167,139,250,0.1); border-color: rgba(167,139,250,0.25); }

    .icon { font-size: 16px; width: 20px; text-align: center; flex-shrink: 0; }
    .label { display: block; line-height: 1.2; }
    .sub { display: block; font-size: 10px; color: rgba(255,255,255,0.4); font-weight: 400; margin-top: 1px; }

    .divider { height: 1px; background: rgba(255,255,255,0.06); }

    .status { padding: 8px 12px; border-radius: 8px; font-size: 11px; text-align: center; display: none; }
    .status.show { display: block; }
    .status.loading { background: rgba(79,110,247,0.1); color: rgba(79,110,247,0.9); border: 1px solid rgba(79,110,247,0.2); }
    .status.ok { background: rgba(34,197,94,0.1); color: rgba(34,197,94,0.9); border: 1px solid rgba(34,197,94,0.2); }
    .status.err { background: rgba(239,68,68,0.1); color: rgba(239,68,68,0.9); border: 1px solid rgba(239,68,68,0.2); }

    .ctx-out {
      background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07);
      border-radius: 8px; padding: 8px 10px; font-size: 10px; color: rgba(255,255,255,0.6);
      max-height: 120px; overflow-y: auto; white-space: pre-wrap; display: none; line-height: 1.5;
    }
    .ctx-out.show { display: block; }
  `;
  shadow.appendChild(styleEl);

  // ─── Panel HTML ────────────────────────────────────────────────────────────
  const panel = document.createElement('div');
  panel.innerHTML = `
    <div id="menu">
      <div class="header">
        <div class="dot"></div>
        <span class="title">Y-OS</span>
      </div>
      <div class="url-label" id="url-label"></div>

      <button class="btn mem" id="btn-mem-page">
        <span class="icon">📥</span>
        <span><span class="label">Mémoriser page</span><span class="sub">Save this page to yOS Memory</span></span>
      </button>

      <button class="btn mem" id="btn-mem-sel">
        <span class="icon">✂️</span>
        <span><span class="label">Mémoriser sélection</span><span class="sub">Save selected text</span></span>
      </button>

      <div class="divider"></div>

      <button class="btn hyd" id="btn-hyd">
        <span class="icon">💧</span>
        <span><span class="label">Hydrater</span><span class="sub">Load yOS context → clipboard</span></span>
      </button>

      <div class="divider"></div>

      <button class="btn vivi" id="btn-vivi">
        <span class="icon">🎙</span>
        <span><span class="label">Open VIVI</span><span class="sub">Voice & Vision Interface</span></span>
      </button>

      <div class="status" id="status"></div>
      <div class="ctx-out" id="ctx-out"></div>
    </div>

    <div id="toggle" title="yOS Memory Panel">🧠</div>
  `;
  shadow.appendChild(panel);

  // ─── Append host to body ───────────────────────────────────────────────────
  // Use a MutationObserver to ensure body exists even on SPAs
  function mount() {
    if (document.body && !document.getElementById('yos-panel-host')) {
      document.body.appendChild(host);
      init();
    }
  }

  if (document.body) {
    mount();
  } else {
    const obs = new MutationObserver(() => { if (document.body) { obs.disconnect(); mount(); } });
    obs.observe(document.documentElement, { childList: true });
  }

  // ─── Init logic ────────────────────────────────────────────────────────────
  function init() {
    const toggle = shadow.getElementById('toggle');
    const menu = shadow.getElementById('menu');
    const statusEl = shadow.getElementById('status');
    const ctxOut = shadow.getElementById('ctx-out');
    const urlLabel = shadow.getElementById('url-label');

    if (urlLabel) urlLabel.textContent = location.hostname + location.pathname.slice(0, 30);

    // Toggle
    toggle && toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      panelVisible = !panelVisible;
      menu && menu.classList.toggle('open', panelVisible);
    });

    // Close on outside click — listen on document, not shadow
    document.addEventListener('click', (e) => {
      if (panelVisible && !host.contains(e.target)) {
        panelVisible = false;
        menu && menu.classList.remove('open');
      }
    });

    // ── Helpers ──
    function showStatus(msg, type) {
      if (!statusEl) return;
      statusEl.textContent = msg;
      statusEl.className = 'status show ' + type;
    }
    function hideStatus() { if (statusEl) statusEl.className = 'status'; }

    function getPageText() {
      const selectors = ['main', 'article', '[role="main"]', '.content', '#content', 'body'];
      for (const s of selectors) {
        const el = document.querySelector(s);
        if (el && el.innerText && el.innerText.length > 100) return el.innerText.slice(0, 3000);
      }
      return document.body.innerText.slice(0, 3000);
    }

    function getSelection() { return window.getSelection() ? window.getSelection().toString() : ''; }

    function detectProject() {
      const url = location.href.toLowerCase();
      if (url.includes('notion')) return 'yOS';
      if (url.includes('casatao') || url.includes('home-assistant')) return 'CasaTAO';
      if (url.includes('github') || url.includes('manus.im')) return 'yOS';
      return '';
    }

    function postIntake(payload) {
      if (isProcessing) return;
      isProcessing = true;
      showStatus('Sending to yOS Memory...', 'loading');
      GM_xmlhttpRequest({
        method: 'POST', url: INTAKE_URL,
        headers: { 'Content-Type': 'application/json' },
        data: JSON.stringify(payload),
        onload: (res) => {
          isProcessing = false;
          try {
            const d = JSON.parse(res.responseText);
            if (d.success) { showStatus('✓ Saved to Notion Inbox', 'ok'); setTimeout(hideStatus, 3000); }
            else { showStatus('Error: ' + (d.error || 'Unknown'), 'err'); }
          } catch { showStatus('Parse error', 'err'); }
        },
        onerror: () => { isProcessing = false; showStatus('Connection error', 'err'); }
      });
    }

    // ── Mémoriser page ──
    shadow.getElementById('btn-mem-page') && shadow.getElementById('btn-mem-page').addEventListener('click', () => {
      postIntake({
        type: 'url',
        content: 'URL: ' + location.href + '\n\nTitle: ' + document.title + '\n\nContent:\n' + getPageText(),
        title: '[WEB] ' + document.title.slice(0, 80),
        source_app: 'Web',
        project: detectProject() || undefined,
        tags: ['web', 'capture'],
        priority: 'Medium',
      });
    });

    // ── Mémoriser sélection ──
    shadow.getElementById('btn-mem-sel') && shadow.getElementById('btn-mem-sel').addEventListener('click', () => {
      const sel = getSelection();
      if (!sel) { showStatus('No text selected', 'err'); setTimeout(hideStatus, 2000); return; }
      postIntake({
        type: 'text',
        content: sel,
        title: '[SEL] ' + sel.slice(0, 60),
        source_app: 'Web',
        tags: ['selection', 'capture'],
        priority: 'Medium',
      });
    });

    // ── Hydrater ──
    shadow.getElementById('btn-hyd') && shadow.getElementById('btn-hyd').addEventListener('click', () => {
      if (isProcessing) return;
      isProcessing = true;
      showStatus('Loading yOS context...', 'loading');
      if (ctxOut) ctxOut.className = 'ctx-out';
      GM_xmlhttpRequest({
        method: 'POST', url: CONTEXT_URL,
        headers: { 'Content-Type': 'application/json' },
        data: JSON.stringify({ type: 'context_request', mode: 'voice', project: detectProject() || undefined }),
        onload: (res) => {
          isProcessing = false;
          try {
            const d = JSON.parse(res.responseText);
            hideStatus();
            if (ctxOut) { ctxOut.textContent = d.context || 'No context'; ctxOut.className = 'ctx-out show'; }
            const full = (d.instructions || '') + '\n\n' + (d.context || '');
            navigator.clipboard.writeText(full).then(() => {
              showStatus('✓ Context copied (' + (d.sources || 0) + ' items)', 'ok');
              setTimeout(hideStatus, 3000);
            }).catch(() => {
              showStatus('✓ Context loaded (' + (d.sources || 0) + ' items)', 'ok');
              setTimeout(hideStatus, 3000);
            });
          } catch { showStatus('Parse error', 'err'); }
        },
        onerror: () => { isProcessing = false; showStatus('Connection error', 'err'); }
      });
    });

    // ── Open VIVI ──
    shadow.getElementById('btn-vivi') && shadow.getElementById('btn-vivi').addEventListener('click', () => {
      window.open(VIVI_BASE, '_blank', 'width=420,height=720,left=80,top=80');
      panelVisible = false;
      menu && menu.classList.remove('open');
    });
  }

})();
