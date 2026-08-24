import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

const SITE = resolve('.');
const dataSrc = readFileSync(`${SITE}/assets/js/data.js`, 'utf8');
const ctx = {};
new Function(`${dataSrc}; this.VOLUMES=VOLUMES; this.SPACES=SPACES; this.CATEGORIES=CATEGORIES; this.COLLECTION=COLLECTION;`).call(ctx);
const { VOLUMES, SPACES, CATEGORIES, COLLECTION } = ctx;

const esc = (s) => (s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
const slugOf = (d) => d.img.split('/').pop().replace('.jpg', '');
const volName = (id) => (VOLUMES.find(v => v.id === id) || {}).name || 'Wall Jewels';

const plates = COLLECTION.map((d, i) => {
  const slug = slugOf(d);
  return `          <article class="plate" id="${slug}" data-slug="${slug}" data-vol="${esc(volName(d.v))}" data-code="${esc(d.no)}" data-sub="${esc(d.sub || '')}" data-desc="${esc(d.b || '')}">
            <div class="plate__media">
              <img src="${d.img}" alt="${esc(d.n)} — ${esc(d.no)}" loading="lazy">
              ${d.tag ? `<span class="plate__tag">${esc(d.tag)}</span>` : ''}
            </div>
            <div class="plate__body">
              <p class="plate__vol">${esc(volName(d.v))} · ${esc(d.no)}</p>
              <h3 class="plate__name">${esc(d.n)}</h3>
              ${d.sub ? `<p class="plate__sub" style="font-size:0.82rem; color:var(--c-gold,#c89d5c); margin-top:-2px; margin-bottom:6px;">${esc(d.sub)}</p>` : ''}
              <p class="plate__blurb">${esc(d.b)}</p>
              <div class="plate__row">
                <a class="plate__view" href="https://wa.me/919677042903?text=${encodeURIComponent(`Namaste Wall Jewels — I'd like to enquire about "${d.n}" (${d.no}).`)}" rel="noopener">Enquire</a>
                <span style="display:flex; gap:2px">
                  <button class="wish" type="button" data-slug="${slug}" aria-label="Mark ${esc(d.n)} on your wishlist" aria-pressed="false">
                    <svg viewBox="0 0 22 22" aria-hidden="true"><circle class="ring" cx="11" cy="11" r="7"/><circle class="core" cx="11" cy="11" r="3"/></svg>
                  </button>
                  <button class="wish" type="button" data-add-basket="${slug}" aria-label="Add ${esc(d.n)} to your enquiry docket">
                    <svg viewBox="0 0 22 22" fill="none" aria-hidden="true"><path d="M11 4 V18 M4 11 H18" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
                  </button>
                </span>
              </div>
            </div>
          </article>`;
}).join('\n');

const volChips = VOLUMES.filter(v => !v.soon).map(v =>
  `          <button class="fchip" type="button" data-filter="v:${v.id}" aria-pressed="false"><span class="mark"></span>${v.name}</button>`).join('\n');
const catChips = CATEGORIES.map(c =>
  `          <button class="fchip" type="button" data-filter="c:${c.id}" aria-pressed="false"><span class="mark"></span>${c.label}</button>`).join('\n');
const spaceChips = SPACES.map(s =>
  `          <button class="fchip" type="button" data-filter="s:${s.id}" aria-pressed="false"><span class="mark"></span>${s.label}</button>`).join('\n');

const html = `<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>The Collection — Wall Jewels Wallpaper World · Chennai, Since 1978</title>
  <!-- Favicon & Brand Icons (Embedded Data URI + Multi-Format Fallbacks) -->
  <link rel="icon" type="image/png" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAADxElEQVR4nN1WTYgcRRR+9b2qnh9nMtlNYlwNRoRcPERkRQlR8CJ4iafsTdGgBxG85SYheApegooQEQTBk4oKoqISUNSLsprc/EEUkRU0i9nM7s5MT1f1k9dTHRo17szuzh580FRXvVff+3/dRP8XOk0EXYXI7KReI1HxpgFoa3dFXxaJ3N5O50Aty25zIsmefv9dIspN5E/LALq4f/91s2trt0qe39LK/d21IAcTymeczx9UbEMUNsKwkyrVHKtnv7bbh8zq6tFmlh1uh/AQSLre4G0Cf24oz2VMbExqQHln92Bw5/Vp+mwjzzNLMgDRLm/MbAA+jnJhKgYYoqBRaGXZW4boBBtz8wB8kcjsM8as19P0FyHicfK/bdSr148MrH2tmyTHryUjIhCR7W1RIWJ9ohEHPfCFB85fajRulEqL6jrRfJARMErweGbKfeQXgELkVHZo7SmBETFGhpZfjTy71TlB/2V51cuetUcE8GKMD8D6cqNxoJRbc+6OP2dmOhvhUQnWd+6EBz7sJclC6cnS3FwzZX7BAxeGzK90W6195R1FfGNhgT3wvUZAAOlb+wSJmNS5c7r3wGfjGGB0pmfMPyhQYKR/NJtzyhta+0EBHhV45guXO53dMVVOZVLms8oTY4IHvk6tPV/KZ8zPV528lgFW14G1JwXIBSbXSKjHYgpgCUBfgFTznTKfifdqWherzh0OQBBj9G4hn4+UP1Mq3zACRERX2u09Abis+YweFY8HPrnSbh/ywHcCEwLw2/Ls7K6yOFPnHg1AVtwzJgvAz4MkObah5/8WhZT5uah8tSgs5qUyHSnzixod5afOPaZnA5ucumos1PAiQmcjZo3GpdOjMOH3ZvOGwPyjAgUg7ddq90UwrCfJsUqul4bWflQq90BfuyC+v1edFWOTxFRopfece3jNudvjeQGkLeWBlVGui1qRaOi3K83mvAcWowFfVvE2ZURJlalWGDG09qnC6/hk1r6utVPwgPfVgAz4Rvebnr8yGjT/mGalcT1rj6bA4z1r76mwjQc+jREoe39r03DMCBW5Xm40bvJAV4s0Yz4XeRP/d4xFUamNa6JnqXMvFTMDkF69fm8pR9MkiZNwPUmOh9H3QIbAm1ML/99rRN9XarUHAnityD3zV9opE3+GJ6FqWHvOPaIjV8M+tPadsb58WyGJwIvz8y5j+7IqDsClobVPVmQwzbCbfq12v2f+KQCDjPlMOaanHXboum7tXRnz4tDap7ut1t4Kf7rVXlLZcpX91V+0HSUZzYCdV7yd9BdkGd/XhbBmKgAAAABJRU5ErkJggg==">
  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png?v=20260824d">
  <link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png?v=20260824d">
  <link rel="shortcut icon" type="image/x-icon" href="favicon.ico?v=20260824d">
  <link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png?v=20260824d">
  <link rel="manifest" href="site.webmanifest?v=20260824d">
  <meta name="description" content="Browse the Wall Jewels collections — Kala Parampara and Kala Rasa. ${COLLECTION.length} master plates of authentic heritage, botanical, abstract and world designs, printable to your wall's exact measure.">
  <link rel="canonical" href="https://www.walljewels.in/collection.html">
  <meta name="theme-color" content="#0b0d11">
  <link rel="preload" href="assets/fonts/marcellus-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/jost-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="assets/css/styles.css?v=2026-08-24-exactkp">
</head>
<body>

  <a class="skip" href="#main">Skip to content</a>

  <div class="annbar" role="note" aria-label="House announcements">
    <div class="annbar__track">
      <span><strong>Pioneers of Wallpaper in South India — Since 1978</strong></span>
      <span class="sep">·</span><span>Customisation Available</span>
      <span class="sep">·</span><span>In-House Manufacturing</span>
      <span class="sep">·</span><span>Pan-India Delivery</span>
      <span class="sep">·</span><span>Complete Installation</span>
      <span class="sep" aria-hidden="true">·</span>
      <span aria-hidden="true"><strong>Pioneers of Wallpaper in South India — Since 1978</strong></span>
      <span class="sep" aria-hidden="true">·</span><span aria-hidden="true">Customisation Available</span>
      <span class="sep" aria-hidden="true">·</span><span aria-hidden="true">In-House Manufacturing</span>
      <span class="sep" aria-hidden="true">·</span><span aria-hidden="true">Pan-India Delivery</span>
      <span class="sep" aria-hidden="true">·</span><span aria-hidden="true">Complete Installation</span>
    </div>
  </div>

  <header class="header">
    <div class="header__in">
      <a class="wordmark wordmark--img" href="index.html" aria-label="Wall Jewels Wallpaper World — home">
        <img src="assets/img/brand/logo-light.png" alt="Wall Jewels Wallpaper World">
      </a>
      <nav class="nav" aria-label="Primary">
        <a href="collection.html" aria-current="page">Collection</a>
        <a href="index.html#visualiser">Custom Printing</a>
        <a href="index.html#record">Our Work</a>
        <a href="index.html#why">The House</a>
        <a href="index.html#journal">Journal</a>
        <a href="index.html#visit">Visit</a>
      </nav>
      <a class="btn btn--ghost header__cta" href="index.html#visualiser"><span class="dot-a"></span>Visualise on Wall</a>
    </div>
  </header>

  <main id="main">
    <section class="c-hero">
      <div class="c-hero__in">
        <p class="c-hero__eyebrow"><span class="dot-a"></span> THE COMPLETE CATALOGUE · SINCE 1978</p>
        <h1 class="c-hero__title">The Collection</h1>
        <p class="c-hero__lede">Every plate in our library is manufactured in-house in Chennai and custom-scaled to the exact dimensions of your wall. Select a design to preview, calculate pricing, or enquire directly via WhatsApp.</p>
      </div>
    </section>

    <section class="filters-wrap" aria-label="Filter the collection">
      <div class="filters">
        <div class="filters__group">
          <span class="filters__label">Volume</span>
          <div class="filters__chips">
            <button class="fchip is-active" type="button" data-filter="all" aria-pressed="true"><span class="mark"></span>All Volumes</button>
${volChips}
          </div>
        </div>
        <div class="filters__group">
          <span class="filters__label">Theme</span>
          <div class="filters__chips">
${catChips}
          </div>
        </div>
        <div class="filters__group">
          <span class="filters__label">Space</span>
          <div class="filters__chips">
${spaceChips}
          </div>
        </div>
      </div>
    </section>

    <section class="grid-wrap" aria-label="Wallpaper designs">
      <div class="grid" id="collection-grid">
${plates}
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="footer__in">
      <div class="footer__brand">
        <img src="assets/img/brand/logo-light.png" alt="Wall Jewels" width="180">
        <p>South India's pioneer in luxury wallpapers and in-house bespoke manufacturing since 1978.</p>
      </div>
      <div class="footer__col">
        <h4>Showrooms</h4>
        <ul>
          <li><a href="showrooms/parrys-flagship.html">Parry's Flagship (Park Town)</a></li>
          <li><a href="showrooms/omr-experience-centre.html">OMR Experience Centre</a></li>
          <li><a href="showrooms/tnagar-boutique.html">T. Nagar Boutique</a></li>
        </ul>
      </div>
      <div class="footer__col">
        <h4>Direct Hotline</h4>
        <ul>
          <li><a href="https://wa.me/919677042903">WhatsApp: +91 96770 42903</a></li>
          <li><a href="tel:+919840064205">Phone: +91 98400 64205</a></li>
          <li><a href="mailto:info@walljewels.com">info@walljewels.com</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__bar">
      <p>© 2026 Wall Jewels Wallpaper World Pvt. Ltd. · All Rights Reserved.</p>
    </div>
  </footer>

  <script src="assets/js/data.js?v=2026-08-24-exactkp"></script>
  <script src="assets/js/app.js?v=2026-08-24-exactkp" defer></script>
  <script src="assets/js/webgl-bg.js?v=2026-08-24" defer></script>
</body>
</html>
`;

writeFileSync(`${SITE}/collection.html`, html, 'utf8');
console.log(`collection.html written: ${COLLECTION.length} plates`);
