/**
 * ============================================================================
 * WALL JEWELS — Sunset Spore & Gold Foil Drift WebGL Background
 * ============================================================================
 * Strictly background layer (z-index: -1, non-intrusive).
 * Renders a warm dusk sunset terracotta atmosphere with floating
 * 3D gold foil flakes, glowing embers, and sunlit spores.
 */

(function () {
  'use strict';

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Create or retrieve background canvas
  let canvas = document.getElementById('wj-webgl-bg');
  if (!canvas) {
    canvas = document.createElement('canvas');
    canvas.id = 'wj-webgl-bg';
    canvas.setAttribute('aria-hidden', 'true');
    document.body.prepend(canvas);
  }

  // Strict Background Layering (behind all HTML content)
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
    alpha: true, 
    antialias: true, 
    powerPreference: 'high-performance'
  }) || canvas.getContext('experimental-webgl');

  if (!gl) {
    console.warn('WebGL not supported on this browser.');
    return;
  }

  // =========================================================================
  // 1. SUNSET BACKGROUND GRADIENT SHADER
  // =========================================================================
  const bgVsSource = `
    attribute vec2 a_position;
    varying vec2 v_uv;
    void main() {
      v_uv = (a_position + 1.0) * 0.5;
      gl_Position = vec4(a_position, 0.999, 1.0);
    }
  `;

  const bgFsSource = `
    precision mediump float;
    varying vec2 v_uv;
    uniform vec2 u_resolution;
    uniform float u_time;
    uniform vec2 u_mouse;

    void main() {
      vec2 uv = v_uv;
      vec2 m = u_mouse / u_resolution;
      
      // Warm Sunset Terracotta & Saffron Sky Palette
      vec3 skyTop      = vec3(0.08, 0.06, 0.05); // Twilight Baked Earth (#140f0d)
      vec3 skyMid      = vec3(0.38, 0.14, 0.08); // Kaavi Terracotta (#612414)
      vec3 skyHorizon  = vec3(0.72, 0.32, 0.12); // Deep Amber Sunset (#b8521f)
      vec3 sunGlowCol  = vec3(0.96, 0.68, 0.24); // Saffron Gold Horizon Glow (#f5ad3d)

      // Vertical atmospheric gradient
      float y = uv.y;
      vec3 col = mix(skyHorizon, skyMid, smoothstep(0.2, 0.65, y));
      col = mix(col, skyTop, smoothstep(0.65, 1.0, y));

      // Sun halo center on horizon
      vec2 sunPos = vec2(0.5 + (m.x - 0.5) * 0.15, 0.28 + (m.y - 0.5) * 0.1);
      float distToSun = length((uv - sunPos) * vec2(u_resolution.x / u_resolution.y, 1.0));
      float sunGlow = exp(-distToSun * 2.2) * 0.55;
      col += sunGlowCol * sunGlow;

      // Subtle slow heat shimmer / horizon wave
      float wave = sin(uv.x * 6.0 + u_time * 0.4) * 0.015;
      col += vec3(0.08, 0.03, 0.01) * sin(uv.y * 12.0 + wave + u_time * 0.2);

      gl_FragColor = vec4(col, 1.0);
    }
  `;

  // =========================================================================
  // 2. SUNSET SPORES & GOLD FOIL PARTICLES SHADER
  // =========================================================================
  const ptVsSource = `
    attribute vec3 a_position;
    attribute vec3 a_velocity;
    attribute vec4 a_color;
    attribute vec3 a_params; // x: size, y: phase/sparkle, z: tumble speed

    uniform vec2 u_resolution;
    uniform float u_time;
    uniform vec2 u_mouse;
    uniform float u_mouse_speed;

    varying vec4 v_color;
    varying float v_sparkle;
    varying float v_depth;

    void main() {
      vec3 pos = a_position;

      // Organic thermal convection (rising warm currents)
      float t = u_time * 0.65;
      pos.x += sin(t * 0.8 + pos.y * 1.4 + a_params.y) * 0.08;
      pos.y += cos(t * 0.5 + pos.x * 1.1 + a_params.y) * 0.06;
      pos.z += sin(t * 0.4 + a_params.y) * 0.05;

      // Mouse interactive airflow
      vec2 mNorm = (u_mouse / u_resolution) * 2.0 - 1.0;
      mNorm.y = -mNorm.y;
      
      vec2 diff = pos.xy - mNorm;
      float dist = length(diff);
      float repelRadius = 0.65;

      if (dist < repelRadius && dist > 0.001) {
        float force = (1.0 - dist / repelRadius) * (0.18 + u_mouse_speed * 0.5);
        pos.xy += normalize(diff) * force;
      }

      float zScale = (pos.z + 1.2) * 0.5;
      v_depth = clamp(zScale, 0.15, 1.0);

      // Sunset metallic glint
      float glint = abs(sin(u_time * (2.0 + a_params.z * 2.0) + pos.x * 8.0 + a_params.y));
      v_sparkle = pow(glint, 3.5);

      v_color = a_color;

      float baseSize = a_params.x * (u_resolution.y / 700.0);
      gl_PointSize = baseSize * (0.65 + v_depth * 1.1);
      gl_Position = vec4(pos.xy, pos.z * 0.4, 1.0);
    }
  `;

  const ptFsSource = `
    precision mediump float;
    varying vec4 v_color;
    varying float v_sparkle;
    varying float v_depth;

    void main() {
      vec2 coord = gl_PointCoord - vec2(0.5);
      float dist = length(coord);

      if (dist > 0.5) {
        discard;
      }

      float halo = smoothstep(0.5, 0.0, dist);
      float core = exp(-dist * 6.0) * (0.7 + v_sparkle * 2.0);

      // Sunset glowing core
      vec3 sunsetHighlight = vec3(1.0, 0.88, 0.55) * (core * 1.2 + v_sparkle * 0.5);
      vec3 finalCol = v_color.rgb * (halo * 0.8 + core * 0.4) + sunsetHighlight;
      float finalAlpha = clamp(v_color.a * (halo * 0.85 + core * 0.5) * (0.5 + v_depth * 0.5), 0.0, 1.0);

      gl_FragColor = vec4(finalCol, finalAlpha);
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

  const bgProg = createProgram(gl, createShader(gl, gl.VERTEX_SHADER, bgVsSource), createShader(gl, gl.FRAGMENT_SHADER, bgFsSource));
  const ptProg = createProgram(gl, createShader(gl, gl.VERTEX_SHADER, ptVsSource), createShader(gl, gl.FRAGMENT_SHADER, ptFsSource));

  // Background Quad Buffer
  const bgQuadBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, bgQuadBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
    -1.0, -1.0,
     1.0, -1.0,
    -1.0,  1.0,
    -1.0,  1.0,
     1.0, -1.0,
     1.0,  1.0
  ]), gl.STATIC_DRAW);

  // Sunset Palette: Glowing Amber, Molten Gold, Terracotta, Coral
  const SUNSET_PALETTE = [
    { r: 1.00, g: 0.75, b: 0.28, a: 0.95 }, // Molten Saffron Gold (#ffbf47)
    { r: 0.98, g: 0.55, b: 0.18, a: 0.90 }, // Radiant Sunset Amber (#fa8c2e)
    { r: 0.88, g: 0.32, b: 0.14, a: 0.85 }, // Kaavi Terracotta (#e05224)
    { r: 1.00, g: 0.88, b: 0.60, a: 0.95 }, // 24K Sunlit Gold Leaf (#ffe099)
    { r: 0.95, g: 0.45, b: 0.35, a: 0.75 }  // Coral Sunset Mote (#f27359)
  ];

  const PARTICLE_COUNT = 2600;
  const posData = new Float32Array(PARTICLE_COUNT * 3);
  const velData = new Float32Array(PARTICLE_COUNT * 3);
  const colData = new Float32Array(PARTICLE_COUNT * 4);
  const paramData = new Float32Array(PARTICLE_COUNT * 3);

  for (let i = 0; i < PARTICLE_COUNT; i++) {
    posData[i * 3 + 0] = (Math.random() * 2.4 - 1.2);
    posData[i * 3 + 1] = (Math.random() * 2.4 - 1.2);
    posData[i * 3 + 2] = (Math.random() * 2.0 - 1.0);

    velData[i * 3 + 0] = (Math.random() - 0.5) * 0.0006;
    velData[i * 3 + 1] = Math.random() * 0.0010 + 0.0003; // Gentle upward thermal drift
    velData[i * 3 + 2] = (Math.random() - 0.5) * 0.0005;

    const rand = Math.random();
    let col = SUNSET_PALETTE[0];
    if (rand < 0.35) col = SUNSET_PALETTE[0];
    else if (rand < 0.65) col = SUNSET_PALETTE[1];
    else if (rand < 0.82) col = SUNSET_PALETTE[2];
    else if (rand < 0.93) col = SUNSET_PALETTE[3];
    else col = SUNSET_PALETTE[4];

    colData[i * 4 + 0] = col.r;
    colData[i * 4 + 1] = col.g;
    colData[i * 4 + 2] = col.b;
    colData[i * 4 + 3] = col.a;

    const isLarge = Math.random() < 0.18;
    paramData[i * 3 + 0] = isLarge ? (Math.random() * 12.0 + 14.0) : (Math.random() * 7.0 + 4.0);
    paramData[i * 3 + 1] = Math.random() * 6.2831;
    paramData[i * 3 + 2] = Math.random() * 1.5 + 0.5;
  }

  const posBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, posBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, posData, gl.DYNAMIC_DRAW);

  const colBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, colBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, colData, gl.STATIC_DRAW);

  const paramBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, paramBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, paramData, gl.STATIC_DRAW);

  let mouse = { x: window.innerWidth * 0.5, y: window.innerHeight * 0.5 };
  let targetMouse = { x: window.innerWidth * 0.5, y: window.innerHeight * 0.5 };
  let mouseSpeed = 0;
  let lastMouseTime = performance.now();
  let startTime = performance.now();

  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 1.5);
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

  // Animation Loop
  function render(now) {
    mouse.x += (targetMouse.x - mouse.x) * 0.06;
    mouse.y += (targetMouse.y - mouse.y) * 0.06;
    mouseSpeed *= 0.92;

    const time = prefersReducedMotion ? (now - startTime) * 0.0002 : (now - startTime) * 0.001;
    const speedMult = prefersReducedMotion ? 0.3 : 1.0;

    // 1. Render Sunset Background Quad
    gl.disable(gl.BLEND);
    if (bgProg) {
      gl.useProgram(bgProg);
      const bgPosLoc = gl.getAttribLocation(bgProg, 'a_position');
      gl.enableVertexAttribArray(bgPosLoc);
      gl.bindBuffer(gl.ARRAY_BUFFER, bgQuadBuffer);
      gl.vertexAttribPointer(bgPosLoc, 2, gl.FLOAT, false, 0, 0);

      gl.uniform2f(gl.getUniformLocation(bgProg, 'u_resolution'), canvas.width, canvas.height);
      gl.uniform1f(gl.getUniformLocation(bgProg, 'u_time'), time);
      gl.uniform2f(gl.getUniformLocation(bgProg, 'u_mouse'), mouse.x, mouse.y);

      gl.drawArrays(gl.TRIANGLES, 0, 6);
    }

    // 2. Update & Render Sunset Spore & Foil Particles
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      posData[i * 3 + 0] += velData[i * 3 + 0] * speedMult;
      posData[i * 3 + 1] += velData[i * 3 + 1] * speedMult;
      posData[i * 3 + 2] += velData[i * 3 + 2] * speedMult;

      if (posData[i * 3 + 1] > 1.25) {
        posData[i * 3 + 1] = -1.25;
        posData[i * 3 + 0] = (Math.random() * 2.4 - 1.2);
      }
      if (posData[i * 3 + 0] > 1.25) posData[i * 3 + 0] = -1.25;
      if (posData[i * 3 + 0] < -1.25) posData[i * 3 + 0] = 1.25;
      if (posData[i * 3 + 2] > 1.0) posData[i * 3 + 2] = -1.0;
      if (posData[i * 3 + 2] < -1.0) posData[i * 3 + 2] = 1.0;
    }

    gl.bindBuffer(gl.ARRAY_BUFFER, posBuffer);
    gl.bufferSubData(gl.ARRAY_BUFFER, 0, posData);

    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE); // Luminous additive overlay on sunset background

    if (ptProg) {
      gl.useProgram(ptProg);

      const posLoc = gl.getAttribLocation(ptProg, 'a_position');
      gl.enableVertexAttribArray(posLoc);
      gl.bindBuffer(gl.ARRAY_BUFFER, posBuffer);
      gl.vertexAttribPointer(posLoc, 3, gl.FLOAT, false, 0, 0);

      const colLoc = gl.getAttribLocation(ptProg, 'a_color');
      gl.enableVertexAttribArray(colLoc);
      gl.bindBuffer(gl.ARRAY_BUFFER, colBuffer);
      gl.vertexAttribPointer(colLoc, 4, gl.FLOAT, false, 0, 0);

      const paramLoc = gl.getAttribLocation(ptProg, 'a_params');
      gl.enableVertexAttribArray(paramLoc);
      gl.bindBuffer(gl.ARRAY_BUFFER, paramBuffer);
      gl.vertexAttribPointer(paramLoc, 3, gl.FLOAT, false, 0, 0);

      gl.uniform2f(gl.getUniformLocation(ptProg, 'u_resolution'), canvas.width, canvas.height);
      gl.uniform1f(gl.getUniformLocation(ptProg, 'u_time'), time);
      gl.uniform2f(gl.getUniformLocation(ptProg, 'u_mouse'), mouse.x, mouse.y);
      gl.uniform1f(gl.getUniformLocation(ptProg, 'u_mouse_speed'), mouseSpeed);

      gl.drawArrays(gl.POINTS, 0, PARTICLE_COUNT);
    }

    requestAnimationFrame(render);
  }

  requestAnimationFrame(render);
})();
