# Wallpaper Rolls — build contract (SPEC)

This document is the single contract shared by everyone building the
"Wallpaper Rolls" product system for walljewels.in. Read it fully before
touching any file. Where it says MUST, do exactly that — other builders rely on it.

Site root (all paths below are relative to it):
`C:\Users\Chintan Kamani\Desktop\TheVisionarys Ltd\TheVisionarysLtd_UK - Documents\The Visionarys Ltd Products\Websites\WJWP New Website-Fable\walljewels-site`

## 0. What already exists (do not break)

* Pure static site, no build step, no package.json, no npm. Deployed by
  `.github/workflows/deploy.yml` (copies `*.html`, `assets/`, `showrooms/`,
  `.htaccess` etc. to the `production` branch; Hostinger serves it from the
  domain root). Local dev server: `python tools/serve.py 5178`.
* Chrome shared by every page: announcement bar `.annbar`, sticky `header.header`
  (`.header__in` → theme toggle `.theme`, `.header__center` (logo `.wordmark--img` +
  `nav.nav`), `.header__tools` (socials + `.burger[data-open-drawer]`)),
  mobile `nav.drawer` (`.drawer__head`, `.drawer__nav`, `.drawer__foot`),
  `footer.footer` (`.footer__main` → `.footer__brand`, `.footer__links` with
  `nav.fcol` columns, `.footer__connect`; `.footer__bottom`).
  Copy the exact markup from `luxury-wallpapers.html` (a clean secondary page)
  and `index.html` (header with socials, full footer). Keep the favicon block,
  GA tag, font preloads and `<html lang="en" class="no-js">` exactly as they are.
* Scripts every page loads, in this order, all `defer`:
  `assets/js/vendor/lenis.min.js`, `assets/js/data.js`, `assets/js/webgl-bg.js`,
  `assets/js/app.js`. (Home/collection also load `kolam.js` — rolls pages do NOT.)
  Rolls pages add `assets/js/rolls-data.js` then `assets/js/rolls.js` AFTER app.js.
  Stylesheets: `assets/css/styles.css` then (rolls pages only) `assets/css/rolls.css`.
  Cache-busting query `?v=v1787671063` is appended to asset URLs on existing pages;
  the deploy workflow rewrites `?v=...` to the commit hash. Use `?v=rolls1` on new pages.
* `app.js` (IIFE, `'use strict'`) provides: Lenis smooth scroll, theme toggle
  (`#theme-toggle`, `localStorage wj-theme`, sets `data-theme="light"` + `body.theme-light`),
  header `.is-scrolled`, drawer open/close, `.rv` reveal-on-scroll (adds `.is-in`),
  `toast()` (private), the enquiry docket (`.docket`, uses `data.js` COLLECTION —
  NOT used for rolls), site-wide "universal click → lightbox" on any `<img>` or
  `.card/.tile/.plate…` — rolls markup MUST opt out (see §7 app.js patches),
  catalogue flip viewer for the existing volumes (`[data-open-catalogue]`, `.catview`),
  coverflow. Everything is guarded by `if (element exists)`; it is safe on rolls pages.
* Design system (styles.css tokens, dark default, light theme via `[data-theme="light"]`):
  fonts `--f-display` Marcellus (headings) / `--f-text` Jost (text);
  colours `--ground #14110c`, `--ground-deep`, `--panel`, `--panel-2`, `--hairline`,
  `--hairline-2`, `--ink #f2edde`, `--ink-soft`, `--ink-dim`, `--gold #cfa14e`,
  `--gold-bright #e6c47f`, `--kaavi #b0492f`; `--night-*` tokens for surfaces that
  stay dark in light theme; module `--u: 8px`; `--frame: 15vw` side mat;
  motion `--beat 640ms`, `--beat-slow 1100ms`, `--ease cubic-bezier(.19,1,.22,1)`.
  Layout: `.section` (padding-block) → `.wrap` (a glass card: dark translucent
  panel, 1px gold hairline, radius 18px, inner padding; margin-inline `--frame`).
  Type: `.d1/.d2/.d3` display sizes, `.lead`, `.small`, `.cap` (uppercase tracked label),
  `.headgroup` (centred heading group), `.threshold` (hairline rule with gold dot),
  `.coverflow-pill` (small uppercase pill/eyebrow).
  Buttons: `.btn` (uppercase tracked outline with corner dots — ALWAYS include
  `<span class="dot-a"></span>` as first child), variants `.btn--fill` (gold fill,
  primary), `.btn--gold`, `.btn--ghost`, `.btn--wa`, `.btn--sm`.
  Filter chips: `.fchip` (+ `.is-active` / `aria-pressed="true"`). Form fields:
  `.dfield` (label + input with bottom hairline). Overlays: `.docket` (right drawer
  + `.docket-scrim`), `.catview` (full-screen viewer, `z-index 99999`), `.lightbox`.
  Reveal: add `.rv` (and `style="--i:n"` for stagger) to elements that should fade up.
  Contact: WhatsApp `https://wa.me/919677042903`, email `info@walljewels.com`,
  phone `+91 98400 64205`. Brand lines: "Wall Jewels Wallpaper World",
  "South India's Pioneers in Wallpapers Since 1978".

## 1. URL & file layout (MUST)

```
wallpaper-rolls/index.html                         → /wallpaper-rolls/
wallpaper-rolls/calculator/index.html              → /wallpaper-rolls/calculator/
wallpaper-rolls/<collection-slug>/index.html       → /wallpaper-rolls/athenic-india/
wallpaper-rolls/<collection-slug>/<design-slug>/index.html
                                                   → /wallpaper-rolls/athenic-india/12/
assets/rolls/collections.json                      hand-editable source of truth
assets/rolls/designs.json                          generated by extractors / hand-editable
assets/rolls/<collection-slug>/catalogue.pdf       the actual catalogue PDF
assets/rolls/<collection-slug>/cover.jpg           collection card image (≈1200px)
assets/rolls/<collection-slug>/pages/p001.jpg …    catalogue page renders, 1400px wide, q80
assets/rolls/<collection-slug>/pages/m001.jpg …    same pages, 800px wide (mobile)
assets/rolls/<collection-slug>/pages/t001.jpg …    page thumbnails, 200px wide
assets/rolls/<collection-slug>/designs/<design-slug>/full.jpg   native crop (hi-res source)
assets/rolls/<collection-slug>/designs/<design-slug>/web.jpg    ≤1200px long edge, q82
assets/rolls/<collection-slug>/designs/<design-slug>/thumb.jpg  480px wide, q78
assets/rolls/<collection-slug>/designs/<design-slug>/swatch.jpg optional pattern swatch
assets/rolls/<collection-slug>/designs/<design-slug>/detail.jpg optional close-up
assets/js/rolls-data.js                            generated: window.WJ_ROLLS = {...}
assets/js/rolls.js                                 runtime (vanilla, zero deps)
assets/css/rolls.css                               rolls styles (loaded after styles.css)
tools/rolls/build.mjs                              generator (Node 24, zero deps)
tools/rolls/prepare-images.py                      derivatives + page renders (PyMuPDF + Pillow)
tools/rolls/extract-athenic.py / extract-plain.py  catalogue-specific extractors
tools/rolls/test-calc.mjs                          unit tests (node --test)
tools/rolls/ADMIN-GUIDE.md                         how to add a collection
```

Design slug = design number lower-cased, every run of characters other than
`a-z0-9` replaced by `-`, trimmed of leading/trailing `-`. "6877/2" → "6877-2",
"12" → "12". Must be unique inside a collection (the generator MUST abort on
duplicates). Display the designNumber verbatim everywhere (never the slug).

Relative paths: nested pages reference assets with a depth prefix
(`../`, `../../`, `../../../`) exactly like `showrooms/*.html` do. The generator
computes `ROOT` per page and MUST set `<html lang="en" class="no-js" data-root="../../">`
so app.js can resolve the theme logo swap (see §7).

## 2. Data contract (MUST)

`assets/rolls/collections.json`:
```json
{ "collections": [ {
  "id": "athenic-india", "slug": "athenic-india", "name": "Athenic India",
  "tagline": "Premium wallpapers by Jenta Home Decor",
  "description": "one or two sentences shown on the collection page",
  "catalogueName": "ATHENIC INDIA.pdf",
  "catalogueFile": "assets/rolls/athenic-india/catalogue.pdf",
  "catalogueSizeMB": 12.4, "pageCount": 18,
  "coverImage": "assets/rolls/athenic-india/cover.jpg",
  "rollSize": 54, "coverage": 45, "pricePerSqFt": 55, "rollPrice": 2970,
  "unit": "sq.ft", "currency": "INR", "sort": 1, "published": true
} ] }
```
`assets/rolls/designs.json`:
```json
{ "designs": [ {
  "id": "athenic-india:12", "collectionId": "athenic-india",
  "designNumber": "12", "slug": "12",
  "image": "assets/rolls/athenic-india/designs/12/full.jpg",
  "web": "assets/rolls/athenic-india/designs/12/web.jpg",
  "thumbnail": "assets/rolls/athenic-india/designs/12/thumb.jpg",
  "swatch": "assets/rolls/athenic-india/designs/12/swatch.jpg",   // optional
  "detail": null,                                                  // optional
  "width": 1435, "height": 1420,                                   // of image (full.jpg)
  "cataloguePage": 5,                                              // 1-based; null if unknown
  "patternRepeat": "53 cm",                                        // optional
  "colourway": "Blush",                                            // optional
  "group": "8-10-12-13",                                           // optional: colourway family
  "needsReview": false, "reviewNote": ""                           // flagged for manual mapping
} ] }
```
Every field except `id, collectionId, designNumber, slug, image, thumbnail` is
optional; runtime and generator MUST tolerate missing optional fields.
Design order within a collection = natural numeric order of designNumber
(numeric-aware sort: 2 < 10; "5314/9" < "5314/10").

Generated `assets/js/rolls-data.js` (written by build.mjs, one line per record OK):
```js
window.WJ_ROLLS = {
  "generatedAt": "2026-09-14T00:00:00Z",
  "contact": { "whatsapp": "919677042903", "email": "info@walljewels.com" },
  "collections": [ {...collection as above...} ],
  "designs": [ {...design as above, plus "url": "wallpaper-rolls/athenic-india/12/"...} ]
};
```
`url` is root-relative WITHOUT leading slash; runtime prefixes `WJ_ROOT`
(`document.documentElement.dataset.root || ''`) to make links. Image paths
likewise are root-relative and MUST be prefixed with WJ_ROOT at runtime.

## 3. Calculation (MUST, shared by everything)

```
area  = width_in * height_in / 144           (sq.ft)
rolls = Math.ceil(area / collection.coverage - 1e-9)   // never use rollSize here
cost  = rolls * collection.rollPrice
```
Round UP always. No GST, delivery, installation or other charges — wallpaper cost only.
Validation: width and height are numbers > 0 (decimals allowed), max 2400 inches.
Empty, zero, negative, NaN or >2400 → no result, show a quiet inline message
("Enter a wall width in inches", "Enter a value between 1 and 2400"). Never NaN in UI.
Display: area with up to 2 decimals (`90`, `90.08`), rolls as integer,
money as `₹5,940` (en-IN grouping, no decimals), wall size as `120″ × 108″`.
Reference tests: 120×108 → 90 sq.ft; Athenic 2 rolls ₹5,940; Plain 2 rolls ₹2,850;
100 sq.ft Athenic → 3 rolls ₹8,910; 135×48 Athenic (45 sq.ft) → 1 roll.
Expose `window.WJRolls.calculate(widthIn, heightIn, collection)` →
`{ ok:true, area, rolls, cost }` or `{ ok:false, error:'…' }` (pure, no DOM),
and `window.WJRolls.formatINR(n)`, `window.WJRolls.slugify(str)`.
`tools/rolls/test-calc.mjs` imports the same pure function: put the pure maths in
`assets/js/rolls-calc.js`? NO — keep one runtime file. Instead rolls.js MUST expose
the pure functions on `window.WJRolls`, and test-calc.mjs loads rolls.js in a tiny
fake-window (`globalThis.window = globalThis; globalThis.document = {…stub…}`) — OR
simpler and REQUIRED: rolls.js starts with a UMD-ish block:
```js
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  root.WJRolls = Object.assign(root.WJRolls || {}, api);
})(typeof window !== 'undefined' ? window : globalThis, function () {
  /* pure: calculate, formatINR, slugify, sortDesigns, matchesQuery */
  return { calculate, formatINR, slugify, sortDesigns, matchesQuery };
});
(function () { 'use strict'; if (typeof document === 'undefined') return; /* DOM runtime */ })();
```
`node --test tools/rolls/test-calc.mjs` must pass (use `createRequire` to require rolls.js).

## 4. Page anatomy (generator output)

Shared: `<body class="page-rolls">`, skip link, annbar (text: "Wallpaper Rolls ·
Catalogues, designs & roll calculator · Wall Jewels Wallpaper World · Since 1978"),
header (WITH the Products menu — see §6), drawer, `<main id="main">`, footer,
enquiry panel markup (§4.5), scripts. Set `aria-current="page"` on the Wallpaper
Rolls link inside the Products menu on all rolls pages.

### 4.1 Landing `/wallpaper-rolls/` (title: "Wallpaper Rolls & Collections | Wall Jewels Wallpaper World")
meta description: "Explore Wall Jewels Wallpaper World wallpaper roll collections, browse catalogues and designs, and calculate the approximate rolls required for your walls."
1. Hero `.section.rolls-hero` → `.wrap`: `.coverflow-pill` eyebrow "Wall Jewels Wallpaper World · South India's Pioneers in Wallpapers Since 1978";
   `h1.d1` "Wallpaper Rolls"; `p.lead` "Explore Our Wallpaper Collections";
   quote paragraph: "Discover curated wallpaper collections, browse individual designs, view complete catalogues and calculate the approximate rolls required for your walls."
2. Collections `.section#collections` → `.wrap`: `h2.d2` "Our Collections"; grid `.rolls-collections` of
   `article.rolls-collection` cards (image-led: cover image top, then name `h3`, spec list
   `54 sq.ft / Roll · Approx. 45 sq.ft Wall Coverage · ₹2,970 / Roll` as a 3-row `.rolls-specs`,
   then 3 buttons: `EXPLORE DESIGNS` (`.btn.btn--fill`, link to collection page),
   `VIEW CATALOGUE` (`.btn` `button[data-open-rolls-catalogue="<slug>"]`),
   `CALCULATE REQUIREMENT` (`.btn` link `#calculator?collection=<slug>` → use
   `href="#calculator" data-calc-collection="<slug>"`; runtime preselects)).
   Card count is dynamic from data. Cards stack on mobile.
3. Design library `.section#designs` → `.wrap`: heading "Browse Individual Designs";
   toolbar `.rolls-toolbar`: search `input[type=search][data-rolls-search]`
   labelled "Search by Design Number" (placeholder "e.g. 12 or 14156"),
   chips `.rolls-filters` (`button.fchip[data-rolls-filter="all"]` "ALL" + one per collection,
   generated from data), count `.rolls-count[data-rolls-count]`.
   Gallery `.rolls-gallery[data-rolls-gallery][data-collection="all"]`: the generator emits
   the FIRST 48 cards statically (SEO + no-JS); runtime hydrates and renders the rest / filters.
   Card markup (MUST, used by both generator and runtime):
   ```html
   <a class="rolls-card" href="<ROOT>wallpaper-rolls/athenic-india/12/" data-design-id="athenic-india:12" data-no-lightbox>
     <span class="rolls-card__media"><img src="<ROOT>…/thumb.jpg" srcset="<ROOT>…/thumb.jpg 480w, <ROOT>…/web.jpg 1200w" sizes="(max-width: 600px) 50vw, (max-width: 1100px) 33vw, 25vw" width="1435" height="1420" alt="Athenic India wallpaper design 12" loading="lazy" decoding="async"></span>
     <span class="rolls-card__body"><span class="rolls-card__no">Design No. 12</span><span class="rolls-card__coll">Athenic India</span></span>
   </a>
   ```
   Runtime: clicking a card opens the quick-view modal (§4.6) unless modifier-click; keyboard Enter same.
   "Show more" button `.rolls-more[data-rolls-more]` appears when more than 48 match;
   also auto-loads via IntersectionObserver. Empty state `.rolls-empty` ("No design matches “xyz”. Try the design number printed in the catalogue, or WhatsApp us a photo.").
4. Calculator `.section#calculator` → `.wrap`: the calculator component (§4.4) with heading
   `h2.d2` "Calculate How Many Rolls You Need".
5. Disclaimer block `.rolls-disclaimer` (also directly under every calculator instance):
   `.cap` "Approximate calculation" then the two sentences verbatim:
   "Roll requirements are calculated based on approximate coverage and may vary depending on wall dimensions, pattern repeat, design alignment, cutting, wastage and installation requirements."
   "Final roll requirement will be confirmed by the Wall Jewels team before order confirmation."
6. SEO prose `.section.rolls-seo` → `.wrap`: `h2.d3` "Wallpaper Rolls in Chennai, from South India's Pioneers"
   + 2 short paragraphs naturally using: wallpaper rolls, wallpaper roll price, wallpaper catalogue,
   wallpaper collection, wallpaper calculator, designer wallpaper, imported wallpaper, wallpaper for home,
   wallpaper Chennai, Wall Jewels wallpaper. No stuffing. Mention the three Chennai showrooms and
   that customised printed wallpaper is a separate service (link `custom-wallpaper-printing.html`).
7. CTA band: `.btn.btn--wa` WhatsApp "WhatsApp the design team" (prefilled text
   "Namaste Wall Jewels — I'd like help choosing wallpaper rolls.") + link to `#calculator`.
JSON-LD: WebPage + BreadcrumbList (Home › Wallpaper Rolls) + ItemList of collections (each `@type: Product`/`ProductGroup` with name, url, image, offers price rollPrice INR, priceCurrency INR, availability InStock, brand Wall Jewels Wallpaper World).

### 4.2 Collection `/wallpaper-rolls/<slug>/` (title: "<Name> Wallpaper Rolls — Designs, Catalogue & Roll Calculator | Wall Jewels")
Hero: breadcrumb `.rolls-crumbs` (Home › Wallpaper Rolls › Name), eyebrow, `h1.d1` Name, lead = tagline,
spec row (Roll size / Approx. coverage / Price per roll / Book price ₹55 per sq.ft / N designs / catalogue pages),
buttons: VIEW CATALOGUE (opens viewer page 1), CALCULATE REQUIREMENT (#calculator), DOWNLOAD PDF (`.btn.btn--ghost`, `href` to catalogue.pdf, `target="_blank" rel="noopener"`, shows size in MB).
Then: designs section with the same toolbar/gallery (`data-collection="<slug>"`; chips still list ALL + every collection so the customer can hop; search is global — matching designs from other collections are shown with their collection label). Generator emits ALL of this collection's cards statically (they are the SEO payload) — cap at 120 static; runtime renders beyond.
Then calculator (collection preselected & locked via `data-lock-collection`) + disclaimer + enquiry CTA.
JSON-LD: CollectionPage + BreadcrumbList + ItemList of designs (Product entries; `image`, `sku` = designNumber, offers rollPrice).
Opening deep link: `?catalogue=1&page=N` opens the viewer on load at page N.

### 4.3 Design `/wallpaper-rolls/<slug>/<design-slug>/` (title: "<Name> Design <No> — Wallpaper Roll ₹<rollPrice> | Wall Jewels")
meta description: "<Name> wallpaper roll, design number <No>. <rollSize> sq.ft roll, approx. <coverage> sq.ft wall coverage, ₹<rollPrice> per roll. View the catalogue, calculate rolls and enquire with Wall Jewels Wallpaper World, Chennai."
Layout `.rolls-design` (two columns ≥ 900px, stacked on mobile):
* Media column: `figure.rolls-design__media[data-no-lightbox]` with `<img src="web.jpg" data-full="full.jpg" width height alt>`; clicking opens the simple zoom overlay `.rolls-zoom` (full.jpg, pinch/scroll zoom, close, Esc). Below: swatch chip (if `swatch`) and detail image (if `detail`), each small, labelled "Swatch" / "Close-up".
* Info column: breadcrumb; `.cap` collection name; `h1.d2` "Design No. 12"; definition list `.rolls-meta`:
  Collection · Design Number (verbatim, large, `.rolls-meta__no`) · Roll Size "54 sq.ft" · Approximate Wall Coverage "45 sq.ft" · Price "₹2,970 per roll" (+ "Book price ₹55 / sq.ft" small) · Pattern Repeat (if any) · Catalogue "ATHENIC INDIA.pdf · page 5" (if page known).
  If `needsReview` → small `.rolls-flag` note "Design number to be confirmed by the Wall Jewels team" (kept honest, never hidden).
  Buttons (stack on mobile, full-width): `CALCULATE ROLLS` (`.btn.btn--fill`, `href="#calculator"`),
  `ENQUIRE ABOUT THIS DESIGN` (`.btn.btn--wa button[data-rolls-enquire]`),
  `VIEW COMPLETE CATALOGUE` (`.btn button[data-open-rolls-catalogue="<slug>"]`),
  `VIEW IN CATALOGUE` (only when cataloguePage: `button[data-open-rolls-catalogue="<slug>"][data-page="5"]`).
* Below: calculator locked to this collection with the design number shown (`data-design="12"`), disclaimer, then "More from <Name>" strip `.rolls-strip` of up to 8 neighbouring designs (prev/next order) as `.rolls-card`s, plus prev/next links.
JSON-LD: Product (name "Athenic India Wallpaper Roll — Design 12", sku, image, brand, offers {price rollPrice, priceCurrency INR, availability InStock, url}), BreadcrumbList (Home › Wallpaper Rolls › Name › Design 12).
`?enquire=1` in the URL opens the enquiry panel on load. `#calculator` scrolls.

### 4.4 Calculator component (runtime renders INTO the mount; generator emits a no-JS fallback note inside)
```html
<div class="rolls-calc" data-rolls-calc data-collection="athenic-india" data-design="12" data-lock-collection>
  <noscript><p class="small">Enable JavaScript to use the roll calculator, or WhatsApp us your wall size.</p></noscript>
</div>
```
Runtime markup: `form.rolls-calc__form` with `.dfield`s: Wall Width (inches, `inputmode="decimal"`, `min=1 max=2400 step=any`), Wall Height (inches), Collection `<select>` (all published collections; disabled+shown when locked), Design Number (text; prefilled+readonly when `data-design`; otherwise optional free text "e.g. 12"), then `button.btn.btn--fill` "CALCULATE" (form submit; also live-updates on input once both numbers valid). Under the select show the selected collection's live facts: "54 sq.ft roll · approx. 45 sq.ft coverage · ₹2,970 per roll · ₹55 per sq.ft" (`.rolls-calc__facts`, updates on change).
Result `.rolls-estimate[aria-live=polite]` (hidden until valid): `.cap` "Your Wallpaper Estimate"; rows (`.rolls-estimate__row` `<span>label</span><b>value</b>`): Wall Size `120″ × 108″`; Wall Area `90 sq.ft`; Collection; Design Number (if any); Roll Size `54 sq.ft`; Approx. Coverage `45 sq.ft / Roll`; Estimated Rolls `2 Rolls`; Price Per Roll `₹2,970`; Estimated Wallpaper Cost `₹5,940` (large, gold, `.rolls-estimate__total`). Then `button.btn.btn--wa[data-rolls-quote]` "REQUEST A QUOTE" → opens enquiry panel with everything prefilled. Then the disclaimer block (§4.1.5). Inline errors `.rolls-calc__error` next to the field.
URL prefill: `?w=120&h=108&collection=plain&design=14156` supported on any page with a calculator; `#calculator` scrolls to it; `[data-calc-collection]` links set the select.

### 4.5 Enquiry panel (one per page, markup emitted by generator; runtime fills it)
Right-hand drawer like the docket: `.rolls-enquiry-scrim` + `aside.rolls-enquiry[aria-label="Wallpaper rolls enquiry"] inert`:
head (`.cap` "Wallpaper rolls enquiry", `h2` "Enquire about this design" / "Request a quote", close `button.tool[data-rolls-enquiry-close]`),
summary card `.rolls-enquiry__summary` (Collection, Design Number, Wall Size, Wall Area, Estimated Rolls, Estimated Cost — rows only when known),
fields (`.dfield`): Name* `#re-name`, Phone Number* `#re-phone` (tel, inputmode tel), Email `#re-email`, Wall Width `#re-w` (inches), Wall Height `#re-h`, Message `#re-msg` (textarea). Width/height prefilled from the calculator; editing them recalculates the summary live (same calculate()).
Validation: name required; phone OR email required; dims optional but if given must validate.
Buttons: `button.btn.btn--wa[data-rolls-enquiry-send]` "SEND VIA WHATSAPP" (opens `https://wa.me/919677042903?text=<encoded>` in a new tab — this IS the site's enquiry system) and `a.btn.btn--ghost[data-rolls-enquiry-mail]` "SEND BY EMAIL" (`mailto:info@walljewels.com?subject=…&body=…`, same text). Small print: "Or call +91 98400 64205 · Nothing here is an order — final roll count and price are confirmed by the Wall Jewels team."
Message text (exact structure, omit lines whose value is unknown):
```
Namaste Wall Jewels — Wallpaper Rolls enquiry
Collection: Athenic India
Design Number: 12
Wall Width: 120 in
Wall Height: 108 in
Wall Area: 90 sq.ft
Estimated Rolls: 2 (approx. 45 sq.ft coverage per roll)
Estimated Cost: ₹5,940 (2 × ₹2,970 per roll)
Name: …
Phone: …
Email: …
Message: …
Design page: https://www.walljewels.in/wallpaper-rolls/athenic-india/12/
Please confirm the exact roll requirement and quote.
```
Opening: `[data-rolls-enquire]` (design page; uses page design + last calculator values), `[data-rolls-quote]` (from any calculator result), `?enquire=1`. Focus moves into the panel; Esc / scrim / close returns focus.

### 4.6 Quick-view modal (runtime only) `.rolls-modal[role=dialog]`
Opened from gallery cards: large image (web.jpg, `data-full` full.jpg → click opens zoom overlay), collection, "Design No. 12", 3 spec lines (roll size / coverage / price), buttons: CALCULATE ROLLS (→ design page `#calculator`), ENQUIRE ABOUT THIS DESIGN (→ design page `?enquire=1`), VIEW IN CATALOGUE (opens viewer at page, when known; else VIEW COMPLETE CATALOGUE page 1), OPEN DESIGN PAGE (`.textlink`). Prev/next within the current filtered list (arrows + keyboard + swipe). Esc/backdrop/close. Focus trap; restore focus on close. Do NOT change history.

### 4.7 Catalogue viewer (runtime only) `.rolls-viewer[role=dialog][aria-modal=true]`
Opened by `[data-open-rolls-catalogue="<slug>"]` (+ optional `data-page="N"`), by `?catalogue=1&page=N` on collection pages, and by `?catalogue=<slug>&page=N` on the landing page.
Full-screen overlay (`z-index 99999` like `.catview`, dark `rgba(8,9,12,.97)`), top bar: title "<Name> — Catalogue" + "ATHENIC INDIA.pdf", page control `input[type=number]` "N" / total (Enter jumps), buttons: Zoom out (−), Zoom in (+), Fit (1:1 reset), Full screen (Fullscreen API on the overlay; toggle icon; hide the button if `!document.fullscreenEnabled`), Open PDF (`<a target=_blank rel=noopener href=catalogue.pdf>` — opens the actual PDF inline in a new tab, never forces download), Close (×).
Stage `.rolls-viewer__stage` (scrollable both axes, `touch-action: pan-x pan-y`): the current page `<img>` fitted to stage width at zoom 1 (tall Athenic pages scroll vertically inside the stage — that is expected), zoom steps 1 → 1.5 → 2 → 3 (and pinch-zoom via pointer events; double-tap toggles 1↔2). Chooses `m###.jpg` when stage width × devicePixelRatio ≤ 900 else `p###.jpg`. Preloads previous/next page. Prev/next round buttons at the sides (`.rolls-viewer__nav`), keyboard ← → (page), +/- (zoom), Esc (close), swipe left/right on mobile (only when not zoomed beyond 1). Bottom thumbnail rail `.rolls-viewer__rail` (t###.jpg, current highlighted, click to jump; hidden below 720px). Page counter updates. `document.body.style.overflow='hidden'` while open; restore focus on close. Loading state: skeleton + spinner-less fade. Works with a single page catalogue.

## 5. Runtime (assets/js/rolls.js) responsibilities
Reads `window.WJ_ROLLS`; `WJ_ROOT = document.documentElement.dataset.root || ''`; utilities:
`calculate`, `formatINR`, `slugify`, `sortDesigns` (numeric-aware), `matchesQuery(design, q)` —
normalise both sides by removing spaces, `-`, `/`, `.` and lower-casing; a design matches when its
normalised number contains the normalised query; exact matches sort first, then prefix, then contains.
Components (each initialised only if its mount exists): gallery (toolbar/search/filter/pagination/
hydration; also reads `?q=` and `?collection=` from the URL), quick-view modal, calculator(s) (multiple
per page allowed), enquiry panel, catalogue viewer, zoom overlay, Products nav toggle (if not already
handled by app.js — see §7; do not double-bind). Use event delegation; no globals except `WJRolls`.
Never inject unescaped strings: HTML-escape every data value with an `esc()` helper.
Performance: gallery renders in 48-card batches via DocumentFragment; images `loading="lazy"`.
Accessibility: every control keyboard-operable; dialogs use `role="dialog"`, `aria-modal`, focus trap,
Esc; buttons ≥ 44px tap targets on touch; visible focus (site style `:focus-visible` gold dotted).

## 6. Site integration (every existing page)
Header nav: insert after the "Collection" link, in ALL pages that have `nav.nav`
(index.html, collection.html, custom-wallpaper-printing.html, luxury-wallpapers.html,
wall-murals.html, wallpaper-buying-guide.html, wallpaper-chennai.html, wallpaper-installation.html,
wallpaper-manufacturer-india.html, webgl-preview.html, showrooms/*.html (use `../` prefix there)):
```html
<div class="nav__menu" data-nav-menu>
  <button class="nav__trigger" type="button" aria-haspopup="true" aria-expanded="false" aria-controls="nav-products">Products <svg class="nav__chev" width="10" height="10" viewBox="0 0 10 10" aria-hidden="true"><path d="M2 3.5 L5 6.5 L8 3.5" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg></button>
  <div class="nav__panel" id="nav-products">
    <a href="wallpaper-rolls/">Wallpaper Rolls <span class="nav__hint">Catalogues · designs · roll calculator</span></a>
  </div>
</div>
```
CSS (add to styles.css, section "Products menu"): trigger styled exactly like `.nav a`; panel absolutely
positioned under the trigger, `--panel-2` glass background, gold hairline, radius 8px, min-width 260px,
opens on `:hover`, `:focus-within` and `[aria-expanded="true"]`; light-theme variants mirror
`[data-theme="light"] .header .nav a`. Header must not overflow between 1081px and 1400px — if the
nav is too wide, reduce `.nav a` / `.nav__trigger` padding at `max-width: 1300px` (media query).
Drawer (`.drawer__nav`): after Collection add a group label `<span class="drawer__group">Products</span>`
and `<a href="wallpaper-rolls/">Wallpaper Rolls <span class="num">2 collections</span></a>`.
Footer: in the "Shop & Murals" column (index) / "Pages" column (secondary pages) add
`<li><a href="wallpaper-rolls/">Wallpaper Rolls</a></li>` right after the first item.
sitemap.xml: generator maintains a block between `<!-- rolls:start -->` and `<!-- rolls:end -->`
(landing 0.9 weekly, calculator 0.7, collections 0.85 weekly, designs 0.6 monthly, with image entries).
llms.txt / llms-full.txt: add a "Wallpaper Rolls" line (URL + one sentence).
.github/workflows/deploy.yml: also copy `wallpaper-rolls/` into dist (`cp -r assets showrooms wallpaper-rolls dist/`).
.htaccess: add `<FilesMatch "\.pdf$"> Header set Cache-Control "public, max-age=604800"` and
`Header set Content-Disposition "inline"` for pdf, plus `AddType application/pdf .pdf`.
Do NOT touch the custom-wallpaper visualiser (#visualiser / #custom), the docket, collection.html data
or any existing route.

## 7. app.js patches (minimal, backwards compatible)
1. Near the top: `const ROOT = document.documentElement.dataset.root || '';` then use
   `${ROOT}assets/img/brand/logo-…png` in `applyTheme`, `${ROOT}collection.html` in `openSearch`
   fallback, `${ROOT}index.html?visualise=` in the lightbox calc fallback. Also the `wordmark`
   click handler compares `location.pathname` — leave as is.
2. Universal lightbox click listener: FIRST line → `if (e.target.closest('[data-no-lightbox], .page-rolls .rolls-card, .rolls-viewer, .rolls-modal, .rolls-enquiry, .rolls-zoom')) return;`
   and in `buildGalleryList` fallback branches skip images inside `[data-no-lightbox]`.
3. Products menu: click/tap toggles `aria-expanded` on `.nav__trigger`; click outside / Esc closes;
   (CSS handles hover/focus). Keep it inside app.js so every page gets it; rolls.js MUST NOT bind it again.
Nothing else in app.js changes.

## 8. Style (assets/css/rolls.css)
Match the house: image-led, minimal, generous whitespace on the 8px module, gold hairlines only,
no gradients beyond what styles.css already uses, no icons other than thin line SVGs already in use,
no cheap card shadows — cards are the artwork itself with a hairline and a quiet caption.
Gallery grid: `repeat(auto-fill, minmax(min(100%, 240px), 1fr))`, 2 columns at ≤600px (min 150px),
square-ish media with `object-fit: cover` and `aspect-ratio: 1/1` (Athenic room shots are ~1:1;
Plain swatches are portrait — use `object-fit: cover` on the card, `contain` in modal/design page).
Hover: image scale 1.03 over `--beat`, caption gold — nothing louder. Respect `prefers-reduced-motion`.
Both themes: use tokens; test light theme (`[data-theme="light"]`) explicitly — text on panels must stay legible.
Touch targets ≥ 44px. All inputs 16px font on mobile (no iOS zoom). Buttons wrap/stack at ≤ 600px.

## 9. Generator (tools/rolls/build.mjs)
`node tools/rolls/build.mjs` (from site root; zero deps; ESM). Steps: read JSON → validate
(unique slugs, required fields, referenced images exist → warn, catalogue exists) → write
`assets/js/rolls-data.js` → render pages from template functions (string templates in the same
file or `tools/rolls/templates/*.mjs`) → update sitemap block → print a summary
(collections, designs, pages written, warnings). Idempotent; deletes stale design folders under
`wallpaper-rolls/<slug>/` that no longer exist in data. `--check` flag: validate only.
HTML-escape all data. Keep generated HTML formatted (2-space indent) and readable.

## 10. Image pipeline (tools/rolls/prepare-images.py)
`python tools/rolls/prepare-images.py [--collection slug] [--force]`: for each collection, render
catalogue pages (PyMuPDF, `dpi` chosen so width = 1400px, JPEG q80 → p###.jpg; 800px q76 → m###.jpg;
200px q70 → t###.jpg), and for each design folder containing `full.jpg` produce `web.jpg`
(≤1200px long edge q82, progressive) and `thumb.jpg` (480px wide q78) with Pillow (LANCZOS);
skip if up to date (mtime). Writes `width/height` back into designs.json entries when missing.
Never alter full.jpg. Print a summary. Also `--pdf-only` / `--designs-only`.

## 11. Testing expectations
`node --test tools/rolls/test-calc.mjs` green. Pages validate visually at 390px, 768px, 1280px, both
themes. Every button in §4 does what it says. No console errors. Existing pages unchanged apart from §6.
