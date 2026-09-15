// The four page types (SPEC §4.1–§4.4). Each builder returns { path, html }.
// `model` = { collections (published, sorted), designs (sorted, with url), byCollection: Map<slug, design[]> }

import { renderDocument } from './chrome.mjs';
import {
  esc, formatINR, formatNumber, specStrings, absUrl, rootFor, waLink, BRAND, BRAND_LINE, CONTACT,
} from './util.mjs';
import {
  threshold, eyebrow, breadcrumbs, designCard, collectionCard, gallerySection, calculatorSection,
  ctaBand, indentBlock, CHEVRON_SVG, CHEVRON_BACK_SVG,
} from './partials.mjs';

const LANDING_STATIC_CARDS = 48;
const COLLECTION_STATIC_CARDS = 120;
const STRIP_SIZE = 8;

const ROLLS_URL = 'wallpaper-rolls/';

function brandLd() {
  return { '@type': 'Brand', name: BRAND };
}

function breadcrumbLd(id, items) {
  return {
    '@type': 'BreadcrumbList',
    '@id': `${id}#breadcrumb`,
    itemListElement: items.map((it, i) => ({
      '@type': 'ListItem', position: i + 1, name: it.name, item: it.url,
    })),
  };
}

function offerLd(collection, url) {
  return {
    '@type': 'Offer',
    price: collection.rollPrice,
    priceCurrency: collection.currency || 'INR',
    availability: 'https://schema.org/InStock',
    itemCondition: 'https://schema.org/NewCondition',
    url,
    seller: { '@type': 'Organization', name: BRAND },
  };
}

function collectionUrl(collection) {
  return `${ROLLS_URL}${collection.slug}/`;
}

function designProductLd(design, collection) {
  const url = absUrl(design.url);
  return {
    '@type': 'Product',
    '@id': `${url}#product`,
    name: `${collection.name} Wallpaper Roll — Design ${design.designNumber}`,
    sku: design.designNumber,
    image: absUrl(design.web || design.image),
    description: `${collection.name} wallpaper roll, design number ${design.designNumber}. ${formatNumber(collection.rollSize)} ${collection.unit || 'sq.ft'} roll, approx. ${formatNumber(collection.coverage)} ${collection.unit || 'sq.ft'} wall coverage.`,
    brand: brandLd(),
    category: 'Wallpaper rolls',
    url,
    offers: offerLd(collection, url),
  };
}

/* ---------------------------------------------------------------- landing */

export function buildLanding(model) {
  const root = rootFor([]);
  const canonical = absUrl(ROLLS_URL);
  const { collections } = model;
  const allCards = model.designs.map((d) => ({ design: d, collection: model.collectionById.get(d.collectionId) }));
  const ogImage = collections[0] ? absUrl(collections[0].coverImage) : absUrl('assets/img/collection/pichwai-eternal-melody.jpg');

  const collectionCards = collections
    .map((c, i) => indentBlock(collectionCard(root, c, (model.byCollection.get(c.slug) || []).length, i), 6))
    .join('\n');

  const hero = `<section class="section rolls-hero">
  <div class="wrap">
    ${threshold()}
    <div class="headgroup">
      ${eyebrow(`${BRAND} · ${BRAND_LINE}`)}
      <h1 class="d1 rv">Wallpaper Rolls</h1>
      <p class="lead rv" style="--i:1">Explore Our Wallpaper Collections</p>
      <p class="rolls-hero__quote rv" style="--i:2">Discover curated wallpaper collections, browse individual designs, view complete catalogues and calculate the approximate rolls required for your walls.</p>
      <div class="rolls-hero__actions rv" style="--i:3">
        <a class="btn btn--fill" href="#collections"><span class="dot-a"></span>Explore Collections</a>
        <a class="btn" href="#calculator"><span class="dot-a"></span>Calculate Rolls</a>
      </div>
    </div>
  </div>
</section>`;

  const collectionsSection = `<section class="section" id="collections">
  <div class="wrap">
    ${threshold()}
    <div class="headgroup">
      <span class="cap cap--gold rv">The books</span>
      <h2 class="d2 rv" style="--i:1">Our Collections</h2>
      <p class="lead rv" style="--i:2">Each collection is a physical catalogue in our showrooms. Roll size, approximate coverage and price are stated for every design.</p>
    </div>
    <div class="rolls-collections">
${collectionCards}
    </div>
  </div>
</section>`;

  const library = gallerySection({
    root,
    collections,
    activeSlug: 'all',
    cards: allCards,
    totalCount: allCards.length,
    staticLimit: LANDING_STATIC_CARDS,
    heading: 'Browse Individual Designs',
  });

  const calculator = calculatorSection({
    id: 'calculator',
    heading: 'Calculate How Many Rolls You Need',
    intro: 'Enter your wall width and height in inches, choose a collection, and see the approximate rolls and wallpaper cost.',
  });

  const showrooms = `<a href="${root}showrooms/parrys-flagship.html">Parry’s flagship</a>, the <a href="${root}showrooms/omr-experience-centre.html">OMR experience centre</a> and the <a href="${root}showrooms/tnagar-boutique.html">T. Nagar boutique</a>`;
  const seo = `<section class="section rolls-seo">
  <div class="wrap">
    ${threshold()}
    <div class="rolls-seo__prose prose">
      <h2 class="d3 rv">Wallpaper Rolls in Chennai, from South India's Pioneers</h2>
      <p class="rv" style="--i:1">Wall Jewels wallpaper rolls are chosen the way we have chosen wallpaper since 1978 — by handling the book. Every wallpaper collection on this page is a physical wallpaper catalogue in our showrooms, and the wallpaper roll price is stated plainly, per roll and per square foot, so a designer wallpaper or an imported wallpaper for home can be costed before you visit. Browse each catalogue page by page, open any design on its own page, and use the wallpaper calculator to see approximately how many rolls a wall will need.</p>
      <p class="rv" style="--i:2">Rolls are stocked and sold from our three Chennai showrooms — the ${showrooms} — and delivered across India. For wallpaper in Chennai, a roll from these collections is the quickest route to a finished wall. When a wall calls for an artwork printed to its exact measure, that is our <a href="${root}custom-wallpaper-printing.html">customised printed wallpaper</a> service, quoted separately from Wall Jewels wallpaper rolls.</p>
    </div>
  </div>
</section>`;

  const main = [hero, collectionsSection, library, calculator, seo, ctaBand()]
    .map((s) => indentBlock(s, 4))
    .join('\n\n');

  const ldGraph = [
    {
      '@type': 'WebPage',
      '@id': `${canonical}#page`,
      name: 'Wallpaper Rolls & Collections',
      description: 'Explore Wall Jewels Wallpaper World wallpaper roll collections, browse catalogues and designs, and calculate the approximate rolls required for your walls.',
      url: canonical,
      inLanguage: 'en-IN',
      isPartOf: { '@type': 'WebSite', name: BRAND, url: absUrl('') },
    },
    breadcrumbLd(canonical, [
      { name: 'Home', url: absUrl('') },
      { name: 'Wallpaper Rolls', url: canonical },
    ]),
    {
      '@type': 'ItemList',
      '@id': `${canonical}#collections`,
      name: 'Wallpaper roll collections',
      numberOfItems: collections.length,
      itemListElement: collections.map((c, i) => ({
        '@type': 'ListItem',
        position: i + 1,
        item: {
          '@type': 'Product',
          name: `${c.name} Wallpaper Rolls`,
          description: c.description || c.tagline || '',
          url: absUrl(collectionUrl(c)),
          image: absUrl(c.coverImage),
          brand: brandLd(),
          category: 'Wallpaper rolls',
          offers: offerLd(c, absUrl(collectionUrl(c))),
        },
      })),
    },
  ];

  const html = renderDocument({
    root,
    collectionCount: collections.length,
    enquiryHeading: 'Request a quote',
    meta: {
      title: 'Wallpaper Rolls & Collections | Wall Jewels Wallpaper World',
      description: 'Explore Wall Jewels Wallpaper World wallpaper roll collections, browse catalogues and designs, and calculate the approximate rolls required for your walls.',
      keywords: 'wallpaper rolls, wallpaper roll price, wallpaper catalogue, wallpaper collection, wallpaper calculator, designer wallpaper, imported wallpaper, wallpaper for home, wallpaper Chennai, Wall Jewels wallpaper',
      canonical,
      ogImage,
      ldGraph,
    },
    main,
  });
  return { path: 'wallpaper-rolls/index.html', html };
}

/* ------------------------------------------------------------- collection */

export function buildCollectionPage(model, collection) {
  const root = rootFor([collection.slug]);
  const canonical = absUrl(collectionUrl(collection));
  const designs = model.byCollection.get(collection.slug) || [];
  const s = specStrings(collection);
  const count = designs.length;
  const countLabel = `${count} ${count === 1 ? 'design' : 'designs'}`;
  const sizeMB = collection.catalogueSizeMB ? ` · ${formatNumber(collection.catalogueSizeMB, 1)} MB` : '';
  const pages = collection.pageCount ? `${collection.pageCount} ${collection.pageCount === 1 ? 'page' : 'pages'}` : '';

  const crumbs = breadcrumbs([
    { label: 'Home', href: `${root}index.html` },
    { label: 'Wallpaper Rolls', href: `${root}${ROLLS_URL}` },
    { label: collection.name },
  ]);

  const specRow = `<dl class="rolls-specrow rv" style="--i:3">
  <div><dt>Roll size</dt><dd>${esc(s.roll)}</dd></div>
  <div><dt>Approx. coverage</dt><dd>${esc(s.coverage)}</dd></div>
  <div><dt>Price per roll</dt><dd>${esc(s.price)}</dd></div>
  <div><dt>Book price</dt><dd>${esc(formatINR(collection.pricePerSqFt))} per ${esc(s.unit)}</dd></div>
  <div><dt>Designs</dt><dd>${esc(String(count))}</dd></div>${pages ? `\n  <div><dt>Catalogue</dt><dd>${esc(pages)}</dd></div>` : ''}
</dl>`;

  const hero = `<section class="section rolls-hero rolls-hero--collection">
  <div class="wrap">
    ${indentBlock(crumbs, 4).trimStart()}
    ${threshold()}
    <div class="headgroup">
      ${eyebrow(`Wallpaper Rolls · ${BRAND}`)}
      <h1 class="d1 rv">${esc(collection.name)}</h1>
      <p class="lead rv" style="--i:1">${esc(collection.tagline || '')}</p>
      ${collection.description ? `<p class="rolls-hero__quote rv" style="--i:2">${esc(collection.description)}</p>` : ''}
      ${indentBlock(specRow, 6).trimStart()}
      <div class="rolls-hero__actions rv" style="--i:4">
        <button class="btn btn--fill" type="button" data-open-rolls-catalogue="${esc(collection.slug)}" data-page="1"><span class="dot-a"></span>View Catalogue</button>
        <a class="btn" href="#calculator" data-calc-collection="${esc(collection.slug)}"><span class="dot-a"></span>Calculate Requirement</a>
        <a class="btn btn--ghost" href="${esc(`${root}${collection.catalogueFile}`)}" target="_blank" rel="noopener"><span class="dot-a"></span>Download PDF${esc(sizeMB)}</a>
      </div>
      <p class="small rv" style="--i:5">${esc(collection.catalogueName || 'Catalogue PDF')} opens in a new tab.</p>
    </div>
  </div>
</section>`;

  const library = gallerySection({
    root,
    collections: model.collections,
    activeSlug: collection.slug,
    cards: designs.map((d) => ({ design: d, collection })),
    totalCount: count,
    staticLimit: COLLECTION_STATIC_CARDS,
    heading: `${collection.name} Designs`,
  });

  const calculator = calculatorSection({
    id: 'calculator',
    heading: `Calculate ${collection.name} Rolls`,
    intro: `${s.roll} per roll · approx. ${s.coverage} wall coverage · ${s.price} per roll. Enter your wall size in inches for an approximate roll count and cost.`,
    collection: collection.slug,
    lock: true,
  });

  const cta = ctaBand({
    heading: `Enquire about ${collection.name}`,
    lead: 'Tell us the design number and your wall size. The team confirms the exact roll count, availability and quote.',
    waText: `Namaste Wall Jewels — I'd like help choosing from the ${collection.name} wallpaper collection.`,
  });

  const main = [hero, library, calculator, cta].map((sec) => indentBlock(sec, 4)).join('\n\n');

  const ldGraph = [
    {
      '@type': 'CollectionPage',
      '@id': `${canonical}#page`,
      name: `${collection.name} Wallpaper Rolls`,
      description: collection.description || collection.tagline || '',
      url: canonical,
      inLanguage: 'en-IN',
      image: absUrl(collection.coverImage),
    },
    breadcrumbLd(canonical, [
      { name: 'Home', url: absUrl('') },
      { name: 'Wallpaper Rolls', url: absUrl(ROLLS_URL) },
      { name: collection.name, url: canonical },
    ]),
    {
      '@type': 'ItemList',
      '@id': `${canonical}#designs`,
      name: `${collection.name} designs`,
      numberOfItems: count,
      itemListElement: designs.map((d, i) => ({
        '@type': 'ListItem',
        position: i + 1,
        item: designProductLd(d, collection),
      })),
    },
  ];

  const description = `${collection.name} wallpaper rolls — ${countLabel} at ${s.price} per roll (${s.roll} roll, approx. ${s.coverage} wall coverage). Browse the ${collection.catalogueName || 'catalogue'} online, open every design and calculate the rolls your wall needs. Wall Jewels Wallpaper World, Chennai.`;

  const html = renderDocument({
    root,
    collectionCount: model.collections.length,
    enquiryHeading: 'Request a quote',
    meta: {
      title: `${collection.name} Wallpaper Rolls — Designs, Catalogue & Roll Calculator | Wall Jewels`,
      description,
      keywords: `${collection.name} wallpaper, ${collection.name} wallpaper rolls, wallpaper catalogue, wallpaper roll price, wallpaper Chennai, Wall Jewels wallpaper`,
      canonical,
      ogImage: absUrl(collection.coverImage),
      ldGraph,
    },
    main,
  });
  return { path: `wallpaper-rolls/${collection.slug}/index.html`, html };
}

/* ----------------------------------------------------------------- design */

/** Up to STRIP_SIZE neighbours around index `i`, in catalogue order, excluding the design itself. */
function neighbours(list, i) {
  const half = Math.floor(STRIP_SIZE / 2);
  let start = Math.max(0, i - half);
  let end = Math.min(list.length, start + STRIP_SIZE + 1);
  start = Math.max(0, end - STRIP_SIZE - 1);
  return list.slice(start, end).filter((d) => d !== list[i]).slice(0, STRIP_SIZE);
}

function extraFigure(root, src, label, alt) {
  return `<figure class="rolls-design__extra" data-no-lightbox>
  <img src="${esc(`${root}${src}`)}" alt="${esc(alt)}" loading="lazy" decoding="async">
  <figcaption class="cap">${esc(label)}</figcaption>
</figure>`;
}

export function buildDesignPage(model, design) {
  const collection = model.collectionById.get(design.collectionId);
  const root = rootFor([collection.slug, design.slug]);
  const canonical = absUrl(design.url);
  const s = specStrings(collection);
  const list = model.byCollection.get(collection.slug) || [];
  const index = list.indexOf(design);
  const prev = index > 0 ? list[index - 1] : null;
  const next = index < list.length - 1 ? list[index + 1] : null;
  const no = design.designNumber;
  const title = `Design No. ${no}`;
  const imgSrc = design.web || design.image;
  const dims = (design.width && design.height) ? ` width="${esc(design.width)}" height="${esc(design.height)}"` : '';
  const alt = `${collection.name} wallpaper design ${no}`;

  const crumbs = breadcrumbs([
    { label: 'Home', href: `${root}index.html` },
    { label: 'Wallpaper Rolls', href: `${root}${ROLLS_URL}` },
    { label: collection.name, href: `${root}${collectionUrl(collection)}` },
    { label: title },
  ]);

  const extras = [
    design.swatch ? extraFigure(root, design.swatch, 'Swatch', `${alt} — pattern swatch`) : '',
    design.detail ? extraFigure(root, design.detail, design.detailLabel || 'Close-up', `${alt} — ${(design.detailLabel || 'close-up').toLowerCase()}`) : '',
  ].filter(Boolean);
  const extrasHtml = extras.length
    ? `\n    <div class="rolls-design__extras">\n${extras.map((e) => indentBlock(e, 6)).join('\n')}\n    </div>`
    : '';

  const metaRows = [
    ['Collection', `<a href="${esc(`${root}${collectionUrl(collection)}`)}">${esc(collection.name)}</a>`],
    ['Design Number', `<span class="rolls-meta__no">${esc(no)}</span>`],
    ['Roll Size', esc(s.roll)],
    ['Approximate Wall Coverage', esc(s.coverage)],
    ['Price', `${esc(s.price)} per roll <span class="small">Book price ${esc(formatINR(collection.pricePerSqFt))} / ${esc(s.unit)}</span>`],
  ];
  if (design.patternRepeat) metaRows.push(['Pattern Repeat', esc(design.patternRepeat)]);
  if (design.colourway) metaRows.push(['Colourway', esc(design.colourway)]);
  if (design.cataloguePage) metaRows.push(['Catalogue', `${esc(collection.catalogueName || 'Catalogue')} · page ${esc(design.cataloguePage)}`]);
  const metaHtml = metaRows.map(([k, v]) => `          <div class="rolls-meta__row"><dt>${k}</dt><dd>${v}</dd></div>`).join('\n');

  const flag = design.needsReview
    ? `\n        <p class="rolls-flag small">Design number to be confirmed by the Wall Jewels team${design.reviewNote ? ` — ${esc(design.reviewNote)}` : '.'}</p>`
    : '';

  const viewInCatalogue = design.cataloguePage
    ? `\n      <button class="btn" type="button" data-open-rolls-catalogue="${esc(collection.slug)}" data-page="${esc(design.cataloguePage)}"><span class="dot-a"></span>View in Catalogue</button>`
    : '';

  const waText = `Namaste Wall Jewels — Wallpaper Rolls enquiry\nCollection: ${collection.name}\nDesign Number: ${no}\nDesign page: ${canonical}\nPlease confirm the exact roll requirement and quote.`;

  const layout = `<section class="section rolls-design-page">
  <div class="wrap">
    ${indentBlock(crumbs, 4).trimStart()}
    <div class="rolls-design">
      <div class="rolls-design__col rolls-design__col--media">
        <figure class="rolls-design__media" data-no-lightbox>
          <img src="${esc(`${root}${imgSrc}`)}" data-full="${esc(`${root}${design.image}`)}"${dims} alt="${esc(alt)}" decoding="async" fetchpriority="high">
          <figcaption class="small">Tap the image to zoom.</figcaption>
        </figure>${indentBlock(extrasHtml, 4)}
      </div>
      <div class="rolls-design__col rolls-design__col--info rolls-design__info">
        <span class="cap cap--gold"><a href="${esc(`${root}${collectionUrl(collection)}`)}">${esc(collection.name)}</a></span>
        <h1 class="d2">${esc(title)}</h1>${flag}
        <dl class="rolls-meta">
${metaHtml}
        </dl>
        <div class="rolls-design__actions">
          <a class="btn btn--fill" href="#calculator"><span class="dot-a"></span>Calculate Rolls</a>
          <button class="btn btn--wa" type="button" data-rolls-enquire><span class="dot-a"></span>Enquire About This Design</button>
          <button class="btn" type="button" data-open-rolls-catalogue="${esc(collection.slug)}"><span class="dot-a"></span>View Complete Catalogue</button>${indentBlock(viewInCatalogue, 4)}
          <noscript>
            <a class="textlink" href="${esc(waLink(waText))}" target="_blank" rel="noopener">Enquire on WhatsApp ${CHEVRON_SVG}</a>
            <a class="textlink" href="${esc(`${root}${collection.catalogueFile}`)}" target="_blank" rel="noopener">Open the catalogue PDF ${CHEVRON_SVG}</a>
          </noscript>
        </div>
      </div>
    </div>
  </div>
</section>`;

  const calculator = calculatorSection({
    id: 'calculator',
    heading: `Calculate Rolls for ${title}`,
    intro: `${collection.name} · ${s.roll} per roll · approx. ${s.coverage} wall coverage · ${s.price} per roll.`,
    collection: collection.slug,
    design: no,
    lock: true,
  });

  const stripCards = neighbours(list, index)
    .map((d) => indentBlock(designCard(root, d, collection), 6))
    .join('\n');
  const pager = `<nav class="rolls-pager" aria-label="Previous and next design">
${prev ? `  <a class="rolls-pager__prev textlink" href="${esc(`${root}${prev.url}`)}" rel="prev">${CHEVRON_BACK_SVG} Design No. ${esc(prev.designNumber)}</a>` : '  <span class="rolls-pager__prev" aria-hidden="true"></span>'}
  <a class="rolls-pager__all textlink" href="${esc(`${root}${collectionUrl(collection)}`)}">All ${esc(collection.name)} designs</a>
${next ? `  <a class="rolls-pager__next textlink" href="${esc(`${root}${next.url}`)}" rel="next">Design No. ${esc(next.designNumber)} ${CHEVRON_SVG}</a>` : '  <span class="rolls-pager__next" aria-hidden="true"></span>'}
</nav>`;
  const related = stripCards
    ? `<section class="section section--tight rolls-related">
  <div class="wrap">
    ${threshold()}
    <div class="headgroup">
      <span class="cap cap--gold rv">Neighbouring pages</span>
      <h2 class="d3 rv" style="--i:1">More from ${esc(collection.name)}</h2>
    </div>
    <div class="rolls-strip" data-no-lightbox>
${stripCards}
    </div>
    ${indentBlock(pager, 4).trimStart()}
  </div>
</section>`
    : '';

  const main = [layout, calculator, related].filter(Boolean).map((sec) => indentBlock(sec, 4)).join('\n\n');

  const ldGraph = [
    designProductLd(design, collection),
    breadcrumbLd(canonical, [
      { name: 'Home', url: absUrl('') },
      { name: 'Wallpaper Rolls', url: absUrl(ROLLS_URL) },
      { name: collection.name, url: absUrl(collectionUrl(collection)) },
      { name: `Design ${no}`, url: canonical },
    ]),
  ];

  const description = `${collection.name} wallpaper roll, design number ${no}. ${formatNumber(collection.rollSize)} ${s.unit} roll, approx. ${formatNumber(collection.coverage)} ${s.unit} wall coverage, ${s.price} per roll. View the catalogue, calculate rolls and enquire with Wall Jewels Wallpaper World, Chennai.`;

  const html = renderDocument({
    root,
    collectionCount: model.collections.length,
    enquiryHeading: 'Enquire about this design',
    meta: {
      title: `${collection.name} Design ${no} — Wallpaper Roll ${s.price} | Wall Jewels`,
      description,
      canonical,
      ogImage: absUrl(imgSrc),
      ogTitle: `${collection.name} — Design No. ${no} · ${s.price} per roll`,
      ldGraph,
    },
    main,
  });
  return { path: `wallpaper-rolls/${collection.slug}/${design.slug}/index.html`, html };
}

/* ------------------------------------------------------------- calculator */

export function buildCalculatorPage(model) {
  const root = rootFor(['calculator']);
  const canonical = absUrl(`${ROLLS_URL}calculator/`);
  const { collections } = model;
  const ogImage = collections[0] ? absUrl(collections[0].coverImage) : absUrl('assets/img/collection/pichwai-eternal-melody.jpg');

  const crumbs = breadcrumbs([
    { label: 'Home', href: `${root}index.html` },
    { label: 'Wallpaper Rolls', href: `${root}${ROLLS_URL}` },
    { label: 'Roll Calculator' },
  ]);

  const hero = `<section class="section rolls-hero rolls-hero--calculator">
  <div class="wrap">
    ${indentBlock(crumbs, 4).trimStart()}
    ${threshold()}
    <div class="headgroup">
      ${eyebrow(`${BRAND} · ${BRAND_LINE}`)}
      <h1 class="d1 rv">Wallpaper Roll Calculator</h1>
      <p class="lead rv" style="--i:1">Calculate How Many Rolls You Need</p>
      <p class="rolls-hero__quote rv" style="--i:2">Measure the wall in inches, choose a collection, and see the approximate number of rolls and the wallpaper cost. Wallpaper cost only — no GST, delivery or installation.</p>
    </div>
  </div>
</section>`;

  const calculator = calculatorSection({
    id: 'calculator',
    heading: 'Enter Your Wall Size',
    intro: 'Width and height in inches. The estimate updates as you type once both numbers are valid.',
  });

  const rows = collections.map((c) => {
    const s = specStrings(c);
    const n = (model.byCollection.get(c.slug) || []).length;
    return `          <tr>
            <th scope="row"><a href="${esc(`${root}${collectionUrl(c)}`)}">${esc(c.name)}</a></th>
            <td>${esc(s.roll)}</td>
            <td>${esc(s.coverage)}</td>
            <td>${esc(s.price)}</td>
            <td>${esc(formatINR(c.pricePerSqFt))} / ${esc(s.unit)}</td>
            <td>${esc(String(n))}</td>
          </tr>`;
  }).join('\n');

  const method = `<section class="section rolls-method">
  <div class="wrap">
    ${threshold()}
    <div class="headgroup">
      <span class="cap cap--gold rv">How the estimate works</span>
      <h2 class="d2 rv" style="--i:1">Three Steps, Always Rounded Up</h2>
    </div>
    <ol class="rolls-steps">
      <li class="rv" style="--i:1"><span class="num">01</span><h3>Wall area</h3><p>Width in inches × height in inches ÷ 144 gives the wall area in square feet. A 120″ × 108″ wall is 90 sq.ft.</p></li>
      <li class="rv" style="--i:2"><span class="num">02</span><h3>Rolls</h3><p>Wall area ÷ the collection's approximate coverage per roll, rounded up to the next whole roll. 90 sq.ft at 45 sq.ft coverage is 2 rolls.</p></li>
      <li class="rv" style="--i:3"><span class="num">03</span><h3>Wallpaper cost</h3><p>Rolls × the price per roll. Pattern repeat, alignment, cutting and wastage are why the coverage figure is lower than the roll size.</p></li>
    </ol>
    <div class="rolls-table-wrap">
      <table class="rolls-facts-table">
        <caption class="cap">Roll facts by collection</caption>
        <thead>
          <tr><th scope="col">Collection</th><th scope="col">Roll size</th><th scope="col">Approx. coverage</th><th scope="col">Price per roll</th><th scope="col">Book price</th><th scope="col">Designs</th></tr>
        </thead>
        <tbody>
${rows}
        </tbody>
      </table>
    </div>
  </div>
</section>`;

  const main = [hero, calculator, method, ctaBand({ calcLabel: 'Back to the Calculator' })]
    .map((sec) => indentBlock(sec, 4))
    .join('\n\n');

  const ldGraph = [
    {
      '@type': 'WebPage',
      '@id': `${canonical}#page`,
      name: 'Wallpaper Roll Calculator',
      description: 'Calculate the approximate number of wallpaper rolls and the wallpaper cost for your wall from its width and height in inches.',
      url: canonical,
      inLanguage: 'en-IN',
      isPartOf: { '@type': 'WebSite', name: BRAND, url: absUrl('') },
    },
    breadcrumbLd(canonical, [
      { name: 'Home', url: absUrl('') },
      { name: 'Wallpaper Rolls', url: absUrl(ROLLS_URL) },
      { name: 'Roll Calculator', url: canonical },
    ]),
  ];

  const html = renderDocument({
    root,
    collectionCount: collections.length,
    enquiryHeading: 'Request a quote',
    meta: {
      title: 'Wallpaper Roll Calculator | Wall Jewels Wallpaper World',
      description: 'Calculate the approximate number of wallpaper rolls and cost for your wall. Enter the wall width and height in inches, choose a Wall Jewels collection and get an instant estimate, confirmed by our team before order.',
      keywords: 'wallpaper calculator, wallpaper roll calculator, how many wallpaper rolls, wallpaper roll price, wallpaper Chennai, Wall Jewels wallpaper',
      canonical,
      ogImage,
      ldGraph,
    },
    main,
  });
  return { path: 'wallpaper-rolls/calculator/index.html', html };
}

export const STATIC_LIMITS = Object.freeze({ landing: LANDING_STATIC_CARDS, collection: COLLECTION_STATIC_CARDS });
export { CONTACT };
