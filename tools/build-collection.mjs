import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

const SITE = resolve('.');
const dataSrc = readFileSync(`${SITE}/assets/js/data.js`, 'utf8');
const ctx = {};
new Function(`${dataSrc}; this.VOLUMES=VOLUMES; this.SPACES=SPACES; this.CATEGORIES=CATEGORIES; this.COLLECTION=COLLECTION;`).call(ctx);
const { VOLUMES, SPACES, CATEGORIES, COLLECTION } = ctx;

const BUILD_V = `v${Date.now()}`;

const esc = (s) => (s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
const slugOf = (d) => d.img.split('/').pop().replace('.jpg', '');
const volName = (id) => (VOLUMES.find(v => v.id === id) || {}).name || (id === 'kala-rasa' ? 'Kala Rasa' : 'Kala Parampara');

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
              ${d.sub ? `<p class="plate__sub" style="font-size:0.82rem; color:var(--c-gold,#c89d5c); margin-top:-2px; margin-bottom:6px; font-weight:500;">${esc(d.sub)}</p>` : ''}
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
  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png?v=${BUILD_V}">
  <link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png?v=${BUILD_V}">
  <link rel="shortcut icon" type="image/x-icon" href="favicon.ico?v=${BUILD_V}">
  <link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png?v=${BUILD_V}">
  <link rel="manifest" href="site.webmanifest?v=${BUILD_V}">
  <meta name="description" content="Browse the Wall Jewels collections — Kala Parampara and Kala Rasa. ${COLLECTION.length} master plates of authentic heritage, botanical, abstract and world designs, printable to your wall's exact measure.">
  <link rel="canonical" href="https://www.walljewels.in/collection.html">
  <meta name="theme-color" content="#0b0d11">
  <link rel="preload" href="assets/fonts/marcellus-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="assets/fonts/jost-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="assets/css/styles.css?v=${BUILD_V}">
</head>
<body class="page-collection">
<!-- Generated grid: regenerate with tools/build-collection.mjs after editing data.js. World: see index.html contract. -->

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
      <div class="header__tools">
        <button class="tool" type="button" data-open-search aria-label="Search the collection">
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <circle cx="10.5" cy="10.5" r="6.5" stroke="currentColor" stroke-width="1.5"/>
            <path d="M15.5 15.5 L20.5 20.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <circle cx="10.5" cy="10.5" r="1.3" fill="currentColor"/>
          </svg>
        </button>
        <a class="tool" href="collection.html" aria-label="Your wishlist — marked designs">
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <circle cx="12" cy="12" r="7.2" stroke="currentColor" stroke-width="1.5"/>
            <circle cx="12" cy="12" r="2.4" fill="currentColor"/>
            <circle cx="12" cy="2.6" r="1.1" fill="currentColor"/>
            <circle cx="21.4" cy="12" r="1.1" fill="currentColor"/>
            <circle cx="12" cy="21.4" r="1.1" fill="currentColor"/>
            <circle cx="2.6" cy="12" r="1.1" fill="currentColor"/>
          </svg>
          <span class="tool__count" data-count-wish></span>
        </a>
        <button class="tool" type="button" data-open-docket aria-label="Your enquiry docket">
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M6 3.5 H18 V20.5 L15.5 19 L13 20.5 L10.5 19 L8 20.5 L6 19.2 Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
            <path d="M9 8.5 H15 M9 12 H15" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
          </svg>
          <span class="tool__count" data-count-basket></span>
        </button>
        <button class="tool burger" type="button" data-open-drawer aria-label="Open menu">
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M4 7.5 H20 M4 12 H20 M4 16.5 H20" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
        </button>
      </div>
    </div>
  </header>

  <nav class="drawer" aria-label="Menu" inert>
    <div class="drawer__head">
      <a class="wordmark wordmark--img" href="index.html"><img src="assets/img/brand/logo-light.png" alt="Wall Jewels Wallpaper World"></a>
      <button class="tool" type="button" data-close-drawer aria-label="Close menu">
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M6 6 L18 18 M18 6 L6 18" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
      </button>
    </div>
    <div class="drawer__nav">
      <a href="collection.html">Collection <span class="num">${COLLECTION.length} plates</span></a>
      <a href="index.html#visualiser">Custom Printing <span class="num">Your wall</span></a>
      <a href="index.html#record">Our Work <span class="num">Since 1978</span></a>
      <a href="index.html#why">The House</a>
      <a href="index.html#journal">Journal</a>
      <a href="index.html#visit">Visit <span class="num">3 showrooms</span></a>
    </div>
    <div class="drawer__foot">
      <a class="btn btn--wa" href="https://wa.me/919677042903" rel="noopener"><span class="dot-a"></span>WhatsApp the design team</a>
      <p class="small">Parry’s · OMR · T. Nagar — Chennai<br><a href="tel:+919840064205">+91 98400 64205</a> · <a href="mailto:info@walljewels.com">info@walljewels.com</a></p>
    </div>
  </nav>

  <main id="main">
    <section class="coll-hero">
      <canvas class="coll-hero__fireworks" id="coll-fireworks-canvas" aria-hidden="true"></canvas>
      <div class="coll-hero__content">
        <div class="headgroup">
          <h1 class="d2">The collection</h1>
          <p class="lead">${COLLECTION.length} master plates from the Wall Jewels volumes — every one recomposed, recoloured
            and printed to your wall's exact measure. No prices here by design: a wall deserves a conversation,
            and the conversation is free.</p>
        </div>
      </div>
    </section>

    <div class="coll-filters">
      <div class="coll-filters__in">
        <div class="fgroup" role="group" aria-label="Filter by volume">
          <button class="fchip is-active" type="button" data-filter="all" aria-pressed="true"><span class="mark"></span>All Volumes</button>
${volChips}
        </div>
        <div class="fgroup" role="group" aria-label="Filter by category">
${catChips}
        </div>
        <div class="fgroup" role="group" aria-label="Filter by space">
${spaceChips}
        </div>
        <span class="coll-count" data-coll-count>${COLLECTION.length} designs</span>
      </div>
    </div>

    <section class="coll-main-section" aria-label="All designs">
      <div class="coll-grid" id="coll-grid" data-coll-grid>
${plates}
      </div>
      <p class="coll-empty" style="display:none">Nothing answers that combination yet — loosen a filter, or
        <a href="https://wa.me/919677042903" rel="noopener">WhatsApp us</a>; if it exists, we can print it.</p>
    </section>

    <section class="finale" aria-labelledby="coll-cta">
      <div class="finale__kolam" aria-hidden="true"><svg></svg></div>
      <div class="wrap">
        <h2 class="d2" id="coll-cta">Seen something your wall would love?</h2>
        <p class="finale__steps">
          <span>Mark it</span><span class="sep">·</span>
          <span>Add it to your docket</span><span class="sep">·</span>
          <span>Send it with your wall size</span>
        </p>
        <div class="finale__cta">
          <a class="btn btn--wa" href="https://wa.me/919677042903?text=Namaste%20Wall%20Jewels%20%E2%80%94%20I%20have%20been%20browsing%20the%20collection." rel="noopener"><span class="dot-a"></span>WhatsApp our design team</a>
        </div>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="wrap">
      <div class="footer__bottom" style="border-top:0">
        <span>© Wall Jewels Wallpaper World Pvt. Ltd. · Chennai · Since 1978</span>
        <span><a href="index.html">Home</a> · <a href="tel:+919840064205">+91 98400 64205</a> · <a href="mailto:info@walljewels.com">info@walljewels.com</a></span>
      </div>
    </div>
  </footer>

  <div class="docket-scrim"></div>
  <aside class="docket" aria-label="Your enquiry docket" inert>
    <div class="docket__head">
      <div>
        <span class="docket__no">Commission docket</span>
        <h2>Your enquiry</h2>
        <p class="small">Nothing here is an order — it is a conversation, prepared.</p>
      </div>
      <button class="tool" type="button" data-close-docket aria-label="Close the docket">
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 6 L18 18 M18 6 L6 18" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
      </button>
    </div>
    <div class="docket__list" aria-live="polite"></div>
    <div class="docket__fields">
      <div class="dfield"><label for="dk-w">Wall width · ft</label><input id="dk-w" type="number" min="1" max="200" inputmode="decimal" placeholder="12"></div>
      <div class="dfield"><label for="dk-h">Wall height · ft</label><input id="dk-h" type="number" min="1" max="60" inputmode="decimal" placeholder="9"></div>
      <div class="dfield dfield--full"><label for="dk-name">Your name</label><input id="dk-name" type="text" autocomplete="name" placeholder="How shall we address you?"></div>
      <div class="dfield dfield--full"><label for="dk-notes">Notes</label><textarea id="dk-notes" rows="2" placeholder="The room, the light, the deadline — anything that helps."></textarea></div>
    </div>
    <div class="docket__send">
      <button class="btn btn--wa" type="button" data-send-docket><span class="dot-a"></span>Send via WhatsApp</button>
      <p class="small">Or write to <a href="mailto:info@walljewels.com">info@walljewels.com</a> — no enquiry goes unanswered.</p>
    </div>
  </aside>

  <div class="search-veil" inert>
    <div class="search-box" role="search">
      <input type="search" placeholder="Search designs — “pichwai”, “marble”, “kids”…" aria-label="Search the collection">
      <p class="small">Enter at least two letters. Every result is a Wall Jewels plate.</p>
      <div class="search-results"></div>
    </div>
  </div>

  <script src="assets/js/vendor/lenis.min.js?v=${BUILD_V}" defer></script>
  <script src="assets/js/data.js?v=${BUILD_V}" defer></script>
  <script src="assets/js/kolam.js?v=${BUILD_V}" defer></script>
  <script src="assets/js/webgl-bg.js?v=${BUILD_V}" defer></script>
  <script src="assets/js/fireworks.js?v=${BUILD_V}" defer></script>
  <script src="assets/js/app.js?v=${BUILD_V}" defer></script>
</body>
</html>
`;

writeFileSync(`${SITE}/collection.html`, html, 'utf8');
console.log(`collection.html written: ${COLLECTION.length} plates (version: ${BUILD_V})`);
