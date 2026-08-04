# Wall Jewels Wallpaper World — new website

Static site. No build step, no framework, no dependencies. Two HTML files, one CSS file,
two JS files. It will run on any host — Netlify, Vercel, Cloudflare Pages, GoDaddy, cPanel,
or the same server the current site is on.

```
walljewels-site/
├─ index.html            landing page
├─ collection.html       filterable collection browser
└─ assets/
   ├─ css/styles.css     the whole design system
   └─ js/
      ├─ data.js         ← all content you'll want to edit
      ├─ app.js          behaviour + the collection deck
      └─ background.js   plasma shader
```

## The collection deck

The premium collection on the landing page is a **coverflow arc carousel**, built the same
way as the Consultancy Solutions block on thevisionarys.com: every card sits at the same
absolute origin and is separated purely by `transform` and `z-index`, so sliding never
triggers a layout pass.

Controls: arrows, dots, click a side card to centre it, arrow keys, drag with a mouse,
swipe on touch. Autoplay runs every 4.6s and stops on hover, focus, or any interaction.
Only the centred card is a tab stop; the rest are `aria-hidden` with `tabindex="-1"`.

Tune the geometry with the CSS variables on `.deck` (`assets/css/styles.css`, section 22):

| variable | what it does |
| --- | --- |
| `--card-w` / `--card-h` | card size |
| `--step` | horizontal gap between fanned cards |
| `--tilt` | degrees of rotation per card away from centre |

`VISIBLE` in `app.js` sets how many cards fan out either side (currently 3). Which designs
appear is the `picks` array — just names from `COLLECTION`.

## The background

Two fixed, non-interactive layers behind everything (`z-index: -1`):

1. **A WebGL shader** — `assets/js/background.js`, five effects to choose from.
2. **Colour splash** — pure CSS, four layered radial washes with a slow 34s drift.
   `.splash` in the stylesheet. Also the standalone fallback.

Visitors pick the effect from the swatch button in the header, next to the light/dark
toggle. The choice is remembered in `localStorage` and carries across pages.

| Effect | Character |
| --- | --- |
| **Plasma** | Slow molten drift. The default. |
| **Silk** | Flowing fabric bands, quiet and horizontal. |
| **Aurora** | Soft drifting colour clouds. The calmest. |
| **Damask** | A living wallpaper repeat, on a half-drop like real wallpaper. |
| **Marble** | Veined stone, nodding to the Calacatta range. |
| **Off** | No shader. Splash gradients only, no animation. |

All five use the same warm brand palette (`PALETTE` in `background.js`) — reds, terracotta
and gold, not the indigo-purple from the Visionarys site — and repaint on theme switch.

**On intensity.** The first version was too pale in light mode to see, which was a real
bug: the wash worked out to about 16% coverage of an almost-white peach, a colour distance
of ~14 from the paper background. It's now a properly saturated terracotta/gold and every
effect is normalised to 13–20% coverage, giving a distance of 28–35 in light mode. The
per-effect `gain` values do that normalisation — Aurora needs a much lower gain than the
rest because its three blobs sum toward full coverage across most of the frame.

Measured text contrast over the wash, all five effects × both themes: body ≥ 14.8:1,
muted ≥ 5.99:1, small mono labels ≥ 5.0:1. Nothing below WCAG AA.

Two dials if you want it different:

- Overall strength: `--plasma-op` in the stylesheet (`.88` light, `.82` dark).
- Per-effect strength: the `gain` value on each entry in `MODES`.
- Remove entirely: delete the `.bg-layers` block from both HTML files.

It degrades on purpose: no WebGL hides the picker and the splash gradients carry it alone
(tested by blocking `webgl`, `webgl2` and `experimental-webgl`); reduced-motion draws one
static frame with no animation loop; a hidden tab parks the loop. The shader renders at
0.5× and upscales, since it's a soft blur — full resolution would just burn GPU.

## Run it locally

```bash
python -m http.server 5178
```

Then open <http://localhost:5178>. (It must be served over http, not opened as a `file://`
path, or the room/theme deep links won't behave.)

## Deploy

Upload the folder as-is to your web root. Nothing to compile.

**Your current live site has not been touched.** This is a separate build, ready to go
whenever you are.

---

## Phase 2 — swapping in your own photographs

Everything image-related lives in one place: `assets/js/data.js`.

1. Put your photos in `assets/img/collection/`.
2. In `data.js`, change the `img` field:

```js
{ t: 'Calacatta Gold', room: 'living', theme: 'texture',
  blurb: '…',
  img: 'assets/img/collection/calacatta-gold.jpg',   // ← this line
  tone: ['#EDE6DA','#BFA46F'], tag: 'Bestseller' },
```

That's it — the landing page showcase, the room cards, the collection grid and the counts
all update themselves.

**Useful details:**

- `img: null` draws a generated wallpaper swatch instead of a photo. Three pooja-room
  entries use this right now (Om Mandala, Lakshmi Kamal, Ganesha Relief) because I would
  not put an unverified stock photo behind a deity. Replace with your own images.
- `tone: ['#light','#dark']` is the two-colour pair used for that swatch, and as the
  fallback if a photo ever fails to load. No design will ever render as a broken image.
- `tag:` is the little red corner label ("Bestseller", "New"). Omit it for no label.
- To add a design, copy any line in `COLLECTION`. To add a whole room or theme, add an
  entry to `ROOMS` or `THEMES` — filters, footer links and counts pick it up automatically.

The photos you sent me (the Buddha 3D mural, the Spiderman wall, the balcony vertical
gardens, Palazzo, the IMAX foyer) are the strongest assets you have. They belong in the
**Selected work** section of `index.html` — search for `class="project__media"` and swap
the four `src` values.

## Placeholder images

All current photography is Unsplash (free licence, hotlink-permitted). Every URL was
load-tested; there are no broken images. They are placeholders — replace them with your
own work in phase 2.

---

## Things to confirm

- **Phone numbers.** The site currently uses `+91 98400 64205 / 06 / 07` (from your
  existing website) for the showrooms, and `+91 99207 70172` (from your new WJWP posters)
  for WhatsApp and custom-printing enquiries. Tell me if that split is wrong.
- **Email.** Using `info@walljewels.com`.
- **Branch addresses.** The company profile says three Chennai branches and a 5,000 sq.ft
  flagship at Parry's, but gives no street addresses. The "Visit" section has placeholder
  copy for branches two and three — send me the addresses and I'll put them in.
- **Enquiry form.** It currently opens a pre-filled WhatsApp message so no enquiry is lost.
  If you want it to email you instead, point it at a Formspree endpoint or your CRM —
  see the marked block in `assets/js/app.js`.
- **Rajinikanth's residence.** It's in the company profile, so I've included it. Worth a
  quick check that you're happy to name it publicly on the website.

## Notes on the build

- Light and dark mode. Follows the OS setting on first visit, then remembers the choice.
  Toggle is in the header.
- All text passes WCAG AA contrast in both themes (lowest measured ratio: 4.62:1).
- No horizontal scroll at 375px through to 1440px+.
- Respects `prefers-reduced-motion`.
- If JavaScript fails to load, all content still renders — nothing is hidden behind JS.
