/* ============================================================================
   WALL JEWELS — kolam engine
   ----------------------------------------------------------------------------
   Draws the site's line grammar: sikku-style interlaced loops around pulli
   (dot) grids, radial flower kolam, and the scroll spine. All lines draw
   themselves: dasharray/dashoffset driven either by IntersectionObserver
   (thresholds) or by scroll progress (hero, spine, finale).
   ========================================================================== */
(function () {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  const el = (name, attrs) => {
    const n = document.createElementNS(NS, name);
    for (const k in attrs) n.setAttribute(k, attrs[k]);
    return n;
  };

  /* ---- sikku weave: interlaced quarter-arc loops around a dot lattice ---- */
  function weave(svg, cols, rows, cell, ox, oy, opts) {
    opts = opts || {};
    const r = cell / 2;
    for (let y = 0; y < rows; y++) {
      for (let x = 0; x < cols; x++) {
        if (opts.skip && opts.skip(x, y)) continue;
        const cx = ox + x * cell, cy = oy + y * cell;
        const flip = (x + y) % 2 === 0;
        let d;
        if (flip) {
          d = `M ${cx} ${cy + r} A ${r} ${r} 0 0 1 ${cx + r} ${cy}` +
              ` M ${cx + cell} ${cy + r} A ${r} ${r} 0 0 0 ${cx + r} ${cy + cell}`;
        } else {
          d = `M ${cx + r} ${cy} A ${r} ${r} 0 0 1 ${cx + cell} ${cy + r}` +
              ` M ${cx + r} ${cy + cell} A ${r} ${r} 0 0 0 ${cx} ${cy + r}`;
        }
        svg.appendChild(el('path', { d }));
        if (!opts.noDots) {
          svg.appendChild(el('circle', { cx: cx + r, cy: cy + r, r: 1.6 }));
        }
      }
    }
  }

  /* ---- radial flower kolam: petals looping between a dot ring ---- */
  function flower(svg, cx, cy, R, petals) {
    const paths = [];
    for (let i = 0; i < petals; i++) {
      const a0 = (i / petals) * Math.PI * 2 - Math.PI / 2;
      const a1 = ((i + 1) / petals) * Math.PI * 2 - Math.PI / 2;
      const am = (a0 + a1) / 2;
      const r0 = R * 0.42, r1 = R;
      const x0 = cx + Math.cos(a0) * r0, y0 = cy + Math.sin(a0) * r0;
      const x1 = cx + Math.cos(a1) * r0, y1 = cy + Math.sin(a1) * r0;
      const px = cx + Math.cos(am) * r1, py = cy + Math.sin(am) * r1;
      const w = R * 0.34;
      const lx = cx + Math.cos(am - 0.5 / petals * Math.PI * 2) * (r1 - w * 0.1);
      const ly = cy + Math.sin(am - 0.5 / petals * Math.PI * 2) * (r1 - w * 0.1);
      const rx = cx + Math.cos(am + 0.5 / petals * Math.PI * 2) * (r1 - w * 0.1);
      const ry = cy + Math.sin(am + 0.5 / petals * Math.PI * 2) * (r1 - w * 0.1);
      const d = `M ${x0} ${y0} C ${lx} ${ly} ${px - (py - cy) * 0.18} ${py + (px - cx) * 0.18} ${px} ${py}` +
                ` C ${px + (py - cy) * 0.18} ${py - (px - cx) * 0.18} ${rx} ${ry} ${x1} ${y1}`;
      paths.push(svg.appendChild(el('path', { d })));
      const dx = cx + Math.cos(am) * (R * 1.12), dy = cy + Math.sin(am) * (R * 1.12);
      svg.appendChild(el('circle', { cx: dx, cy: dy, r: 1.8 }));
    }
    const ring = R * 0.28;
    svg.appendChild(el('path', {
      d: `M ${cx + ring} ${cy} A ${ring} ${ring} 0 1 1 ${cx - ring} ${cy} A ${ring} ${ring} 0 1 1 ${cx + ring} ${cy}`
    }));
    svg.appendChild(el('circle', { cx, cy, r: 2.2 }));
    return paths;
  }

  /* ---- prepare stroke-draw on every path of an svg ---- */
  function prime(svg) {
    svg.querySelectorAll('path').forEach((p, i) => {
      const L = p.getTotalLength();
      p.style.strokeDasharray = L;
      p.style.strokeDashoffset = reduced ? 0 : L;
      p.dataset.len = L;
      p.style.transition = reduced ? 'none' :
        `stroke-dashoffset 1.6s cubic-bezier(.19,1,.22,1) ${i * 45}ms`;
    });
    svg.querySelectorAll('circle').forEach((c, i) => {
      c.style.opacity = reduced ? 1 : 0;
      c.style.transition = reduced ? 'none' : `opacity .8s ease ${400 + i * 24}ms`;
    });
  }
  function play(svg) {
    svg.querySelectorAll('path').forEach(p => { p.style.strokeDashoffset = 0; });
    svg.querySelectorAll('circle').forEach(c => { c.style.opacity = 1; });
  }

  /* ---- threshold gates: small weave before each section heading ---- */
  const GATE_FORMS = [
    { cols: 4, rows: 2, cell: 22 },
    { cols: 3, rows: 2, cell: 26 },
    { cols: 6, rows: 1, cell: 30 },
    { cols: 5, rows: 2, cell: 18 }
  ];
  document.querySelectorAll('[data-kolam="gate"]').forEach((host, gi) => {
    const f = GATE_FORMS[gi % GATE_FORMS.length];
    const w = f.cols * f.cell + 8, h = f.rows * f.cell + 4;
    const svg = el('svg', { viewBox: `0 0 ${w} ${h}`, width: w, height: h, 'aria-hidden': 'true' });
    svg.style.overflow = 'visible';
    weave(svg, f.cols, f.rows, f.cell, 4, 2);
    svg.querySelectorAll('path').forEach(p => { p.style.stroke = 'rgba(43,36,26,.55)'; p.style.fill = 'none'; p.style.strokeWidth = 1.2; });
    svg.querySelectorAll('circle').forEach(c => { c.style.fill = 'rgba(169,123,34,.9)'; });
    host.prepend(svg);
    prime(svg);
  });

  /* ---- hero corner kolam ---- */
  const heroK = document.querySelector('.hero__kolam');
  if (heroK) {
    heroK.setAttribute('viewBox', '0 0 200 200');
    heroK.setAttribute('preserveAspectRatio', 'xMaxYMin meet');
    weave(heroK, 5, 5, 38, 6, 6);
    prime(heroK);
  }

  /* ---- finale flower ---- */
  const finK = document.querySelector('.finale__kolam svg');
  if (finK) {
    finK.setAttribute('viewBox', '0 0 400 400');
    flower(finK, 200, 200, 150, 12);
    prime(finK);
  }

  /* ---- observer: draw when a kolam enters ---- */
  const io = new IntersectionObserver((ents) => {
    ents.forEach(e => {
      if (e.isIntersecting) { play(e.target); io.unobserve(e.target); }
    });
  }, { threshold: 0.35 });
  document.querySelectorAll('.threshold svg, .hero__kolam, .finale__kolam svg').forEach(s => io.observe(s));

  /* ---- the scroll spine: one continuous line down the page's left margin ---- */
  const spineHost = document.querySelector('[data-spine]');
  if (spineHost && matchMedia('(min-width: 1180px)').matches) {
    const svg = el('svg', { 'aria-hidden': 'true' });
    Object.assign(svg.style, {
      position: 'absolute', top: 0, left: 0, width: '72px', height: '100%',
      pointerEvents: 'none', zIndex: 1, overflow: 'visible'
    });
    spineHost.appendChild(svg);

    let path = null;
    function build() {
      svg.innerHTML = '';
      const H = spineHost.scrollHeight;
      svg.setAttribute('viewBox', `0 0 72 ${H}`);
      svg.setAttribute('preserveAspectRatio', 'xMinYMin meet');
      const marks = [...document.querySelectorAll('[data-spine-mark]')]
        .map(s => s.getBoundingClientRect().top + scrollY + 40)
        .filter(y => y > 400 && y < H - 400)
        .sort((a, b) => a - b);
      let d = `M 36 240`;
      marks.forEach(y => {
        d += ` L 36 ${y - 30}`;
        d += ` C 36 ${y - 14} 20 ${y - 14} 20 ${y}`;
        d += ` C 20 ${y + 14} 36 ${y + 14} 36 ${y + 30}`;
      });
      d += ` L 36 ${H - 260}`;
      path = el('path', { d });
      path.style.cssText = 'fill:none;stroke:rgba(43,36,26,.3);stroke-width:1.1;vector-effect:non-scaling-stroke';
      svg.appendChild(path);
      marks.forEach(y => {
        const c = el('circle', { cx: 20, cy: y, r: 2.4 });
        c.style.fill = 'rgba(169,123,34,.8)';
        svg.appendChild(c);
      });
      const L = path.getTotalLength();
      path.style.strokeDasharray = L;
      path.style.strokeDashoffset = reduced ? 0 : L;
      path.dataset.len = L;
    }

    let ticking = false;
    function onScroll() {
      if (reduced || !path) return;
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        ticking = false;
        const L = +path.dataset.len;
        const total = spineHost.scrollHeight - innerHeight;
        const p = Math.min(1, Math.max(0, (scrollY + innerHeight * 0.55) / (total + innerHeight * 0.55)));
        path.style.strokeDashoffset = L * (1 - p);
      });
    }
    build();
    addEventListener('scroll', onScroll, { passive: true });
    addEventListener('resize', () => { build(); onScroll(); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => { build(); onScroll(); });
    setTimeout(() => { build(); onScroll(); }, 600);
  }

  /* ---- process step diagrams (wordless, numbered; prior state ghosted) ---- */
  window.WJ_KOLAM = { el, weave, flower, prime, play, NS };
})();
