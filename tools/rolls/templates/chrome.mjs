// Page chrome shared by every generated rolls page: head, announcement bar,
// header (with the Products menu), mobile drawer, footer, enquiry panel, scripts.
// Markup mirrors index.html / luxury-wallpapers.html so the existing app.js and
// styles.css behave identically on the new pages.

import { FAVICON_DATA_URI } from './favicon.mjs';
import { INSTAGRAM_PATH, FACEBOOK_PATH, LINKEDIN_PATH, WHATSAPP_PATH, WHATSAPPFOOTER_PATH } from './icons.mjs';
import { esc, asset, jsonLd, indent, CONTACT, BRAND } from './util.mjs';

const GA_ID = 'G-Y6B7GHF42V';

function socialIcon(cls, href, label, path) {
  return `<a class="${cls}" href="${esc(href)}" target="_blank" rel="noopener" aria-label="${esc(label)}">
  <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="${path}"/></svg>
</a>`;
}

/**
 * <head> for a rolls page.
 * meta: { title, description, canonical (absolute), ogImage (absolute), ogTitle?, ogDescription?, keywords?, ogType?, ldGraph (object|array) }
 */
export function renderHead(root, meta) {
  const og = meta.ogTitle || meta.title;
  const ogDesc = meta.ogDescription || meta.description;
  const ld = Array.isArray(meta.ldGraph)
    ? { '@context': 'https://schema.org', '@graph': meta.ldGraph }
    : meta.ldGraph;
  const keywords = meta.keywords ? `  <meta name="keywords" content="${esc(meta.keywords)}">\n` : '';
  return `<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=${GA_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', '${GA_ID}');
  </script>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>${esc(meta.title)}</title>
  <!-- Favicon & Brand Icons (Embedded Data URI + Multi-Format Fallbacks) -->
  <link rel="icon" type="image/png" href="${FAVICON_DATA_URI}">
  <link rel="icon" type="image/png" sizes="32x32" href="${asset(root, 'favicon-32x32.png')}">
  <link rel="icon" type="image/png" sizes="16x16" href="${asset(root, 'favicon-16x16.png')}">
  <link rel="shortcut icon" type="image/x-icon" href="${asset(root, 'favicon.ico')}">
  <link rel="apple-touch-icon" sizes="180x180" href="${asset(root, 'apple-touch-icon.png')}">
  <link rel="manifest" href="${asset(root, 'site.webmanifest')}">
  <meta name="description" content="${esc(meta.description)}">
${keywords}  <meta name="author" content="Wall Jewels Wallpaper World Pvt. Ltd.">
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <link rel="canonical" href="${esc(meta.canonical)}">
  <link rel="alternate" hreflang="en-IN" href="${esc(meta.canonical)}">
  <link rel="alternate" hreflang="x-default" href="${esc(meta.canonical)}">

  <meta property="og:site_name" content="${BRAND}">
  <meta property="og:type" content="${esc(meta.ogType || 'website')}">
  <meta property="og:url" content="${esc(meta.canonical)}">
  <meta property="og:title" content="${esc(og)}">
  <meta property="og:description" content="${esc(ogDesc)}">
  <meta property="og:image" content="${esc(meta.ogImage)}">
  <meta property="og:locale" content="en_IN">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="${esc(og)}">
  <meta name="twitter:description" content="${esc(ogDesc)}">
  <meta name="twitter:image" content="${esc(meta.ogImage)}">

  <meta name="theme-color" content="#0b0d11">
  <link rel="preload" href="${root}assets/fonts/marcellus-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="${root}assets/fonts/jost-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="${asset(root, 'assets/css/styles.css')}">
  <link rel="stylesheet" href="${asset(root, 'assets/css/rolls.css')}">

  <script type="application/ld+json">
${indent(jsonLd(ld), 2)}
  </script>
</head>`;
}

const ANN_ITEMS = [
  ['strong', 'Wallpaper Rolls'],
  ['span', 'Catalogues, designs &amp; roll calculator'],
  ['span', 'Wall Jewels Wallpaper World'],
  ['span', 'Since 1978'],
];

/** The marquee track is duplicated (second copy aria-hidden) because the CSS animation slides by 50%. */
export function renderAnnbar() {
  const run = (hidden) => ANN_ITEMS.map(([tag, text], i) => {
    const sep = i === 0 ? '' : `<span class="sep"${hidden}>·</span>`;
    const item = tag === 'strong' ? `<span${hidden}><strong>${text}</strong></span>` : `<span${hidden}>${text}</span>`;
    return `      ${sep}${item}`;
  }).join('\n');
  return `  <div class="annbar" role="note" aria-label="House announcements">
    <div class="annbar__track">
${run('')}
      <span class="sep" aria-hidden="true">·</span>
${run(' aria-hidden="true"')}
    </div>
  </div>`;
}

function themeToggle() {
  const parts = '<span class="theme__icon-part"></span>'.repeat(9);
  return `      <div class="theme" title="Toggle Light / Dark mode">
        <label class="theme__label" for="theme-toggle" aria-label="Toggle light and dark mode">
          <span class="theme__toggle-wrap">
            <input class="theme__toggle" type="checkbox" id="theme-toggle" role="switch" name="theme" checked>
            <span class="theme__icon">
              ${parts}
            </span>
          </span>
        </label>
      </div>`;
}

/** Primary nav links used in both the header and the drawer. */
function navLinks(root) {
  return {
    collection: `${root}collection.html`,
    rolls: `${root}wallpaper-rolls/`,
    custom: `${root}custom-wallpaper-printing.html`,
    luxury: `${root}luxury-wallpapers.html`,
    about: `${root}index.html#why`,
    visit: `${root}index.html#visit`,
  };
}

const HEADER_WA_TEXT = 'Namaste Wall Jewels — I’d like to consult the design team.';
const FOOTER_WA_TEXT = 'Namaste Wall Jewels — I’d like to connect.';

export function renderHeader(root) {
  const l = navLinks(root);
  const wa = `https://wa.me/${CONTACT.whatsapp}?text=${encodeURIComponent(HEADER_WA_TEXT)}`;
  return `  <header class="header">
    <div class="header__in">
${themeToggle()}
      <div class="header__center">
        <a class="wordmark wordmark--img" href="${root}index.html" aria-label="Wall Jewels Wallpaper World — home">
          <img src="${root}assets/img/brand/logo-dark.png" alt="Wall Jewels Wallpaper World">
        </a>
        <nav class="nav" aria-label="Primary">
          <a href="${l.collection}">Collection</a>
          <div class="nav__menu" data-nav-menu>
            <button class="nav__trigger" type="button" aria-haspopup="true" aria-expanded="false" aria-controls="nav-products">Products <svg class="nav__chev" width="10" height="10" viewBox="0 0 10 10" aria-hidden="true"><path d="M2 3.5 L5 6.5 L8 3.5" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg></button>
            <div class="nav__panel" id="nav-products">
              <a href="${l.rolls}" aria-current="page">Wallpaper Rolls <span class="nav__hint">Catalogues · designs · roll calculator</span></a>
            </div>
          </div>
          <a href="${l.custom}">Custom Printing</a>
          <a href="${l.luxury}">Luxury Wallpapers</a>
          <a href="${l.about}">About Us</a>
          <a href="${l.visit}">Visit</a>
        </nav>
      </div>
      <div class="header__tools">
        <div class="header__socials" aria-label="Social links">
${indent(socialIcon('nav-social nav-social--ig', 'https://www.instagram.com/walljewelswallpaperworld/', 'Follow Wall Jewels on Instagram', INSTAGRAM_PATH), 10)}
${indent(socialIcon('nav-social nav-social--fb', 'https://www.facebook.com/walljewelswallpaper/', 'Follow Wall Jewels on Facebook', FACEBOOK_PATH), 10)}
${indent(socialIcon('nav-social nav-social--li', 'https://www.linkedin.com/company/wall-jewels-wallpaper-world---india/', 'Follow Wall Jewels on LinkedIn', LINKEDIN_PATH), 10)}
${indent(socialIcon('nav-social nav-social--wa', wa, 'Chat on WhatsApp with Design Team', WHATSAPP_PATH), 10)}
        </div>
        <button class="tool burger" type="button" data-open-drawer aria-label="Open menu">
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M4 7.5 H20 M4 12 H20 M4 16.5 H20" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
          </svg>
        </button>
      </div>
    </div>
  </header>`;
}

export function renderDrawer(root, collectionCount) {
  const l = navLinks(root);
  const count = `${collectionCount} ${collectionCount === 1 ? 'collection' : 'collections'}`;
  return `  <nav class="drawer" aria-label="Menu" inert>
    <div class="drawer__head">
      <a class="wordmark wordmark--img" href="${root}index.html"><img src="${root}assets/img/brand/logo-dark.png" alt="Wall Jewels Wallpaper World"></a>
      <button class="tool" type="button" data-close-drawer aria-label="Close menu">
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M6 6 L18 18 M18 6 L6 18" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
        </svg>
      </button>
    </div>
    <div class="drawer__nav">
      <a href="${l.collection}">Collection <span class="num">70+ designs</span></a>
      <span class="drawer__group">Products</span>
      <a href="${l.rolls}" aria-current="page">Wallpaper Rolls <span class="num">${esc(count)}</span></a>
      <a href="${l.custom}">Custom Printing <span class="num">Your wall</span></a>
      <a href="${l.luxury}">Luxury Wallpapers</a>
      <a href="${l.about}">About Us</a>
      <a href="${l.visit}">Visit <span class="num">3 showrooms</span></a>
    </div>
    <div class="drawer__foot">
      <a class="btn btn--wa" href="https://wa.me/${CONTACT.whatsapp}" rel="noopener"><span class="dot-a"></span>WhatsApp the design team</a>
      <p class="small">Parry’s · OMR · T. Nagar — Chennai<br><a href="${CONTACT.phoneHref}">${CONTACT.phone}</a> · <a href="mailto:${CONTACT.email}">${CONTACT.email}</a></p>
    </div>
  </nav>`;
}

export function renderFooter(root) {
  const wa = `https://wa.me/${CONTACT.whatsapp}?text=${encodeURIComponent(FOOTER_WA_TEXT)}`;
  const li = (href, text) => `              <li><a href="${root}${href}">${text}</a></li>`;
  return `  <footer class="footer">
    <div class="wrap">
      <div class="footer__main">
        <div class="footer__brand">
          <a class="wordmark wordmark--img" href="${root}index.html"><img src="${root}assets/img/brand/logo-dark.png" alt="Wall Jewels Wallpaper World"></a>
          <p>Pioneers of wallpaper in South India since 1978. Premium wallpapers, customised murals, in-house manufacturing and complete installation — from three showrooms in Chennai to walls across India.</p>
        </div>

        <div class="footer__links">
          <nav class="fcol" aria-label="Shop">
            <span class="cap">Shop &amp; Murals</span>
            <ul>
${li('collection.html', 'All Wallpapers')}
${li('wallpaper-rolls/', 'Wallpaper Rolls')}
${li('custom-wallpaper-printing.html', 'Custom Printing')}
${li('luxury-wallpapers.html', 'Luxury Wallpapers')}
${li('wall-murals.html', 'Custom Wall Murals')}
${li('collection.html?c=kids', 'Kids &amp; Nursery')}
            </ul>
          </nav>
          <nav class="fcol" aria-label="Collections">
            <span class="cap">Collections</span>
            <ul>
${li('collection.html', 'Kala Parampara · I')}
${li('collection.html', 'Kala Rasa · II')}
${li('collection.html', 'Vishwa Darshan · III')}
${li('index.html#collections', 'Prakriti · IV')}
${li('wallpaper-manufacturer-india.html', 'Factory Manufacturing')}
            </ul>
          </nav>
          <nav class="fcol" aria-label="Guides">
            <span class="cap">Guides &amp; Authority</span>
            <ul>
${li('wallpaper-chennai.html', 'Wallpaper Chennai')}
${li('wallpaper-buying-guide.html', 'Wallpaper Buying Guide')}
${li('wallpaper-installation.html', '4-Hour Installation')}
${li('collection.html?s=living', 'Living Room Murals')}
${li('collection.html?s=temple', 'Temple &amp; Pooja Walls')}
            </ul>
          </nav>
          <nav class="fcol" aria-label="About Us">
            <span class="cap">About Us</span>
            <ul>
${li('index.html#why', 'About Wall Jewels (1978)')}
${li('index.html#record', 'Our Landmark Work')}
${li('showrooms/parrys-flagship.html', 'Parry’s Flagship')}
${li('showrooms/omr-experience-centre.html', 'OMR Experience Centre')}
${li('showrooms/tnagar-boutique.html', 'T. Nagar Boutique')}
            </ul>
          </nav>
        </div>

        <div class="footer__connect">
          <span class="cap">Follow Us</span>
          <div class="footer__social">
${indent(socialIcon('social-icon social-icon--ig', 'https://www.instagram.com/walljewelswallpaperworld/', 'Wall Jewels on Instagram', INSTAGRAM_PATH), 12)}
${indent(socialIcon('social-icon social-icon--fb', 'https://www.facebook.com/walljewelswallpaper/', 'Wall Jewels on Facebook', FACEBOOK_PATH), 12)}
${indent(socialIcon('social-icon social-icon--li', 'https://www.linkedin.com/company/wall-jewels-wallpaper-world---india/', 'Wall Jewels on LinkedIn', LINKEDIN_PATH), 12)}
${indent(socialIcon('social-icon social-icon--wa', wa, 'Wall Jewels on WhatsApp', WHATSAPPFOOTER_PATH), 12)}
          </div>
        </div>
      </div>
      <div class="footer__bottom">
        <span>© Wall Jewels Wallpaper World Pvt. Ltd. · Chennai · Since 1978</span>
        <span><a href="${CONTACT.phoneHref}">${CONTACT.phone}</a> · <a href="mailto:${CONTACT.email}">${CONTACT.email}</a></span>
      </div>
    </div>
  </footer>`;
}

/**
 * Enquiry panel (SPEC §4.5). One per page; the runtime fills the summary and
 * composes the WhatsApp / mailto message. Fields are real inputs so the panel
 * is usable the moment it opens.
 */
export function renderEnquiryPanel(heading) {
  const field = (id, label, input, full) =>
    `      <div class="dfield${full ? ' dfield--full' : ''}"><label for="${id}">${label}</label>${input}</div>`;
  const mailSubject = encodeURIComponent('Wallpaper Rolls enquiry');
  return `  <div class="rolls-enquiry-scrim"></div>
  <aside class="rolls-enquiry" aria-label="Wallpaper rolls enquiry" inert>
    <div class="rolls-enquiry__head">
      <div>
        <span class="cap">Wallpaper rolls enquiry</span>
        <h2>${esc(heading)}</h2>
      </div>
      <button class="tool" type="button" data-rolls-enquiry-close aria-label="Close the enquiry panel">
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M6 6 L18 18 M18 6 L6 18" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
        </svg>
      </button>
    </div>
    <div class="rolls-enquiry__summary" aria-live="polite"></div>
    <form class="rolls-enquiry__fields" novalidate>
${field('re-name', 'Name <span aria-hidden="true">*</span>', '<input id="re-name" type="text" autocomplete="name" required aria-required="true" placeholder="How shall we address you?">', true)}
${field('re-phone', 'Phone Number <span aria-hidden="true">*</span>', '<input id="re-phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="+91 …">')}
${field('re-email', 'Email', '<input id="re-email" type="email" inputmode="email" autocomplete="email" placeholder="you@example.com">')}
${field('re-w', 'Wall Width · inches', '<input id="re-w" type="number" inputmode="decimal" min="1" max="2400" step="any" placeholder="120">')}
${field('re-h', 'Wall Height · inches', '<input id="re-h" type="number" inputmode="decimal" min="1" max="2400" step="any" placeholder="108">')}
${field('re-msg', 'Message', '<textarea id="re-msg" rows="3" placeholder="The room, the light, the deadline — anything that helps."></textarea>', true)}
      <p class="small rolls-enquiry__hint">Name and a phone number or email are needed so the team can reply.</p>
    </form>
    <div class="rolls-enquiry__send">
      <button class="btn btn--wa" type="button" data-rolls-enquiry-send><span class="dot-a"></span>Send via WhatsApp</button>
      <a class="btn btn--ghost" href="mailto:${CONTACT.email}?subject=${mailSubject}" data-rolls-enquiry-mail><span class="dot-a"></span>Send by Email</a>
      <p class="small">Or call <a href="${CONTACT.phoneHref}">${CONTACT.phone}</a> · Nothing here is an order — final roll count and price are confirmed by the Wall Jewels team.</p>
    </div>
  </aside>`;
}

export function renderScripts(root) {
  const files = [
    'assets/js/vendor/lenis.min.js',
    'assets/js/data.js',
    'assets/js/webgl-bg.js',
    'assets/js/app.js',
    'assets/js/rolls-data.js',
    'assets/js/rolls.js',
  ];
  return files.map((f) => `  <script src="${asset(root, f)}" defer></script>`).join('\n');
}

/**
 * Full document. page = { root, meta, main (HTML string), enquiryHeading, collectionCount }
 */
export function renderDocument(page) {
  const { root } = page;
  return `<!DOCTYPE html>
<html lang="en" class="no-js" data-root="${root}">
${renderHead(root, page.meta)}
<body class="page-rolls">
  <a class="skip" href="#main">Skip to content</a>

${renderAnnbar()}

${renderHeader(root)}

${renderDrawer(root, page.collectionCount)}

  <main id="main">
${page.main}
  </main>

${renderFooter(root)}

${renderEnquiryPanel(page.enquiryHeading || 'Request a quote')}

${renderScripts(root)}
</body>
</html>
`;
}
