// Reusable fragments shared by the rolls page templates.
// Every hook the runtime reads (data-* attributes, class names) is defined in SPEC §4.

import { esc, formatINR, formatNumber, specStrings, waLink, CONTACT } from './util.mjs';

/** Thin-line star used by the existing secondary pages as the eyebrow glyph. */
export const PILL_STAR_SVG = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>';

export const CHEVRON_SVG = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
export const CHEVRON_BACK_SVG = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>';

export const DISCLAIMER_LINE_1 = 'Roll requirements are calculated based on approximate coverage and may vary depending on wall dimensions, pattern repeat, design alignment, cutting, wastage and installation requirements.';
export const DISCLAIMER_LINE_2 = 'Final roll requirement will be confirmed by the Wall Jewels team before order confirmation.';

export function threshold() {
  return '<div class="threshold" data-kolam="gate"><span class="rule"></span></div>';
}

export function eyebrow(text) {
  return `<div class="coverflow-pill rv">${PILL_STAR_SVG}<span>${esc(text)}</span></div>`;
}

/**
 * Breadcrumb trail. items = [{ label, href }] — the last item is the current page (no link).
 */
export function breadcrumbs(items) {
  const parts = items.map((it, i) => {
    const last = i === items.length - 1;
    const body = last
      ? `<span aria-current="page">${esc(it.label)}</span>`
      : `<a href="${esc(it.href)}">${esc(it.label)}</a>`;
    return `    <li>${body}</li>`;
  });
  return `<nav class="rolls-crumbs" aria-label="Breadcrumb">
  <ol>
${parts.join('\n')}
  </ol>
</nav>`;
}

/** Gallery card — the exact markup from SPEC §4.1.3 (also produced by the runtime). */
export function designCard(root, design, collection, extraClass = '') {
  const alt = `${collection.name} wallpaper design ${design.designNumber}`;
  const thumb = `${root}${design.thumbnail}`;
  const srcset = design.web ? ` srcset="${esc(thumb)} 480w, ${esc(`${root}${design.web}`)} 1200w"` : '';
  const dims = (design.width && design.height) ? ` width="${esc(design.width)}" height="${esc(design.height)}"` : '';
  const cls = extraClass ? `rolls-card ${extraClass}` : 'rolls-card';
  return `<a class="${cls}" href="${esc(`${root}${design.url}`)}" data-design-id="${esc(design.id)}" data-no-lightbox>
  <span class="rolls-card__media"><img src="${esc(thumb)}"${srcset} sizes="(max-width: 600px) 50vw, (max-width: 1100px) 33vw, 25vw"${dims} alt="${esc(alt)}" loading="lazy" decoding="async"></span>
  <span class="rolls-card__body"><span class="rolls-card__no">Design No. ${esc(design.designNumber)}</span><span class="rolls-card__coll">${esc(collection.name)}</span></span>
</a>`;
}

/** Collection card on the landing page (SPEC §4.1.2). */
export function collectionCard(root, collection, designCount, index) {
  const s = specStrings(collection);
  const href = `${root}wallpaper-rolls/${collection.slug}/`;
  const count = `${designCount} ${designCount === 1 ? 'design' : 'designs'}`;
  return `<article class="rolls-collection rv" style="--i:${index}" data-collection-card="${esc(collection.slug)}" data-no-lightbox>
  <a class="rolls-collection__media" href="${esc(href)}" aria-label="${esc(`Explore ${collection.name} designs`)}">
    <img src="${esc(`${root}${collection.coverImage}`)}" alt="${esc(`${collection.name} wallpaper collection`)}" width="1200" height="1200" loading="lazy" decoding="async">
  </a>
  <div class="rolls-collection__body">
    <span class="cap">${esc(count)} · ${esc(collection.pageCount || '')} catalogue pages</span>
    <h3>${esc(collection.name)}</h3>
    <p class="rolls-collection__tagline">${esc(collection.tagline || '')}</p>
    <ul class="rolls-specs">
      <li><span>${esc(s.roll)} / Roll</span></li>
      <li><span>Approx. ${esc(s.coverage)} Wall Coverage</span></li>
      <li><span>${esc(s.price)} / Roll</span></li>
    </ul>
    <div class="rolls-collection__actions">
      <a class="btn btn--fill" href="${esc(href)}"><span class="dot-a"></span>Explore Designs</a>
      <button class="btn" type="button" data-open-rolls-catalogue="${esc(collection.slug)}"><span class="dot-a"></span>View Catalogue</button>
      <a class="btn" href="#calculator" data-calc-collection="${esc(collection.slug)}"><span class="dot-a"></span>Calculate Requirement</a>
      <noscript><a class="textlink" href="${esc(`${root}${collection.catalogueFile}`)}" target="_blank" rel="noopener">Open the catalogue PDF ${CHEVRON_SVG}</a></noscript>
    </div>
  </div>
</article>`;
}

/**
 * Design library: toolbar + gallery (SPEC §4.1.3 / §4.2).
 * opts = { root, collections, activeSlug ('all' | slug), cards: [{design, collection}], totalCount, staticLimit, heading }
 */
export function gallerySection(opts) {
  const { root, collections, activeSlug, cards, totalCount, staticLimit } = opts;
  const shown = cards.slice(0, staticLimit);
  const hasMore = cards.length > shown.length;
  const chip = (slug, label, active) =>
    `        <button class="fchip${active ? ' is-active' : ''}" type="button" data-rolls-filter="${esc(slug)}" aria-pressed="${active ? 'true' : 'false'}"><span class="mark" aria-hidden="true"></span>${esc(label)}</button>`;
  const chips = [chip('all', 'All', activeSlug === 'all')]
    .concat(collections.map((c) => chip(c.slug, c.name, activeSlug === c.slug)))
    .join('\n');
  const countLabel = `${totalCount} ${totalCount === 1 ? 'design' : 'designs'}`;
  const cardHtml = shown.map(({ design, collection }) => indentBlock(designCard(root, design, collection), 6)).join('\n');
  const more = hasMore
    ? `\n    <div class="rolls-more-wrap">
      <button class="btn rolls-more" type="button" data-rolls-more><span class="dot-a"></span>Show More Designs</button>
      <noscript><p class="small">Showing the first ${shown.length} of ${totalCount} designs. Open a collection page to browse every design without JavaScript.</p></noscript>
    </div>`
    : '';
  return `<section class="section rolls-library" id="designs">
  <div class="wrap">
    ${threshold()}
    <div class="headgroup">
      <span class="cap cap--gold rv">Design library</span>
      <h2 class="d2 rv" style="--i:1">${esc(opts.heading || 'Browse Individual Designs')}</h2>
      <p class="lead rv" style="--i:2">Search by the design number printed in the catalogue, or filter by collection. Every design opens on its own page with roll size, coverage and price.</p>
    </div>
    <div class="rolls-toolbar">
      <div class="dfield rolls-search">
        <label for="rolls-search">Search by Design Number</label>
        <input id="rolls-search" type="search" data-rolls-search placeholder="e.g. 12 or 14156" autocomplete="off" autocorrect="off" spellcheck="false" enterkeyhint="search">
      </div>
      <div class="rolls-filters" role="group" aria-label="Filter by collection">
${chips}
      </div>
      <p class="rolls-count" data-rolls-count aria-live="polite">${esc(countLabel)}</p>
    </div>
    <div class="rolls-gallery" data-rolls-gallery data-collection="${esc(activeSlug)}">
${cardHtml}
    </div>${more}
  </div>
</section>`;
}

/** Calculator mount (SPEC §4.4). The runtime renders the form into it. */
export function calculatorMount(opts = {}) {
  const attrs = ['data-rolls-calc'];
  if (opts.collection) attrs.push(`data-collection="${esc(opts.collection)}"`);
  if (opts.design) attrs.push(`data-design="${esc(opts.design)}"`);
  if (opts.lock) attrs.push('data-lock-collection');
  return `<div class="rolls-calc" ${attrs.join(' ')}>
  <noscript><p class="small">Enable JavaScript to use the roll calculator, or WhatsApp us your wall size.</p></noscript>
</div>`;
}

/** The two disclaimer sentences (SPEC §4.1.5), under every calculator. */
export function disclaimer() {
  return `<div class="rolls-disclaimer">
  <span class="cap">Approximate calculation</span>
  <p class="small">${DISCLAIMER_LINE_1}</p>
  <p class="small">${DISCLAIMER_LINE_2}</p>
</div>`;
}

/**
 * Calculator section wrapper: heading + mount + disclaimer.
 * opts = { id, heading, intro?, collection?, design?, lock?, facts? }
 */
export function calculatorSection(opts) {
  const intro = opts.intro
    ? `\n      <p class="lead rv" style="--i:2">${esc(opts.intro)}</p>`
    : '';
  const facts = opts.facts ? `\n    ${opts.facts}` : '';
  return `<section class="section rolls-calculator" id="${esc(opts.id || 'calculator')}">
  <div class="wrap">
    ${threshold()}
    <div class="headgroup">
      <span class="cap cap--gold rv">Roll calculator</span>
      <h2 class="d2 rv" style="--i:1">${esc(opts.heading)}</h2>${intro}
    </div>${facts}
    ${indentBlock(calculatorMount(opts), 4).trimStart()}
    ${indentBlock(disclaimer(), 4).trimStart()}
  </div>
</section>`;
}

/** Closing CTA band (SPEC §4.1.7). */
export function ctaBand(opts = {}) {
  const text = opts.waText || "Namaste Wall Jewels — I'd like help choosing wallpaper rolls.";
  const calcLabel = opts.calcLabel || 'Calculate Rolls';
  return `<section class="section section--tight rolls-cta">
  <div class="wrap">
    <div class="headgroup">
      <span class="cap cap--gold rv">Talk to the house</span>
      <h2 class="d3 rv" style="--i:1">${esc(opts.heading || 'Unsure which roll or how many? Ask us.')}</h2>
      <p class="lead rv" style="--i:2">${esc(opts.lead || 'Send a photo of your wall and the design number you like. The team replies with a confirmed roll count and quote.')}</p>
      <div class="rolls-cta__actions rv" style="--i:3">
        <a class="btn btn--wa" href="${esc(waLink(text))}" target="_blank" rel="noopener"><span class="dot-a"></span>WhatsApp the design team</a>
        <a class="btn" href="#calculator"><span class="dot-a"></span>${esc(calcLabel)}</a>
      </div>
      <p class="small rv" style="--i:4">Or call <a href="${CONTACT.phoneHref}">${CONTACT.phone}</a> · <a href="mailto:${CONTACT.email}">${CONTACT.email}</a></p>
    </div>
  </div>
</section>`;
}

/** Live facts line for a collection, as text (the runtime shows the same under the calculator select). */
export function factsLine(collection) {
  const s = specStrings(collection);
  return `${s.roll} roll · approx. ${s.coverage} coverage · ${s.price} per roll · ${formatINR(collection.pricePerSqFt)} per ${s.unit}`;
}

export function priceLabel(collection) {
  return `${formatINR(collection.rollPrice)} per roll`;
}

export function coverageLabel(collection) {
  return `${formatNumber(collection.coverage)} ${collection.unit || 'sq.ft'}`;
}

/** Local indent helper that keeps blank lines blank. */
export function indentBlock(block, n) {
  const pad = ' '.repeat(n);
  return String(block)
    .split('\n')
    .map((line) => (line.trim() ? pad + line : ''))
    .join('\n');
}
