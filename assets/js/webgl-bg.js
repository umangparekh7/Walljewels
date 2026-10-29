/**
 * ============================================================================
 * WALL JEWELS — Dual-Mode Dynamic WebGL Background Engine
 * ============================================================================
 * Dark Mode:  Sacred Kolam Geometry & 24K Gold Wire Lattice (100% UNTOUCHED).
 * Light Mode: Alabaster Marble & Translucent Liquid Gold Ribbons.
 * Smooth GPU-accelerated theme transition with zero layout reflow.
 * Strictly background layer (z-index: -1, pointer-events: none).
 */

(function () {
  'use strict';

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Retrieve or create background canvas
  let canvas = document.getElementById('wj-webgl-bg');
  if (!canvas) {
    canvas = document.createElement('canvas');
    canvas.id = 'wj-webgl-bg';
    canvas.setAttribute('aria-hidden', 'true');
    document.body.prepend(canvas);
  }

  // Strict Background Layering
  Object.assign(canvas.style, {
    position: 'fixed',
    top: '0',
    left: '0',
    width: '100%',
    height: '100%',
    pointerEvents: 'none',
    zIndex: '-1',
    opacity: '1.0'
  });

  const gl = canvas.getContext('webgl', { 
    alpha: false, 
    antialias: true, 
    powerPreference: 'high-performance'
  }) || canvas.getContext('experimental-webgl');

  if (!gl) {
    console.warn('WebGL not supported on this browser.');
    return;
  }

  // =========================================================================
  // SHADER SOURCES
  // =========================================================================
  const vsSource = `
    attribute vec2 a_position;
    varying vec2 v_uv;
    void main() {
      v_uv = (a_position + 1.0) * 0.5;
      gl_Position = vec4(a_position, 0.0, 1.0);
    }
  `;

  const fsSource = `
    precision highp float;
    varying vec2 v_uv;
    uniform vec2 u_resolution;
    uniform float u_time;
    uniform vec2 u_mouse;
    uniform float u_mouse_speed;
    uniform float u_is_light; // 0.0 = Dark Mode (Untouched), 1.0 = Light Mode (Alabaster & Gold Ribbons)

    #define PI 3.14159265359
    #define TWO_PI 6.28318530718

    // 2D Rotation
    mat2 rotate2D(float angle) {
      return mat2(cos(angle), -sin(angle), sin(angle), cos(angle));
    }

    // Hash & Noise for Marble Veining
    float hash(vec2 p) {
      return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123);
    }

    float noise2D(vec2 p) {
      vec2 i = floor(p);
      vec2 f = fract(p);
      vec2 u = f * f * (3.0 - 2.0 * f);
      return mix(mix(hash(i + vec2(0.0,0.0)), hash(i + vec2(1.0,0.0)), u.x),
                 mix(hash(i + vec2(0.0,1.0)), hash(i + vec2(1.0,1.0)), u.x), u.y);
    }

    float fbm(vec2 p) {
      float v = 0.0;
      float a = 0.5;
      for (int i = 0; i < 4; i++) {
        v += a * noise2D(p);
        p = rotate2D(0.45) * p * 2.0;
        a *= 0.5;
      }
      return v;
    }

    // Sacred Kolam Knot (Dark Mode - Untouched)
    float kolamKnot(vec2 p, float scale, float t) {
      vec2 grid = fract(p * scale) - 0.5;
      float dotDist = length(grid);
      float pulli = smoothstep(0.065, 0.035, dotDist);

      float angle = atan(grid.y, grid.x);
      float petalDist = abs(sin(angle * 4.0 + t * 0.5)) * 0.28 + 0.12;
      float loopLine = abs(dotDist - petalDist);
      float loopGlow = smoothstep(0.035, 0.005, loopLine);

      vec2 diagP = abs(grid) - vec2(0.25);
      float diagLine = abs(diagP.x + diagP.y);
      float diagGlow = smoothstep(0.04, 0.008, diagLine);

      return pulli * 1.5 + loopGlow * 0.85 + diagGlow * 0.45;
    }

    // Mandala Floral Radial Kolam (Dark Mode - Untouched)
    float mandalaKolam(vec2 p, float t) {
      float r = length(p);
      float a = atan(p.y, p.x);

      float f1 = abs(sin(a * 4.0 + t * 0.2)) * 0.35 + 0.25;
      float f2 = abs(cos(a * 8.0 - t * 0.3)) * 0.18 + 0.45;
      float f3 = abs(sin(a * 12.0 + t * 0.1)) * 0.08 + 0.65;

      float ring1 = smoothstep(0.02, 0.002, abs(r - f1));
      float ring2 = smoothstep(0.02, 0.002, abs(r - f2));
      float ring3 = smoothstep(0.02, 0.002, abs(r - f3));
      float centerDot = smoothstep(0.08, 0.02, r);

      return ring1 * 0.9 + ring2 * 0.75 + ring3 * 0.6 + centerDot * 1.2;
    }

    // Light Mode: Alabaster Marble Veins (Enriched deeper warm tone)
    vec3 renderMarble(vec2 uv, float t) {
      vec3 marbleBase = vec3(0.895, 0.855, 0.795); // Deeper warm biscuit parchment #e4dacf
      vec3 marbleWarm = vec3(0.810, 0.745, 0.665); // Antique stone shadow #cfbeaa
      vec3 veinColor  = vec3(0.550, 0.390, 0.210); // Deep rich gold-bronze vein #8c6335

      vec2 p = uv * 1.8 + vec2(t * 0.012, t * 0.009);
      float n = fbm(p + fbm(p * 1.5 + vec2(1.7, 3.2)));
      float vein = abs(sin(p.x * 2.0 + p.y * 1.5 + n * 4.0));
      vein = smoothstep(0.15, 0.0, vein) * 0.65;

      float n2 = fbm(p * 3.0 + 4.0);
      float fineVein = smoothstep(0.10, 0.0, abs(sin(p.y * 3.0 - p.x * 2.0 + n2 * 3.0))) * 0.45;

      vec3 col = mix(marbleBase, marbleWarm, n * 0.65);
      col = mix(col, veinColor, vein + fineVein);
      return col;
    }

    // Light Mode: Floating Translucent Liquid Gold Ribbons (Richer golden depth)
    vec3 renderGoldRibbons(vec2 uv, float t, float mouseWave) {
      vec3 gold1 = vec3(0.95, 0.70, 0.25); // 24K rich deep gold
      vec3 gold2 = vec3(0.76, 0.48, 0.16); // Deep antique gold bronze
      vec3 highlight = vec3(0.98, 0.92, 0.80); // Warm gold sheen

      vec3 ribbonAccum = vec3(0.0);

      // Ribbon 1 (Top sweeping curve)
      float y1 = uv.y - sin(uv.x * 1.4 + t * 0.6) * 0.38 - cos(uv.x * 0.8 - t * 0.4) * 0.2 - 0.35;
      float d1 = abs(y1);
      float ribbon1 = smoothstep(0.24, 0.01, d1);
      float sheen1 = pow(1.0 - clamp(d1 / 0.20, 0.0, 1.0), 2.5);

      // Ribbon 2 (Bottom diagonal ascending wave)
      float y2 = uv.y + sin(uv.x * 1.2 - t * 0.5) * 0.42 + cos(uv.x * 0.6 + t * 0.3) * 0.18 + 0.4;
      float d2 = abs(y2);
      float ribbon2 = smoothstep(0.26, 0.01, d2);
      float sheen2 = pow(1.0 - clamp(d2 / 0.22, 0.0, 1.0), 2.5);

      // Ribbon 3 (Center subtle flowing filament)
      float y3 = uv.y - sin(uv.x * 2.0 - t * 0.7) * 0.22 + cos(uv.x * 1.1 + t * 0.5) * 0.15;
      float d3 = abs(y3);
      float ribbon3 = smoothstep(0.18, 0.01, d3);
      float sheen3 = pow(1.0 - clamp(d3 / 0.15, 0.0, 1.0), 2.5);

      // Liquid silk modulation & caustics
      float caustic = sin(uv.x * 8.0 + uv.y * 6.0 + t * 1.2) * 0.5 + 0.5;
      caustic += sin(uv.x * 12.0 - uv.y * 8.0 - t * 0.8) * 0.5 + 0.5;
      caustic *= 0.3;

      vec3 col1 = mix(gold2, gold1, sheen1) + highlight * pow(sheen1, 3.0) * 0.8;
      vec3 col2 = mix(gold2, gold1, sheen2) + highlight * pow(sheen2, 3.0) * 0.8;
      vec3 col3 = mix(gold2, gold1, sheen3) + highlight * pow(sheen3, 3.0) * 0.7;

      ribbonAccum += col1 * ribbon1 * (0.80 + caustic * 0.30 + mouseWave * 0.45);
      ribbonAccum += col2 * ribbon2 * (0.75 + caustic * 0.25 + mouseWave * 0.40);
      ribbonAccum += col3 * ribbon3 * (0.60 + caustic * 0.20 + mouseWave * 0.35);

      return ribbonAccum;
    }

    void main() {
      // Aspect ratio correction
      vec2 uv = (gl_FragCoord.xy * 2.0 - u_resolution.xy) / min(u_resolution.x, u_resolution.y);
      vec2 mouseNorm = (u_mouse * 2.0 - u_resolution.xy) / min(u_resolution.x, u_resolution.y);

      float t = u_time * 0.45;

      // Distance to mouse for interactive light wave
      float distToMouse = length(uv - mouseNorm);
      float mouseWave = exp(-distToMouse * 2.0) * (0.8 + u_mouse_speed * 1.2);
      float ripple = sin(distToMouse * 12.0 - u_time * 2.5) * exp(-distToMouse * 1.5) * 0.15;

      // ===================================================================
      // 1. DARK MODE (100% UNTOUCHED ORIGINAL PIGMENTS & MESH)
      // ===================================================================
      vec3 groundBase = vec3(0.08, 0.07, 0.05); // #14110c
      vec3 groundWarm = vec3(0.12, 0.09, 0.06); // #1f170f
      vec3 kaaviShade = vec3(0.22, 0.08, 0.05); // Kaavi terracotta warmth (#38140d)

      float vignette = 1.0 - length(v_uv - 0.5) * 0.65;
      vec3 colDark = mix(groundBase, groundWarm, vignette);
      colDark = mix(colDark, kaaviShade, mouseWave * 0.4);

      float noise = fract(sin(dot(v_uv * 180.0, vec2(12.9898, 78.233))) * 43758.5453);
      colDark += (noise - 0.5) * 0.015;

      vec2 gridP = uv * 3.5 + vec2(t * 0.02, t * 0.015);
      float k1 = kolamKnot(gridP, 1.2, t);

      vec2 rotP = rotate2D(PI * 0.25) * uv * 2.2 + vec2(0.5, 0.5);
      float k2 = kolamKnot(rotP, 1.0, -t * 0.8);

      vec2 mP1 = uv - vec2(0.55 * (u_resolution.x / u_resolution.y), 0.1);
      float mandala1 = mandalaKolam(mP1 * 1.4, t);

      vec2 mP2 = uv + vec2(0.65 * (u_resolution.x / u_resolution.y), 0.25);
      float mandala2 = mandalaKolam(mP2 * 1.6, -t * 0.7);

      float totalKolam = k1 * 0.65 + k2 * 0.45 + mandala1 * 0.55 + mandala2 * 0.45;

      vec3 goldBright = vec3(0.96, 0.82, 0.50); // 24K Gold Wire (#f5d180)
      vec3 goldWarm   = vec3(0.81, 0.63, 0.31); // Warm Antique Gold (#cfa14e)
      vec3 riceFlour  = vec3(0.95, 0.93, 0.88); // Rice Flour White (#f2ede0)
      vec3 kaaviColor = vec3(0.70, 0.26, 0.17); // Sacred Kaavi (#b3422b)

      vec3 lineCol = mix(goldWarm, goldBright, sin(t + uv.x * 2.0) * 0.5 + 0.5);
      lineCol = mix(lineCol, riceFlour, 0.25);
      lineCol = mix(lineCol, goldBright, mouseWave);

      colDark += lineCol * (totalKolam * 0.45);
      colDark += kaaviColor * (k2 * 0.25);
      colDark += goldBright * (mouseWave * 0.28 + ripple * totalKolam * 0.5);

      float ambientLamp = exp(-length(uv - vec2(0.0, 0.6)) * 1.2) * 0.18;
      colDark += goldWarm * ambientLamp;

      // ===================================================================
      // 2. LIGHT MODE (Alabaster Marble & Translucent Liquid Gold Ribbons)
      // ===================================================================
      vec3 colLight = renderMarble(uv, t);
      vec3 ribbons = renderGoldRibbons(uv, t, mouseWave);
      colLight += ribbons;
      colLight += (noise - 0.5) * 0.012;

      // Seamless interpolation between Dark (0.0) and Light (1.0)
      vec3 finalColor = mix(colDark, colLight, clamp(u_is_light, 0.0, 1.0));

      gl_FragColor = vec4(finalColor, 1.0);
    }
  `;

  function createShader(gl, type, source) {
    const s = gl.createShader(type);
    gl.shaderSource(s, source);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
      console.error('Shader compile error:', gl.getShaderInfoLog(s));
      gl.deleteShader(s);
      return null;
    }
    return s;
  }

  function createProgram(gl, vs, fs) {
    const p = gl.createProgram();
    gl.attachShader(p, vs);
    gl.attachShader(p, fs);
    gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) {
      console.error('Program link error:', gl.getProgramInfoLog(p));
      return null;
    }
    return p;
  }

  const vs = createShader(gl, gl.VERTEX_SHADER, vsSource);
  const fs = createShader(gl, gl.FRAGMENT_SHADER, fsSource);
  const program = createProgram(gl, vs, fs);

  // Fullscreen Quad Buffer
  const quadBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, quadBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
    -1.0, -1.0,
     1.0, -1.0,
    -1.0,  1.0,
    -1.0,  1.0,
     1.0, -1.0,
     1.0,  1.0
  ]), gl.STATIC_DRAW);

  // State Tracking
  let mouse = { x: window.innerWidth * 0.5, y: window.innerHeight * 0.5 };
  let targetMouse = { x: window.innerWidth * 0.5, y: window.innerHeight * 0.5 };
  let mouseSpeed = 0;
  let lastMouseTime = performance.now();
  let startTime = performance.now();

  let currentLight = document.documentElement.getAttribute('data-theme') === 'light' ? 1.0 : 0.0;
  let targetLight = currentLight;

  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const w = window.innerWidth;
    const h = window.innerHeight;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    gl.viewport(0, 0, canvas.width, canvas.height);
  }

  window.addEventListener('resize', resize, { passive: true });
  resize();

  window.addEventListener('pointermove', (e) => {
    const now = performance.now();
    const dt = Math.max(now - lastMouseTime, 16);
    const dx = e.clientX - targetMouse.x;
    const dy = e.clientY - targetMouse.y;
    mouseSpeed = Math.min(Math.hypot(dx, dy) / dt, 2.5);
    lastMouseTime = now;

    targetMouse.x = e.clientX;
    targetMouse.y = e.clientY;
  }, { passive: true });

  // Main Render Loop (Solid 60 FPS)
  function render(now) {
    mouse.x += (targetMouse.x - mouse.x) * 0.08;
    mouse.y += (targetMouse.y - mouse.y) * 0.08;
    mouseSpeed *= 0.92;

    const isLightMode = document.documentElement.getAttribute('data-theme') === 'light';
    targetLight = isLightMode ? 1.0 : 0.0;
    currentLight += (targetLight - currentLight) * 0.08;

    const time = prefersReducedMotion ? (now - startTime) * 0.0001 : (now - startTime) * 0.001;

    if (program) {
      gl.useProgram(program);

      const posLoc = gl.getAttribLocation(program, 'a_position');
      gl.enableVertexAttribArray(posLoc);
      gl.bindBuffer(gl.ARRAY_BUFFER, quadBuffer);
      gl.vertexAttribPointer(posLoc, 2, gl.FLOAT, false, 0, 0);

      const uRes = gl.getUniformLocation(program, 'u_resolution');
      const uTime = gl.getUniformLocation(program, 'u_time');
      const uMouse = gl.getUniformLocation(program, 'u_mouse');
      const uMouseSpd = gl.getUniformLocation(program, 'u_mouse_speed');
      const uIsLight = gl.getUniformLocation(program, 'u_is_light');

      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      gl.uniform2f(uRes, canvas.width, canvas.height);
      gl.uniform1f(uTime, time);
      gl.uniform2f(uMouse, mouse.x * dpr, (window.innerHeight - mouse.y) * dpr);
      gl.uniform1f(uMouseSpd, mouseSpeed);
      gl.uniform1f(uIsLight, currentLight);

      gl.drawArrays(gl.TRIANGLES, 0, 6);
    }

    requestAnimationFrame(render);
  }

  requestAnimationFrame(render);
})();
