/* ============================================================================
   WALL JEWELS — behaviour
   ----------------------------------------------------------------------------
   Enhancement only: every section renders complete without this file.
   One motion clock (var --beat); marks, not hues, for state; the docket
   never deletes — it voids, and a void can be restored.
   ========================================================================== */
(function () {
  'use strict';
  // Permanent WJ Diamond Favicon Lock
  (function lockWJFavicon() {
    try {
      const uri = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAADxElEQVR4nN1WTYgcRRR+9b2qnh9nMtlNYlwNRoRcPERkRQlR8CJ4iafsTdGgBxG85SYheApegooQEQTBk4oKoqISUNSLsprc/EEUkRU0i9nM7s5MT1f1k9dTHRo17szuzh580FRXvVff+3/dRP8XOk0EXYXI7KReI1HxpgFoa3dFXxaJ3N5O50Aty25zIsmefv9dIspN5E/LALq4f/91s2trt0qe39LK/d21IAcTymeczx9UbEMUNsKwkyrVHKtnv7bbh8zq6tFmlh1uh/AQSLre4G0Cf24oz2VMbExqQHln92Bw5/Vp+mwjzzNLMgDRLm/MbAA+jnJhKgYYoqBRaGXZW4boBBtz8wB8kcjsM8as19P0FyHicfK/bdSr148MrH2tmyTHryUjIhCR7W1RIWJ9ohEHPfCFB85fajRulEqL6jrRfJARMErweGbKfeQXgELkVHZo7SmBETFGhpZfjTy71TlB/2V51cuetUcE8GKMD8D6cqNxoJRbc+6OP2dmOhvhUQnWd+6EBz7sJclC6cnS3FwzZX7BAxeGzK90W6195R1FfGNhgT3wvUZAAOlb+wSJmNS5c7r3wGfjGGB0pmfMPyhQYKR/NJtzyhta+0EBHhV45guXO53dMVVOZVLms8oTY4IHvk6tPV/KZ8zPV528lgFW14G1JwXIBSbXSKjHYgpgCUBfgFTznTKfifdqWherzh0OQBBj9G4hn4+UP1Mq3zACRERX2u09Abis+YweFY8HPrnSbh/ywHcCEwLw2/Ls7K6yOFPnHg1AVtwzJgvAz4MkObah5/8WhZT5uah8tSgs5qUyHSnzixod5afOPaZnA5ucumos1PAiQmcjZo3GpdOjMOH3ZvOGwPyjAgUg7ddq90UwrCfJsUqul4bWflQq90BfuyC+v1edFWOTxFRopfece3jNudvjeQGkLeWBlVGui1qRaOi3K83mvAcWowFfVvE2ZURJlalWGDG09qnC6/hk1r6utVPwgPfVgAz4Rvebnr8yGjT/mGalcT1rj6bA4z1r76mwjQc+jREoe39r03DMCBW5Xm40bvJAV4s0Yz4XeRP/d4xFUamNa6JnqXMvFTMDkF69fm8pR9MkiZNwPUmOh9H3QIbAm1ML/99rRN9XarUHAnityD3zV9opE3+GJ6FqWHvOPaIjV8M+tPadsb58WyGJwIvz8y5j+7IqDsClobVPVmQwzbCbfq12v2f+KQCDjPlMOaanHXboum7tXRnz4tDap7ut1t4Kf7rVXlLZcpX91V+0HSUZzYCdV7yd9BdkGd/XhbBmKgAAAABJRU5ErkJggg==";
      let links = document.querySelectorAll("link[rel*='icon']");
      links.forEach(l => l.href = uri);
      if (links.length === 0) {
        const l = document.createElement('link');
        l.rel = 'icon';
        l.type = 'image/png';
        l.href = uri;
        document.head.appendChild(l);
      }
    } catch (e) {}
  })();

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

  /* ---------------- Light / Dark Theme Switcher (Dark default) ---------------- */
  const themeToggle = $('#theme-toggle');
  const applyTheme = (isLight) => {
    if (isLight) {
      document.documentElement.setAttribute('data-theme', 'light');
      document.body.classList.add('theme-light');
      if (themeToggle) themeToggle.checked = false;
    } else {
      document.documentElement.removeAttribute('data-theme');
      document.body.classList.remove('theme-light');
      if (themeToggle) themeToggle.checked = true;
    }
    // Switch header & drawer logo dynamically (Footer always stays dark)
    document.querySelectorAll('.header .wordmark img, .drawer__head .wordmark img').forEach(img => {
      img.src = isLight ? 'assets/img/brand/logo-light.png' : 'assets/img/brand/logo-dark.png';
    });
  };

  const savedTheme = localStorage.getItem('wj-theme');
  if (savedTheme === 'light') {
    applyTheme(true);
  } else {
    applyTheme(false); // default dark
  }

  if (themeToggle) {
    themeToggle.addEventListener('change', (e) => {
      const isLight = !e.target.checked;
      applyTheme(isLight);
      localStorage.setItem('wj-theme', isLight ? 'light' : 'dark');
    });
  }

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
    let uploaded = false;
    let currentUploadedFile = null;
    let uploadedFileName = '';
    let uploadedImageHostedUrl = '';
    let pastedLink = '';
    let lastGeneratedMsg = '';

    async function uploadReferenceImage(file) {
      try {
        const fd = new FormData();
        fd.append('files[]', file, file.name);
        const res = await fetch('https://uguu.se/upload.php?output=json', {
          method: 'POST',
          body: fd
        });
        const data = await res.json();
        if (data && data.success && data.files && data.files[0] && data.files[0].url) {
          return data.files[0].url;
        }
      } catch (err) {
        console.warn('Primary image host fallback:', err);
      }

      try {
        const fd2 = new FormData();
        fd2.append('file', file, file.name);
        const res2 = await fetch('https://tmpfiles.org/api/v1/upload', {
          method: 'POST',
          body: fd2
        });
        const data2 = await res2.json();
        if (data2 && data2.status === 'success' && data2.data && data2.data.url) {
          return data2.data.url.replace('tmpfiles.org/', 'tmpfiles.org/dl/');
        }
      } catch (err2) {
        console.warn('Secondary image host fallback:', err2);
      }
      return '';
    }

    fileIn && fileIn.addEventListener('change', async () => {
      const f = fileIn.files && fileIn.files[0];
      if (!f) return;
      currentUploadedFile = f;
      img.src = URL.createObjectURL(f);
      uploaded = true;
      uploadedFileName = f.name;
      uploadedImageHostedUrl = '';
      pastedLink = '';
      if (urlIn) urlIn.value = '';
      update();
      toast('Reference loaded — preparing WhatsApp image link...');

      const remoteUrl = await uploadReferenceImage(f);
      if (remoteUrl) {
        uploadedImageHostedUrl = remoteUrl;
        update();
      }
    });

    urlIn && urlIn.addEventListener('change', () => {
      const u = urlIn.value.trim();
      if (!u) return;
      currentUploadedFile = null;
      uploaded = false;
      uploadedFileName = '';
      uploadedImageHostedUrl = '';
      pastedLink = u;
      const probe = new Image();
      probe.onload = () => { img.src = u; };
      probe.onerror = () => toast('That site blocks previews — the link will still be sent with your enquiry');
      probe.src = u;
      update();
    });

    const baseOut = $('[data-cfg-base]', cfg), gstOut = $('[data-cfg-gst]', cfg);
    const GST = 0.18;
    const inr = (n) => `₹${Math.round(n).toLocaleString('en-IN')}`;
    let customDesignName = '';

    window.loadDesignIntoVisualiser = function(src, name) {
      if (!src) return;
      uploaded = false;
      currentUploadedFile = null;
      uploadedFileName = '';
      uploadedImageHostedUrl = '';
      pastedLink = '';
      customDesignName = name || '';
      img.src = src;
      img.alt = name || 'Wall Jewels Wallpaper Design';
      if (fileIn) fileIn.value = '';
      if (urlIn) urlIn.value = '';
      update();
      cfg.scrollIntoView({ behavior: 'smooth', block: 'center' });
      cfg.classList.add('is-highlighted');
      setTimeout(() => cfg.classList.remove('is-highlighted'), 2000);
      toast(`Loaded "${name || 'Wallpaper'}" into wall price calculator!`);
    };

    // Auto-load design into visualiser if passed in URL params
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('visualise')) {
      const vSrc = urlParams.get('visualise');
      const vName = urlParams.get('name') || 'Selected Wallpaper';
      setTimeout(() => {
        window.loadDesignIntoVisualiser(vSrc, vName);
      }, 350);
    }

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

        let designLine = '';
        if (uploaded) {
          if (uploadedImageHostedUrl) {
            designLine = `Design: my uploaded reference (${uploadedFileName || 'custom-reference.jpg'})\nReference Image: ${uploadedImageHostedUrl}\n`;
          } else {
            designLine = `Design: my uploaded reference (${uploadedFileName || 'custom-reference.jpg'})\n`;
          }
        } else if (pastedLink) {
          designLine = `Design: online link reference (${pastedLink})\n`;
        } else {
          const rawSrc = img.dataset.full || img.currentSrc || img.getAttribute('src') || '';
          const absSrc = rawSrc.startsWith('http') ? rawSrc : (window.location.origin + (rawSrc.startsWith('/') ? '' : '/') + rawSrc);
          const designName = customDesignName || (img.alt || 'Wall Jewels Collection').replace("Wallpaper preview at your wall's proportions", 'Lord Ganesha · Bespoke Collection');
          designLine = `Design: ${designName}\nPreview: ${absSrc}\n`;
        }

        let msg = `Namaste Wall Jewels — I'd like a custom wallpaper.\n` +
          `${designLine}` +
          `Wall: ${w} × ${h} inches (${sqft.toFixed(1)} sq.ft)\n` +
          `Finish: ${finName} @ ₹${rate}/sq.ft\n` +
          `Wallpaper: ${inr(base)}\n` +
          `GST 18%: ${inr(gst)}\n` +
          `Total incl. GST: ${inr(total)}\n` +
          `Please confirm my exact quote.`;

        lastGeneratedMsg = msg;
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

    waBtn && waBtn.addEventListener('click', async () => {
      if (uploaded && currentUploadedFile) {
        try {
          if (navigator.clipboard && window.ClipboardItem) {
            await navigator.clipboard.write([
              new ClipboardItem({ [currentUploadedFile.type || 'image/png']: currentUploadedFile })
            ]);
          }
        } catch (e) {
          // Clipboard write fallback
        }
      }
    });

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

  /* ---------------- lightbox: full gallery navigation with Next / Prev arrows ---------------- */
  let lb = null;
  let currentLbSrc = '';
  let currentLbTitle = '';
  let activeGalleryItems = [];
  let currentGalleryIndex = 0;

  function buildGalleryList() {
    // 1. If on collection.html with .card elements
    const visibleCards = Array.from(document.querySelectorAll('.card:not([hidden]), .plate, .tile, .feature'));
    if (visibleCards.length > 0) {
      const items = [];
      visibleCards.forEach(card => {
        const img = card.querySelector('img');
        if (!img) return;
        const s = img.dataset.full || img.currentSrc || img.getAttribute('src') || '';
        if (!s || s.includes('logo-') || s.includes('data:image')) return;
        const titleEl = card.querySelector('h3, h2, .card__title, .plate__title, .tile__name');
        const codeEl = card.querySelector('.chip, .plate__no, .card__no');
        const descEl = card.querySelector('p:not(.chip), .card__desc, .plate__desc');
        const title = (titleEl ? titleEl.textContent : (img.alt || img.title || '')).split(' — ')[0].split(' · ')[0].trim();
        const code = codeEl ? codeEl.textContent.trim() : '';
        const desc = descEl ? descEl.textContent.trim() : '';
        items.push({ src: s, title: title || 'Wall Jewels Original Wallpaper', code, desc });
      });
      if (items.length > 0) return items;
    }

    // 2. Fallback to COLLECTION array if available
    if (typeof COLLECTION !== 'undefined' && Array.isArray(COLLECTION) && COLLECTION.length > 0) {
      return COLLECTION.map(c => ({
        src: c.img,
        title: c.n,
        code: c.no || '',
        desc: c.b || ''
      }));
    }

    // 3. Fallback to all artwork images on page
    const allImgs = Array.from(document.querySelectorAll('img')).filter(i => {
      const s = i.currentSrc || i.src || '';
      return s && !s.includes('logo-') && !s.includes('data:image') && !i.closest('.wordmark, .header, .nav, .footer');
    });
    return allImgs.map(i => ({
      src: i.dataset.full || i.currentSrc || i.src,
      title: (i.alt || i.title || 'Wall Jewels Wallpaper').split(' — ')[0].split(' · ')[0].trim(),
      code: '',
      desc: ''
    }));
  }

  function ensureLB() {
    if (lb) return lb;
    lb = document.createElement('div');
    lb.className = 'lightbox';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-label', 'Design preview and quote');
    lb.innerHTML = `
      <button class="lightbox__close" type="button" aria-label="Close preview dialog">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
          <path d="M4 4 L16 16 M16 4 L4 16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
      </button>
      <button class="lightbox__nav lightbox__nav--prev" type="button" aria-label="Previous design">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
      </button>
      <button class="lightbox__nav lightbox__nav--next" type="button" aria-label="Next design">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </button>
      <div class="lightbox__dialog">
        <div class="lightbox__media">
          <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 4 3'%3E%3Crect width='4' height='3' fill='%23191c23'/%3E%3C/svg%3E" alt="">
        </div>
        <div class="lightbox__panel">
          <div class="lightbox__header-meta">
            <span class="lightbox__tag"><span class="dot-a"></span> WALL JEWELS · ORIGINAL DESIGN</span>
            <div class="lightbox__indicators">
              <span class="lightbox__code" style="display:none;"></span>
              <span class="lightbox__counter"></span>
            </div>
          </div>
          <h2 class="lightbox__title"></h2>
          <p class="lightbox__desc">
            Custom scaled and printed to your room proportions on your choice of 5 luxury architectural substrates. In-house manufactured in Chennai since 1978.
          </p>

          <div class="lightbox__badges">
            <span class="lightbox__badge">📐 Exact Room Sizing</span>
            <span class="lightbox__badge">✨ 5 Substrates from ₹120/sq.ft</span>
            <span class="lightbox__badge">⚡ 4-Hour Installation</span>
          </div>

          <div class="lightbox__actions">
            <button class="lightbox__calc-btn btn btn--fill" type="button">
              <span class="dot-a"></span>Visualise on My Wall &amp; Get Price
            </button>
            <a class="lightbox__wa-link btn btn--wa" target="_blank" rel="noopener" href="https://wa.me/919677042903">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" style="margin-right:6px;"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91C2.13 13.66 2.59 15.36 3.45 16.86L2.05 22L7.3 20.62C8.75 21.41 10.38 21.83 12.04 21.83C17.5 21.83 21.95 17.38 21.95 11.92C21.95 6.46 17.5 2 12.04 2ZM12.04 20.15C10.56 20.15 9.11 19.76 7.85 19.01L7.55 18.83L4.44 19.65L5.27 16.61L5.07 16.29C4.24 14.97 3.8 13.46 3.8 11.91C3.8 7.37 7.5 3.67 12.05 3.67C14.25 3.67 16.32 4.53 17.88 6.09C19.44 7.65 20.3 9.72 20.3 11.92C20.29 16.46 16.59 20.15 12.04 20.15ZM16.56 14.39C16.31 14.27 15.09 13.67 14.86 13.58C14.63 13.5 14.47 13.46 14.3 13.7C14.14 13.95 13.67 14.5 13.53 14.67C13.38 14.83 13.24 14.85 12.99 14.73C12.74 14.6 11.95 14.34 11.01 13.5C10.28 12.85 9.78 12.04 9.64 11.8C9.5 11.55 9.62 11.41 9.75 11.29C9.86 11.17 10 10.99 10.12 10.85C10.25 10.71 10.29 10.61 10.37 10.44C10.45 10.28 10.41 10.13 10.35 10.01C10.29 9.89 9.8 8.68 9.59 8.19C9.4 7.71 9.2 7.77 9.05 7.76H8.58C8.42 7.76 8.15 7.82 7.93 8.07C7.7 8.31 7.07 8.9 7.07 10.12C7.07 11.33 7.95 12.5 8.08 12.67C8.2 12.83 9.82 15.34 12.3 16.41C12.89 16.66 13.35 16.82 13.71 16.93C14.3 17.12 14.84 17.09 15.27 17.03C15.74 16.96 16.73 16.43 16.93 15.86C17.14 15.29 17.14 14.8 17.08 14.7C17.01 14.6 16.81 14.52 16.56 14.39Z"/></svg>
              WhatsApp Design Team for this Wallpaper
            </a>
          </div>

          <span class="lightbox__note">✦ Free on-site measurement &amp; white-glove installation support</span>
        </div>
      </div>`;
    document.body.appendChild(lb);

    lb.addEventListener('click', (e) => {
      if (e.target === lb || e.target.closest('.lightbox__close')) closeLightbox();
    });

    const prevBtn = $('.lightbox__nav--prev', lb);
    prevBtn && prevBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      renderGalleryItem(currentGalleryIndex - 1);
    });

    const nextBtn = $('.lightbox__nav--next', lb);
    nextBtn && nextBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      renderGalleryItem(currentGalleryIndex + 1);
    });

    // Touch swipe support on dialog
    let touchStartX = 0;
    let touchStartY = 0;
    lb.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
      touchStartY = e.changedTouches[0].screenY;
    }, { passive: true });

    lb.addEventListener('touchend', (e) => {
      const touchEndX = e.changedTouches[0].screenX;
      const touchEndY = e.changedTouches[0].screenY;
      const dx = touchEndX - touchStartX;
      const dy = touchEndY - touchStartY;
      if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy) * 1.5) {
        if (dx < 0) renderGalleryItem(currentGalleryIndex + 1);
        else renderGalleryItem(currentGalleryIndex - 1);
      }
    }, { passive: true });

    const calcBtn = $('.lightbox__calc-btn', lb);
    calcBtn && calcBtn.addEventListener('click', () => {
      closeLightbox();
      if (window.loadDesignIntoVisualiser) {
        window.loadDesignIntoVisualiser(currentLbSrc, currentLbTitle);
      } else {
        window.location.href = `index.html?visualise=${encodeURIComponent(currentLbSrc)}&name=${encodeURIComponent(currentLbTitle)}#visualiser`;
      }
    });

    return lb;
  }

  function renderGalleryItem(index) {
    if (!activeGalleryItems || activeGalleryItems.length === 0) return;
    currentGalleryIndex = ((index % activeGalleryItems.length) + activeGalleryItems.length) % activeGalleryItems.length;
    const item = activeGalleryItems[currentGalleryIndex];
    if (!item) return;

    currentLbSrc = item.src;
    currentLbTitle = item.title;

    const box = ensureLB();
    const img = $('.lightbox__media img', box);
    if (img) {
      img.style.transition = 'opacity 0.2s ease';
      img.style.opacity = '0.4';
      img.src = item.src;
      img.alt = item.title;
      img.onload = () => { img.style.opacity = '1'; };
    }
    const titleEl = $('.lightbox__title', box);
    if (titleEl) titleEl.textContent = item.title;

    const codeEl = $('.lightbox__code', box);
    if (codeEl) {
      if (item.code) {
        codeEl.textContent = item.code;
        codeEl.style.display = 'inline-block';
      } else {
        codeEl.style.display = 'none';
      }
    }

    const counterEl = $('.lightbox__counter', box);
    if (counterEl) {
      counterEl.textContent = `${currentGalleryIndex + 1} / ${activeGalleryItems.length}`;
    }

    const descEl = $('.lightbox__desc', box);
    if (descEl) {
      if (item.desc && item.desc.length > 5) {
        descEl.textContent = item.desc;
      } else {
        descEl.textContent = 'Custom scaled and printed to your room proportions on your choice of 5 luxury architectural substrates. In-house manufactured in Chennai since 1978.';
      }
    }

    const waLink = $('.lightbox__wa-link', box);
    if (waLink) {
      const absSrc = item.src.startsWith('http') ? item.src : (window.location.origin + (item.src.startsWith('/') ? '' : '/') + item.src);
      const msg = `Namaste Wall Jewels — I would like to enquire about this wallpaper.\n\n` +
        `Design Name: ${item.title}` + (item.code ? ` (${item.code})` : '') + `\n` +
        `Image Preview: ${absSrc}\n\n` +
        `Please advise on sizing, finishes and pricing for my wall.`;
      waLink.href = `https://wa.me/919677042903?text=${encodeURIComponent(msg)}`;
    }
  }

  function openLightbox(src, alt) {
    if (!src) return;
    activeGalleryItems = buildGalleryList();

    // Find clicked index in active gallery
    const cleanTitle = (alt || '').split(' — ')[0].split(' · ')[0].trim();
    let foundIdx = activeGalleryItems.findIndex(i => i.src === src || (cleanTitle && i.title.toLowerCase() === cleanTitle.toLowerCase()));
    if (foundIdx === -1) {
      // Add current item as single fallback
      activeGalleryItems.unshift({ src, title: cleanTitle || 'Wall Jewels Original Wallpaper', code: '', desc: '' });
      foundIdx = 0;
    }

    const box = ensureLB();
    renderGalleryItem(foundIdx);

    box.classList.add('is-open');
    document.body.style.overflow = 'hidden';
    $('.lightbox__close', box).focus({ preventScroll: true });
  }

  function closeLightbox() {
    if (!lb) return;
    lb.classList.remove('is-open');
    document.body.style.overflow = '';
  }

  // Universal click listener for all wallpaper images across landing and collection
  document.addEventListener('click', (e) => {
    // If clicking flipbook or specific buttons, let them handle their action
    if (e.target.closest('button, .uiverse, .vol-badge, .flipbook-trigger, .lightbox__close, .lightbox__nav, .lightbox__wa-link')) return;

    // Check if clicked element is an image or inside an image container
    const img = e.target.closest('img');
    if (img) {
      if (img.closest('.wordmark, .header, .drawer__head, .nav, .footer__brand, .sr-only')) return;
      const src = img.dataset.full || img.currentSrc || img.src;
      if (!src || src.includes('logo-') || src.includes('data:image')) return;
      e.preventDefault();
      e.stopPropagation();
      openLightbox(src, img.alt || img.title || '');
      return;
    }

    // Check if clicking on wallpaper containers (.feature, .tile, .plate, .coverflow-card, etc.)
    const card = e.target.closest('.feature, .tile, .plate, .volume__media, .coverflow-card, .fan-card, .journey__art, .j2art, .space, .soon, .proof__frame, .cfg__preview, .card');
    if (card && !e.target.closest('a:not(.textlink), button')) {
      const cardImg = card.querySelector('img');
      if (cardImg) {
        const src = cardImg.dataset.full || cardImg.currentSrc || cardImg.src;
        if (src && !src.includes('logo-') && !src.includes('data:image')) {
          e.preventDefault();
          e.stopPropagation();
          openLightbox(src, cardImg.alt || cardImg.title || '');
        }
      }
    }
  });

  addEventListener('keydown', (e) => {
    if (!lb || !lb.classList.contains('is-open')) return;
    if (e.key === 'Escape') closeLightbox();
    else if (e.key === 'ArrowLeft') renderGalleryItem(currentGalleryIndex - 1);
    else if (e.key === 'ArrowRight') renderGalleryItem(currentGalleryIndex + 1);
  });

  /* hero films click to open full still artwork of the currently visible active slide */
  document.addEventListener('click', (e) => {
    // Ignore clicks on header, nav, hero control buttons, dots, or text links
    if (e.target.closest('.hero__bar, .hero__dots, .header, button, a')) return;

    const hero = e.target.closest('.hero');
    if (!hero) return;

    const activeSlide = hero.querySelector('.slide.is-on');
    if (!activeSlide) return;

    const v = activeSlide.querySelector('video') || activeSlide.querySelector('img');
    if (!v) return;

    const full = v.dataset.full || v.poster || v.src;
    if (full) {
      e.preventDefault();
      e.stopPropagation();
      openLightbox(full, v.dataset.title || v.getAttribute('aria-label') || '');
    }
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
