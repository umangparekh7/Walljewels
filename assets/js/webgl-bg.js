/**
 * ============================================================================
 * WALL JEWELS — WebGL Ambient Luxury Canvas
 * ============================================================================
 * Dark Mode: Sacred Kolam Geometry & Rice-Flour Light Grid (100% Preserved)
 * Light Mode: Alabaster Marble & Translucent Liquid Gold Silk Ribbons
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
    width: '100vw',
    height: '100vh',
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
  // SHADER SOURCE
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
    uniform float u_theme; // 0.0 = Dark Mode (Kolam), 1.0 = Light Mode (Alabaster & Gold Ribbons)

    #define PI 3.14159265359
    #define TWO_PI 6.28318530718

    // 2D Rotation
    mat2 rotate2D(float angle) {
      return mat2(cos(angle), -sin(angle), sin(angle), cos(angle));
    }

    // Sacred Kolam Knot (Dark Mode)
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

    // Mandala Floral Radial Kolam (Dark Mode)
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

    // Smooth Noise for Marble Veins
    float hash21(vec2 p) {
      p = fract(p * vec2(234.34, 435.345));
      p += dot(p, p + 34.23);
      return fract(p.x * p.y);
    }
    float noise2D(vec2 p) {
      vec2 i = floor(p);
      vec2 f = fract(p);
      f = f * f * (3.0 - 2.0 * f);
      float a = hash21(i);
      float b = hash21(i + vec2(1.0, 0.0));
      float c = hash21(i + vec2(0.0, 1.0));
      float d = hash21(i + vec2(1.0, 1.0));
      return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
    }
    float fbm(vec2 p) {
      float v = 0.0;
      float a = 0.5;
      for (int i = 0; i < 4; i++) {
        v += a * noise2D(p);
        p = p * 2.0 + vec2(100.0);
        a *= 0.5;
      }
      return v;
    }

    // Liquid Gold Silk Ribbon Generator (Light Mode)
    vec4 goldRibbon(vec2 uv, float offset, float freq, float speed, float width, float t, vec2 mouseNorm) {
      float wave = sin(uv.x * freq + t * speed + offset) * 0.38
                 + cos(uv.x * (freq * 0.6) - t * (speed * 0.8) + offset * 1.5) * 0.18;
      
      // Interactive mouse wave
      float mDist = length(uv - mouseNorm);
      wave += exp(-mDist * 2.5) * 0.12 * sin(t * 3.0);

      float dist = abs(uv.y - wave);
      float ribbonMask = smoothstep(width, 0.001, dist);
      float edgeHighlight = smoothstep(width * 0.12, 0.001, abs(dist - width * 0.85));
      
      float gradient = (uv.y - wave) / max(width, 0.001);
      float sheen = pow(1.0 - abs(gradient), 2.5);

      return vec4(ribbonMask, edgeHighlight, sheen, gradient);
    }

    void main() {
      vec2 uv = (gl_FragCoord.xy * 2.0 - u_resolution.xy) / min(u_resolution.x, u_resolution.y);
      vec2 mouseNorm = (u_mouse * 2.0 - u_resolution.xy) / min(u_resolution.x, u_resolution.y);

      float t = u_time * 0.45;
      float distToMouse = length(uv - mouseNorm);
      float mouseWave = exp(-distToMouse * 2.0) * (0.8 + u_mouse_speed * 1.2);
      float ripple = sin(distToMouse * 12.0 - u_time * 2.5) * exp(-distToMouse * 1.5) * 0.15;

      // =====================================================================
      // 1. DARK MODE SHADER (Sacred Kolam Geometry — 100% Locked)
      // =====================================================================
      vec3 groundBase = vec3(0.08, 0.07, 0.05); // #14110c
      vec3 groundWarm = vec3(0.12, 0.09, 0.06); // #1f170f
      vec3 kaaviShade = vec3(0.22, 0.08, 0.05); // #38140d

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

      vec3 goldBright = vec3(0.96, 0.82, 0.50);
      vec3 goldWarm   = vec3(0.81, 0.63, 0.31);
      vec3 riceFlour  = vec3(0.95, 0.93, 0.88);
      vec3 kaaviColor = vec3(0.70, 0.26, 0.17);

      vec3 lineCol = mix(goldWarm, goldBright, sin(t + uv.x * 2.0) * 0.5 + 0.5);
      lineCol = mix(lineCol, riceFlour, 0.25);
      lineCol = mix(lineCol, goldBright, mouseWave);

      colDark += lineCol * (totalKolam * 0.45);
      colDark += kaaviColor * (k2 * 0.25);
      colDark += goldBright * (mouseWave * 0.28 + ripple * totalKolam * 0.5);

      float ambientLamp = exp(-length(uv - vec2(0.0, 0.6)) * 1.2) * 0.18;
      colDark += goldWarm * ambientLamp;

      // =====================================================================
      // 2. LIGHT MODE SHADER (Alabaster Marble & Translucent Liquid Gold Ribbons)
      // =====================================================================
      vec3 alabasterBase = vec3(0.985, 0.975, 0.955); // Pure warm alabaster #fcf9f4
      vec3 marbleVeinCol = vec3(0.89, 0.83, 0.74);   // Soft warm sandalwood vein #e3d4bd
      vec3 marbleAmber   = vec3(0.84, 0.75, 0.62);   // Amber mineral accent #d6c09e

      vec2 marbleUV = uv * 1.5;
      float veinNoise = fbm(marbleUV + vec2(fbm(marbleUV * 2.0 + t * 0.015), fbm(marbleUV * 1.8)));
      float veinPattern = smoothstep(0.48, 0.54, sin(marbleUV.x * 1.8 + marbleUV.y * 1.2 + veinNoise * 4.0));
      
      vec3 colLight = mix(alabasterBase, marbleVeinCol, veinPattern * 0.45);
      colLight = mix(colLight, marbleAmber, fbm(marbleUV * 3.5) * 0.12);

      vec4 r1 = goldRibbon(uv, 0.2, 1.4, 0.4, 0.22, t, mouseNorm);
      vec4 r2 = goldRibbon(uv, 2.4, 1.1, -0.32, 0.28, t, mouseNorm);
      vec4 r3 = goldRibbon(uv, 4.6, 1.8, 0.25, 0.18, t * 1.2, mouseNorm);

      vec3 ribbonGoldDeep = vec3(0.82, 0.63, 0.28);
      vec3 ribbonGoldPure = vec3(0.95, 0.80, 0.44);
      vec3 ribbonGoldRim  = vec3(0.99, 0.92, 0.70);

      vec3 rCol1 = mix(ribbonGoldDeep, ribbonGoldPure, r1.z);
      rCol1 = mix(rCol1, ribbonGoldRim, r1.y * 0.9);
      colLight = mix(colLight, rCol1, r1.x * 0.55);

      vec3 rCol2 = mix(ribbonGoldDeep, ribbonGoldPure, r2.z);
      rCol2 = mix(rCol2, ribbonGoldRim, r2.y * 0.85);
      colLight = mix(colLight, rCol2, r2.x * 0.48);

      vec3 rCol3 = mix(ribbonGoldDeep, ribbonGoldPure, r3.z);
      rCol3 = mix(rCol3, ribbonGoldRim, r3.y * 0.8);
      colLight = mix(colLight, rCol3, r3.x * 0.40);

      float caustic = sin(uv.x * 14.0 + t * 1.2) * cos(uv.y * 14.0 - t * 0.9) * 0.035;
      colLight += vec3(caustic * 0.6, caustic * 0.5, caustic * 0.2);
      colLight += ribbonGoldPure * (mouseWave * 0.14 + ripple * 0.08);
      colLight += (noise - 0.5) * 0.01;

      // =====================================================================
      // INTERPOLATE THEME
      // =====================================================================
      vec3 finalCol = mix(colDark, colLight, clamp(u_theme, 0.0, 1.0));
      gl_FragColor = vec4(finalCol, 1.0);
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
  let currentTheme = document.documentElement.getAttribute('data-theme') === 'light' ? 1.0 : 0.0;

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

    const isLight = document.documentElement.getAttribute('data-theme') === 'light';
    const targetTheme = isLight ? 1.0 : 0.0;
    currentTheme += (targetTheme - currentTheme) * 0.08;

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
      const uTheme = gl.getUniformLocation(program, 'u_theme');

      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      gl.uniform2f(uRes, canvas.width, canvas.height);
      gl.uniform1f(uTime, time);
      gl.uniform2f(uMouse, mouse.x * dpr, (window.innerHeight - mouse.y) * dpr);
      gl.uniform1f(uMouseSpd, mouseSpeed);
      gl.uniform1f(uTheme, currentTheme);

      gl.drawArrays(gl.TRIANGLES, 0, 6);
    }

    requestAnimationFrame(render);
  }

  requestAnimationFrame(render);
})();
