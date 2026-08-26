import re

# 1. Update fireworks.js
fireworks_code = """/**
 * Fireworks — Originkit (Canvas 2D top-down / perspective particle simulation)
 * Dedicated background engine for .coll-hero on the collection page.
 * Full width edge-to-edge rendering with zero layout thrashing.
 */

(function () {
  'use strict';

  function parseColor(c) {
    if (!c) return { r: 0, g: 0, b: 0 };
    if (c[0] === "#") {
      let h = c.slice(1);
      if (h.length === 3)
        h = h.split("").map((x) => x + x).join("");
      const n = parseInt(h.slice(0, 6), 16);
      return { r: (n >> 16) & 255, g: (n >> 8) & 255, b: n & 255 };
    }
    const m = c.match(/[\d.]+/g);
    if (m) return { r: +m[0], g: +m[1], b: +m[2] };
    return { r: 0, g: 0, b: 0 };
  }

  function hslToRgb(h, s, l) {
    if (s === 0) {
      const v = Math.round(l * 255);
      return { r: v, g: v, b: v };
    }
    const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    const p = 2 * l - q;
    const hue = (t) => {
      if (t < 0) t += 1;
      if (t > 1) t -= 1;
      if (t < 1 / 6) return p + (q - p) * 6 * t;
      if (t < 1 / 2) return q;
      if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
      return p;
    };
    return {
      r: Math.round(hue(h + 1 / 3) * 255),
      g: Math.round(hue(h) * 255),
      b: Math.round(hue(h - 1 / 3) * 255),
    };
  }

  // World extents / camera
  const FIELD = 1.6;
  const APEX_LO = 0.7;
  const APEX_HI = 1.6;
  const CAM_DIST = 3.4;
  const G0 = 2.2;
  const CAP = 6000;

  const DEFAULT_COLORS = [
    "#FFD166",
    "#FF4D6D",
    "#4CC9F0",
    "#B15CFF",
    "#FF0000",
    "#007FFF",
    "#C1FF00",
  ];

  const GRAVITY = 0.55 * G0;
  const RAINBOW_SAT = 0.9 * 0.9 + 0.1;

  function initFireworks() {
    const hero = document.querySelector('.coll-hero');
    if (!hero) return;

    let canvas = hero.querySelector('.coll-hero__fireworks');
    if (!canvas) {
      canvas = document.createElement('canvas');
      canvas.className = 'coll-hero__fireworks';
      canvas.id = 'coll-fireworks-canvas';
      canvas.setAttribute('aria-hidden', 'true');
      hero.prepend(canvas);
    }

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const live = {
      colors: DEFAULT_COLORS,
      background: '#05060a',
      rate: 100,
      sparks: 240,
      size: 92,
      trail: 76,
      speed: 72,
      tilt: 45,
    };

    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    let raf = 0;
    let isVisible = true;

    let W = hero.clientWidth || window.innerWidth || 1200;
    let H = hero.clientHeight || 420;

    const P = {
      x: new Float32Array(CAP),
      y: new Float32Array(CAP),
      z: new Float32Array(CAP),
      vx: new Float32Array(CAP),
      vy: new Float32Array(CAP),
      vz: new Float32Array(CAP),
      life: new Float32Array(CAP),
      max: new Float32Array(CAP),
      r: new Float32Array(CAP),
      g: new Float32Array(CAP),
      b: new Float32Array(CAP),
    };
    let cursor = 0;

    let rockets = [];
    let acc = 0;
    let last = 0;

    const pickColor = () => {
      const list = live.colors;
      if (Array.isArray(list) && list.length > 0) {
        const i = Math.min(
          list.length - 1,
          (Math.random() * list.length) | 0
        );
        return parseColor(list[i]);
      }
      return hslToRgb(Math.random(), RAINBOW_SAT, 0.6);
    };

    const spawnRocket = () => {
      const apex = APEX_LO + Math.random() * (APEX_HI - APEX_LO);
      const col = pickColor();
      rockets.push({
        x: (Math.random() * 2 - 1) * FIELD,
        z: (Math.random() * 2 - 1) * FIELD,
        y: 0,
        vy: Math.sqrt(2 * GRAVITY * apex),
        r: col.r,
        g: col.g,
        b: col.b,
      });
    };

    const burst = (rk) => {
      const n = Math.max(20, live.sparks | 0);
      const spread = 0.9 * (live.size / 100);
      for (let i = 0; i < n; i++) {
        const u = Math.random() * 2 - 1;
        const th = Math.random() * Math.PI * 2;
        const rr = Math.sqrt(1 - u * u);
        const spd = spread * (0.45 + Math.random() * 0.55);
        const c = cursor;
        cursor = (cursor + 1) % CAP;
        P.x[c] = rk.x;
        P.y[c] = rk.y;
        P.z[c] = rk.z;
        P.vx[c] = rr * Math.cos(th) * spd;
        P.vy[c] = u * spd;
        P.vz[c] = rr * Math.sin(th) * spd;
        const life = 1.1 + Math.random() * 0.9;
        P.life[c] = life;
        P.max[c] = life;
        P.r[c] = rk.r;
        P.g[c] = rk.g;
        P.b[c] = rk.b;
      }
    };

    const sizeCanvas = () => {
      W = hero.clientWidth || window.innerWidth || 1200;
      H = hero.clientHeight || 420;
      const bw = Math.floor(W * dpr);
      const bh = Math.floor(H * dpr);
      if (canvas.width !== bw || canvas.height !== bh) {
        canvas.width = bw;
        canvas.height = bh;
      }
      canvas.style.width = '100%';
      canvas.style.height = '100%';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.fillStyle = live.background;
      ctx.fillRect(0, 0, W, H);
    };

    sizeCanvas();

    const render = (now) => {
      if (!isVisible) {
        last = now;
        raf = requestAnimationFrame(render);
        return;
      }

      if (!last) last = now;
      let dt = (now - last) / 1000;
      last = now;
      if (dt > 0.05) dt = 0.05;
      dt *= Math.max(0, live.speed) / 100;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      // Trail fade: draw low-alpha background over previous frame
      const bg = parseColor(live.background);
      const fade = 0.5 - (live.trail / 100) * 0.47;
      ctx.globalCompositeOperation = 'source-over';
      ctx.globalAlpha = 1;
      ctx.fillStyle = `rgba(${bg.r},${bg.g},${bg.b},${fade})`;
      ctx.fillRect(0, 0, W, H);

      // Camera pitch
      const a = (live.tilt * Math.PI) / 180;
      const cosA = Math.cos(a);
      const sinA = Math.sin(a);
      const focal = Math.min(W, H) * 0.9;
      const cx = W / 2;
      const cy = H / 2;

      const project = (x, y, z) => {
        const depth = -y * sinA + z * cosA + CAM_DIST;
        if (depth <= 0.05) return null;
        const vUp = y * cosA + z * sinA;
        const persp = focal / depth;
        return {
          sx: cx + x * persp,
          sy: cy - vUp * persp,
          dscale: CAM_DIST / depth,
        };
      };

      // Spawn timer
      acc += dt;
      const interval = 1 / (0.2 + (live.rate / 100) * 3.8);
      let guard = 0;
      while (acc >= interval && guard < 6) {
        acc -= interval;
        if (rockets.length < 35) spawnRocket();
        guard++;
      }

      ctx.globalCompositeOperation = 'lighter';

      // Rockets
      const sizeF = live.size / 100;
      for (let i = rockets.length - 1; i >= 0; i--) {
        const rk = rockets[i];
        rk.vy -= GRAVITY * dt;
        rk.y += rk.vy * dt;
        if (rk.vy <= 0 || rk.y <= 0) {
          burst(rk);
          rockets.splice(i, 1);
          continue;
        }
        const p = project(rk.x, rk.y, rk.z);
        if (p) {
          const s = Math.max(
            1,
            Math.min(6, Math.round(2.4 * sizeF * p.dscale))
          );
          ctx.globalAlpha = 1;
          ctx.fillStyle = `rgb(${rk.r | 0},${rk.g | 0},${rk.b | 0})`;
          ctx.fillRect((p.sx - s / 2) | 0, (p.sy - s / 2) | 0, s, s);
        }
      }

      // Sparks
      const drag = Math.pow(0.5, dt);
      for (let c = 0; c < CAP; c++) {
        let lf = P.life[c];
        if (lf <= 0) continue;
        lf -= dt;
        if (lf <= 0) {
          P.life[c] = 0;
          continue;
        }
        P.life[c] = lf;
        P.vy[c] -= GRAVITY * dt;
        P.vx[c] *= drag;
        P.vy[c] *= drag;
        P.vz[c] *= drag;
        const x = (P.x[c] += P.vx[c] * dt);
        const y = (P.y[c] += P.vy[c] * dt);
        const z = (P.z[c] += P.vz[c] * dt);
        const p = project(x, y, z);
        if (!p) continue;
        const bright = lf / P.max[c];
        ctx.globalAlpha = bright * bright;
        const s = Math.max(
          1,
          Math.min(5, Math.round((0.8 + sizeF) * p.dscale))
        );
        ctx.fillStyle = `rgb(${P.r[c] | 0},${P.g[c] | 0},${P.b[c] | 0})`;
        ctx.fillRect((p.sx - s / 2) | 0, (p.sy - s / 2) | 0, s, s);
      }

      ctx.globalAlpha = 1;
      raf = requestAnimationFrame(render);
    };

    raf = requestAnimationFrame(render);

    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver((entries) => {
        isVisible = entries[0].isIntersecting;
      }, { threshold: 0.05 });
      io.observe(hero);
    }

    let resizeTimer = 0;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(sizeCanvas, 100);
    }, { passive: true });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initFireworks);
  } else {
    initFireworks();
  }
})();
"""

with open('assets/js/fireworks.js', 'w', encoding='utf-8') as f:
    f.write(fireworks_code)

# 2. Update styles.css for full-width collection page layout
with open('assets/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace coll-hero rules
coll_hero_css = """/* ---------- Collection Hero Section (Full Width with Fireworks) ---------- */
.coll-hero {
  position: relative;
  width: 100%;
  overflow: hidden;
  padding-top: clamp(64px, 8vw, 108px);
  padding-bottom: clamp(38px, 4.5vw, 64px);
  background: #05060a;
  border-bottom: 1px solid var(--hairline);
  text-align: center;
}
.coll-hero__fireworks {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
  display: block;
}
.coll-hero .wrap {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 800px;
  margin-inline: auto;
  padding-inline: 20px;
}
.coll-hero .headgroup {
  max-width: 680px;
  margin-inline: auto;
  text-align: center;
  position: relative;
  z-index: 2;
}
.coll-hero .d2 {
  font-family: var(--f-display);
  font-size: clamp(2rem, 3.8vw, 3.2rem);
  font-weight: 400;
  color: #ffffff;
  margin: 0 0 14px;
}
.coll-hero .lead {
  font-size: clamp(13.5px, 1.1vw, 15.5px);
  line-height: 1.55;
  color: var(--night-soft, #cfc9b8);
  max-width: 62ch;
  margin: 0 auto;
}
"""

# Replace in styles.css
css = re.sub(r'/\* ---------- 30\. Collection page ---------- \*/.*?(?=/\* ---------- 31\. Collection Filter Bar ---------- \*/)', '/* ---------- 30. Collection page ---------- */\n' + coll_hero_css + '\n', css, flags=re.DOTALL)

# Update full-width rules for Collection page ONLY
full_width_collection_css = """
/* Full Available Width for Collection Page ONLY */
.coll-filters .wrap,
section[aria-label="All designs"] .wrap {
  max-width: 100% !important;
  width: 100% !important;
  padding-inline: clamp(16px, 2.2vw, 40px) !important;
  margin-inline: 0 !important;
}

.coll-grid {
  display: grid;
  grid-template-columns: repeat(7, minmax(0, 1fr)) !important;
  gap: clamp(8px, 1vw, 16px) !important;
  width: 100% !important;
  padding-block: clamp(18px, 2.5vw, 36px) !important;
}

@media (max-width: 1080px) {
  .coll-grid {
    grid-template-columns: repeat(5, minmax(0, 1fr)) !important;
  }
}

@media (max-width: 820px) {
  .coll-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
  }
}

@media (max-width: 520px) {
  .coll-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    gap: 6px !important;
  }
}
"""

# Replace end of coll-grid section
css = re.sub(r'\.coll-filters \.wrap,\s*section\[aria-label="All designs"\] \.wrap\s*\{.*?(?=\.coll-grid \.plate \{)', full_width_collection_css + '\n', css, flags=re.DOTALL)

with open('assets/css/styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Applied full-width styling for Collection page only and edge-to-edge hero fireworks!")
