/**
 * ============================================================================
 * WALL JEWELS — Sacred Kolam Geometry & Rice-Flour Light Grid WebGL Background
 * ============================================================================
 * Concept 3: Sacred Kolam Geometry & Pulli Dot Constellation.
 * South Indian heritage geometric lattice with glowing golden loop curves,
 * rice-flour dot matrix, and interactive light waves.
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
  // SACRED KOLAM GEOMETRY SHADER
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

    #define PI 3.14159265359
    #define TWO_PI 6.28318530718

    // 2D Rotation
    mat2 rotate2D(float angle) {
      return mat2(cos(angle), -sin(angle), sin(angle), cos(angle));
    }

    // Sacred Kolam Knot (Sikku Loop around pulli dots)
    float kolamKnot(vec2 p, float scale, float t) {
      vec2 grid = fract(p * scale) - 0.5;
      vec2 id = floor(p * scale);

      // Distance to central pulli dot
      float dotDist = length(grid);
      float pulli = smoothstep(0.065, 0.035, dotDist);

      // Petal & loop curvature calculations
      float angle = atan(grid.y, grid.x);
      float petalDist = abs(sin(angle * 4.0 + t * 0.5)) * 0.28 + 0.12;
      float loopLine = abs(dotDist - petalDist);
      float loopGlow = smoothstep(0.035, 0.005, loopLine);

      // Diagonal cross-linking strands
      vec2 diagP = abs(grid) - vec2(0.25);
      float diagLine = abs(diagP.x + diagP.y);
      float diagGlow = smoothstep(0.04, 0.008, diagLine);

      return pulli * 1.5 + loopGlow * 0.85 + diagGlow * 0.45;
    }

    // Mandala Floral Radial Kolam
    float mandalaKolam(vec2 p, float t) {
      float r = length(p);
      float a = atan(p.y, p.x);

      // 8-fold sacred symmetry
      float f1 = abs(sin(a * 4.0 + t * 0.2)) * 0.35 + 0.25;
      float f2 = abs(cos(a * 8.0 - t * 0.3)) * 0.18 + 0.45;
      float f3 = abs(sin(a * 12.0 + t * 0.1)) * 0.08 + 0.65;

      float ring1 = smoothstep(0.02, 0.002, abs(r - f1));
      float ring2 = smoothstep(0.02, 0.002, abs(r - f2));
      float ring3 = smoothstep(0.02, 0.002, abs(r - f3));
      float centerDot = smoothstep(0.08, 0.02, r);

      return ring1 * 0.9 + ring2 * 0.75 + ring3 * 0.6 + centerDot * 1.2;
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

      // Base Ground Palette: Deep Warm Handmade Dark Charcoal Paper
      vec3 groundBase = vec3(0.08, 0.07, 0.05); // #14110c
      vec3 groundWarm = vec3(0.12, 0.09, 0.06); // #1f170f
      vec3 kaaviShade = vec3(0.22, 0.08, 0.05); // Kaavi terracotta warmth (#38140d)

      // Radial Vignette
      float vignette = 1.0 - length(v_uv - 0.5) * 0.65;
      vec3 col = mix(groundBase, groundWarm, vignette);
      col = mix(col, kaaviShade, mouseWave * 0.4);

      // Micro Paper Grain Texture
      float noise = fract(sin(dot(v_uv * 180.0, vec2(12.9898, 78.233))) * 43758.5453);
      col += (noise - 0.5) * 0.015;

      // 1. Structural Pulli Dot Matrix
      vec2 gridP = uv * 3.5 + vec2(t * 0.02, t * 0.015);
      float k1 = kolamKnot(gridP, 1.2, t);

      // 2. Secondary Offset Sacred Grid (45 deg turned)
      vec2 rotP = rotate2D(PI * 0.25) * uv * 2.2 + vec2(0.5, 0.5);
      float k2 = kolamKnot(rotP, 1.0, -t * 0.8);

      // 3. Central Ambient Mandala Centers (revolving slowly)
      vec2 mP1 = uv - vec2(0.55 * (u_resolution.x / u_resolution.y), 0.1);
      float mandala1 = mandalaKolam(mP1 * 1.4, t);

      vec2 mP2 = uv + vec2(0.65 * (u_resolution.x / u_resolution.y), 0.25);
      float mandala2 = mandalaKolam(mP2 * 1.6, -t * 0.7);

      // Combine Kolam geometry patterns
      float totalKolam = k1 * 0.65 + k2 * 0.45 + mandala1 * 0.55 + mandala2 * 0.45;

      // Color Pigments
      vec3 goldBright = vec3(0.96, 0.82, 0.50); // 24K Gold Wire (#f5d180)
      vec3 goldWarm   = vec3(0.81, 0.63, 0.31); // Warm Antique Gold (#cfa14e)
      vec3 riceFlour  = vec3(0.95, 0.93, 0.88); // Rice Flour White (#f2ede0)
      vec3 kaaviColor = vec3(0.70, 0.26, 0.17); // Sacred Kaavi (#b3422b)

      // Lighting modulation
      vec3 lineCol = mix(goldWarm, goldBright, sin(t + uv.x * 2.0) * 0.5 + 0.5);
      lineCol = mix(lineCol, riceFlour, 0.25);
      lineCol = mix(lineCol, goldBright, mouseWave);

      // Additive luminous energy
      col += lineCol * (totalKolam * 0.45);
      col += kaaviColor * (k2 * 0.25);

      // Interactive Mouse Light Corona & Golden Ray
      col += goldBright * (mouseWave * 0.28 + ripple * totalKolam * 0.5);

      // Subtle ambient lamp glow
      float ambientLamp = exp(-length(uv - vec2(0.0, 0.6)) * 1.2) * 0.18;
      col += goldWarm * ambientLamp;

      gl_FragColor = vec4(col, 1.0);
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

      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      gl.uniform2f(uRes, canvas.width, canvas.height);
      gl.uniform1f(uTime, time);
      gl.uniform2f(uMouse, mouse.x * dpr, (window.innerHeight - mouse.y) * dpr);
      gl.uniform1f(uMouseSpd, mouseSpeed);

      gl.drawArrays(gl.TRIANGLES, 0, 6);
    }

    requestAnimationFrame(render);
  }

  requestAnimationFrame(render);
})();
