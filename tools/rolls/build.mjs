#!/usr/bin/env node
// Wallpaper Rolls static-site generator (SPEC §9).
//
//   node tools/rolls/build.mjs            build everything
//   node tools/rolls/build.mjs --check    validate the data only, write nothing
//
// Reads assets/rolls/collections.json + designs.json, validates them, writes
// assets/js/rolls-data.js, renders every page under wallpaper-rolls/, removes
// stale design folders, and maintains the rolls block in sitemap.xml.
// Zero dependencies; runs on Node 18+ (built for Node 24).

import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync, rmSync, statSync } from 'node:fs';
import { dirname, join, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

import { slugify, sortDesigns, absUrl, escXml, CONTACT } from './templates/util.mjs';
import { buildLanding, buildCollectionPage, buildDesignPage, buildCalculatorPage } from './templates/pages.mjs';

const SITE = resolve(dirname(fileURLToPath(import.meta.url)), '..', '..');
const OUT_DIR = 'wallpaper-rolls';
const RESERVED_DIRS = new Set(['calculator']);
const MAX_SORT_FALLBACK = 1e9;

const args = new Set(process.argv.slice(2));
const CHECK_ONLY = args.has('--check');

const errors = [];
const warnings = [];
const fail = (msg) => errors.push(msg);
const warn = (msg) => warnings.push(msg);

/* ------------------------------------------------------------------ data */

function readJson(relPath) {
  const abs = join(SITE, relPath);
  if (!existsSync(abs)) {
    fail(`Missing ${relPath}`);
    return null;
  }
  try {
    return JSON.parse(readFileSync(abs, 'utf8'));
  } catch (err) {
    fail(`${relPath} is not valid JSON: ${err.message}`);
    return null;
  }
}

const isPositiveNumber = (v) => typeof v === 'number' && Number.isFinite(v) && v > 0;
const isNonEmptyString = (v) => typeof v === 'string' && v.trim().length > 0;
const fileExists = (relPath) => isNonEmptyString(relPath) && existsSync(join(SITE, relPath));

function validateCollections(raw) {
  const list = Array.isArray(raw?.collections) ? raw.collections : null;
  if (!list) {
    fail('collections.json must contain a "collections" array');
    return [];
  }
  const seen = new Set();
  const valid = [];
  list.forEach((c, i) => {
    const label = `collections[${i}] (${c?.slug || c?.id || 'unnamed'})`;
    if (!c || typeof c !== 'object') return fail(`${label}: not an object`);
    for (const key of ['id', 'slug', 'name', 'catalogueFile', 'coverImage']) {
      if (!isNonEmptyString(c[key])) fail(`${label}: "${key}" is required`);
    }
    for (const key of ['rollSize', 'coverage', 'pricePerSqFt', 'rollPrice']) {
      if (!isPositiveNumber(c[key])) fail(`${label}: "${key}" must be a number > 0`);
    }
    if (isNonEmptyString(c.slug)) {
      if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(c.slug)) fail(`${label}: slug must be lower-case a-z, 0-9 and single hyphens`);
      if (RESERVED_DIRS.has(c.slug)) fail(`${label}: slug "${c.slug}" is reserved`);
      if (seen.has(c.slug)) fail(`${label}: duplicate collection slug "${c.slug}"`);
      seen.add(c.slug);
    }
    if (c.id !== c.slug) warn(`${label}: id "${c.id}" differs from slug "${c.slug}" — designs reference collectionId, keep them equal`);
    if (typeof c.published !== 'boolean') warn(`${label}: "published" missing, treating as true`);
    if (c.pageCount !== undefined && c.pageCount !== null && !isPositiveNumber(c.pageCount)) warn(`${label}: pageCount should be a number > 0`);
    if (!fileExists(c.catalogueFile)) warn(`${label}: catalogue not found at ${c.catalogueFile}`);
    if (!fileExists(c.coverImage)) warn(`${label}: cover image not found at ${c.coverImage}`);
    if (isPositiveNumber(c.rollSize) && isPositiveNumber(c.coverage) && c.coverage > c.rollSize) {
      warn(`${label}: coverage (${c.coverage}) is greater than rollSize (${c.rollSize})`);
    }
    valid.push(c);
  });
  return valid;
}

function validateDesigns(raw, collectionById) {
  const list = Array.isArray(raw?.designs) ? raw.designs : null;
  if (!list) {
    fail('designs.json must contain a "designs" array');
    return [];
  }
  const slugsByCollection = new Map();
  const valid = [];
  list.forEach((d, i) => {
    const label = `designs[${i}] (${d?.id || 'unnamed'})`;
    if (!d || typeof d !== 'object') return fail(`${label}: not an object`);
    for (const key of ['id', 'collectionId', 'designNumber', 'slug', 'image', 'thumbnail']) {
      if (!isNonEmptyString(d[key])) fail(`${label}: "${key}" is required`);
    }
    if (!isNonEmptyString(d.collectionId) || !isNonEmptyString(d.designNumber)) return;
    const collection = collectionById.get(d.collectionId);
    if (!collection) return fail(`${label}: unknown collectionId "${d.collectionId}"`);
    const expectedSlug = slugify(d.designNumber);
    if (!expectedSlug) return fail(`${label}: designNumber "${d.designNumber}" produces an empty slug`);
    if (d.slug !== expectedSlug) fail(`${label}: slug "${d.slug}" must equal slugify(designNumber) = "${expectedSlug}"`);
    const expectedId = `${d.collectionId}:${d.designNumber}`;
    if (d.id !== expectedId) warn(`${label}: id should be "${expectedId}"`);
    const bucket = slugsByCollection.get(d.collectionId) || new Set();
    if (bucket.has(expectedSlug)) fail(`${label}: duplicate design slug "${expectedSlug}" in collection "${d.collectionId}"`);
    bucket.add(expectedSlug);
    slugsByCollection.set(d.collectionId, bucket);
    for (const key of ['image', 'thumbnail', 'web', 'swatch', 'detail']) {
      if (d[key] && !fileExists(d[key])) warn(`${label}: ${key} not found at ${d[key]}`);
    }
    if (!d.web) warn(`${label}: no "web" image — cards will use the thumbnail only`);
    if (d.width !== undefined && d.width !== null && !isPositiveNumber(d.width)) warn(`${label}: width should be a number > 0`);
    if (d.height !== undefined && d.height !== null && !isPositiveNumber(d.height)) warn(`${label}: height should be a number > 0`);
    if (d.cataloguePage !== undefined && d.cataloguePage !== null) {
      if (!Number.isInteger(d.cataloguePage) || d.cataloguePage < 1) warn(`${label}: cataloguePage should be a positive integer`);
      else if (collection.pageCount && d.cataloguePage > collection.pageCount) warn(`${label}: cataloguePage ${d.cataloguePage} exceeds pageCount ${collection.pageCount}`);
    }
    valid.push(d);
  });
  return valid;
}

/** Build the model every template reads: published collections in order, designs sorted, urls attached. */
function buildModel(collectionsRaw, designsRaw) {
  const collections = collectionsRaw
    .filter((c) => c.published !== false)
    .sort((a, b) => (a.sort ?? MAX_SORT_FALLBACK) - (b.sort ?? MAX_SORT_FALLBACK) || a.name.localeCompare(b.name));
  const collectionById = new Map(collections.map((c) => [c.id, c]));
  const byCollection = new Map();
  for (const c of collections) byCollection.set(c.slug, []);
  for (const d of designsRaw) {
    const c = collectionById.get(d.collectionId);
    if (!c) continue; // unpublished collection: skipped silently (already validated)
    byCollection.get(c.slug).push({ ...d, url: `${OUT_DIR}/${c.slug}/${d.slug}/` });
  }
  const designs = [];
  for (const c of collections) {
    const sorted = sortDesigns(byCollection.get(c.slug));
    byCollection.set(c.slug, sorted);
    designs.push(...sorted);
  }
  return { collections, collectionById, byCollection, designs };
}

/* --------------------------------------------------------------- writing */

const written = [];
const unchanged = [];

function writeIfChanged(relPath, content) {
  const abs = join(SITE, relPath);
  mkdirSync(dirname(abs), { recursive: true });
  if (existsSync(abs) && readFileSync(abs, 'utf8') === content) {
    unchanged.push(relPath);
    return;
  }
  writeFileSync(abs, content, 'utf8');
  written.push(relPath);
}

function writeRollsData(model) {
  const payload = {
    generatedAt: new Date().toISOString().replace(/\.\d{3}Z$/, 'Z'),
    site: absUrl(''),
    contact: { whatsapp: CONTACT.whatsapp, email: CONTACT.email, phone: CONTACT.phone },
    collections: model.collections,
    designs: model.designs,
  };
  const lines = [
    '// Generated by tools/rolls/build.mjs from assets/rolls/*.json — do not edit by hand.',
    'window.WJ_ROLLS = {',
    `  "generatedAt": ${JSON.stringify(payload.generatedAt)},`,
    `  "site": ${JSON.stringify(payload.site)},`,
    `  "contact": ${JSON.stringify(payload.contact)},`,
    '  "collections": [',
    payload.collections.map((c) => `    ${JSON.stringify(c)}`).join(',\n'),
    '  ],',
    '  "designs": [',
    payload.designs.map((d) => `    ${JSON.stringify(d)}`).join(',\n'),
    '  ]',
    '};',
    '',
  ];
  const content = lines.join('\n').replace(/<\//g, '<\\/');
  // generatedAt changes every run; only rewrite when the data itself changed so mtimes stay honest.
  const abs = join(SITE, 'assets/js/rolls-data.js');
  if (existsSync(abs)) {
    const strip = (s) => s.replace(/"generatedAt": "[^"]*"/, '');
    if (strip(readFileSync(abs, 'utf8')) === strip(content)) {
      unchanged.push('assets/js/rolls-data.js');
      return;
    }
  }
  writeIfChanged('assets/js/rolls-data.js', content);
}

function renderPages(model) {
  const pages = [buildLanding(model), buildCalculatorPage(model)];
  for (const c of model.collections) {
    pages.push(buildCollectionPage(model, c));
    for (const d of model.byCollection.get(c.slug)) pages.push(buildDesignPage(model, d));
  }
  for (const p of pages) writeIfChanged(p.path, p.html);
  return pages;
}

/** Remove folders under wallpaper-rolls/ that no longer correspond to data (collections or designs). */
function pruneStale(model) {
  const removed = [];
  const outAbs = join(SITE, OUT_DIR);
  if (!existsSync(outAbs)) return removed;
  const isDir = (p) => existsSync(p) && statSync(p).isDirectory();
  const validCollections = new Set(model.collections.map((c) => c.slug));
  for (const name of readdirSync(outAbs)) {
    const abs = join(outAbs, name);
    if (!isDir(abs) || RESERVED_DIRS.has(name)) continue;
    if (!validCollections.has(name)) {
      rmSync(abs, { recursive: true, force: true });
      removed.push(`${OUT_DIR}/${name}/`);
      continue;
    }
    const validDesigns = new Set(model.byCollection.get(name).map((d) => d.slug));
    for (const sub of readdirSync(abs)) {
      const subAbs = join(abs, sub);
      if (!isDir(subAbs) || validDesigns.has(sub)) continue;
      rmSync(subAbs, { recursive: true, force: true });
      removed.push(`${OUT_DIR}/${name}/${sub}/`);
    }
  }
  return removed;
}

/* --------------------------------------------------------------- sitemap */

const SITEMAP_START = '<!-- rolls:start -->';
const SITEMAP_END = '<!-- rolls:end -->';

function sitemapEntry({ loc, changefreq, priority, images = [] }, lastmod) {
  const imgs = images.map((img) => `    <image:image>
      <image:loc>${escXml(img.loc)}</image:loc>
      <image:title>${escXml(img.title)}</image:title>
    </image:image>`).join('\n');
  return `  <url>
    <loc>${escXml(loc)}</loc>
    <lastmod>${lastmod}</lastmod>
    <changefreq>${changefreq}</changefreq>
    <priority>${priority}</priority>${imgs ? `\n${imgs}` : ''}
  </url>`;
}

function buildSitemapBlock(model) {
  const lastmod = new Date().toISOString().slice(0, 10);
  const entries = [];
  entries.push({
    loc: absUrl(`${OUT_DIR}/`), changefreq: 'weekly', priority: '0.9',
    images: model.collections.map((c) => ({ loc: absUrl(c.coverImage), title: `${c.name} wallpaper collection` })),
  });
  entries.push({ loc: absUrl(`${OUT_DIR}/calculator/`), changefreq: 'monthly', priority: '0.7' });
  for (const c of model.collections) {
    entries.push({
      loc: absUrl(`${OUT_DIR}/${c.slug}/`), changefreq: 'weekly', priority: '0.85',
      images: [{ loc: absUrl(c.coverImage), title: `${c.name} wallpaper collection` }],
    });
    for (const d of model.byCollection.get(c.slug)) {
      entries.push({
        loc: absUrl(d.url), changefreq: 'monthly', priority: '0.6',
        images: [{ loc: absUrl(d.web || d.image), title: `${c.name} wallpaper design ${d.designNumber}` }],
      });
    }
  }
  return `${SITEMAP_START}\n${entries.map((e) => sitemapEntry(e, lastmod)).join('\n')}\n  ${SITEMAP_END}`;
}

function updateSitemap(model) {
  const rel = 'sitemap.xml';
  const abs = join(SITE, rel);
  if (!existsSync(abs)) {
    warn('sitemap.xml not found — rolls block not written');
    return;
  }
  const xml = readFileSync(abs, 'utf8');
  const block = buildSitemapBlock(model);
  const start = xml.indexOf(SITEMAP_START);
  const end = xml.indexOf(SITEMAP_END);
  let next;
  if (start !== -1 && end !== -1 && end > start) {
    next = xml.slice(0, start) + block + xml.slice(end + SITEMAP_END.length);
  } else if (start === -1 && end === -1) {
    const close = xml.lastIndexOf('</urlset>');
    if (close === -1) {
      warn('sitemap.xml has no </urlset> — rolls block not written');
      return;
    }
    next = `${xml.slice(0, close).replace(/\s*$/, '')}\n  ${block}\n</urlset>\n`;
  } else {
    warn('sitemap.xml has an unbalanced rolls block — fix the markers by hand');
    return;
  }
  // Keep lastmod stable when nothing but the date would change.
  const stripDates = (s) => s.replace(/<lastmod>\d{4}-\d{2}-\d{2}<\/lastmod>/g, '<lastmod/>');
  if (stripDates(next) === stripDates(xml)) {
    unchanged.push(rel);
    return;
  }
  writeIfChanged(rel, next);
}

/* ------------------------------------------------------------------ main */

function report(model, pages, removed) {
  const out = [];
  out.push(`Wallpaper Rolls build — ${CHECK_ONLY ? 'check only' : 'complete'}`);
  out.push(`  collections : ${model.collections.length} published (${model.collections.map((c) => `${c.name} ${model.byCollection.get(c.slug).length}`).join(', ') || 'none'})`);
  out.push(`  designs     : ${model.designs.length}`);
  if (!CHECK_ONLY) {
    out.push(`  pages       : ${pages.length} rendered (${written.filter((f) => f.startsWith(OUT_DIR)).length} written, ${unchanged.filter((f) => f.startsWith(OUT_DIR)).length} unchanged)`);
    out.push(`  data        : assets/js/rolls-data.js ${written.includes('assets/js/rolls-data.js') ? 'written' : 'unchanged'}`);
    out.push(`  sitemap     : ${written.includes('sitemap.xml') ? 'rolls block updated' : 'unchanged'}`);
    if (removed.length) out.push(`  removed     : ${removed.join(', ')}`);
  }
  if (warnings.length) {
    out.push(`  warnings    : ${warnings.length}`);
    for (const w of warnings) out.push(`    - ${w}`);
  } else {
    out.push('  warnings    : none');
  }
  console.log(out.join('\n'));
}

function main() {
  const collectionsRaw = readJson('assets/rolls/collections.json');
  const designsRaw = readJson('assets/rolls/designs.json');
  if (errors.length) return finish(null, [], []);

  const collections = validateCollections(collectionsRaw);
  const collectionById = new Map(collections.map((c) => [c.id, c]));
  const designs = validateDesigns(designsRaw, collectionById);
  if (errors.length) return finish(null, [], []);

  const model = buildModel(collections, designs);
  if (!model.collections.length) warn('no published collections — landing page will have no cards');
  if (CHECK_ONLY) return finish(model, [], []);

  writeRollsData(model);
  const pages = renderPages(model);
  const removed = pruneStale(model);
  updateSitemap(model);
  return finish(model, pages, removed);
}

function finish(model, pages, removed) {
  if (errors.length) {
    console.error(`Wallpaper Rolls build — ${errors.length} error${errors.length === 1 ? '' : 's'}, nothing written`);
    for (const e of errors) console.error(`  ✖ ${e}`);
    if (warnings.length) {
      console.error(`  warnings: ${warnings.length}`);
      for (const w of warnings) console.error(`    - ${w}`);
    }
    process.exitCode = 1;
    return;
  }
  report(model, pages, removed);
}

main();
