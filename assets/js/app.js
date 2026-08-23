/* ============================================================================
   WALL JEWELS — behaviour
   ----------------------------------------------------------------------------
   Enhancement only: every section renders complete without this file.
   One motion clock (var --beat); marks, not hues, for state; the docket
   never deletes — it voids, and a void can be restored.
   ========================================================================== */
(function () {
  'use strict';
  const $ = (s, c) => (c || document).querySelector(s);
  const $$ = (s, c) => [...(c || document).querySelectorAll(s)];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.documentElement.classList.remove('no-js');

  /* ---------------- smooth inertial scrolling (Lenis) ---------------- */
  let lenis = null;
  if (!reduced && typeof Lenis !== 'undefined') {
    document.documentElement.classList.add('has-lenis');
    lenis = new Lenis({ lerp: 0.085, wheelMultiplier: 1.0, touchMultiplier: 1.4 });
    const rafLoop = (t) => { lenis.raf(t); requestAnimationFrame(rafLoop); };
    requestAnimationFrame(rafLoop);
    /* in-page anchors glide instead of jump */
    document.addEventListener('click', (e) => {
      const a = e.target.closest('a[href^="#"]');
      if (!a) return;
      const target = document.getElementById(a.getAttribute('href').slice(1));
      if (!target) return;
      e.preventDefault();
      lenis.scrollTo(target, { offset: -88, duration: 1.35 });
    });
  }

  /* ---------------- Scroll Restoration & Logo Navigation ---------------- */
  if ('scrollRestoration' in history) {
    history.scrollRestoration = 'manual';
  }

  // Smooth top-level navigation when clicking logo on home page
  document.addEventListener('click', (e) => {
    const logo = e.target.closest('.wordmark, a[href="index.html"]');
    if (logo && (location.pathname.endsWith('index.html') || location.pathname === '/' || location.pathname.endsWith('/'))) {
      e.preventDefault();
      if (lenis) {
        lenis.scrollTo(0, { duration: 1.2 });
      } else {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
      if (location.hash) {
        history.pushState('', document.title, window.location.pathname + window.location.search);
      }
    }
  });

  // On page refresh / load, reset to top if no deep link hash
  if (!window.location.hash) {
    if (lenis) {
      lenis.scrollTo(0, { immediate: true });
    } else {
      window.scrollTo(0, 0);
    }
  }

  const slugOf = (d) => d.img.split('/').pop().replace('.jpg', '');
  const bySlug = {};
  if (typeof COLLECTION !== 'undefined') COLLECTION.forEach(d => { bySlug[slugOf(d)] = d; });
  const volName = (id) => (typeof VOLUMES !== 'undefined' && (VOLUMES.find(v => v.id === id) || {}).name) || '';

  /* ---------------- header ---------------- */
  const header = $('.header');
  addEventListener('scroll', () => {
    header && header.classList.toggle('is-scrolled', scrollY > 8);
  }, { passive: true });

  const drawer = $('.drawer');
  $('[data-open-drawer]') && $('[data-open-drawer]').addEventListener('click', () => {
    drawer.classList.add('is-open');
    drawer.removeAttribute('inert');
    document.body.style.overflow = 'hidden';
  });
  const closeDrawer = () => {
    if (!drawer) return;
    drawer.classList.remove('is-open');
    drawer.setAttribute('inert', '');
    document.body.style.overflow = '';
  };
  $('[data-close-drawer]') && $('[data-close-drawer]').addEventListener('click', closeDrawer);
  drawer && $$('.drawer__nav a', drawer).forEach(a => a.addEventListener('click', closeDrawer));

  /* ---------------- reveals ---------------- */
  const io = new IntersectionObserver((ents) => {
    ents.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
  }, { threshold: 0.16, rootMargin: '0px 0px -6% 0px' });
  $$('.rv, .rv--wipe, .hero__title').forEach(n => io.observe(n));

  /* litany lines light as they pass the middle of the screen */
  const litanyIO = new IntersectionObserver((ents) => {
    ents.forEach(e => e.target.classList.toggle('is-in', e.isIntersecting));
  }, { rootMargin: '-42% 0px -42% 0px' });
  $$('.litany__lines p').forEach(p => litanyIO.observe(p));

  /* ---------------- parallax (committed rates, one clock) ---------------- */
  const plx = $$('[data-plx]');
  if (plx.length && !reduced) {
    let ticking = false;
    const step = () => {
      ticking = false;
      const vh = innerHeight;
      plx.forEach(n => {
        const r = n.parentElement.getBoundingClientRect();
        if (r.bottom < -80 || r.top > vh + 80) return;
        const p = (r.top + r.height / 2 - vh / 2) / (vh / 2 + r.height / 2);
        n.style.transform = `translate3d(0, ${(-p * parseFloat(n.dataset.plx) * 100).toFixed(2)}px, 0)`;
      });
    };
    addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(step); } }, { passive: true });
    step();
  }

  /* ---------------- rails ---------------- */
  $$('.rail-zone').forEach(zone => {
    const rail = $('.rail', zone);
    if (!rail) return;
    const prev = $('[data-rail-prev]', zone), next = $('[data-rail-next]', zone);
    const stepBy = () => Math.min(rail.clientWidth * 0.8, 420);
    prev && prev.addEventListener('click', () => rail.scrollBy({ left: -stepBy(), behavior: reduced ? 'auto' : 'smooth' }));
    next && next.addEventListener('click', () => rail.scrollBy({ left: stepBy(), behavior: reduced ? 'auto' : 'smooth' }));
    const sync = () => {
      if (prev) prev.disabled = rail.scrollLeft < 20;
      if (next) next.disabled = rail.scrollLeft > rail.scrollWidth - rail.clientWidth - 20;
    };
    rail.addEventListener('scroll', sync, { passive: true });
    sync();
  });

  /* plate tilt — quiet 3D, pointer only */
  if (matchMedia('(hover: hover)').matches && !reduced) {
    $$('.plate').forEach(p => {
      p.addEventListener('pointermove', (e) => {
        const r = p.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5;
        const y = (e.clientY - r.top) / r.height - 0.5;
        p.style.transform = `perspective(900px) rotateY(${(x * 5).toFixed(2)}deg) rotateX(${(-y * 4).toFixed(2)}deg) translateY(-4px)`;
      });
      p.addEventListener('pointerleave', () => { p.style.transform = ''; });
    });
  }

  /* ---------------- edit rows: floating peek ---------------- */
  const peek = $('.edit-row__peek');
  if (peek && matchMedia('(hover: hover)').matches) {
    $$('.edit-row').forEach(row => {
      row.addEventListener('pointerenter', () => {
        const img = row.dataset.peek;
        if (!img) return;
        peek.querySelector('img').src = img;
        peek.classList.add('is-on');
      });
      row.addEventListener('pointermove', (e) => {
        peek.style.left = Math.min(innerWidth - 260, e.clientX + 28) + 'px';
        peek.style.top = Math.min(innerHeight - 320, e.clientY - 150) + 'px';
      });
      row.addEventListener('pointerleave', () => peek.classList.remove('is-on'));
    });
  }

  /* ---------------- stores ---------------- */
  const store = {
    get wish() { try { return JSON.parse(localStorage.getItem('wjwp:wish') || '[]'); } catch { return []; } },
    set wish(v) { localStorage.setItem('wjwp:wish', JSON.stringify(v)); },
    get basket() { try { return JSON.parse(localStorage.getItem('wjwp:basket') || '[]'); } catch { return []; } },
    set basket(v) { localStorage.setItem('wjwp:basket', JSON.stringify(v)); }
  };

  const counts = () => {
    const w = store.wish.length, b = store.basket.filter(i => !i.void).length;
    $$('[data-count-wish]').forEach(n => n.textContent = w || '');
    $$('[data-count-basket]').forEach(n => n.textContent = b || '');
  };

  /* wishlist buttons */
  function syncWishButtons() {
    const w = store.wish;
    $$('.wish[data-slug]').forEach(b => b.setAttribute('aria-pressed', w.includes(b.dataset.slug)));
  }
  document.addEventListener('click', (e) => {
    const b = e.target.closest('.wish[data-slug]');
    if (!b) return;
    const slug = b.dataset.slug;
    let w = store.wish;
    if (w.includes(slug)) { w = w.filter(s => s !== slug); toast('Removed from your wishlist'); }
    else {
      w.push(slug);
      const d = bySlug[slug];
      toast((d ? `“${d.n}”` : 'Design') + ' marked on your wishlist');
    }
    store.wish = w;
    syncWishButtons(); counts();
  });

  /* add-to-docket buttons */
  document.addEventListener('click', (e) => {
    const b = e.target.closest('[data-add-basket]');
    if (!b) return;
    const slug = b.dataset.addBasket;
    const basket = store.basket;
    const hit = basket.find(i => i.slug === slug);
    if (hit) { hit.void = false; }
    else basket.push({ slug, void: false });
    store.basket = basket;
    counts(); renderDocket();
    const d = bySlug[slug];
    toast((d ? `“${d.n}”` : 'Design') + ' entered on your enquiry docket');
  });

  /* ---------------- docket ---------------- */
  const docket = $('.docket'), scrim = $('.docket-scrim');
  const openDocket = () => {
    if (!docket) return;
    renderDocket();
    docket.classList.add('is-open'); scrim.classList.add('is-open');
    docket.removeAttribute('inert');
    document.body.style.overflow = 'hidden';
    const first = $('.docket__void, input', docket);
    first && first.focus({ preventScroll: true });
  };
  const closeDocket = () => {
    if (!docket) return;
    docket.classList.remove('is-open'); scrim.classList.remove('is-open');
    docket.setAttribute('inert', '');
    document.body.style.overflow = '';
  };
  $$('[data-open-docket]').forEach(b => b.addEventListener('click', openDocket));
  $('[data-close-docket]') && $('[data-close-docket]').addEventListener('click', closeDocket);
  scrim && scrim.addEventListener('click', closeDocket);
  addEventListener('keydown', (e) => {
    if (e.key === 'Escape') { closeDocket(); closeSearch(); closeDrawer(); }
  });

  function renderDocket() {
    const list = $('.docket__list');
    if (!list) return;
    const basket = store.basket;
    if (!basket.length) {
      list.innerHTML = `<div class="docket__empty">
        <svg width="54" height="54" viewBox="0 0 54 54" fill="none" aria-hidden="true">
          <circle cx="27" cy="27" r="18" stroke="currentColor" stroke-width="1.2"/>
          <circle cx="27" cy="27" r="2" fill="currentColor"/>
          <circle cx="27" cy="9" r="1.6" fill="currentColor"/><circle cx="45" cy="27" r="1.6" fill="currentColor"/>
          <circle cx="27" cy="45" r="1.6" fill="currentColor"/><circle cx="9" cy="27" r="1.6" fill="currentColor"/>
        </svg>
        <p>Your docket is empty.<br>Mark any design “Add to enquiry” and it is entered here.</p>
      </div>`;
      return;
    }
    list.innerHTML = basket.map(item => {
      const d = bySlug[item.slug];
      if (!d) return '';
      return `<div class="docket__item ${item.void ? 'is-void' : ''}" data-slug="${item.slug}">
        <img src="${d.img}" alt="" loading="lazy">
        <div>
          <div class="docket__iname">${d.n}</div>
          <div class="docket__ivol">${volName(d.v)} · ${d.no}</div>
        </div>
        <button class="docket__void" data-void="${item.slug}">${item.void ? 'Restore' : 'Void'}</button>
      </div>`;
    }).join('');
  }
  document.addEventListener('click', (e) => {
    const b = e.target.closest('[data-void]');
    if (!b) return;
    const basket = store.basket;
    const hit = basket.find(i => i.slug === b.dataset.void);
    if (hit) hit.void = !hit.void;
    store.basket = basket;
    renderDocket(); counts();
  });

  /* docket → WhatsApp */
  const sendBtn = $('[data-send-docket]');
  sendBtn && sendBtn.addEventListener('click', () => {
    const live = store.basket.filter(i => !i.void).map(i => bySlug[i.slug]).filter(Boolean);
    const name = ($('#dk-name') || {}).value || '';
    const w = ($('#dk-w') || {}).value || '';
    const h = ($('#dk-h') || {}).value || '';
    const notes = ($('#dk-notes') || {}).value || '';
    let msg = 'Namaste Wall Jewels — I would like a consultation.\n';
    if (live.length) {
      msg += '\nDesigns on my docket:\n' + live.map(d => `• ${d.n} (${d.no})`).join('\n') + '\n';
    }
    if (w || h) msg += `\nWall size: ${w || '—'} ft wide × ${h || '—'} ft high`;
    if (name) msg += `\nName: ${name}`;
    if (notes) msg += `\nNotes: ${notes}`;
    open(`${CONTACT.whatsappHref}?text=${encodeURIComponent(msg)}`, '_blank', 'noopener');
  });

  /* ---------------- toast ---------------- */
  let toastT;
  function toast(text) {
    let t = $('.toast');
    if (!t) {
      t = document.createElement('div');
      t.className = 'toast';
      t.setAttribute('role', 'status');
      t.innerHTML = '<span class="dot"></span><span class="toast__msg"></span>';
      document.body.appendChild(t);
    }
    $('.toast__msg', t).textContent = text;
    t.classList.add('is-on');
    clearTimeout(toastT);
    toastT = setTimeout(() => t.classList.remove('is-on'), 2600);
  }

  /* ---------------- search ---------------- */
  const veil = $('.search-veil');
  const sInput = $('.search-box input');
  const sOut = $('.search-results');
  const openSearch = () => {
    if (!veil) { location.href = 'collection.html'; return; }
    veil.classList.add('is-open');
    veil.removeAttribute('inert');
    document.body.style.overflow = 'hidden';
    setTimeout(() => sInput && sInput.focus(), 80);
  };
  const closeSearch = () => {
    if (!veil) return;
    veil.classList.remove('is-open');
    veil.setAttribute('inert', '');
    document.body.style.overflow = '';
  };
  $$('[data-open-search]').forEach(b => b.addEventListener('click', openSearch));
  veil && veil.addEventListener('click', (e) => { if (e.target === veil) closeSearch(); });

  function searchRender(q) {
    if (!sOut) return;
    q = q.trim().toLowerCase();
    if (q.length < 2) { sOut.innerHTML = ''; return; }
    const hits = COLLECTION.filter(d => {
      const hay = `${d.n} ${d.no} ${d.c} ${d.s} ${d.b} ${volName(d.v)}`.toLowerCase();
      return q.split(/\s+/).every(w => hay.includes(w));
    }).slice(0, 9);
    sOut.innerHTML = hits.length
      ? hits.map(d => `<a href="collection.html#${slugOf(d)}">
          <img src="${d.img}" alt="" loading="lazy">
          <span><span class="sr-name">${d.n}</span><br><span class="sr-meta">${volName(d.v)} · ${d.no}</span></span>
        </a>`).join('')
      : `<a href="collection.html"><span><span class="sr-name">No design answers “${q}” yet</span><br>
         <span class="sr-meta">Browse the full collection — or WhatsApp us; if it exists, we can print it.</span></span></a>`;
  }
  sInput && sInput.addEventListener('input', () => searchRender(sInput.value));

  /* ---------------- visualiser & price calculator ---------------- */
  const cfg = $('#visualiser');
  if (cfg) {
    const img = $('[data-cfg-img]', cfg);
    const preview = $('[data-cfg-preview]', cfg);
    const fileIn = $('[data-cfg-file]', cfg);
    const urlIn = $('[data-cfg-url]', cfg);
    const wIn = $('#cfg-w'), hIn = $('#cfg-h'), fin = $('[data-cfg-fin]', cfg);
    const areaOut = $('[data-cfg-area]', cfg), priceOut = $('[data-cfg-price]', cfg);
    const waBtn = $('[data-cfg-wa]', cfg), note = $('[data-cfg-note]', cfg);
    const wLabel = $('[data-cfg-wlabel]', cfg), hLabel = $('[data-cfg-hlabel]', cfg);
    let source = 'our collection (Pichwai: Eternal Melody)';
    let uploaded = false;

    fileIn && fileIn.addEventListener('change', () => {
      const f = fileIn.files && fileIn.files[0];
      if (!f) return;
      img.src = URL.createObjectURL(f);
      source = `my uploaded reference (${f.name})`;
      uploaded = true;
      if (urlIn) urlIn.value = '';
      update();
      toast('Reference loaded — set your wall size to see it at scale');
    });
    urlIn && urlIn.addEventListener('change', () => {
      const u = urlIn.value.trim();
      if (!u) return;
      source = `this link: ${u}`;
      uploaded = false;
      const probe = new Image();
      probe.onload = () => { img.src = u; };
      probe.onerror = () => toast('That site blocks previews — the link will still be sent with your enquiry');
      probe.src = u;
      update();
    });

    const baseOut = $('[data-cfg-base]', cfg), gstOut = $('[data-cfg-gst]', cfg);
    const GST = 0.18;
    const inr = (n) => `₹${Math.round(n).toLocaleString('en-IN')}`;
    function update() {
      const w = parseFloat(wIn.value) || 0;
      const h = parseFloat(hIn.value) || 0;
      const rate = parseFloat(fin.value) || 120;
      const finName = fin.selectedOptions[0] ? fin.selectedOptions[0].dataset.name : 'Non-Woven';
      if (w >= 12 && h >= 12) {
        const sqft = (w * h) / 144;
        const base = sqft * rate;
        const gst = base * GST;
        const total = base + gst;
        areaOut.textContent = `${w}″ × ${h}″  ·  ${sqft.toFixed(1)} sq.ft`;
        baseOut.textContent = `${inr(base)}  ·  @ ₹${rate}/sq.ft`;
        gstOut.textContent = inr(gst);
        priceOut.textContent = inr(total);
        preview.style.aspectRatio = Math.min(2.6, Math.max(0.45, w / h));
        wLabel.textContent = `${w} in`;
        hLabel.textContent = `${h} in`;
        let msg = `Namaste Wall Jewels — I'd like a custom wallpaper.\n` +
          `Design: ${source}\n` +
          `Wall: ${w} × ${h} inches (${sqft.toFixed(1)} sq.ft)\n` +
          `Finish: ${finName} @ ₹${rate}/sq.ft\n` +
          `Wallpaper: ${inr(base)}\n` +
          `GST 18%: ${inr(gst)}\n` +
          `Total incl. GST: ${inr(total)}\n` +
          `Please confirm my exact quote.`;
        waBtn.href = `https://wa.me/919677042903?text=${encodeURIComponent(msg)}`;
        waBtn.hidden = false;
        note.hidden = !uploaded;
      } else {
        areaOut.textContent = 'enter your wall size above';
        baseOut.textContent = '—';
        gstOut.textContent = '—';
        priceOut.textContent = '—';
        waBtn.hidden = true;
        note.hidden = true;
        wLabel.textContent = 'Width';
        hLabel.textContent = 'Height';
      }
    }
    [wIn, hIn, fin].forEach(el => el && el.addEventListener('input', update));

    const finishRows = $$('[data-pick-finish]', cfg);
    finishRows.forEach((row, idx) => {
      row.addEventListener('click', () => {
        if (fin && fin.options[idx]) {
          fin.selectedIndex = idx;
          update();
        }
      });
    });

    update();
  }

  /* ---------------- journey stepper: artwork -> your wall ---------------- */
  const j2 = $('.journey2');
  if (j2) {
    const stage = $('.j2stage', j2);
    const items = $$('.j2list li', j2);
    let k = 0, jt = null, visible = false;
    const apply = (i) => {
      k = i;
      items.forEach((li, x) => li.classList.toggle('is-on', x === i));
      stage.dataset.k = i;
    };
    const restart = () => {
      clearInterval(jt);
      if (!reduced) jt = setInterval(() => {
        if (visible && !document.hidden) apply((k + 1) % items.length);
      }, 2400);
    };
    items.forEach((li, i) => li.addEventListener('click', () => { apply(i); restart(); }));
    new IntersectionObserver((ents) => { visible = ents[0].isIntersecting; }, { threshold: 0.35 }).observe(j2);
    apply(0);
    restart();
    j2.addEventListener('pointerenter', () => clearInterval(jt));
    j2.addEventListener('pointerleave', restart);
  }

  /* ---------------- collection page ---------------- */
  const grid = $('[data-coll-grid]');
  if (grid) {
    const chips = $$('.fchip[data-filter]');
    const countOut = $('[data-coll-count]');
    const state = { v: null, c: null, s: null, search: '' };
    const params = new URLSearchParams(location.search);
    ['v', 'c', 's'].forEach(k => { if (params.get(k)) state[k] = params.get(k); });
    if (params.get('search')) state.search = params.get('search');

    function match(d) {
      if (state.v && d.v !== state.v) return false;
      if (state.c && d.c !== state.c) return false;
      if (state.s && d.s !== state.s) return false;
      if (state.search) {
        const hay = `${d.n} ${d.no} ${d.c} ${d.s} ${d.b}`.toLowerCase();
        if (!state.search.toLowerCase().split(/\s+/).every(w => hay.includes(w))) return false;
      }
      return true;
    }
    function applyFilters() {
      let shown = 0;
      $$('.plate[data-slug]', grid).forEach(p => {
        const d = bySlug[p.dataset.slug];
        const on = d && match(d);
        p.style.display = on ? '' : 'none';
        if (on) shown++;
      });
      if (countOut) countOut.textContent = `${shown} design${shown === 1 ? '' : 's'}`;
      $('.coll-empty') && ($('.coll-empty').style.display = shown ? 'none' : '');
      chips.forEach(ch => {
        const [k, v] = ch.dataset.filter.split(':');
        ch.setAttribute('aria-pressed', state[k] === v);
      });
    }
    chips.forEach(ch => ch.addEventListener('click', () => {
      const [k, v] = ch.dataset.filter.split(':');
      state[k] = state[k] === v ? null : v;
      applyFilters();
    }));
    applyFilters();
    if (location.hash) {
      const target = $(location.hash);
      if (target) setTimeout(() => target.scrollIntoView({ block: 'center' }), 60);
    }
  }

  /* ---------------- hero slideshow (every 3s) ---------------- */
  const slides = $$('.hero__media .slide');
  if (slides.length) {
    const dotsHost = $('.hero__dots');
    let cur = 0, timer = null;
    const dots = slides.map((s, i) => {
      if (!dotsHost) return null;
      const b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('aria-label', `Show design ${i + 1} of ${slides.length}`);
      b.addEventListener('click', () => { go(i); restart(); });
      dotsHost.appendChild(b);
      return b;
    });
    function go(k) {
      const prevMedia = $('video', slides[cur]);
      prevMedia && prevMedia.pause();
      slides[cur].classList.remove('is-on');
      dots[cur] && dots[cur].setAttribute('aria-current', 'false');
      cur = (k + slides.length) % slides.length;
      slides[cur].classList.add('is-on');
      dots[cur] && dots[cur].setAttribute('aria-current', 'true');
      const media = $('img,video', slides[cur]);
      if (media && media.tagName === 'VIDEO') {
        if (media.preload === 'none') media.preload = 'auto';
        media.play && media.play().catch(() => {});
        const nxt = $('video', slides[(cur + 1) % slides.length]);
        if (nxt && nxt.preload === 'none') nxt.preload = 'auto';
      }
      const title = (media && media.dataset.title) || '';
      const [dn, dc] = title.split(' · ');
      const nameEl = $('.hero__dname'), metaEl = $('.hero__dmeta');
      if (nameEl && dn) nameEl.textContent = dn;
      if (metaEl) metaEl.textContent = `${dc || 'Wall Jewels'} · Where walls become art — since 1978`;
    }
    const HOLD = $('.hero__media video') ? 6000 : 3000; /* films need room to breathe */
    function restart() {
      clearInterval(timer);
      if (!reduced) timer = setInterval(() => { if (!document.hidden) go(cur + 1); }, HOLD);
    }
    go(0);
    restart();
    const hero = $('.hero');
    hero && hero.addEventListener('pointerenter', () => clearInterval(timer));
    hero && hero.addEventListener('pointerleave', restart);
  }

  /* ---------------- lightbox: any artwork click opens full view ---------------- */
  const LB_SEL = '.plate__media img, .tile__img img, .space__img img, .volume__media img, .feature__media img, .journey__art img, .hero__media .slide.is-on img, .soon img';
  let lb = null;
  function ensureLB() {
    if (lb) return lb;
    lb = document.createElement('div');
    lb.className = 'lightbox';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-label', 'Design full view');
    lb.innerHTML = `
      <button class="lightbox__close" type="button" aria-label="Close full view">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
          <path d="M4 4 L16 16 M16 4 L4 16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
      </button>
      <figure><img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 4 3'%3E%3Crect width='4' height='3' fill='%23191c23'/%3E%3C/svg%3E" alt=""><figcaption></figcaption></figure>`;
    document.body.appendChild(lb);
    lb.addEventListener('click', (e) => {
      if (e.target === lb || e.target.closest('.lightbox__close')) closeLightbox();
    });
    return lb;
  }
  function openLightbox(src, alt) {
    const box = ensureLB();
    const img = $('img', box);
    img.src = src;
    img.alt = alt || '';
    $('figcaption', box).textContent = (alt || '').split(' — ')[0];
    box.classList.add('is-open');
    document.body.style.overflow = 'hidden';
    $('.lightbox__close', box).focus({ preventScroll: true });
  }
  function closeLightbox() {
    if (!lb) return;
    lb.classList.remove('is-open');
    document.body.style.overflow = '';
  }
  document.addEventListener('click', (e) => {
    const img = e.target.closest(LB_SEL);
    if (!img) return;
    if (img.closest('[data-open-catalogue]')) return; /* catalogue viewer owns these */
    const a = img.closest('a');
    if (a) e.preventDefault();
    openLightbox(img.currentSrc || img.src, img.alt);
  });
  addEventListener('keydown', (e) => { if (e.key === 'Escape') closeLightbox(); });
  /* hero films open their full still artwork */
  document.addEventListener('click', (e) => {
    const v = e.target.closest('.hero__media .slide.is-on video');
    if (!v || !v.dataset.full) return;
    openLightbox(v.dataset.full, v.getAttribute('aria-label') || '');
  });

  /* ---------------- catalogue viewer: flip through the volumes ---------------- */
  const CATALOGUES = {
    kp: { name: 'Kala Parampara · Volume I', count: 82, prefix: 'assets/img/catalogue/kp-' },
    kr: { name: 'Kala Rasa · Volume II', count: 189, prefix: 'assets/img/catalogue/kr-' }
  };
  const catViews = {};
  let activeCat = null;

  function buildCatView(id) {
    const c = CATALOGUES[id];
    const view = document.createElement('div');
    view.className = 'catview';
    view.setAttribute('role', 'dialog');
    view.setAttribute('aria-label', `${c.name} — catalogue`);
    view.innerHTML = `
      <div class="catview__bar">
        <span class="catview__title">${c.name}</span>
        <span class="catview__count"><span data-cat-cur>1</span> / ${c.count}</span>
        <button class="tool" type="button" data-cat-close aria-label="Close the catalogue">
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" width="22" height="22">
            <path d="M6 6 L18 18 M18 6 L6 18" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
        </button>
      </div>
      <div class="catview__strip" tabindex="0"></div>
      <button class="catview__nav catview__nav--prev" type="button" aria-label="Previous page">
        <svg width="18" height="18" viewBox="0 0 16 16" fill="none"><path d="M14 8 H2 M7 3 L2 8 L7 13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </button>
      <button class="catview__nav catview__nav--next" type="button" aria-label="Next page">
        <svg width="18" height="18" viewBox="0 0 16 16" fill="none"><path d="M2 8 H14 M9 3 L14 8 L9 13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </button>
      <p class="catview__hint">Scroll or swipe through the pages · click a page for full view · Esc to close</p>`;
    const strip = $('.catview__strip', view);
    for (let i = 0; i < c.count; i++) {
      const pg = document.createElement('div');
      pg.className = 'catview__page';
      pg.innerHTML = `<img data-src="${c.prefix}${String(i).padStart(3, '0')}.jpg"
        src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1280 717'%3E%3Crect width='1280' height='717' fill='%23191c23'/%3E%3C/svg%3E"
        alt="${c.name} — page ${i + 1}" decoding="async"><span class="pgnum">${i + 1}</span>`;
      strip.appendChild(pg);
    }
    const lazyIO = new IntersectionObserver((ents) => {
      ents.forEach(e => {
        if (e.isIntersecting) {
          const im = $('img', e.target);
          if (im && im.dataset.src) { im.src = im.dataset.src; delete im.dataset.src; }
          lazyIO.unobserve(e.target);
        }
      });
    }, { root: strip, rootMargin: '0px 1600px 0px 1600px' });
    $$('.catview__page', strip).forEach(p => lazyIO.observe(p));

    const cur = $('[data-cat-cur]', view);
    const pageStep = () => strip.querySelector('.catview__page').getBoundingClientRect().width + parseFloat(getComputedStyle(strip).gap || 24);
    strip.addEventListener('scroll', () => {
      cur.textContent = Math.min(c.count, Math.max(1, Math.round(strip.scrollLeft / pageStep()) + 1));
    }, { passive: true });
    $('.catview__nav--prev', view).addEventListener('click', () => strip.scrollBy({ left: -pageStep(), behavior: 'smooth' }));
    $('.catview__nav--next', view).addEventListener('click', () => strip.scrollBy({ left: pageStep(), behavior: 'smooth' }));
    $('[data-cat-close]', view).addEventListener('click', closeCatalogue);
    document.body.appendChild(view);
    return view;
  }
  function openCatalogue(id) {
    if (!CATALOGUES[id]) return;
    activeCat = catViews[id] || (catViews[id] = buildCatView(id));
    activeCat.classList.add('is-open');
    document.body.style.overflow = 'hidden';
    $('.catview__strip', activeCat).focus({ preventScroll: true });
  }
  function closeCatalogue() {
    if (!activeCat) return;
    activeCat.classList.remove('is-open');
    activeCat = null;
    document.body.style.overflow = '';
  }
  document.addEventListener('click', (e) => {
    const t = e.target.closest('[data-open-catalogue]');
    if (!t) return;
    e.preventDefault();
    openCatalogue(t.dataset.openCatalogue);
  });
  document.addEventListener('keydown', (e) => {
    if (!activeCat) return;
    if (e.key === 'Escape') { closeCatalogue(); return; }
    const strip = $('.catview__strip', activeCat);
    const step = strip.querySelector('.catview__page').getBoundingClientRect().width + 24;
    if (e.key === 'ArrowRight') strip.scrollBy({ left: step, behavior: 'smooth' });
    if (e.key === 'ArrowLeft') strip.scrollBy({ left: -step, behavior: 'smooth' });
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.target.matches && e.target.matches('[data-open-catalogue]')) {
      openCatalogue(e.target.dataset.openCatalogue);
    }
  });

  /* ---------------- 3D Cover Flow Carousels ---------------- */
  function initCoverflow() {
    const sections = $$('.coverflow-section');
    if (!sections.length) return;

    sections.forEach(section => {
      const stage = $('[data-coverflow]', section);
      if (!stage) return;

      const cards = $$('.coverflow-card', stage);
      if (!cards.length) return;

      const currEl = $('.cf-curr', section);
      const totalEl = $('.cf-total', section);
      const prevBtn = $('.cf-prev', section);
      const nextBtn = $('.cf-next', section);
      const toggleBtn = $('.cf-toggle', section);
      const iconPause = toggleBtn ? $('.icon-pause', toggleBtn) : null;
      const iconPlay = toggleBtn ? $('.icon-play', toggleBtn) : null;

      let current = 0;
      const total = cards.length;
      let isPlaying = true;
      let timer = null;

      if (totalEl) totalEl.textContent = total;

      function render() {
        const isMobile = window.innerWidth <= 768;
        const xSpacing = isMobile ? 85 : 130;
        const zDepth = isMobile ? 55 : 85;
        const rotAngle = isMobile ? 18 : 22;

        cards.forEach((card, idx) => {
          let diff = idx - current;

          // Circular wrap for smooth nearest path
          if (diff > total / 2) diff -= total;
          if (diff < -total / 2) diff += total;

          const absDiff = Math.abs(diff);
          const isCenter = diff === 0;

          if (isCenter) {
            card.style.transform = `translate3d(0, 0, 40px) scale(1.06) rotateY(0deg)`;
            card.style.opacity = '1';
            card.style.filter = 'none';
            card.style.zIndex = '30';
            card.style.pointerEvents = 'auto';
            card.classList.add('is-active');
          } else if (absDiff <= 3) {
            const sign = Math.sign(diff);
            const tx = sign * (xSpacing * (1 + (absDiff - 1) * 0.7));
            const tz = -absDiff * zDepth;
            const ry = -sign * rotAngle;
            const scale = Math.max(0.68, 1 - absDiff * 0.11);
            const opacity = Math.max(0.25, 1 - absDiff * 0.28);
            const blur = Math.min(2, absDiff * 0.7);

            card.style.transform = `translate3d(${tx}px, 0, ${tz}px) scale(${scale}) rotateY(${ry}deg)`;
            card.style.opacity = opacity.toString();
            card.style.filter = `blur(${blur}px)`;
            card.style.zIndex = (20 - absDiff).toString();
            card.style.pointerEvents = 'auto';
            card.classList.remove('is-active');
          } else {
            card.style.transform = `translate3d(${Math.sign(diff) * 320}px, 0, -300px) scale(0.5)`;
            card.style.opacity = '0';
            card.style.filter = 'blur(4px)';
            card.style.zIndex = '0';
            card.style.pointerEvents = 'none';
            card.classList.remove('is-active');
          }
        });

        if (currEl) currEl.textContent = (current + 1);
      }

      function goTo(idx) {
        current = (idx + total) % total;
        render();
      }

      function next() { goTo(current + 1); }
      function prev() { goTo(current - 1); }

      function startAuto() {
        stopAuto();
        if (isPlaying) {
          timer = setInterval(next, 3800);
        }
      }

      function stopAuto() {
        if (timer) { clearInterval(timer); timer = null; }
      }

      // Card click: center that card
      cards.forEach((card, idx) => {
        card.addEventListener('click', (e) => {
          if (current !== idx) {
            e.preventDefault();
            goTo(idx);
            startAuto();
          }
        });
      });

      // Button controls
      prevBtn && prevBtn.addEventListener('click', () => { prev(); startAuto(); });
      nextBtn && nextBtn.addEventListener('click', () => { next(); startAuto(); });

      // Toggle autoplay
      toggleBtn && toggleBtn.addEventListener('click', () => {
        isPlaying = !isPlaying;
        if (isPlaying) {
          if (iconPause) iconPause.style.display = 'block';
          if (iconPlay) iconPlay.style.display = 'none';
          startAuto();
        } else {
          if (iconPause) iconPause.style.display = 'none';
          if (iconPlay) iconPlay.style.display = 'block';
          stopAuto();
        }
      });

      // Pause on hover
      stage.addEventListener('mouseenter', stopAuto);
      stage.addEventListener('mouseleave', () => { if (isPlaying) startAuto(); });

      // Touch & swipe gestures
      let startX = 0;
      let isSwiping = false;

      stage.addEventListener('touchstart', (e) => {
        startX = e.touches[0].clientX;
        isSwiping = true;
        stopAuto();
      }, { passive: true });

      stage.addEventListener('touchend', (e) => {
        if (!isSwiping) return;
        isSwiping = false;
        const endX = e.changedTouches[0].clientX;
        const diff = endX - startX;
        if (Math.abs(diff) > 40) {
          if (diff > 0) prev();
          else next();
        }
        startAuto();
      }, { passive: true });

      window.addEventListener('resize', render, { passive: true });
      render();
      startAuto();
    });
  }

  /* ---------------- boot ---------------- */
  counts(); syncWishButtons(); renderDocket(); initCoverflow();
})();
