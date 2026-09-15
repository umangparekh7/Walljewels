// Shared helpers for the Wallpaper Rolls generator.
// Pure functions only — no file system access here.

export const SITE_URL = 'https://www.walljewels.in/';
export const ASSET_V = 'rolls1';
export const BRAND = 'Wall Jewels Wallpaper World';
export const BRAND_LINE = "South India's Pioneers in Wallpapers Since 1978";
export const CONTACT = Object.freeze({
  whatsapp: '919677042903',
  email: 'info@walljewels.com',
  phone: '+91 98400 64205',
  phoneHref: 'tel:+919840064205',
});

/** HTML-escape a value for text nodes and double-quoted attributes. */
export function esc(value) {
  if (value === null || value === undefined) return '';
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

/** Escape for use inside an XML text node or attribute (sitemap). */
export const escXml = esc;

/** Design slug rule from SPEC §1. */
export function slugify(str) {
  return String(str ?? '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

/** ₹5,940 — en-IN grouping, no decimals. */
export function formatINR(n) {
  const value = Math.round(Number(n) || 0);
  const sign = value < 0 ? '-' : '';
  const digits = String(Math.abs(value));
  if (digits.length <= 3) return `${sign}₹${digits}`;
  const last3 = digits.slice(-3);
  const rest = digits.slice(0, -3).replace(/\B(?=(\d{2})+(?!\d))/g, ',');
  return `${sign}₹${rest},${last3}`;
}

/** Plain number with en-IN grouping and no currency sign (for JSON-LD we use raw numbers). */
export function formatNumber(n, maxDecimals = 2) {
  const value = Number(n) || 0;
  const fixed = Number(value.toFixed(maxDecimals));
  return String(fixed);
}

/** Split "5314/10" into comparable chunks: numeric runs compare as numbers. */
function chunks(str) {
  return String(str ?? '').match(/\d+|\D+/g) || [];
}

/** Numeric-aware comparison of two design numbers: 2 < 10, "5314/9" < "5314/10". */
export function compareDesignNumbers(a, b) {
  const ca = chunks(a);
  const cb = chunks(b);
  const len = Math.max(ca.length, cb.length);
  for (let i = 0; i < len; i += 1) {
    const x = ca[i];
    const y = cb[i];
    if (x === undefined) return -1;
    if (y === undefined) return 1;
    const xn = /^\d+$/.test(x);
    const yn = /^\d+$/.test(y);
    if (xn && yn) {
      const diff = Number(x) - Number(y);
      if (diff !== 0) return diff;
      if (x.length !== y.length) return x.length - y.length;
    } else if (x !== y) {
      return x < y ? -1 : 1;
    }
  }
  return 0;
}

/** Returns a new array of designs in natural numeric order of designNumber. */
export function sortDesigns(designs) {
  return [...designs].sort((a, b) => compareDesignNumbers(a.designNumber, b.designNumber));
}

/** Depth prefix for a page at `wallpaper-rolls/<...segments>/index.html`. */
export function rootFor(segments) {
  return '../'.repeat(segments.length + 1);
}

/** Absolute URL on the live site from a root-relative path (no leading slash). */
export function absUrl(path) {
  return SITE_URL + String(path ?? '').replace(/^\/+/, '');
}

/** Cache-busted asset href with the depth prefix applied. */
export function asset(root, path) {
  return `${root}${path}?v=${ASSET_V}`;
}

/** JSON-LD safe serialisation: `<` and `&` are escaped so the script block can never be closed early. */
export function jsonLd(graph) {
  return JSON.stringify(graph, null, 2)
    .replace(/</g, '\\u003c')
    .replace(/>/g, '\\u003e')
    .replace(/&/g, '\\u0026');
}

/** Indent every line of a multi-line block by `n` spaces (keeps generated HTML readable). */
export function indent(block, n) {
  const pad = ' '.repeat(n);
  return String(block)
    .split('\n')
    .map((line) => (line.trim() ? pad + line : ''))
    .join('\n');
}

/** Build a wa.me link with a prefilled message. */
export function waLink(text) {
  return `https://wa.me/${CONTACT.whatsapp}?text=${encodeURIComponent(text)}`;
}

/** Roll specs as display strings, shared by every template. */
export function specStrings(collection) {
  const unit = collection.unit || 'sq.ft';
  return {
    roll: `${formatNumber(collection.rollSize)} ${unit}`,
    coverage: `${formatNumber(collection.coverage)} ${unit}`,
    price: formatINR(collection.rollPrice),
    perSqFt: `${formatINR(collection.pricePerSqFt)} / ${unit}`,
    wastage: collection.wastage ? `${formatNumber(collection.wastage)} ${unit}` : null,
    unit,
  };
}
