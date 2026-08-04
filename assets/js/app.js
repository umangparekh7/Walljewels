/* =============================================================
   Wall Jewels Wallpaper World — behaviour
   ============================================================= */
(function () {
  'use strict';

  const $  = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => [...(r || document).querySelectorAll(s)];
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  /* ---------- Woven fallback swatch -------------------------
     If a photo fails to load we don't show a broken frame — we
     draw a plausible wallpaper swatch from the design's own
     colours, so the page still reads as intentional.          */
  function swatch(tone, label) {
    const [a, b] = tone || ['#E8E0D4', '#9A8B76'];
    // A 12-petal rosette on a diagonal lattice — reads as a real wallpaper
    // repeat rather than a "missing image" box.
    let petals = '';
    for (let i = 0; i < 12; i++) {
      petals += `<ellipse cx="60" cy="34" rx="6.5" ry="17" transform="rotate(${i * 30} 60 60)"/>`;
    }
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="800" height="640" viewBox="0 0 800 640">
      <defs>
        <linearGradient id="g" x1="0" y1="0" x2=".85" y2="1">
          <stop offset="0" stop-color="${a}"/><stop offset="1" stop-color="${b}"/>
        </linearGradient>
        <pattern id="p" width="120" height="120" patternUnits="userSpaceOnUse">
          <g fill="none" stroke="${a}" stroke-opacity=".5" stroke-width="1.1">${petals}</g>
          <circle cx="60" cy="60" r="7" fill="${a}" fill-opacity=".38"/>
          <circle cx="60" cy="60" r="28" fill="none" stroke="${a}" stroke-opacity=".26" stroke-width="1"/>
          <path d="M0 0h120M0 0v120" stroke="${b}" stroke-opacity=".3" stroke-width="1"/>
          <circle cx="0" cy="0" r="3.5" fill="${a}" fill-opacity=".3"/>
          <circle cx="120" cy="0" r="3.5" fill="${a}" fill-opacity=".3"/>
          <circle cx="0" cy="120" r="3.5" fill="${a}" fill-opacity=".3"/>
        </pattern>
      </defs>
      <rect width="800" height="640" fill="url(#g)"/>
      <rect width="800" height="640" fill="url(#p)"/>
      <rect width="800" height="640" fill="${b}" fill-opacity=".07"/>
      <text x="400" y="600" text-anchor="middle" font-family="monospace" font-size="15"
            letter-spacing="5" fill="${a}" fill-opacity=".7">${esc((label || 'WALL JEWELS').toUpperCase())}</text>
    </svg>`;
    return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
  }

  function guardImages(scope) {
    $$('img[data-tone]', scope).forEach((img) => {
      if (img.dataset.guarded) return;
      img.dataset.guarded = '1';
      img.addEventListener('error', function handle() {
        img.removeEventListener('error', handle);
        img.src = swatch(img.dataset.tone.split('|'), img.dataset.swatchLabel || '');
      }, { once: true });
    });
  }

  /* ---------- Theme ---------- */
  const root = document.documentElement;
  function setTheme(t) {
    root.dataset.theme = t;
    localStorage.setItem('wj-theme', t);
    const meta = $('meta[name="theme-color"]');
    if (meta) meta.content = t === 'dark' ? '#0D0B0A' : '#FBF8F4';
    document.dispatchEvent(new CustomEvent('wj:themechange', { detail: { theme: t } }));
  }
  $('#theme') && $('#theme').addEventListener('click', () => {
    setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark');
  });

  /* ---------- Nav ---------- */
  const nav = $('#nav');
  if (nav) {
    const onScroll = () => nav.classList.toggle('is-stuck', window.scrollY > 8);
    onScroll();
    addEventListener('scroll', onScroll, { passive: true });
  }

  const sheet = $('#sheet');
  const openSheet = (open) => {
    if (!sheet) return;
    sheet.classList.toggle('is-open', open);
    document.body.style.overflow = open ? 'hidden' : '';
    const b = $('#burger');
    if (b) b.setAttribute('aria-expanded', String(open));
  };
  $('#burger') && $('#burger').addEventListener('click', () => openSheet(true));
  $('#sheet-close') && $('#sheet-close').addEventListener('click', () => openSheet(false));
  sheet && $$('a', sheet).forEach((a) => a.addEventListener('click', () => openSheet(false)));
  addEventListener('keydown', (e) => { if (e.key === 'Escape') openSheet(false); });

  /* ---------- Reveal on scroll ----------
     Deliberately geometry-based rather than IntersectionObserver:
     IO callbacks are delivered during the rendering step, so they can
     stall in backgrounded/non-rendering tabs and leave content at
     opacity 0. This always resolves. rAF-throttled, so it stays cheap. */
  let pending = false;
  function checkReveal() {
    pending = false;
    const h = window.innerHeight || document.documentElement.clientHeight;
    $$('.reveal:not(.is-visible), .step:not(.is-visible)').forEach((el) => {
      const r = el.getBoundingClientRect();
      if (r.top < h * 0.94 && r.bottom > 0) el.classList.add('is-visible');
    });
  }
  function queueReveal() {
    if (pending) return;
    pending = true;
    requestAnimationFrame(checkReveal);
  }
  addEventListener('scroll', queueReveal, { passive: true });
  addEventListener('resize', queueReveal);
  addEventListener('load', checkReveal);
  // rAF is suspended while a document is hidden, so run directly when the
  // tab comes back or is restored from bfcache.
  addEventListener('pageshow', checkReveal);
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') checkReveal();
  });
  const watch = () => checkReveal();
  checkReveal();

  /* ---------- Year ---------- */
  $('#year') && ($('#year').textContent = new Date().getFullYear());

  /* =========================================================
     Shared renderers
     ========================================================= */
  const roomLabel  = (id) => (ROOMS.find((r) => r.id === id) || {}).label || id;
  const roomPhrase = (id) => {
    const r = ROOMS.find((x) => x.id === id);
    return (r && r.in) || roomLabel(id).toLowerCase();
  };
  const themeLabel = (id) => (THEMES.find((t) => t.id === id) || {}).label || id;

  function tileHTML(d, mod) {
    // `img: null` in data.js means "draw the woven swatch" — used where we
    // don't yet have a photograph we're happy to stand behind.
    const src = d.img || swatch(d.tone, d.t);
    return `
      <article class="tile ${mod || ''} reveal">
        <div class="tile__media">
          ${d.tag ? `<span class="chip">${esc(d.tag)}</span>` : ''}
          <img src="${esc(src)}" alt="${esc(d.t)} — ${esc(roomLabel(d.room).toLowerCase())} wallpaper"
               loading="lazy" decoding="async"
               data-tone="${esc(d.tone.join('|'))}" data-swatch-label="${esc(d.t)}">
          <p class="tile__blurb">${esc(d.blurb)}</p>
        </div>
        <div class="tile__body">
          <h3 class="tile__title">${esc(d.t)}</h3>
          <p class="tile__meta">${esc(roomLabel(d.room))} · ${esc(themeLabel(d.theme))}</p>
        </div>
      </article>`;
  }

  /* =========================================================
     HOME PAGE
     ========================================================= */

  /* Marquee */
  const mq = $('#marquee');
  if (mq && typeof CLIENTS !== 'undefined') {
    const row = CLIENTS.map((c) => `<span class="marquee__item">${esc(c)}</span>`).join('');
    mq.innerHTML = row + row; // duplicated for a seamless -50% loop
  }

  /* ---------------------------------------------------------
     Premium collection — coverflow arc deck
     Cards share one origin and are separated purely by transform,
     so there's no layout thrash while sliding.
     --------------------------------------------------------- */
  const stage = $('#deck-stage');
  if (stage) {
    const picks = ['Calacatta Gold', 'Om Mandala', 'Wall-Break Superhero', 'Golden Eleaves',
                   'Facet', 'Vertical Garden', 'Botanical Luxe', 'Rocket Bay',
                   'Pergo Oak Natural', 'Krishna Bansuri', 'Alphabet Wall', 'Ink & Gold Flow'];
    const items = picks.map((n) => COLLECTION.find((x) => x.t === n)).filter(Boolean);
    const N = items.length;
    const VISIBLE = 3;            // cards fanned out either side of centre

    stage.innerHTML = items.map((d) => {
      const src = d.img || swatch(d.tone, d.t);
      return `
        <a class="deck__card" href="collection.html?room=${d.room}">
          <img src="${esc(src)}" alt="${esc(d.t)} — ${esc(roomLabel(d.room).toLowerCase())} wallpaper"
               loading="lazy" decoding="async"
               data-tone="${esc(d.tone.join('|'))}" data-swatch-label="${esc(d.t)}">
          <span class="deck__veil"></span>
          ${d.tag ? `<span class="chip">${esc(d.tag)}</span>` : ''}
          <span class="deck__body">
            <span class="deck__room">${esc(roomLabel(d.room))} · ${esc(themeLabel(d.theme))}</span>
            <span class="deck__title">${esc(d.t)}</span>
            <span class="deck__blurb">${esc(d.blurb)}</span>
          </span>
        </a>`;
    }).join('');

    guardImages(stage);

    const cards = $$('.deck__card', stage);
    const dotsEl = $('#deck-dots');
    const readout = $('#deck-readout');
    dotsEl.innerHTML = items.map((d, i) =>
      `<button class="deck__dot" data-i="${i}" aria-label="Show ${esc(d.t)}"></button>`).join('');
    const dots = $$('.deck__dot', dotsEl);

    let active = 0;
    let dragOffset = 0;          // live px offset while dragging

    // shortest signed distance from active on a wrapped ring
    const delta = (i) => {
      let d = i - active;
      if (d > N / 2) d -= N;
      if (d < -N / 2) d += N;
      return d;
    };

    function layout() {
      const step = parseFloat(getComputedStyle(stage.parentElement).getPropertyValue('--step')) || 130;
      const tilt = parseFloat(getComputedStyle(stage.parentElement).getPropertyValue('--tilt')) || 5;
      const slip = dragOffset / step;

      cards.forEach((card, i) => {
        const o = delta(i) - slip;
        const a = Math.abs(o);
        const far = a > VISIBLE + 0.5;

        // Cards past the fan are invisible, but an absolutely-positioned
        // element still extends the document's scroll width — so park them
        // at the edge of the fan rather than letting them fly off-page.
        const ox = Math.max(-VISIBLE, Math.min(VISIBLE, o));
        const x = ox * step;
        const scale = Math.max(0.62, 1 - Math.min(a, VISIBLE) * 0.085);
        const rot = -ox * tilt;
        const opacity = far ? 0 : Math.max(0, 1 - a * 0.2);

        card.style.transform = `translate3d(${x}px,${Math.min(a, VISIBLE) * 9}px,0) rotate(${rot}deg) scale(${scale})`;
        card.style.opacity = opacity;
        card.style.zIndex = String(100 - Math.round(a * 10));
        card.classList.toggle('is-active', Math.round(o) === 0 && Math.abs(slip) < 0.5);
        card.classList.toggle('is-far', far);
        card.setAttribute('aria-hidden', far ? 'true' : 'false');
        // only the centred card is a tab stop — side cards are reachable
        // via the arrows/dots, so 12 extra stops would just be noise
        card.tabIndex = Math.round(o) === 0 ? 0 : -1;
      });

      dots.forEach((d, i) => d.setAttribute('aria-current', String(i === active)));
      if (readout) readout.textContent = `${active + 1} / ${N} · ${items[active].t}`;
    }

    const go = (i) => { active = ((i % N) + N) % N; layout(); };
    const next = () => go(active + 1);
    const prev = () => go(active - 1);

    $('#deck-next').addEventListener('click', () => { stopAuto(); next(); });
    $('#deck-prev').addEventListener('click', () => { stopAuto(); prev(); });
    dots.forEach((d) => d.addEventListener('click', () => { stopAuto(); go(+d.dataset.i); }));

    // clicking a side card centres it instead of following the link
    cards.forEach((card, i) => card.addEventListener('click', (e) => {
      if (delta(i) !== 0) { e.preventDefault(); stopAuto(); go(i); }
    }));

    // keyboard
    stage.parentElement.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight') { e.preventDefault(); stopAuto(); next(); }
      if (e.key === 'ArrowLeft')  { e.preventDefault(); stopAuto(); prev(); }
    });

    /* drag / swipe */
    let dragging = false, startX = 0, moved = 0;
    stage.addEventListener('pointerdown', (e) => {
      if (e.button != null && e.button !== 0) return;
      dragging = true; startX = e.clientX; moved = 0;
      stage.classList.add('is-dragging');
      stage.setPointerCapture && stage.setPointerCapture(e.pointerId);
      cards.forEach((c) => (c.style.transition = 'none'));
      stopAuto();
    });
    stage.addEventListener('pointermove', (e) => {
      if (!dragging) return;
      moved = e.clientX - startX;
      dragOffset = -moved;
      layout();
    });
    function endDrag() {
      if (!dragging) return;
      dragging = false;
      stage.classList.remove('is-dragging');
      cards.forEach((c) => (c.style.transition = ''));
      const step = parseFloat(getComputedStyle(stage.parentElement).getPropertyValue('--step')) || 130;
      const jump = Math.round(dragOffset / step);
      dragOffset = 0;
      if (jump) go(active + jump); else layout();
      // suppress the click that follows a real drag
      if (Math.abs(moved) > 6) {
        const swallow = (ev) => { ev.preventDefault(); ev.stopPropagation(); };
        stage.addEventListener('click', swallow, { capture: true, once: true });
        setTimeout(() => stage.removeEventListener('click', swallow, { capture: true }), 60);
      }
    }
    stage.addEventListener('pointerup', endDrag);
    stage.addEventListener('pointercancel', endDrag);
    stage.addEventListener('pointerleave', endDrag);

    /* autoplay */
    const slow = matchMedia('(prefers-reduced-motion: reduce)').matches;
    let timer = 0;
    function startAuto() {
      if (slow || timer) return;
      timer = setInterval(() => {
        if (document.visibilityState === 'visible') next();
      }, 4600);
    }
    function stopAuto() { clearInterval(timer); timer = 0; }
    const deck = stage.parentElement;
    deck.addEventListener('pointerenter', stopAuto);
    deck.addEventListener('focusin', stopAuto);
    deck.addEventListener('pointerleave', startAuto);

    addEventListener('resize', layout);
    guardImages(stage);
    layout();
    startAuto();
  }

  /* Room cards */
  const ROOM_IMG = {
    living:   'https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=620&q=70',
    bedroom:  'https://images.unsplash.com/photo-1616594039964-ae9021a400a0?auto=format&fit=crop&w=620&q=70',
    pooja:    'https://images.unsplash.com/photo-1590077428593-a55bb07c4665?auto=format&fit=crop&w=620&q=70',
    kids:     'https://images.unsplash.com/photo-1503919545889-aef636e10ad4?auto=format&fit=crop&w=620&q=70',
    office:   'https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=620&q=70',
    school:   'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=620&q=70',
    balcony:  'https://images.unsplash.com/photo-1466692476868-aef1dfb1e735?auto=format&fit=crop&w=620&q=70',
    flooring: 'https://images.unsplash.com/photo-1595428774223-ef52624120d2?auto=format&fit=crop&w=620&q=70'
  };
  const ROOM_TONE = {
    living: ['#EFE6D8', '#9B7F55'], bedroom: ['#1E1C1A', '#C79A45'], pooja: ['#F3E7CE', '#B08A3E'],
    kids: ['#DDEAD1', '#6E9A55'], office: ['#131C2C', '#C9A24B'], school: ['#EAF2F8', '#3E7CB1'],
    balcony: ['#2A4B2E', '#7CB262'], flooring: ['#D6B98C', '#8A6740']
  };

  const roomsGrid = $('#rooms-grid');
  if (roomsGrid) {
    roomsGrid.innerHTML = ROOMS.map((r, i) => {
      const n = COLLECTION.filter((d) => d.room === r.id).length;
      return `
        <a class="room reveal" data-delay="${i % 4}" href="collection.html?room=${r.id}">
          <img src="${ROOM_IMG[r.id]}" alt="" loading="lazy" decoding="async"
               data-tone="${ROOM_TONE[r.id].join('|')}" data-swatch-label="${esc(r.label)}">
          <span class="room__count num">${n} designs</span>
          <span class="room__name">${esc(r.label)}</span>
          <span class="room__note">${esc(r.note)}</span>
        </a>`;
    }).join('');
    guardImages(roomsGrid);
    watch(roomsGrid);
  }

  /* Myths */
  const mythsEl = $('#myths-grid');
  if (mythsEl && typeof MYTHS !== 'undefined') {
    mythsEl.innerHTML = MYTHS.map((x, i) => `
      <button class="myth reveal" data-delay="${i % 2}" aria-expanded="${i === 0}">
        <span class="myth__q">
          <span class="myth__idx num">0${i + 1}</span>
          <span class="myth__m"><s>${esc(x.m)}</s></span>
          <span class="myth__toggle" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>
          </span>
        </span>
        <span class="myth__a"><span><span class="myth__fact"><span class="myth__fact-label">Fact</span>${esc(x.f)}</span></span></span>
      </button>`).join('');
    mythsEl.addEventListener('click', (e) => {
      const b = e.target.closest('.myth');
      if (b) b.setAttribute('aria-expanded', b.getAttribute('aria-expanded') === 'true' ? 'false' : 'true');
    });
    watch(mythsEl);
  }

  /* Contact form */
  const roomSel = $('#f-room');
  if (roomSel) {
    roomSel.innerHTML = ROOMS.map((r) => `<option value="${r.id}">${esc(r.label)}</option>`).join('')
      + '<option value="other">Somewhere else</option>';
  }
  const form = $('#enquiry');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const note = $('#form-note');
      const name = $('#f-name').value.trim();
      const phone = $('#f-phone').value.trim();
      if (!name || !phone) {
        note.textContent = 'We need a name and a phone number to call you back.';
        note.className = 'form__note';
        note.style.color = 'var(--accent)';
        return;
      }
      /* PHASE 2: point this at your form endpoint (Formspree, your CRM,
         or a mailto handler). For now it hands off to WhatsApp so no
         enquiry is ever lost while the backend is wired up. */
      const msg = `New enquiry from the website%0A%0AName: ${encodeURIComponent(name)}%0APhone: ${encodeURIComponent(phone)}%0ARoom: ${encodeURIComponent($('#f-room').selectedOptions[0].text)}%0ANeed: ${encodeURIComponent($('#f-type').value)}%0ANotes: ${encodeURIComponent($('#f-msg').value.trim() || '—')}`;
      window.open('https://wa.me/919920770172?text=' + msg, '_blank', 'noopener');
      note.textContent = 'Thanks ' + name + ' — opening WhatsApp so you can send it straight through.';
      note.style.color = 'var(--accent)';
      form.reset();
      if (roomSel) roomSel.selectedIndex = 0;
    });
  }

  /* =========================================================
     COLLECTION PAGE
     ========================================================= */
  const grid = $('#col-grid');
  if (!grid) return;

  const params = new URLSearchParams(location.search);
  const state = { room: params.get('room') || 'all', theme: params.get('theme') || 'all' };

  const roomBar  = $('#f-rooms');
  const themeBar = $('#f-themes');
  const countEl  = $('#col-count');
  const titleEl  = $('#col-title');

  function chips(bar, items, key) {
    bar.innerHTML = `<span class="fchip__lbl">${key === 'room' ? 'Room' : 'Theme'}</span>`
      + `<button class="fchip" data-k="${key}" data-v="all">All</button>`
      + items.map((i) => `<button class="fchip" data-k="${key}" data-v="${i.id}">${esc(i.label)}</button>`).join('');
  }
  chips(roomBar, ROOMS, 'room');
  chips(themeBar, THEMES, 'theme');

  function sync() {
    $$('.fchip').forEach((c) => c.setAttribute('aria-pressed', String(state[c.dataset.k] === c.dataset.v)));

    const list = COLLECTION.filter((d) =>
      (state.room === 'all' || d.room === state.room) &&
      (state.theme === 'all' || d.theme === state.theme));

    countEl.textContent = list.length + (list.length === 1 ? ' design' : ' designs');

    titleEl.textContent =
      state.room === 'all' && state.theme === 'all' ? 'The full collection'
      : state.room !== 'all' && state.theme !== 'all' ? `${themeLabel(state.theme)} for ${roomPhrase(state.room)}`
      : state.room !== 'all' ? roomLabel(state.room)
      : themeLabel(state.theme);

    grid.innerHTML = list.length
      ? list.map((d, i) => tileHTML(d).replace('class="tile ', `data-delay="${i % 4}" class="tile `)).join('')
      : '';

    $('#col-empty').hidden = list.length > 0;
    guardImages(grid);
    watch(grid);
    requestAnimationFrame(() => $$('.reveal', grid).forEach((el) => el.classList.add('is-visible')));

    const q = new URLSearchParams();
    if (state.room !== 'all') q.set('room', state.room);
    if (state.theme !== 'all') q.set('theme', state.theme);
    history.replaceState(null, '', location.pathname + (q.toString() ? '?' + q : ''));
  }

  document.addEventListener('click', (e) => {
    const c = e.target.closest('.fchip');
    if (!c) return;
    state[c.dataset.k] = c.dataset.v;
    sync();
  });

  $('#col-reset') && $('#col-reset').addEventListener('click', () => {
    state.room = 'all'; state.theme = 'all'; sync();
  });

  sync();
})();
