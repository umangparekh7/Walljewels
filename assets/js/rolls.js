/* ============================================================================
   WALL JEWELS — Wallpaper Rolls runtime
   ----------------------------------------------------------------------------
   Enhancement only: every rolls page renders complete without this file.
   Part 1 is pure (calculation, formatting, sorting, search) and is shared
   with the unit tests; Part 2 is the DOM runtime and only runs in a browser.
   Contract: tools/rolls/SPEC.md
   ========================================================================== */

/* ---------------------------------------------------------------- Part 1 —
   pure functions, exported as window.WJRolls (browser) / module.exports (node)
   ---------------------------------------------------------------------- */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  root.WJRolls = Object.assign(root.WJRolls || {}, api);
})(typeof window !== 'undefined' ? window : globalThis, function () {
  'use strict';

  const MAX_INCHES = 2400;
  const SQ_IN_PER_SQ_FT = 144;
  const ROUNDING_GUARD = 1e-9; /* exact multiples (90 / 45) must not tip over to 3 */
  const MESSAGES = {
    width: 'Enter a wall width in inches',
    height: 'Enter a wall height in inches',
    range: 'Enter a value between 1 and 2400',
    collection: 'Choose a collection'
  };

  /* One dimension in inches. Accepts numbers or strings; decimals allowed. */
  function parseDimension(value, field) {
    const label = field === 'height' ? 'height' : 'width';
    const raw = typeof value === 'string' ? value.trim() : value;
    if (raw === '' || raw === null || raw === undefined) {
      return { ok: false, error: MESSAGES[label], field: label };
    }
    const n = typeof raw === 'number' ? raw : Number(raw);
    if (!Number.isFinite(n) || n <= 0 || n > MAX_INCHES) {
      return { ok: false, error: MESSAGES.range, field: label };
    }
    return { ok: true, value: n, field: label };
  }

  function isUsableCollection(c) {
    return !!c && typeof c === 'object' &&
      Number.isFinite(Number(c.coverage)) && Number(c.coverage) > 0 &&
      Number.isFinite(Number(c.rollPrice)) && Number(c.rollPrice) >= 0;
  }

  /* area = w × h / 144 ; rolls = ceil(area / coverage) ; cost = rolls × rollPrice */
  function calculate(widthIn, heightIn, collection) {
    const w = parseDimension(widthIn, 'width');
    if (!w.ok) return { ok: false, error: w.error, field: 'width' };
    const h = parseDimension(heightIn, 'height');
    if (!h.ok) return { ok: false, error: h.error, field: 'height' };
    if (!isUsableCollection(collection)) {
      return { ok: false, error: MESSAGES.collection, field: 'collection' };
    }
    const coverage = Number(collection.coverage);
    const rollPrice = Number(collection.rollPrice);
    const area = (w.value * h.value) / SQ_IN_PER_SQ_FT;
    const rolls = Math.ceil(area / coverage - ROUNDING_GUARD);
    const cost = rolls * rollPrice;
    return {
      ok: true,
      width: w.value,
      height: h.value,
      area,
      rolls,
      cost,
      coverage,
      rollPrice,
      rollSize: Number.isFinite(Number(collection.rollSize)) ? Number(collection.rollSize) : null
    };
  }

  /* ₹5,940 · ₹1,42,500 — Indian grouping, no decimals. Never "NaN". */
  function formatINR(n) {
    const v = Math.round(Number(n));
    if (!Number.isFinite(v)) return '—';
    let digits = String(Math.abs(v));
    if (digits.length > 3) {
      const last3 = digits.slice(-3);
      const rest = digits.slice(0, -3).replace(/\B(?=(\d{2})+(?!\d))/g, ',');
      digits = rest + ',' + last3;
    }
    return (v < 0 ? '−' : '') + '₹' + digits;
  }

  /* Up to two decimals, no trailing zeros: 90 → "90", 90.0833 → "90.08". */
  function formatArea(n) {
    const v = Math.round(Number(n) * 100) / 100;
    return Number.isFinite(v) ? String(v) : '—';
  }

  /* "6877/2" → "6877-2", " 12 " → "12" */
  function slugify(str) {
    return String(str === null || str === undefined ? '' : str)
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '');
  }

  /* Numeric-aware compare: 2 < 10, "5314/9" < "5314/10". */
  function naturalCompare(a, b) {
    const sa = String(a === null || a === undefined ? '' : a).toLowerCase();
    const sb = String(b === null || b === undefined ? '' : b).toLowerCase();
    const ta = sa.match(/\d+|\D+/g) || [];
    const tb = sb.match(/\d+|\D+/g) || [];
    const len = Math.min(ta.length, tb.length);
    for (let i = 0; i < len; i++) {
      const x = ta[i], y = tb[i];
      const bothNumeric = /^\d/.test(x) && /^\d/.test(y);
      if (bothNumeric) {
        const diff = Number(x) - Number(y);
        if (diff) return diff < 0 ? -1 : 1;
        if (x.length !== y.length) return x.length < y.length ? -1 : 1; /* "007" after "7" */
      } else if (x !== y) {
        return x < y ? -1 : 1;
      }
    }
    if (ta.length !== tb.length) return ta.length < tb.length ? -1 : 1;
    return 0;
  }

  /* Returns a NEW array ordered by designNumber (natural order), ties by id. */
  function sortDesigns(designs) {
    if (!Array.isArray(designs)) return [];
    return designs.slice().sort((a, b) =>
      naturalCompare(a && a.designNumber, b && b.designNumber) ||
      naturalCompare(a && a.id, b && b.id));
  }

  /* Search key: drop spaces, "-", "/", "." and lower-case ("6877/2" ≡ "6877-2"). */
  function normalise(s) {
    return String(s === null || s === undefined ? '' : s).toLowerCase().replace(/[\s\-/.]+/g, '');
  }

  /* Rank of a design against a query: 3 exact, 2 prefix, 1 contains, 0 none.
     Truthy means "matches"; higher sorts first. Empty query matches everything. */
  function matchesQuery(design, q) {
    const query = normalise(q);
    if (!query) return 1;
    const number = normalise(design && design.designNumber);
    if (!number) return 0;
    if (number === query) return 3;
    if (number.startsWith(query)) return 2;
    if (number.includes(query)) return 1;
    return 0;
  }

  return { calculate, formatINR, formatArea, slugify, sortDesigns, matchesQuery, parseDimension, naturalCompare, normalise };
});

/* ---------------------------------------------------------------- Part 2 —
   DOM runtime (browser only)
   ---------------------------------------------------------------------- */
(function () {
  'use strict';
  if (typeof document === 'undefined') return;

  const WJ = window.WJRolls;
  const $ = (s, c) => (c || document).querySelector(s);
  const $$ = (s, c) => [...(c || document).querySelectorAll(s)];
  const ROOT = document.documentElement.dataset.root || '';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const RAW = (window.WJ_ROLLS && typeof window.WJ_ROLLS === 'object') ? window.WJ_ROLLS : {};
  const CONTACT = Object.assign(
    { whatsapp: '919677042903', email: 'info@walljewels.com', phone: '+91 98400 64205' },
    (RAW.contact && typeof RAW.contact === 'object') ? RAW.contact : {}
  );
  const SITE = /(^|\.)walljewels\.in$/i.test(location.hostname) ? location.origin : 'https://www.walljewels.in';
  const BATCH = 48;
  const SWIPE_MIN_PX = 45;
  const CLOSE_MS = 420; /* matches --beat comfortably; overlay hides after its fade */
  const DOUBLE_TAP_MS = 320;
  const DOUBLE_TAP_PX = 30;
  const FOCUSABLE = 'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';
  const ICON = {
    close: '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true" width="22" height="22"><path d="M6 6 L18 18 M18 6 L6 18" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
    prev: '<svg width="18" height="18" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M14 8 H2 M7 3 L2 8 L7 13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    next: '<svg width="18" height="18" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M2 8 H14 M9 3 L14 8 L9 13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    minus: '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true" width="22" height="22"><path d="M6 12 H18" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
    plus: '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true" width="22" height="22"><path d="M6 12 H18 M12 6 V18" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
    fit: '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true" width="22" height="22"><path d="M4 9 V4 H9 M15 4 H20 V9 M20 15 V20 H15 M9 20 H4 V15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    full: '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true" width="22" height="22"><path d="M9 4 H4 V9 M15 4 H20 V9 M20 15 V20 H15 M4 15 V20 H9 M4 4 L10 10 M20 4 L14 10 M20 20 L14 14 M4 20 L10 14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    pdf: '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true" width="22" height="22"><path d="M14 4 H20 V10 M20 4 L11 13 M18 14 V19 H5 V6 H10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    arrow: '<svg width="18" height="10" viewBox="0 0 18 10" fill="none" aria-hidden="true"><path d="M0 5 H16 M12 1 L16 5 L12 9" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
  };

  /* ---------------- helpers ---------------- */
  const esc = (v) => String(v === null || v === undefined ? '' : v)
    .replace(/[&<>"']/g, (ch) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]));
  const asset = (p) => p ? ROOT + String(p).replace(/^\/+/, '') : '';
  const absolute = (p) => SITE + '/' + String(p || '').replace(/^\/+/, '');
  const inr = WJ.formatINR;
  const fmtArea = WJ.formatArea;
  const fmtIn = (n) => String(Math.round(Number(n) * 100) / 100);
  const fmtDims = (w, h) => `${fmtIn(w)}″ × ${fmtIn(h)}″`;
  const plural = (n, one, many) => `${n} ${n === 1 ? one : many}`;
  const num = (v, fallback) => (Number.isFinite(Number(v)) && v !== null && v !== '') ? Number(v) : fallback;
  const pad3 = (n) => String(n).padStart(3, '0');
  const el = (html) => { const t = document.createElement('template'); t.innerHTML = html.trim(); return t.content.firstElementChild; };
  const isVisible = (n) => n.getClientRects().length > 0;
  const focusEl = (n) => { if (n && n.isConnected && typeof n.focus === 'function') n.focus({ preventScroll: true }); };

  let toastTimer;
  function toast(text) {
    let t = $('.toast');
    if (!t) {
      t = el('<div class="toast" role="status"><span class="dot"></span><span class="toast__msg"></span></div>');
      document.body.appendChild(t);
    }
    $('.toast__msg', t).textContent = text;
    t.classList.add('is-on');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => t.classList.remove('is-on'), 2600);
  }

  /* ---------------- data ---------------- */
  const COLLECTIONS = (Array.isArray(RAW.collections) ? RAW.collections : [])
    .filter((c) => c && typeof c === 'object' && c.slug && c.published !== false)
    .slice()
    .sort((a, b) => (num(a.sort, 999) - num(b.sort, 999)) || WJ.naturalCompare(a.name, b.name));
  const collByKey = new Map();
  COLLECTIONS.forEach((c) => { collByKey.set(String(c.slug), c); if (c.id) collByKey.set(String(c.id), c); });
  const collOf = (d) => d ? collByKey.get(String(d.collectionId)) : null;

  const DESIGNS = [];
  (function buildDesigns() {
    const raw = Array.isArray(RAW.designs) ? RAW.designs : [];
    COLLECTIONS.forEach((c) => {
      const mine = raw.filter((d) => d && typeof d === 'object' && d.id && d.designNumber !== undefined && d.designNumber !== null &&
        (String(d.collectionId) === String(c.id) || String(d.collectionId) === String(c.slug)));
      WJ.sortDesigns(mine).forEach((d) => {
        const slug = d.slug || WJ.slugify(d.designNumber);
        DESIGNS.push(Object.assign({}, d, { slug, url: d.url || `wallpaper-rolls/${c.slug}/${slug}/` }));
      });
    });
  })();
  const designById = new Map(DESIGNS.map((d) => [String(d.id), d]));
  const designIndex = new Map(DESIGNS.map((d, i) => [String(d.id), i]));

  function findDesign(collection, designNumber) {
    if (!collection) return null;
    const key = WJ.normalise(designNumber);
    if (!key) return null;
    return DESIGNS.find((d) => collOf(d) === collection && WJ.normalise(d.designNumber) === key) || null;
  }
  const designAlt = (d, c) => `${(c && c.name) || 'Wall Jewels'} wallpaper design ${d.designNumber}`;
  const collectionFacts = (c) => {
    if (!c) return '';
    const parts = [];
    if (num(c.rollSize)) parts.push(`${c.rollSize} sq.ft roll`);
    if (num(c.coverage)) parts.push(`approx. ${c.coverage} sq.ft coverage`);
    if (num(c.rollPrice) !== undefined) parts.push(`${inr(c.rollPrice)} per roll`);
    if (num(c.pricePerSqFt)) parts.push(`${inr(c.pricePerSqFt)} per sq.ft`);
    return parts.join(' · ');
  };

  /* ---------------- card markup (shared with the generator, SPEC §4.1.3) ---------------- */
  function cardHTML(d) {
    const c = collOf(d) || {};
    const thumb = asset(d.thumbnail || d.web || d.image);
    const web = d.web ? asset(d.web) : '';
    const srcset = web ? ` srcset="${esc(thumb)} 480w, ${esc(web)} 1200w" sizes="(max-width: 600px) 50vw, (max-width: 1100px) 33vw, 25vw"` : '';
    const size = (num(d.width) && num(d.height)) ? ` width="${esc(d.width)}" height="${esc(d.height)}"` : '';
    return `<a class="rolls-card" href="${esc(asset(d.url))}" data-design-id="${esc(d.id)}" data-no-lightbox>
  <span class="rolls-card__media"><img src="${esc(thumb)}"${srcset}${size} alt="${esc(designAlt(d, c))}" loading="lazy" decoding="async"></span>
  <span class="rolls-card__body"><span class="rolls-card__no">Design No. ${esc(d.designNumber)}</span><span class="rolls-card__coll">${esc(c.name || '')}</span></span>
</a>`;
  }

  /* ---------------- overlay stack: scroll lock, Esc, Tab trap, focus return ---------------- */
  const overlays = [];
  function pushOverlay(entry) {
    entry.opener = entry.opener || document.activeElement;
    overlays.push(entry);
    document.body.style.overflow = 'hidden';
  }
  function popOverlay(entry) {
    const i = overlays.indexOf(entry);
    if (i > -1) overlays.splice(i, 1);
    if (!overlays.length) document.body.style.overflow = '';
    focusEl(entry.opener);
  }
  function trapTab(container, e) {
    const items = $$(FOCUSABLE, container).filter(isVisible);
    if (!items.length) { e.preventDefault(); return; }
    const first = items[0], last = items[items.length - 1];
    const active = document.activeElement;
    if (e.shiftKey && (active === first || !container.contains(active))) { e.preventDefault(); focusEl(last); }
    else if (!e.shiftKey && (active === last || !container.contains(active))) { e.preventDefault(); focusEl(first); }
  }
  document.addEventListener('keydown', (e) => {
    const top = overlays[overlays.length - 1];
    if (!top) return;
    if (e.key === 'Tab') { trapTab(top.el, e); return; }
    if (e.key === 'Escape') e.stopPropagation(); /* app.js's window handler would unlock body scroll */
    if (top.onKey) top.onKey(e);
  });
  /* JS-built overlays live hidden (display:none) until used; the class drives the fade. */
  function showOverlay(node) {
    node.hidden = false;
    node.removeAttribute('inert');
    void node.offsetWidth; /* commit display before the class so the fade still runs — no rAF, which stalls in background tabs */
    node.classList.add('is-open');
  }
  function hideOverlay(node) {
    node.classList.remove('is-open');
    node.setAttribute('inert', '');
    const done = () => { if (!node.classList.contains('is-open')) node.hidden = true; };
    if (reduced) done(); else setTimeout(done, CLOSE_MS);
  }
  /* Horizontal swipe on touch (mirrors the lightbox in app.js). */
  function onSwipe(node, handler, allowed) {
    let sx = 0, sy = 0;
    node.addEventListener('touchstart', (e) => { sx = e.changedTouches[0].clientX; sy = e.changedTouches[0].clientY; }, { passive: true });
    node.addEventListener('touchend', (e) => {
      if (allowed && !allowed()) return;
      const dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy;
      if (Math.abs(dx) > SWIPE_MIN_PX && Math.abs(dx) > Math.abs(dy) * 1.5) handler(dx < 0 ? 1 : -1);
    }, { passive: true });
  }

  /* ---------------- zoomable stage (catalogue viewer + zoom overlay) ----------------
     The stage scrolls on both axes; the image is sized to fitWidth × scale.
     Pinch via pointer events, double-tap 1↔2, wheel (ctrl+wheel, or plain when allowed). */
  function createZoomStage(stage, img, opts) {
    const steps = opts.steps || [1, 1.5, 2, 3];
    const min = opts.min || 1, max = opts.max || 4;
    let scale = 1, fitW = 0;
    stage.style.touchAction = 'pan-x pan-y';

    function measure() {
      const natW = img.naturalWidth || num(img.getAttribute('width'), 0);
      const natH = img.naturalHeight || num(img.getAttribute('height'), 0);
      const sw = stage.clientWidth, sh = stage.clientHeight;
      fitW = (opts.fit === 'contain' && natW && natH) ? Math.min(sw, sh * natW / natH) : sw;
      if (!fitW) fitW = sw;
    }
    function apply() {
      img.style.width = `${Math.round(fitW * scale)}px`;
      img.style.maxWidth = 'none';
      img.style.height = 'auto';
      stage.classList.toggle('is-zoomed', scale > 1.001);
      if (opts.onScale) opts.onScale(scale);
    }
    function setScale(next, anchor) {
      if (!fitW) measure();
      const s = Math.min(max, Math.max(min, next));
      const ax = anchor ? anchor.x : stage.clientWidth / 2;
      const ay = anchor ? anchor.y : stage.clientHeight / 2;
      const cx = (stage.scrollLeft + ax) / scale, cy = (stage.scrollTop + ay) / scale;
      scale = s;
      apply();
      stage.scrollLeft = cx * scale - ax;
      stage.scrollTop = cy * scale - ay;
    }
    const stepIn = () => setScale(steps.find((s) => s > scale + 0.001) || max);
    const stepOut = () => setScale([...steps].reverse().find((s) => s < scale - 0.001) || min);
    const reset = () => { scale = 1; measure(); apply(); stage.scrollLeft = 0; stage.scrollTop = 0; };
    const point = (e) => { const r = stage.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; };

    /* pinch + drag-pan + double-tap */
    const pointers = new Map();
    let pinch = null, drag = null, lastTap = null;
    stage.addEventListener('pointerdown', (e) => {
      pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
      if (pointers.size === 2) {
        const [a, b] = [...pointers.values()];
        pinch = { dist: Math.hypot(a.x - b.x, a.y - b.y), scale };
        drag = null;
      } else if (e.pointerType === 'mouse' && scale > 1.001 && e.button === 0) {
        drag = { x: e.clientX, y: e.clientY, sl: stage.scrollLeft, st: stage.scrollTop };
        try { stage.setPointerCapture(e.pointerId); } catch (err) { /* not critical */ }
        e.preventDefault();
      }
    });
    stage.addEventListener('pointermove', (e) => {
      if (!pointers.has(e.pointerId)) return;
      pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
      if (pinch && pointers.size === 2) {
        const [a, b] = [...pointers.values()];
        const dist = Math.hypot(a.x - b.x, a.y - b.y);
        if (!dist) return;
        const r = stage.getBoundingClientRect();
        setScale(pinch.scale * dist / pinch.dist, { x: (a.x + b.x) / 2 - r.left, y: (a.y + b.y) / 2 - r.top });
        e.preventDefault();
      } else if (drag) {
        stage.scrollLeft = drag.sl - (e.clientX - drag.x);
        stage.scrollTop = drag.st - (e.clientY - drag.y);
      }
    });
    const release = (e) => {
      const was = pointers.get(e.pointerId);
      pointers.delete(e.pointerId);
      if (pointers.size < 2) pinch = null;
      if (drag && e.pointerType === 'mouse') drag = null;
      if (e.type === 'pointerup' && e.pointerType === 'touch' && was && !pinch) {
        const now = Date.now();
        if (lastTap && now - lastTap.t < DOUBLE_TAP_MS && Math.hypot(lastTap.x - e.clientX, lastTap.y - e.clientY) < DOUBLE_TAP_PX) {
          setScale(scale > 1.001 ? 1 : 2, point(e));
          lastTap = null;
        } else {
          lastTap = { t: now, x: e.clientX, y: e.clientY };
        }
      }
    };
    stage.addEventListener('pointerup', release);
    stage.addEventListener('pointercancel', release);
    stage.addEventListener('dblclick', (e) => { e.preventDefault(); setScale(scale > 1.001 ? 1 : 2, point(e)); });
    stage.addEventListener('wheel', (e) => {
      if (opts.wheel !== 'always' && !e.ctrlKey) return;
      e.preventDefault();
      setScale(scale * Math.exp(-e.deltaY * 0.0015), point(e));
    }, { passive: false });
    addEventListener('resize', () => { if (isVisible(stage)) { measure(); apply(); } }, { passive: true });

    return { setScale, stepIn, stepOut, reset, measure, apply, get scale() { return scale; } };
  }

  /* ================================================================
     ZOOM OVERLAY  .rolls-zoom  (design page figure, quick-view image)
     ================================================================ */
  let zoom = null;
  function ensureZoom() {
    if (zoom) return zoom;
    const node = el(`<div class="rolls-zoom" role="dialog" aria-modal="true" aria-label="Design zoom" hidden inert data-lenis-prevent>
  <div class="rolls-zoom__bar">
    <span class="rolls-zoom__caption"></span>
    <div class="rolls-zoom__tools">
      <button class="tool" type="button" data-zoom-action="out" aria-label="Zoom out">${ICON.minus}</button>
      <button class="tool" type="button" data-zoom-action="in" aria-label="Zoom in">${ICON.plus}</button>
      <button class="tool" type="button" data-zoom-action="fit" aria-label="Fit to screen">${ICON.fit}</button>
      <button class="tool rolls-zoom__close" type="button" data-zoom-action="close" aria-label="Close zoom">${ICON.close}</button>
    </div>
  </div>
  <div class="rolls-zoom__stage is-loading" tabindex="0" aria-label="Zoomed design — scroll or pinch to zoom, drag to pan"><img class="rolls-zoom__img" alt="" decoding="async"></div>
  <p class="rolls-zoom__hint">Scroll or pinch to zoom · double-tap to toggle · Esc to close</p>
</div>`);
    document.body.appendChild(node);
    const stage = $('.rolls-zoom__stage', node), img = $('.rolls-zoom__img', node);
    const zs = createZoomStage(stage, img, { fit: 'contain', wheel: 'always', steps: [1, 1.5, 2, 3, 4], max: 5 });
    const entry = { el: node, onKey: null };
    const close = () => { hideOverlay(node); popOverlay(entry); };
    entry.onKey = (e) => {
      if (e.key === 'Escape') { e.preventDefault(); close(); }
      else if (e.key === '+' || e.key === '=') zs.stepIn();
      else if (e.key === '-' || e.key === '_') zs.stepOut();
      else if (e.key === '0') zs.reset();
    };
    node.addEventListener('click', (e) => {
      const b = e.target.closest('[data-zoom-action]');
      if (b) {
        const a = b.dataset.zoomAction;
        if (a === 'in') zs.stepIn(); else if (a === 'out') zs.stepOut(); else if (a === 'fit') zs.reset(); else close();
        return;
      }
      if (e.target.closest('img')) e.stopPropagation(); /* keep the site-wide lightbox out of it */
    });
    img.addEventListener('load', () => { stage.classList.remove('is-loading'); img.classList.add('is-loaded'); zs.reset(); });
    img.addEventListener('error', () => { stage.classList.remove('is-loading'); stage.classList.add('is-error'); });
    zoom = { node, stage, img, zs, entry, open(src, alt, opener) {
      if (!src) return;
      stage.classList.add('is-loading'); stage.classList.remove('is-error'); img.classList.remove('is-loaded');
      img.style.width = '';
      img.alt = alt || '';
      $('.rolls-zoom__caption', node).textContent = alt || '';
      img.src = src;
      if (img.complete && img.naturalWidth) { stage.classList.remove('is-loading'); img.classList.add('is-loaded'); zs.reset(); }
      pushOverlay(Object.assign(entry, { opener: opener || document.activeElement }));
      showOverlay(node);
      focusEl(stage);
    } };
    return zoom;
  }
  const openZoom = (src, alt, opener) => ensureZoom().open(src, alt, opener);

  function initZoomTriggers() {
    $$('figure[data-no-lightbox]').forEach((fig) => {
      const img = $('img[data-full]', fig);
      if (!img) return;
      img.setAttribute('tabindex', '0');
      img.setAttribute('role', 'button');
      if (!img.getAttribute('aria-label')) img.setAttribute('aria-label', `Zoom ${img.alt || 'design'}`);
      const open = (e) => { e.preventDefault(); e.stopPropagation(); openZoom(img.dataset.full || img.currentSrc || img.src, img.alt, img); };
      fig.addEventListener('click', (e) => { if (e.target.closest('img[data-full]')) open(e); });
      img.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') open(e); });
    });
  }

  /* ================================================================
     CATALOGUE VIEWER  .rolls-viewer  (one per collection, built on first use)
     ================================================================ */
  const viewers = new Map();
  function pageSrc(slug, n, stageWidth) {
    const prefix = (stageWidth * (window.devicePixelRatio || 1)) <= 900 ? 'm' : 'p';
    return `${ROOT}assets/rolls/${slug}/pages/${prefix}${pad3(n)}.jpg`;
  }
  function buildViewer(c) {
    const total = Math.max(1, Math.round(num(c.pageCount, 1)));
    const uid = `rolls-viewer-${WJ.slugify(c.slug)}`;
    const pdf = c.catalogueFile ? asset(c.catalogueFile) : '';
    const node = el(`<div class="rolls-viewer" role="dialog" aria-modal="true" aria-labelledby="${uid}-title" hidden inert data-lenis-prevent>
  <div class="rolls-viewer__bar">
    <div class="rolls-viewer__title">
      <span class="rolls-viewer__name" id="${uid}-title">${esc(c.name)} — Catalogue</span>
      ${c.catalogueName ? `<span class="rolls-viewer__file">${esc(c.catalogueName)}</span>` : ''}
    </div>
    <div class="rolls-viewer__pager">
      <input class="rolls-viewer__page" id="${uid}-page" type="number" inputmode="numeric" min="1" max="${total}" value="1" aria-label="Page number">
      <span class="rolls-viewer__total">/ ${total}</span>
    </div>
    <div class="rolls-viewer__tools">
      <button class="tool" type="button" data-viewer-action="zoom-out" aria-label="Zoom out">${ICON.minus}</button>
      <button class="tool" type="button" data-viewer-action="zoom-in" aria-label="Zoom in">${ICON.plus}</button>
      <button class="tool" type="button" data-viewer-action="fit" aria-label="Fit to width">${ICON.fit}</button>
      <button class="tool" type="button" data-viewer-action="fullscreen" aria-label="Full screen" aria-pressed="false"${document.fullscreenEnabled ? '' : ' hidden'}>${ICON.full}</button>
      ${pdf ? `<a class="tool" data-viewer-action="pdf" href="${esc(pdf)}" target="_blank" rel="noopener" aria-label="Open the PDF in a new tab">${ICON.pdf}</a>` : ''}
      <button class="tool rolls-viewer__close" type="button" data-viewer-action="close" aria-label="Close the catalogue">${ICON.close}</button>
    </div>
  </div>
  <div class="rolls-viewer__stage is-loading" tabindex="0" aria-label="Catalogue page — arrow keys turn pages, + and − zoom"><img class="rolls-viewer__img" alt="" decoding="async"></div>
  <button class="rolls-viewer__nav rolls-viewer__nav--prev" type="button" aria-label="Previous page">${ICON.prev}</button>
  <button class="rolls-viewer__nav rolls-viewer__nav--next" type="button" aria-label="Next page">${ICON.next}</button>
  <div class="rolls-viewer__rail" aria-label="Pages"></div>
</div>`);
    const stage = $('.rolls-viewer__stage', node), img = $('.rolls-viewer__img', node);
    const pageIn = $('.rolls-viewer__page', node), rail = $('.rolls-viewer__rail', node);
    const prev = $('.rolls-viewer__nav--prev', node), next = $('.rolls-viewer__nav--next', node);
    const fsBtn = $('[data-viewer-action="fullscreen"]', node);
    const zs = createZoomStage(stage, img, { fit: 'width', wheel: 'ctrl', steps: [1, 1.5, 2, 3], max: 3 });
    let current = 0;

    /* rail thumbnails, lazy like the volume viewer in app.js */
    const frag = document.createDocumentFragment();
    for (let n = 1; n <= total; n++) {
      frag.appendChild(el(`<button class="rolls-viewer__thumb" type="button" data-page="${n}" aria-label="Page ${n}"><img data-src="${esc(`${ROOT}assets/rolls/${c.slug}/pages/t${pad3(n)}.jpg`)}" alt="" loading="lazy" decoding="async"><span class="rolls-viewer__thumbno">${n}</span></button>`));
    }
    rail.appendChild(frag);
    const railIO = new IntersectionObserver((ents) => {
      ents.forEach((en) => {
        if (!en.isIntersecting) return;
        const im = $('img', en.target);
        if (im && im.dataset.src) { im.src = im.dataset.src; delete im.dataset.src; }
        railIO.unobserve(en.target);
      });
    }, { root: rail, rootMargin: '0px 800px 0px 800px' });
    $$('.rolls-viewer__thumb', rail).forEach((t) => railIO.observe(t));

    function preload(n) {
      if (n < 1 || n > total) return;
      const im = new Image();
      im.src = pageSrc(c.slug, n, stage.clientWidth || innerWidth);
    }
    function goTo(n) {
      n = Math.min(total, Math.max(1, Math.round(num(n, 1))));
      current = n;
      stage.classList.add('is-loading'); stage.classList.remove('is-error'); img.classList.remove('is-loaded');
      img.alt = `${c.name} catalogue, page ${n}`;
      img.src = pageSrc(c.slug, n, stage.clientWidth || innerWidth);
      if (img.complete && img.naturalWidth) onLoad();
      pageIn.value = String(n);
      prev.disabled = n <= 1; next.disabled = n >= total;
      $$('.rolls-viewer__thumb', rail).forEach((t) => {
        const on = Number(t.dataset.page) === n;
        t.classList.toggle('is-current', on);
        if (on) { t.setAttribute('aria-current', 'true'); if (isVisible(rail)) t.scrollIntoView({ block: 'nearest', inline: 'center', behavior: reduced ? 'auto' : 'smooth' }); }
        else t.removeAttribute('aria-current');
      });
      stage.scrollTop = 0; stage.scrollLeft = 0;
      preload(n + 1); preload(n - 1);
    }
    function onLoad() { stage.classList.remove('is-loading'); img.classList.add('is-loaded'); zs.measure(); zs.apply(); }
    img.addEventListener('load', onLoad);
    img.addEventListener('error', () => { stage.classList.remove('is-loading'); stage.classList.add('is-error'); });

    const entry = { el: node, onKey: null };
    function close() {
      if (document.fullscreenElement === node && document.exitFullscreen) document.exitFullscreen().catch(() => {});
      hideOverlay(node);
      popOverlay(entry);
    }
    function toggleFullscreen() {
      if (!document.fullscreenEnabled) return;
      if (document.fullscreenElement === node) document.exitFullscreen().catch(() => {});
      else node.requestFullscreen().catch(() => {});
    }
    document.addEventListener('fullscreenchange', () => {
      const on = document.fullscreenElement === node;
      node.classList.toggle('is-fullscreen', on);
      if (fsBtn) { fsBtn.setAttribute('aria-pressed', String(on)); fsBtn.setAttribute('aria-label', on ? 'Exit full screen' : 'Full screen'); }
      zs.measure(); zs.apply();
    });
    entry.onKey = (e) => {
      const typing = e.target === pageIn;
      if (e.key === 'Escape') {
        e.preventDefault();
        if (document.fullscreenElement === node) { document.exitFullscreen().catch(() => {}); return; }
        close();
      } else if (!typing && e.key === 'ArrowRight') { e.preventDefault(); goTo(current + 1); }
      else if (!typing && e.key === 'ArrowLeft') { e.preventDefault(); goTo(current - 1); }
      else if (!typing && (e.key === 'Home')) { e.preventDefault(); goTo(1); }
      else if (!typing && (e.key === 'End')) { e.preventDefault(); goTo(total); }
      else if (!typing && (e.key === '+' || e.key === '=')) { e.preventDefault(); zs.stepIn(); }
      else if (!typing && (e.key === '-' || e.key === '_')) { e.preventDefault(); zs.stepOut(); }
      else if (typing && e.key === 'Enter') { e.preventDefault(); goTo(pageIn.value); }
    };
    node.addEventListener('click', (e) => {
      const action = e.target.closest('[data-viewer-action]');
      if (action) {
        const a = action.dataset.viewerAction;
        if (a === 'zoom-in') zs.stepIn(); else if (a === 'zoom-out') zs.stepOut(); else if (a === 'fit') zs.reset();
        else if (a === 'fullscreen') toggleFullscreen(); else if (a === 'close') close();
        return;
      }
      const thumb = e.target.closest('.rolls-viewer__thumb');
      if (thumb) { goTo(thumb.dataset.page); return; }
      if (e.target.closest('.rolls-viewer__nav--prev')) { goTo(current - 1); return; }
      if (e.target.closest('.rolls-viewer__nav--next')) { goTo(current + 1); return; }
      if (e.target.closest('img')) e.stopPropagation();
    });
    pageIn.addEventListener('change', () => goTo(pageIn.value));
    onSwipe(stage, (dir) => goTo(current + dir), () => zs.scale <= 1.001);

    document.body.appendChild(node);
    return { node, entry, open(page, opener) {
      pushOverlay(Object.assign(entry, { opener: opener || document.activeElement }));
      showOverlay(node);
      goTo(page);
      focusEl(stage);
    } };
  }
  function openCatalogue(slug, page, opener) {
    const c = collByKey.get(String(slug || ''));
    if (!c) return false;
    let v = viewers.get(c.slug);
    if (!v) { v = buildViewer(c); viewers.set(c.slug, v); }
    v.open(page || 1, opener);
    return true;
  }

  /* ================================================================
     ENQUIRY PANEL  aside.rolls-enquiry  (markup emitted by the generator)
     ================================================================ */
  const enquiry = { el: $('aside.rolls-enquiry, .rolls-enquiry'), scrim: $('.rolls-enquiry-scrim'), ctx: {}, entry: null };
  const enquiryFields = () => ({
    name: $('#re-name'), phone: $('#re-phone'), email: $('#re-email'), w: $('#re-w'), h: $('#re-h'), msg: $('#re-msg')
  });
  function enquiryEstimate() {
    const f = enquiryFields();
    const w = f.w ? f.w.value : enquiry.ctx.width, h = f.h ? f.h.value : enquiry.ctx.height;
    const hasDims = String(w === undefined || w === null ? '' : w).trim() !== '' || String(h === undefined || h === null ? '' : h).trim() !== '';
    return { w, h, hasDims, result: (hasDims && enquiry.ctx.collection) ? WJ.calculate(w, h, enquiry.ctx.collection) : null };
  }
  function enquiryMessage() {
    const ctx = enquiry.ctx, f = enquiryFields(), est = enquiryEstimate();
    const val = (n) => n ? n.value.trim() : '';
    const lines = ['Namaste Wall Jewels — Wallpaper Rolls enquiry'];
    if (ctx.collection) lines.push(`Collection: ${ctx.collection.name}`);
    if (ctx.designNumber) lines.push(`Design Number: ${ctx.designNumber}`);
    const wOk = WJ.parseDimension(est.w, 'width'), hOk = WJ.parseDimension(est.h, 'height');
    if (wOk.ok) lines.push(`Wall Width: ${fmtIn(wOk.value)} in`);
    if (hOk.ok) lines.push(`Wall Height: ${fmtIn(hOk.value)} in`);
    if (wOk.ok && hOk.ok) lines.push(`Wall Area: ${fmtArea(wOk.value * hOk.value / 144)} sq.ft`);
    if (est.result && est.result.ok) {
      lines.push(`Estimated Rolls: ${est.result.rolls} (approx. ${est.result.coverage} sq.ft coverage per roll)`);
      lines.push(`Estimated Cost: ${inr(est.result.cost)} (${est.result.rolls} × ${inr(est.result.rollPrice)} per roll)`);
    }
    if (val(f.name)) lines.push(`Name: ${val(f.name)}`);
    if (val(f.phone)) lines.push(`Phone: ${val(f.phone)}`);
    if (val(f.email)) lines.push(`Email: ${val(f.email)}`);
    if (val(f.msg)) lines.push(`Message: ${val(f.msg)}`);
    if (ctx.design && ctx.design.url) lines.push(`Design page: ${absolute(ctx.design.url)}`);
    lines.push('Please confirm the exact roll requirement and quote.');
    return lines.join('\n');
  }
  function enquirySubject() {
    const ctx = enquiry.ctx;
    let s = 'Wallpaper Rolls enquiry';
    if (ctx.collection) s += ` — ${ctx.collection.name}`;
    if (ctx.designNumber) s += ` Design ${ctx.designNumber}`;
    return s;
  }
  function renderEnquirySummary() {
    const box = $('.rolls-enquiry__summary', enquiry.el);
    if (!box) return;
    const ctx = enquiry.ctx, est = enquiryEstimate(), rows = [];
    const row = (k, v) => rows.push(`<div class="rolls-enquiry__row"><span>${esc(k)}</span><b>${esc(v)}</b></div>`);
    if (ctx.collection) row('Collection', ctx.collection.name);
    if (ctx.designNumber) row('Design Number', ctx.designNumber);
    if (est.result && est.result.ok) {
      row('Wall Size', fmtDims(est.result.width, est.result.height));
      row('Wall Area', `${fmtArea(est.result.area)} sq.ft`);
      row('Estimated Rolls', plural(est.result.rolls, 'Roll', 'Rolls'));
      row('Estimated Cost', inr(est.result.cost));
    } else {
      const wOk = WJ.parseDimension(est.w, 'width'), hOk = WJ.parseDimension(est.h, 'height');
      if (wOk.ok && hOk.ok) { row('Wall Size', fmtDims(wOk.value, hOk.value)); row('Wall Area', `${fmtArea(wOk.value * hOk.value / 144)} sq.ft`); }
    }
    box.innerHTML = rows.join('');
    box.hidden = !rows.length;
  }
  function enquiryError(text, field) {
    let err = $('.rolls-enquiry__error', enquiry.el);
    if (!err) {
      err = el('<p class="rolls-enquiry__error" role="alert" hidden></p>');
      const fields = $$('.dfield', enquiry.el);
      const anchor = fields.length ? fields[fields.length - 1] : $('[data-rolls-enquiry-send]', enquiry.el);
      if (anchor) anchor.insertAdjacentElement(fields.length ? 'afterend' : 'beforebegin', err);
      else enquiry.el.appendChild(err);
    }
    err.textContent = text || '';
    err.hidden = !text;
    const f = enquiryFields();
    Object.keys(f).forEach((k) => { if (f[k]) f[k].setAttribute('aria-invalid', String(field === k)); });
    if (field && f[field]) focusEl(f[field]);
  }
  function validateEnquiry() {
    const f = enquiryFields();
    const val = (n) => n ? n.value.trim() : '';
    if (f.name && !val(f.name)) return enquiryError('Please enter your name', 'name'), false;
    if ((f.phone || f.email) && !val(f.phone) && !val(f.email)) return enquiryError('Please enter a phone number or an email address', f.phone ? 'phone' : 'email'), false;
    const est = enquiryEstimate();
    if (est.hasDims) {
      const w = WJ.parseDimension(est.w, 'width');
      if (!w.ok) return enquiryError(`Wall width — ${w.error}`, 'w'), false;
      const h = WJ.parseDimension(est.h, 'height');
      if (!h.ok) return enquiryError(`Wall height — ${h.error}`, 'h'), false;
    }
    enquiryError('');
    return true;
  }
  function syncEnquiryLinks() {
    const mail = $('[data-rolls-enquiry-mail]', enquiry.el);
    if (mail) mail.href = `mailto:${CONTACT.email}?subject=${encodeURIComponent(enquirySubject())}&body=${encodeURIComponent(enquiryMessage())}`;
  }
  function waHref(text) { return `https://wa.me/${String(CONTACT.whatsapp).replace(/\D/g, '')}?text=${encodeURIComponent(text)}`; }

  function openEnquiry(ctx, opener) {
    ctx = ctx || {};
    if (ctx.collection && !ctx.design && ctx.designNumber) ctx.design = findDesign(ctx.collection, ctx.designNumber);
    if (ctx.design && !ctx.designNumber) ctx.designNumber = ctx.design.designNumber;
    enquiry.ctx = ctx;
    if (!enquiry.el) { /* no panel on this page — go straight to WhatsApp with what we know */
      window.open(waHref(enquiryMessage()), '_blank', 'noopener');
      return;
    }
    const h2 = $('h2', enquiry.el);
    if (h2) h2.textContent = ctx.designNumber ? 'Enquire about this design' : 'Request a quote';
    const f = enquiryFields();
    const prefill = (input, v, field) => {
      if (!input || v === undefined || v === null || v === '') return;
      const r = WJ.parseDimension(v, field);
      input.value = r.ok ? fmtIn(r.value) : String(v);
    };
    prefill(f.w, ctx.width, 'width');
    prefill(f.h, ctx.height, 'height');
    enquiryError('');
    renderEnquirySummary();
    syncEnquiryLinks();
    if (!enquiry.entry) enquiry.entry = { el: enquiry.el, onKey: (e) => { if (e.key === 'Escape') { e.preventDefault(); closeEnquiry(); } } };
    pushOverlay(Object.assign(enquiry.entry, { opener: opener || document.activeElement }));
    enquiry.el.removeAttribute('inert');
    enquiry.el.classList.add('is-open');
    if (enquiry.scrim) enquiry.scrim.classList.add('is-open');
    focusEl((f.name && !f.name.value) ? f.name : ($('[data-rolls-enquiry-close]', enquiry.el) || f.name));
  }
  function closeEnquiry() {
    if (!enquiry.el || !enquiry.el.classList.contains('is-open')) return;
    enquiry.el.classList.remove('is-open');
    enquiry.el.setAttribute('inert', '');
    if (enquiry.scrim) enquiry.scrim.classList.remove('is-open');
    popOverlay(enquiry.entry);
  }
  function initEnquiry() {
    if (!enquiry.el) return;
    enquiry.el.setAttribute('data-lenis-prevent', '');
    if (!enquiry.el.hasAttribute('aria-label')) enquiry.el.setAttribute('aria-label', 'Wallpaper rolls enquiry');
    enquiry.el.addEventListener('input', () => { renderEnquirySummary(); syncEnquiryLinks(); });
    enquiry.el.addEventListener('click', (e) => {
      if (e.target.closest('[data-rolls-enquiry-close]')) { closeEnquiry(); return; }
      if (e.target.closest('[data-rolls-enquiry-send]')) {
        if (!validateEnquiry()) return;
        const href = waHref(enquiryMessage());
        const win = window.open(href, '_blank', 'noopener');
        if (!win) location.href = href;
        return;
      }
      const mail = e.target.closest('[data-rolls-enquiry-mail]');
      if (mail) { if (!validateEnquiry()) { e.preventDefault(); return; } syncEnquiryLinks(); }
    });
    enquiry.scrim && enquiry.scrim.addEventListener('click', closeEnquiry);
  }

  /* ================================================================
     QUICK-VIEW MODAL  .rolls-modal  (gallery cards; built on first use)
     ================================================================ */
  let modal = null;
  function ensureModal() {
    if (modal) return modal;
    const node = el(`<div class="rolls-modal" role="dialog" aria-modal="true" aria-labelledby="rolls-modal-title" hidden inert data-lenis-prevent>
  <div class="rolls-modal__dialog">
    <button class="tool rolls-modal__close" type="button" aria-label="Close quick view">${ICON.close}</button>
    <button class="rolls-modal__nav rolls-modal__nav--prev" type="button" aria-label="Previous design">${ICON.prev}</button>
    <button class="rolls-modal__nav rolls-modal__nav--next" type="button" aria-label="Next design">${ICON.next}</button>
    <figure class="rolls-modal__media" data-no-lightbox>
      <button class="rolls-modal__zoom" type="button" aria-label="Zoom design"><img class="rolls-modal__img" alt="" decoding="async"></button>
    </figure>
    <div class="rolls-modal__panel">
      <span class="rolls-modal__counter"></span>
      <span class="cap rolls-modal__coll"></span>
      <h2 class="rolls-modal__title" id="rolls-modal-title"></h2>
      <ul class="rolls-modal__specs"></ul>
      <p class="rolls-flag rolls-modal__flag" hidden>Design number to be confirmed by the Wall Jewels team</p>
      <div class="rolls-modal__actions"></div>
      <a class="textlink rolls-modal__link" href="#">Open design page ${ICON.arrow}</a>
    </div>
  </div>
</div>`);
    document.body.appendChild(node);
    const img = $('.rolls-modal__img', node);
    const state = { list: [], index: 0 };
    const entry = { el: node, onKey: null };
    const close = () => { hideOverlay(node); popOverlay(entry); };
    const step = (dir) => { if (state.list.length > 1) render((state.index + dir + state.list.length) % state.list.length); };

    function render(index) {
      const d = state.list[index];
      if (!d) return;
      state.index = index;
      const c = collOf(d) || {};
      const web = asset(d.web || d.image), full = asset(d.image || d.web);
      img.classList.remove('is-loaded');
      img.src = web;
      img.alt = designAlt(d, c);
      img.dataset.full = full;
      if (num(d.width) && num(d.height)) { img.width = d.width; img.height = d.height; } else { img.removeAttribute('width'); img.removeAttribute('height'); }
      $('.rolls-modal__zoom', node).setAttribute('aria-label', `Zoom design ${d.designNumber}`);
      $('.rolls-modal__coll', node).textContent = c.name || '';
      $('.rolls-modal__title', node).textContent = `Design No. ${d.designNumber}`;
      const specs = [];
      if (num(c.rollSize)) specs.push(`${c.rollSize} sq.ft roll`);
      if (num(c.coverage)) specs.push(`Approx. ${c.coverage} sq.ft wall coverage`);
      if (num(c.rollPrice) !== undefined) specs.push(`${inr(c.rollPrice)} per roll`);
      $('.rolls-modal__specs', node).innerHTML = specs.map((s) => `<li>${esc(s)}</li>`).join('');
      $('.rolls-modal__flag', node).hidden = !d.needsReview;
      const url = asset(d.url);
      const page = num(d.cataloguePage);
      $('.rolls-modal__actions', node).innerHTML = `
        <a class="btn btn--fill" href="${esc(url)}#calculator"><span class="dot-a"></span>CALCULATE ROLLS</a>
        <a class="btn btn--wa" href="${esc(url)}?enquire=1"><span class="dot-a"></span>ENQUIRE ABOUT THIS DESIGN</a>
        ${c.slug ? `<button class="btn" type="button" data-open-rolls-catalogue="${esc(c.slug)}"${page ? ` data-page="${esc(page)}"` : ''}><span class="dot-a"></span>${page ? 'VIEW IN CATALOGUE' : 'VIEW COMPLETE CATALOGUE'}</button>` : ''}`;
      $('.rolls-modal__link', node).href = url;
      $('.rolls-modal__counter', node).textContent = state.list.length > 1 ? `${index + 1} / ${state.list.length}` : '';
      $$('.rolls-modal__nav', node).forEach((b) => { b.hidden = state.list.length <= 1; });
      [state.list[index + 1], state.list[index - 1]].forEach((n) => { if (n) { const p = new Image(); p.src = asset(n.web || n.image); } });
    }
    img.addEventListener('load', () => img.classList.add('is-loaded'));
    node.addEventListener('click', (e) => {
      if (e.target === node) { close(); return; }
      if (e.target.closest('.rolls-modal__close')) { close(); return; }
      if (e.target.closest('.rolls-modal__nav--prev')) { step(-1); return; }
      if (e.target.closest('.rolls-modal__nav--next')) { step(1); return; }
      const z = e.target.closest('.rolls-modal__zoom');
      if (z) { e.stopPropagation(); openZoom(img.dataset.full || img.src, img.alt, z); }
    });
    entry.onKey = (e) => {
      if (e.key === 'Escape') { e.preventDefault(); close(); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); step(1); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); step(-1); }
    };
    onSwipe($('.rolls-modal__dialog', node), step);
    modal = { node, entry, open(list, index, opener) {
      state.list = Array.isArray(list) && list.length ? list : [];
      if (!state.list.length) return;
      render(Math.min(Math.max(0, index || 0), state.list.length - 1));
      pushOverlay(Object.assign(entry, { opener: opener || document.activeElement }));
      showOverlay(node);
      focusEl($('.rolls-modal__close', node));
    } };
    return modal;
  }
  const openQuickView = (list, index, opener) => ensureModal().open(list, index, opener);

  /* Any .rolls-card container (gallery or "More from" strip) opens quick view;
     modifier clicks keep the browser's own behaviour. */
  function bindCardContainer(container, currentList) {
    container.addEventListener('click', (e) => {
      const card = e.target.closest('a.rolls-card');
      if (!card || !container.contains(card)) return;
      e.stopPropagation(); /* the site-wide image lightbox must not see this */
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
      const list = currentList ? currentList() : $$('a.rolls-card', container).map((a) => designById.get(a.dataset.designId)).filter(Boolean);
      const idx = list.findIndex((d) => String(d.id) === card.dataset.designId);
      if (idx < 0) return;
      e.preventDefault();
      openQuickView(list, idx, card);
    });
  }

  /* ================================================================
     GALLERY  [data-rolls-gallery]  (toolbar, search, chips, batches, URL state)
     ================================================================ */
  function initGallery() {
    const gallery = $('[data-rolls-gallery]');
    if (!gallery) return;
    if (!DESIGNS.length) { bindCardContainer(gallery); return; } /* no data: static cards keep working as links */

    const scope = gallery.closest('.wrap, section') || document;
    const find = (sel) => $(sel, scope) || $(sel);
    const search = find('[data-rolls-search]');
    const filters = find('.rolls-filters');
    const countOut = find('[data-rolls-count]');
    let more = find('[data-rolls-more]');
    let empty = find('.rolls-empty');
    if (!more) { more = el('<button class="btn rolls-more" type="button" data-rolls-more hidden><span class="dot-a"></span>SHOW MORE DESIGNS</button>'); gallery.insertAdjacentElement('afterend', more); }
    if (!empty) { empty = el('<p class="rolls-empty" hidden></p>'); gallery.insertAdjacentElement('afterend', empty); }
    more.hidden = true; empty.hidden = true;

    const params = new URLSearchParams(location.search);
    const state = { q: '', collection: 'all', list: [], shown: 0 };
    const attrColl = gallery.dataset.collection;
    if (attrColl && collByKey.has(attrColl)) state.collection = collByKey.get(attrColl).slug;
    const urlColl = params.get('collection');
    if (urlColl && collByKey.has(urlColl)) state.collection = collByKey.get(urlColl).slug;
    else if (urlColl === 'all') state.collection = 'all';
    if (params.get('q')) state.q = params.get('q');
    if (search) search.value = state.q;

    /* chips are generated from data so a new collection appears without touching markup */
    if (filters) {
      filters.innerHTML = `<button class="fchip" type="button" data-rolls-filter="all" aria-pressed="false">ALL</button>` +
        COLLECTIONS.map((c) => `<button class="fchip" type="button" data-rolls-filter="${esc(c.slug)}" aria-pressed="false">${esc(String(c.name).toUpperCase())}</button>`).join('');
    }
    const chips = () => $$('[data-rolls-filter]', filters || scope);

    function compute() {
      const q = state.q.trim();
      const active = state.collection;
      let list;
      if (q) {
        /* search is global; the active collection simply ranks first */
        list = DESIGNS.map((d, i) => ({ d, i, r: WJ.matchesQuery(d, q) })).filter((x) => x.r > 0);
        list.sort((a, b) => (b.r - a.r) ||
          ((active !== 'all' && (collOf(b.d) || {}).slug === active) - (active !== 'all' && (collOf(a.d) || {}).slug === active)) ||
          (a.i - b.i));
        list = list.map((x) => x.d);
      } else {
        list = active === 'all' ? DESIGNS : DESIGNS.filter((d) => (collOf(d) || {}).slug === active);
      }
      state.list = list;
    }
    function renderBatch() {
      const frag = document.createDocumentFragment();
      const end = Math.min(state.list.length, state.shown + BATCH);
      for (let i = state.shown; i < end; i++) frag.appendChild(el(cardHTML(state.list[i])));
      gallery.appendChild(frag);
      state.shown = end;
      more.hidden = state.shown >= state.list.length;
    }
    function render() {
      compute();
      gallery.innerHTML = '';
      state.shown = 0;
      gallery.dataset.collection = state.collection;
      renderBatch();
      const n = state.list.length, q = state.q.trim();
      if (countOut) countOut.textContent = q ? `${plural(n, 'design matches', 'designs match')} “${q}”` : plural(n, 'design', 'designs');
      if (n) empty.hidden = true;
      else {
        empty.innerHTML = q
          ? `No design matches “${esc(q)}”. Try the design number printed in the catalogue, or <a href="${esc(waHref('Namaste Wall Jewels — I am looking for a wallpaper roll design. Photo attached.'))}" target="_blank" rel="noopener">WhatsApp us a photo</a>.`
          : 'No designs in this collection yet.';
        empty.hidden = false;
      }
      chips().forEach((ch) => {
        const on = ch.dataset.rollsFilter === state.collection;
        ch.setAttribute('aria-pressed', String(on));
        ch.classList.toggle('is-active', on);
      });
      syncURL();
    }
    function syncURL() {
      const p = new URLSearchParams(location.search);
      if (state.q.trim()) p.set('q', state.q.trim()); else p.delete('q');
      if (state.collection !== 'all' && state.collection !== (attrColl && collByKey.has(attrColl) ? collByKey.get(attrColl).slug : 'all')) p.set('collection', state.collection);
      else p.delete('collection');
      const qs = p.toString();
      const next = location.pathname + (qs ? `?${qs}` : '') + location.hash;
      if (next !== location.pathname + location.search + location.hash) history.replaceState(history.state, '', next);
    }

    let debounce;
    if (search) {
      const onSearch = () => { clearTimeout(debounce); debounce = setTimeout(() => { state.q = search.value; render(); }, 120); };
      search.addEventListener('input', onSearch);
      search.addEventListener('search', onSearch);
      search.addEventListener('keydown', (e) => { if (e.key === 'Enter') e.preventDefault(); });
    }
    (filters || scope).addEventListener('click', (e) => {
      const ch = e.target.closest('[data-rolls-filter]');
      if (!ch) return;
      const f = ch.dataset.rollsFilter;
      state.collection = (f === 'all' || !collByKey.has(f)) ? 'all' : collByKey.get(f).slug;
      render();
    });
    more.addEventListener('click', () => { const firstNew = state.shown; renderBatch(); focusEl(gallery.children[firstNew]); });
    const moreIO = new IntersectionObserver((ents) => { ents.forEach((en) => { if (en.isIntersecting && !more.hidden) renderBatch(); }); }, { rootMargin: '0px 0px 600px 0px' });
    moreIO.observe(more);

    bindCardContainer(gallery, () => state.list);
    render();
  }

  /* ================================================================
     CALCULATOR  [data-rolls-calc]  (any number per page)
     ================================================================ */
  const calcState = { last: null }; /* latest valid estimate, feeds the enquiry panel */
  function buildCalculator(mount, idx, pre) {
    const uid = `rc${idx}`;
    let locked = mount.hasAttribute('data-lock-collection');
    let coll = collByKey.get(String(mount.dataset.collection || ''));
    if (!locked && pre.collection && collByKey.has(pre.collection)) coll = collByKey.get(pre.collection);
    if (!coll) { coll = COLLECTIONS[0]; locked = false; }
    const fixedDesign = (mount.dataset.design || '').trim();
    const designPrefill = fixedDesign || (pre.design || '').trim();
    const hasDisclaimerOutside = !!(mount.parentElement && mount.parentElement.querySelector('.rolls-disclaimer'));

    mount.innerHTML = `<form class="rolls-calc__form" novalidate>
  <div class="rolls-calc__grid">
    <div class="dfield">
      <label for="${uid}-w">Wall Width (inches)</label>
      <input id="${uid}-w" name="width" type="number" inputmode="decimal" min="1" max="2400" step="any" placeholder="e.g. 120" autocomplete="off" aria-describedby="${uid}-w-err">
      <span class="rolls-calc__error" id="${uid}-w-err" hidden></span>
    </div>
    <div class="dfield">
      <label for="${uid}-h">Wall Height (inches)</label>
      <input id="${uid}-h" name="height" type="number" inputmode="decimal" min="1" max="2400" step="any" placeholder="e.g. 108" autocomplete="off" aria-describedby="${uid}-h-err">
      <span class="rolls-calc__error" id="${uid}-h-err" hidden></span>
    </div>
    <div class="dfield">
      <label for="${uid}-c">Collection</label>
      <select id="${uid}-c" name="collection" aria-describedby="${uid}-facts"${locked ? ' disabled' : ''}>
        ${COLLECTIONS.map((c) => `<option value="${esc(c.slug)}"${c === coll ? ' selected' : ''}>${esc(c.name)}</option>`).join('')}
      </select>
      <span class="rolls-calc__facts" id="${uid}-facts"></span>
    </div>
    <div class="dfield">
      <label for="${uid}-d">Design Number${fixedDesign ? '' : ' (optional)'}</label>
      <input id="${uid}-d" name="design" type="text" inputmode="text" placeholder="e.g. 12" autocomplete="off" value="${esc(designPrefill)}"${fixedDesign ? ' readonly' : ''}>
    </div>
  </div>
  <div class="rolls-calc__actions"><button class="btn btn--fill" type="submit"><span class="dot-a"></span>CALCULATE</button></div>
</form>
<div class="rolls-estimate" aria-live="polite" hidden>
  <span class="cap">Your Wallpaper Estimate</span>
  <div class="rolls-estimate__rows"></div>
  <div class="rolls-estimate__row rolls-estimate__total"><span>Estimated Wallpaper Cost</span><b></b></div>
  <p class="rolls-estimate__note"><strong>Plus GST &amp; Installation is Free</strong></p>
  <div class="rolls-estimate__actions"><button class="btn btn--wa" type="button" data-rolls-quote><span class="dot-a"></span>REQUEST A QUOTE</button></div>
  ${hasDisclaimerOutside ? '' : `<div class="rolls-disclaimer"><span class="cap">Approximate calculation</span>
    <p class="small">Roll requirements are calculated based on approximate coverage and may vary depending on wall dimensions, pattern repeat, design alignment, cutting, wastage and installation requirements.</p>
    <p class="small">Final roll requirement will be confirmed by the Wall Jewels team before order confirmation.</p></div>`}
</div>`;

    const form = $('form', mount);
    const wIn = $(`#${uid}-w`), hIn = $(`#${uid}-h`), sel = $(`#${uid}-c`), dIn = $(`#${uid}-d`);
    const facts = $(`#${uid}-facts`), estimate = $('.rolls-estimate', mount);
    const rows = $('.rolls-estimate__rows', estimate), total = $('.rolls-estimate__total b', estimate);
    if (pre.w) wIn.value = pre.w;
    if (pre.h) hIn.value = pre.h;

    const currentCollection = () => collByKey.get(sel.value) || coll;
    const showError = (input, text) => {
      const err = $(`#${input.id}-err`);
      if (!err) return;
      err.textContent = text || '';
      err.hidden = !text;
      input.setAttribute('aria-invalid', String(!!text));
    };
    const renderFacts = () => { facts.textContent = collectionFacts(currentCollection()); };

    function refresh(showErrors) {
      const c = currentCollection();
      const designNumber = dIn.value.trim();
      const result = WJ.calculate(wIn.value, hIn.value, c);
      if (result.ok) {
        showError(wIn, ''); showError(hIn, '');
        const list = [
          ['Wall Size', fmtDims(result.width, result.height)],
          ['Wall Area', `${fmtArea(result.area)} sq.ft`],
          ['Collection', c.name]
        ];
        if (designNumber) list.push(['Design Number', designNumber]);
        if (result.rollSize) list.push(['Roll Size', `${result.rollSize} sq.ft`]);
        list.push(['Approx. Coverage', `${result.coverage} sq.ft / Roll`]);
        list.push(['Estimated Rolls', plural(result.rolls, 'Roll', 'Rolls')]);
        list.push(['Price Per Roll', inr(result.rollPrice)]);
        rows.innerHTML = list.map(([k, v]) => `<div class="rolls-estimate__row"><span>${esc(k)}</span><b>${esc(v)}</b></div>`).join('');
        total.textContent = inr(result.cost);
        estimate.hidden = false;
        calcState.last = { collection: c, designNumber, design: findDesign(c, designNumber), width: result.width, height: result.height, result };
        return;
      }
      estimate.hidden = true;
      if (!showErrors) return;
      const w = WJ.parseDimension(wIn.value, 'width'), h = WJ.parseDimension(hIn.value, 'height');
      showError(wIn, w.ok ? '' : w.error);
      showError(hIn, h.ok ? '' : h.error);
      const firstBad = !w.ok ? wIn : (!h.ok ? hIn : null);
      if (firstBad) focusEl(firstBad);
    }

    form.addEventListener('submit', (e) => { e.preventDefault(); refresh(true); });
    form.addEventListener('input', (e) => {
      if (e.target === wIn || e.target === hIn) {
        const r = WJ.parseDimension(e.target.value, e.target === wIn ? 'width' : 'height');
        if (r.ok || e.target.value === '') showError(e.target, '');
      }
      refresh(false);
    });
    [wIn, hIn].forEach((input) => input.addEventListener('blur', () => {
      if (input.value === '') { showError(input, ''); return; }
      const r = WJ.parseDimension(input.value, input === wIn ? 'width' : 'height');
      showError(input, r.ok ? '' : r.error);
    }));
    sel.addEventListener('change', () => { renderFacts(); refresh(false); });
    estimate.addEventListener('click', (e) => {
      const b = e.target.closest('[data-rolls-quote]');
      if (!b) return;
      const c = currentCollection();
      openEnquiry({ collection: c, designNumber: dIn.value.trim(), width: wIn.value, height: hIn.value }, b);
    });

    renderFacts();
    refresh(false);
    return {
      mount, locked,
      setCollection(slug) { if (locked || !collByKey.has(slug)) return false; sel.value = collByKey.get(slug).slug; renderFacts(); refresh(false); return true; }
    };
  }
  const calculators = [];
  function initCalculators() {
    const mounts = $$('[data-rolls-calc]');
    if (!mounts.length || !COLLECTIONS.length) return;
    const params = new URLSearchParams(location.search);
    const pre = { w: params.get('w') || '', h: params.get('h') || '', collection: params.get('collection') || '', design: params.get('design') || '' };
    mounts.forEach((m, i) => calculators.push(buildCalculator(m, i, pre)));
  }

  /* Context for "Enquire about this design" / ?enquire=1: the page's own design first,
     then the last estimate, then the page's collection. */
  function pageContext(trigger) {
    const t = trigger || {};
    const ds = t.dataset || {};
    const fromButton = designById.get(ds.designId || '');
    if (fromButton) {
      const last = calcState.last;
      return { collection: collOf(fromButton), design: fromButton, designNumber: fromButton.designNumber,
        width: last && last.collection === collOf(fromButton) ? last.width : undefined, height: last && last.collection === collOf(fromButton) ? last.height : undefined };
    }
    const mount = $('[data-rolls-calc][data-design]');
    if (mount) {
      const c = collByKey.get(String(mount.dataset.collection || ''));
      const last = calcState.last;
      return { collection: c, designNumber: mount.dataset.design, design: findDesign(c, mount.dataset.design),
        width: last && last.collection === c ? last.width : undefined, height: last && last.collection === c ? last.height : undefined };
    }
    if (calcState.last) return Object.assign({}, calcState.last);
    const gallery = $('[data-rolls-gallery]');
    const c = collByKey.get(String(ds.collection || (gallery && gallery.dataset.collection) || ''));
    return c ? { collection: c } : {};
  }

  /* ---------------- delegated controls ---------------- */
  document.addEventListener('click', (e) => {
    const cat = e.target.closest('[data-open-rolls-catalogue]');
    if (cat) {
      if (openCatalogue(cat.dataset.openRollsCatalogue, num(cat.dataset.page, 1), cat)) e.preventDefault();
      return;
    }
    const enq = e.target.closest('[data-rolls-enquire]');
    if (enq) { e.preventDefault(); openEnquiry(pageContext(enq), enq); return; }
    const pick = e.target.closest('[data-calc-collection]');
    if (pick) {
      const slug = pick.dataset.calcCollection;
      const done = calculators.map((c) => c.setCollection(slug)).some(Boolean);
      const c = collByKey.get(slug);
      if (done && c) toast(`${c.name} selected in the calculator`);
    }
  });

  function handleDeepLinks() {
    const params = new URLSearchParams(location.search);
    const cat = params.get('catalogue');
    if (cat) {
      const page = num(params.get('page'), 1);
      let slug = collByKey.has(cat) ? collByKey.get(cat).slug : '';
      if (!slug) {
        const gallery = $('[data-rolls-gallery]');
        const lockedCalc = $('[data-rolls-calc][data-lock-collection]');
        const opener = $('[data-open-rolls-catalogue]');
        const guess = (gallery && gallery.dataset.collection !== 'all' && gallery.dataset.collection) ||
          (lockedCalc && lockedCalc.dataset.collection) || (opener && opener.dataset.openRollsCatalogue) || '';
        if (collByKey.has(guess)) slug = collByKey.get(guess).slug;
      }
      if (slug) setTimeout(() => openCatalogue(slug, page, $('[data-open-rolls-catalogue]')), 60);
    }
    if (params.get('enquire') === '1') setTimeout(() => openEnquiry(pageContext(), $('[data-rolls-enquire]')), 80);
  }

  /* ---------------- boot ---------------- */
  initCalculators();
  initGallery();
  $$('.rolls-strip').forEach((s) => bindCardContainer(s));
  initEnquiry();
  initZoomTriggers();
  handleDeepLinks();
})();
