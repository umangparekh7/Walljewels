/**
 * ============================================================================
 * WALL JEWELS — Sunset Terracotta Liquid Silk WebGL Background
 * ============================================================================
 * High-performance 3D liquid silk drapery shader in Sunset Terracotta
 * strictly rendered in background (z-index: -9999).
 */

(function () {
  'use strict';

  // Create background canvas
  const canvas = document.createElement('canvas');
  canvas.id = 'wj-webgl-bg';
  canvas.setAttribute('aria-hidden', 'true');
  
  Object.assign(canvas.style, {
    position: 'fixed',
    top: '0',
    left: '0',
    width: '100vw',
    height: '100vh',
    pointerEvents: 'none',
    zIndex: '-9999',
    opacity: '1.0',
    mixBlendMode: 'normal'
  });

  document.body.prepend(canvas);

  const gl = canvas.getContext('webgl', { alpha: true, antialias: true, premultipliedAlpha: false }) ||
             canvas.getContext('experimental-webgl');

  if (!gl) {
    console.warn('WebGL not supported on this browser.');
    return;
  }

  // Fullscreen Quad Vertex Shader
  const vsSource = `
    attribute vec2 a_position;
    varying vec2 v_uv;
    void main() {
      v_uv = (a_position + 1.0) * 0.5;
      gl_Position = vec4(a_position, 0.0, 1.0);
    }
  `;

  // Sunset Terracotta Liquid Silk Fragment Shader
  const fsSource = `
    precision mediump float;
    varying vec2 v_uv;
    uniform vec2 u_resolution;
    uniform float u_time;
    uniform vec2 u_mouse;
    uniform float u_intensity;
    uniform vec3 u_c1, u_c2, u_c3, u_c4;

    void main() {
      vec2 uv = (gl_FragCoord.xy * 2.0 - u_resolution.xy) / min(u_resolution.x, u_resolution.y);
      vec2 m = (u_mouse * 2.0 - u_resolution.xy) / min(u_resolution.x, u_resolution.y);
      
      float distToMouse = length(uv - m);
      float mouseWave = sin(distToMouse * 10.0 - u_time * 3.0) * exp(-distToMouse * 2.0) * 0.4;

      float t = u_time * 0.45;
      
      // Multi-frequency wave synthesis for liquid silk drape
      float w1 = sin(uv.x * 2.5 + uv.y * 1.8 + t + mouseWave);
      float w2 = cos(uv.x * 3.2 - uv.y * 2.4 - t * 0.8);
      float w3 = sin((uv.x + uv.y) * 4.2 + t * 1.3 + w1 * 1.5);
      float w4 = cos(uv.x * 6.5 - t * 0.6 + w2);
      
      float drape = w1 * 0.4 + w2 * 0.25 + w3 * 0.25 + w4 * 0.1;
      
      // Compute pseudo-normal for specular sheen
      vec2 eps = vec2(0.012, 0.0);
      float dx = (sin((uv.x+eps.x)*2.5 + uv.y*1.8 + t) - w1) / eps.x;
      float dy = (sin(uv.x*2.5 + (uv.y+eps.x)*1.8 + t) - w1) / eps.x;
      vec3 normal = normalize(vec3(-dx * 0.45, -dy * 0.45, 1.0));
      
      vec3 lightDir = normalize(vec3(m.x * 0.6 + 0.4, -m.y * 0.6 + 0.6, 0.7));
      float diff = max(dot(normal, lightDir), 0.0);
      float spec = pow(max(dot(reflect(-lightDir, normal), vec3(0.0, 0.0, 1.0)), 0.0), 22.0);
      
      float fold = smoothstep(-0.85, 0.85, drape);
      vec3 color = mix(u_c1, u_c2, fold * u_intensity);
      color = mix(color, u_c4, smoothstep(0.3, 0.8, w3) * 0.6 * u_intensity);
      color += u_c3 * (spec * 0.85 + diff * 0.4) * u_intensity;

      float alpha = clamp((fold * 0.6 + spec * 0.4 + 0.15) * u_intensity, 0.0, 0.95);
      gl_FragColor = vec4(color, alpha);
    }
  `;

  // Palette: Sunset Terracotta
  const theme = {
    c1: [0.14, 0.05, 0.02],      // Dark Baked Earth base
    c2: [0.88, 0.32, 0.10],      // Vibrant Terracotta
    c3: [0.98, 0.75, 0.15],      // Saffron Sunshine highlight
    c4: [0.95, 0.45, 0.55],      // Coral Rose accent
  };

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

  function createProgram(gl, vsSrc, fsSrc) {
    const vs = createShader(gl, gl.VERTEX_SHADER, vsSrc);
    const fs = createShader(gl, gl.FRAGMENT_SHADER, fsSrc);
    const prog = gl.createProgram();
    gl.attachShader(prog, vs);
    gl.attachShader(prog, fs);
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
      console.error('Program link error:', gl.getProgramInfoLog(prog));
      return null;
    }
    return prog;
  }

  const program = createProgram(gl, vsSource, fsSource);

  // Buffer Quad
  const posBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, posBuffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
    -1.0, -1.0,
     1.0, -1.0,
    -1.0,  1.0,
    -1.0,  1.0,
     1.0, -1.0,
     1.0,  1.0
  ]), gl.STATIC_DRAW);

  let intensity = 0.85;
  let mouse = { x: window.innerWidth * 0.5, y: window.innerHeight * 0.5 };
  let targetMouse = { x: window.innerWidth * 0.5, y: window.innerHeight * 0.5 };
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
    targetMouse.x = e.clientX;
    targetMouse.y = e.clientY;
  }, { passive: true });

  // Animation Loop
  function render(now) {
    mouse.x += (targetMouse.x - mouse.x) * 0.06;
    mouse.y += (targetMouse.y - mouse.y) * 0.06;

    if (program) {
      gl.useProgram(program);

      const posLoc = gl.getAttribLocation(program, 'a_position');
      gl.enableVertexAttribArray(posLoc);
      gl.bindBuffer(gl.ARRAY_BUFFER, posBuffer);
      gl.vertexAttribPointer(posLoc, 2, gl.FLOAT, false, 0, 0);

      const uResLoc = gl.getUniformLocation(program, 'u_resolution');
      const uTimeLoc = gl.getUniformLocation(program, 'u_time');
      const uMouseLoc = gl.getUniformLocation(program, 'u_mouse');
      const uIntLoc = gl.getUniformLocation(program, 'u_intensity');
      const uC1Loc = gl.getUniformLocation(program, 'u_c1');
      const uC2Loc = gl.getUniformLocation(program, 'u_c2');
      const uC3Loc = gl.getUniformLocation(program, 'u_c3');
      const uC4Loc = gl.getUniformLocation(program, 'u_c4');

      const dpr = Math.min(window.devicePixelRatio || 1, 1.5);
      gl.uniform2f(uResLoc, canvas.width, canvas.height);
      gl.uniform1f(uTimeLoc, (now - startTime) * 0.001);
      gl.uniform2f(uMouseLoc, mouse.x * dpr, (window.innerHeight - mouse.y) * dpr);
      gl.uniform1f(uIntLoc, intensity);

      gl.uniform3fv(uC1Loc, theme.c1);
      gl.uniform3fv(uC2Loc, theme.c2);
      gl.uniform3fv(uC3Loc, theme.c3);
      gl.uniform3fv(uC4Loc, theme.c4);

      gl.drawArrays(gl.TRIANGLES, 0, 6);
    }

    requestAnimationFrame(render);
  }

  requestAnimationFrame(render);
})();
