/* =============================================================
   Ambient background — pointer-reactive WebGL effects
   -------------------------------------------------------------
   Six effects that are deliberately NOT variations of each other:
   different geometry (blobs / rings / metaballs / grid / repeat /
   streaks) and a different colour story each.

   All of them follow the pointer. When the pointer is idle — or on
   touch, where there isn't one — a virtual pointer drifts on a
   Lissajous path so the page never looks dead.

   Readability: alpha is damped down the centre column where the text
   lives and opens up toward the margins, so the effect can be strong
   without fighting the copy. See u_safe.
   ============================================================= */
(function () {
  'use strict';

  const canvas = document.getElementById('plasma');
  if (!canvas) return;

  const root = document.documentElement;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const RENDER_SCALE = 0.5;
  const TRAIL = 8;
  const STORE = 'wj-bg';

  let gl = null;
  try {
    const o = { alpha: true, antialias: false, depth: false, stencil: false, premultipliedAlpha: true };
    gl = canvas.getContext('webgl', o) || canvas.getContext('experimental-webgl', o);
  } catch (e) { gl = null; }

  const VERT = 'attribute vec2 p; void main(){ gl_Position = vec4(p,0.0,1.0); }';

  const PRELUDE = `
    precision mediump float;
    uniform vec2  u_res;
    uniform float u_time;
    uniform vec2  u_mouse;      // pointer in uv space
    uniform vec2  u_trail[${TRAIL}];
    uniform float u_speed;      // pointer speed 0..1
    uniform float u_safe;       // half-width of the text column, uv units
    uniform vec3  u_c1;
    uniform vec3  u_c2;
    uniform vec3  u_c3;
    uniform float u_alpha;

    vec2 hash2(vec2 p){
      p = vec2(dot(p,vec2(127.1,311.7)), dot(p,vec2(269.5,183.3)));
      return -1.0 + 2.0*fract(sin(p)*43758.5453123);
    }
    float noise(vec2 p){
      vec2 i = floor(p), f = fract(p);
      vec2 u = f*f*(3.0-2.0*f);
      return mix(mix(dot(hash2(i),               f),
                     dot(hash2(i+vec2(1.0,0.0)), f-vec2(1.0,0.0)), u.x),
                 mix(dot(hash2(i+vec2(0.0,1.0)), f-vec2(0.0,1.0)),
                     dot(hash2(i+vec2(1.0,1.0)), f-vec2(1.0,1.0)), u.x), u.y);
    }
    float fbm(vec2 p){
      float v = 0.0, a = 0.5;
      for (int i = 0; i < 4; i++){ v += a*noise(p); p *= 2.03; a *= 0.5; }
      return v;
    }
    vec2 uvpos(){ return (gl_FragCoord.xy - 0.5*u_res) / min(u_res.x, u_res.y); }

    /* Strong at the margins, gentle behind the centre text column. */
    float readable(vec2 uv){
      float d = abs(uv.x);
      return mix(0.40, 1.0, smoothstep(u_safe*0.70, u_safe*1.75, d));
    }
    float edgefade(vec2 uv){ return 1.0 - smoothstep(0.62, 1.35, length(uv)); }

    /* The ceiling is what protects text contrast: mean coverage lands
       around 0.22 (which is what you actually perceive), but an
       unclamped hotspot under the cursor would spike to 1.0 and crush
       the small mono labels. Capping the peak costs almost no vividness. */
    void emit(vec3 col, float a){
      a = clamp(a, 0.0, 0.82) * readable(uvpos()) * edgefade(uvpos());
      gl_FragColor = vec4(col*a, a);      // premultiplied
    }
  `;

  /* =========================================================
     The six effects
     ========================================================= */
  const MODES = [
    {
      id: 'bloom',
      label: 'Bloom',
      desc: 'Ruby light blooms that trail your cursor.',
      chip: 'radial-gradient(circle at 35% 35%, #FF5A4E 0%, #C0102A 45%, #3A0410 100%)',
      pal: {
        light: { c1: [0.88, 0.16, 0.22], c2: [0.98, 0.58, 0.22], c3: [0.45, 0.03, 0.14], a: 1.45 },
        dark:  { c1: [1.00, 0.30, 0.32], c2: [1.00, 0.70, 0.30], c3: [0.35, 0.02, 0.12], a: 1.55 }
      },
      frag: `${PRELUDE}
        void main(){
          vec2 uv = uvpos(); float t = u_time;
          float g = 0.0, core = 0.0;
          for (int i = 0; i < ${TRAIL}; i++){
            float k = float(i);
            vec2 d = uv - u_trail[i];
            float w = 1.0 - k/float(${TRAIL});           // newest = brightest
            float r = 0.30 + k*0.045;
            float e = exp(-dot(d,d)/(r*r));
            g += e*w;
            core += exp(-dot(d,d)/(0.10*0.10))*w;
          }
          float turb = fbm(uv*2.6 + t*0.15)*0.5 + 0.5;
          float a = g*(0.55 + 0.45*turb) + core*0.55;
          vec3 col = mix(u_c3, u_c1, clamp(g*0.9, 0.0, 1.0));
          col = mix(col, u_c2, clamp(core*0.85 + u_speed*0.25, 0.0, 1.0));
          emit(col, u_alpha*clamp(a, 0.0, 1.2));
        }`
    },
    {
      id: 'ripple',
      label: 'Ripple',
      desc: 'Sapphire rings spreading from the pointer.',
      chip: 'repeating-radial-gradient(circle at 40% 45%, #4FD8E8 0 6%, #0B4D8F 6% 13%, #041A38 13% 20%)',
      pal: {
        light: { c1: [0.06, 0.42, 0.70], c2: [0.20, 0.80, 0.82], c3: [0.02, 0.10, 0.30], a: 2.30 },
        dark:  { c1: [0.16, 0.60, 0.92], c2: [0.35, 0.95, 0.95], c3: [0.02, 0.08, 0.26], a: 2.50 }
      },
      frag: `${PRELUDE}
        void main(){
          vec2 uv = uvpos(); float t = u_time;
          float d1 = length(uv - u_mouse);
          float w1 = sin(d1*26.0 - t*3.2);
          float r1 = smoothstep(0.25, 1.0, w1)*exp(-d1*1.9);

          vec2 p2 = vec2(sin(t*0.23)*0.55, cos(t*0.19)*0.42);
          float d2 = length(uv - p2);
          float w2 = sin(d2*18.0 - t*1.7);
          float r2 = smoothstep(0.45, 1.0, w2)*exp(-d2*1.5);

          float caustic = fbm(uv*3.0 + vec2(t*0.12, -t*0.09))*0.5 + 0.5;
          float a = r1*(1.0 + u_speed*0.8) + r2*0.65 + caustic*0.16;
          vec3 col = mix(u_c3, u_c1, clamp(r1*1.4 + r2*0.9, 0.0, 1.0));
          col = mix(col, u_c2, clamp(r1*1.6, 0.0, 1.0));
          emit(col, u_alpha*clamp(a, 0.0, 1.1));
        }`
    },
    {
      id: 'lava',
      label: 'Lava',
      desc: 'Amethyst metaballs that lean toward you.',
      chip: 'radial-gradient(circle at 30% 30%, #E24BC0 0 18%, transparent 19%), radial-gradient(circle at 68% 62%, #8B3BE0 0 26%, transparent 27%), #2A0A44',
      pal: {
        light: { c1: [0.56, 0.18, 0.78], c2: [0.92, 0.26, 0.58], c3: [0.18, 0.05, 0.34], a: 1.50 },
        dark:  { c1: [0.70, 0.32, 0.96], c2: [1.00, 0.36, 0.70], c3: [0.14, 0.03, 0.30], a: 1.60 }
      },
      frag: `${PRELUDE}
        float ball(vec2 uv, vec2 c, float r){ vec2 d = uv-c; return r*r/max(dot(d,d), 0.0004); }
        void main(){
          vec2 uv = uvpos(); float t = u_time*0.34;
          float f = 0.0;
          f += ball(uv, u_mouse, 0.30);
          f += ball(uv, vec2(sin(t*0.9)*0.62, cos(t*0.7)*0.40) + u_mouse*0.22, 0.26);
          f += ball(uv, vec2(cos(t*0.6)*0.70, sin(t*0.5)*0.46) + u_mouse*0.14, 0.23);
          f += ball(uv, vec2(sin(t*0.4+2.1)*0.50, cos(t*0.8+1.2)*0.52) + u_mouse*0.30, 0.20);
          f += ball(uv, vec2(cos(t*0.33+4.0)*0.44, sin(t*0.45+3.0)*0.36), 0.18);

          float body = smoothstep(0.85, 1.45, f);         // crisp-ish edges, not noise
          float rim  = smoothstep(0.72, 0.92, f) - smoothstep(0.98, 1.35, f);
          vec3 col = mix(u_c3, u_c1, body);
          col = mix(col, u_c2, clamp(rim*1.6 + u_speed*0.2, 0.0, 1.0));
          emit(col, u_alpha*clamp(body*0.85 + rim*0.75, 0.0, 1.1));
        }`
    },
    {
      id: 'mosaic',
      label: 'Mosaic',
      desc: 'Emerald tiles lighting up in a wave around you.',
      chip: 'conic-gradient(from 45deg, #0E7A5F 0 25%, #D8B23C 25% 50%, #0A3B30 50% 75%, #16A37A 75%)',
      pal: {
        light: { c1: [0.05, 0.52, 0.40], c2: [0.88, 0.72, 0.24], c3: [0.02, 0.18, 0.16], a: 2.30 },
        dark:  { c1: [0.10, 0.72, 0.55], c2: [1.00, 0.82, 0.32], c3: [0.01, 0.14, 0.13], a: 2.50 }
      },
      frag: `${PRELUDE}
        void main(){
          vec2 uv = uvpos(); float t = u_time;
          float S = 9.0;
          vec2 g  = uv*S;
          vec2 id = floor(g);
          vec2 f  = fract(g) - 0.5;
          vec2 c  = (id + 0.5)/S;                       // tile centre in uv space

          float d = length(c - u_mouse);
          float wave = sin(d*9.0 - t*2.6)*0.5 + 0.5;
          float near = exp(-d*1.5);
          float lit  = 0.10 + wave*near*1.5 + near*0.35;

          float sq = smoothstep(0.46, 0.36, max(abs(f.x), abs(f.y)));   // square with a grout gap
          float dot_ = smoothstep(0.16, 0.10, length(f));
          float shape = sq*0.85 + dot_*0.5;

          vec3 col = mix(u_c3, u_c1, clamp(lit, 0.0, 1.0));
          col = mix(col, u_c2, clamp((lit-0.7)*1.3, 0.0, 1.0));
          emit(col, u_alpha*shape*clamp(lit, 0.0, 1.25));
        }`
    },
    {
      id: 'damask',
      label: 'Damask',
      desc: 'A wallpaper repeat, lit by a moving spotlight.',
      chip: 'radial-gradient(circle at 50% 50%, #E6C169 0 16%, transparent 17%), radial-gradient(circle at 0 0, #E6C169 0 11%, transparent 12%), radial-gradient(circle at 100% 100%, #E6C169 0 11%, transparent 12%), #3E1030',
      pal: {
        light: { c1: [0.72, 0.54, 0.18], c2: [0.98, 0.88, 0.62], c3: [0.30, 0.08, 0.24], a: 1.60 },
        dark:  { c1: [0.88, 0.68, 0.26], c2: [1.00, 0.94, 0.74], c3: [0.24, 0.05, 0.20], a: 1.75 }
      },
      frag: `${PRELUDE}
        void main(){
          vec2 uv = uvpos(); float t = u_time;
          vec2 p = (uv - u_mouse*0.10) * (3.0 + u_speed*0.7);
          p.x += step(1.0, mod(floor(p.y), 2.0))*0.5;     // half-drop repeat
          vec2 g = fract(p) - 0.5;
          float ang = atan(g.y, g.x);
          float rad = length(g);

          float petal = 0.30 + 0.11*cos(ang*6.0 + t*0.5);
          float motif = smoothstep(petal, petal-0.05, rad);
          float ring  = smoothstep(0.44,0.41,rad) - smoothstep(0.37,0.34,rad);
          float stem  = smoothstep(0.030, 0.0, abs(g.x)) * smoothstep(0.5, 0.1, rad);
          float m = clamp(motif + ring*0.8 + stem*0.6, 0.0, 1.0);

          float spot = exp(-length(uv - u_mouse)*1.35);   // the moving spotlight
          float lit = 0.20 + spot*1.5;

          vec3 col = mix(u_c3, u_c1, m);
          col = mix(col, u_c2, clamp(m*spot*2.0, 0.0, 1.0));
          emit(col, u_alpha*(0.16 + m*0.95)*clamp(lit, 0.0, 1.3));
        }`
    },
    {
      id: 'threads',
      label: 'Threads',
      desc: 'Full-spectrum silk that bends around your cursor.',
      chip: 'linear-gradient(115deg, #E2344B 0 20%, #E8A32A 20% 40%, #2FA36B 40% 60%, #2C6FD1 60% 80%, #8B3BE0 80%)',
      pal: {
        light: { c1: [0.88, 0.18, 0.30], c2: [0.95, 0.66, 0.15], c3: [0.10, 0.42, 0.72], a: 2.00 },
        dark:  { c1: [1.00, 0.30, 0.42], c2: [1.00, 0.76, 0.26], c3: [0.24, 0.58, 0.95], a: 2.20 }
      },
      frag: `${PRELUDE}
        void main(){
          vec2 uv = uvpos(); float t = u_time;
          vec2 d = uv - u_mouse;
          float r = length(d);
          vec2 push = normalize(d + 1e-5) * exp(-r*2.1) * (0.30 + u_speed*0.35);
          vec2 p = uv + push;                            // field bends around the cursor

          float flow = fbm(p*1.7 + vec2(t*0.09, -t*0.06));
          float s  = sin(p.y*9.0 + flow*7.0 + t*0.9);
          float s2 = sin(p.y*19.0 - flow*4.0 - t*0.6);
          float band  = pow(max(s,  0.0), 2.0);
          float band2 = pow(max(s2, 0.0), 4.0);
          float a = band*0.85 + band2*0.45;

          // even thirds, so the blue actually gets screen area instead of
          // being squeezed into the far end of the ramp
          float hue = clamp(flow*1.7 + 0.5 + p.x*0.40, 0.0, 1.0);
          vec3 col = mix(u_c1, u_c2, smoothstep(0.12, 0.48, hue));
          col = mix(col, u_c3, smoothstep(0.50, 0.86, hue));
          col = mix(col, vec3(1.0), exp(-r*3.4)*0.35);   // bright halo at the cursor
          emit(col, u_alpha*clamp(a + exp(-r*3.0)*0.5, 0.0, 1.1));
        }`
    }
  ];

  const themeNow = () => (root.dataset.theme === 'dark' ? 'dark' : 'light');

  let mode = localStorage.getItem(STORE);
  if (!mode || (mode !== 'off' && !MODES.some((m) => m.id === mode))) mode = 'bloom';

  /* =========================================================
     Picker UI
     ========================================================= */
  function buildPicker() {
    const btn = document.getElementById('bgpick-btn');
    const menu = document.getElementById('bgpick-menu');
    if (!btn || !menu) return;
    if (!gl) { btn.remove(); menu.remove(); return; }

    btn.hidden = false;
    const row = (id, label, desc, chip, off) => `
      <button class="bgpick__opt" role="menuitemradio" data-mode="${id}">
        <span class="bgpick__chip${off ? ' bgpick__chip--off' : ''}" style="${off ? '' : 'background:' + chip}"></span>
        <span class="bgpick__text">
          <span class="bgpick__name">${label}</span>
          <span class="bgpick__desc">${desc}</span>
        </span>
        <svg class="bgpick__tick" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>
      </button>`;

    menu.innerHTML =
      `<p class="bgpick__head">Background effect</p>` +
      MODES.map((m) => row(m.id, m.label, m.desc, m.chip)).join('') +
      row('off', 'Off', 'Plain background, no animation.', '', true) +
      `<p class="bgpick__foot">Every effect follows your pointer.</p>`;

    const opts = [...menu.querySelectorAll('.bgpick__opt')];
    const mark = () => opts.forEach((o) => o.setAttribute('aria-checked', String(o.dataset.mode === mode)));
    const open = (v) => {
      menu.hidden = !v;
      btn.setAttribute('aria-expanded', String(v));
      if (v) { mark(); (menu.querySelector('[aria-checked="true"]') || opts[0]).focus(); }
    };

    btn.addEventListener('click', (e) => { e.stopPropagation(); open(menu.hidden); });
    opts.forEach((o) => o.addEventListener('click', () => { setMode(o.dataset.mode); mark(); open(false); btn.focus(); }));
    document.addEventListener('click', (e) => {
      if (!menu.hidden && !menu.contains(e.target) && e.target !== btn) open(false);
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !menu.hidden) { open(false); btn.focus(); }
    });
    menu.addEventListener('keydown', (e) => {
      const i = opts.indexOf(document.activeElement);
      if (e.key === 'ArrowDown') { e.preventDefault(); opts[(i + 1) % opts.length].focus(); }
      if (e.key === 'ArrowUp')   { e.preventDefault(); opts[(i - 1 + opts.length) % opts.length].focus(); }
    });
    mark();
  }

  if (!gl) { buildPicker(); return; }

  /* ---------- GL ---------- */
  function compile(type, src) {
    const s = gl.createShader(type);
    gl.shaderSource(s, src);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
      console.warn('[wj-bg] shader failed:', gl.getShaderInfoLog(s));
      gl.deleteShader(s);
      return null;
    }
    return s;
  }

  const vs = compile(gl.VERTEX_SHADER, VERT);
  if (!vs) { buildPicker(); return; }

  const buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  gl.enable(gl.BLEND);
  gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
  gl.clearColor(0, 0, 0, 0);

  const cache = {};
  let current = null;

  function build(m) {
    const fs = compile(gl.FRAGMENT_SHADER, m.frag);
    if (!fs) return null;
    const prog = gl.createProgram();
    gl.attachShader(prog, vs);
    gl.attachShader(prog, fs);
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
      console.warn('[wj-bg] link failed:', gl.getProgramInfoLog(prog));
      return null;
    }
    return {
      prog, pal: m.pal,
      loc: gl.getAttribLocation(prog, 'p'),
      U: {
        res:   gl.getUniformLocation(prog, 'u_res'),
        time:  gl.getUniformLocation(prog, 'u_time'),
        mouse: gl.getUniformLocation(prog, 'u_mouse'),
        trail: gl.getUniformLocation(prog, 'u_trail'),
        speed: gl.getUniformLocation(prog, 'u_speed'),
        safe:  gl.getUniformLocation(prog, 'u_safe'),
        c1:    gl.getUniformLocation(prog, 'u_c1'),
        c2:    gl.getUniformLocation(prog, 'u_c2'),
        c3:    gl.getUniformLocation(prog, 'u_c3'),
        alpha: gl.getUniformLocation(prog, 'u_alpha')
      }
    };
  }

  function applyPalette() {
    if (!current) return;
    const p = current.pal[themeNow()];
    gl.uniform3fv(current.U.c1, p.c1);
    gl.uniform3fv(current.U.c2, p.c2);
    gl.uniform3fv(current.U.c3, p.c3);
    gl.uniform1f(current.U.alpha, p.a);
  }

  /* ---------- pointer ---------- */
  const pt = { tx: 0, ty: 0, x: 0, y: 0, speed: 0, lastMove: -1e9 };
  const trail = new Float32Array(TRAIL * 2);
  let trailTick = 0;

  addEventListener('pointermove', (e) => {
    const w = innerWidth, h = innerHeight, m = Math.min(w, h);
    pt.tx = (e.clientX - w / 2) / m;
    pt.ty = -(e.clientY - h / 2) / m;      // gl_FragCoord y is up
    pt.lastMove = performance.now();
  }, { passive: true });

  function updatePointer(now) {
    // No pointer for a moment (or a touch device)? Drift on a Lissajous
    // so the effect keeps breathing instead of freezing in a corner.
    if (now - pt.lastMove > 2200) {
      const t = now / 1000;
      pt.tx = Math.sin(t * 0.31) * 0.52 + Math.sin(t * 0.13) * 0.16;
      pt.ty = Math.cos(t * 0.24) * 0.38 + Math.cos(t * 0.17) * 0.12;
    }
    const px = pt.x, py = pt.y;
    pt.x += (pt.tx - pt.x) * 0.10;         // ease toward the target
    pt.y += (pt.ty - pt.y) * 0.10;
    const d = Math.hypot(pt.x - px, pt.y - py);
    pt.speed += (Math.min(d * 26, 1) - pt.speed) * 0.12;

    if (++trailTick % 3 === 0) {           // sample every 3rd frame = longer tail
      for (let i = TRAIL - 1; i > 0; i--) {
        trail[i * 2] = trail[(i - 1) * 2];
        trail[i * 2 + 1] = trail[(i - 1) * 2 + 1];
      }
    }
    trail[0] = pt.x;
    trail[1] = pt.y;
  }

  function sizeCanvas() {
    const w = Math.max(1, Math.round(innerWidth * RENDER_SCALE));
    const h = Math.max(1, Math.round(innerHeight * RENDER_SCALE));
    if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; }
    gl.viewport(0, 0, w, h);
    if (!current) return;
    gl.uniform2f(current.U.res, w, h);
    // half the text column, in the shader's uv units
    const col = Math.min(innerWidth * 0.92, 1240);
    gl.uniform1f(current.U.safe, (col / 2) / Math.min(innerWidth, innerHeight));
  }

  let raf = 0;
  const t0 = performance.now();

  function draw(now) {
    raf = 0;
    if (!current) return;
    now = now || performance.now();
    updatePointer(now);
    gl.uniform1f(current.U.time, (now - t0) / 1000);
    gl.uniform2f(current.U.mouse, pt.x, pt.y);
    gl.uniform1f(current.U.speed, pt.speed);
    if (current.U.trail) gl.uniform2fv(current.U.trail, trail);
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
    if (!reduced && document.visibilityState === 'visible') raf = requestAnimationFrame(draw);
  }

  function kick() {
    if (raf || reduced || !current) return;
    if (document.visibilityState !== 'visible') return;
    raf = requestAnimationFrame(draw);
  }
  function stop() { if (raf) { cancelAnimationFrame(raf); raf = 0; } }

  function setMode(id) {
    mode = id;
    localStorage.setItem(STORE, id);
    root.dataset.bg = id;

    if (id === 'off') {
      stop(); current = null;
      canvas.classList.remove('is-live');
      gl.clear(gl.COLOR_BUFFER_BIT);
      return;
    }
    const m = MODES.find((x) => x.id === id);
    if (!cache[id]) cache[id] = build(m);
    if (!cache[id]) { canvas.classList.remove('is-live'); return; }

    current = cache[id];
    gl.useProgram(current.prog);
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.enableVertexAttribArray(current.loc);
    gl.vertexAttribPointer(current.loc, 2, gl.FLOAT, false, 0, 0);
    sizeCanvas();
    applyPalette();
    draw();
    canvas.classList.add('is-live');
    kick();
  }

  let rt = 0;
  addEventListener('resize', () => {
    clearTimeout(rt);
    rt = setTimeout(() => { sizeCanvas(); draw(); kick(); }, 150);
  });
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') kick(); else stop();
  });
  document.addEventListener('wj:themechange', () => { applyPalette(); draw(); kick(); });

  buildPicker();
  setMode(mode);

  window.WJBackground = {
    modes: MODES.map((m) => ({ id: m.id, label: m.label })).concat([{ id: 'off', label: 'Off' }]),
    set: setMode,
    get: () => mode,
    _pt: pt
  };
})();
