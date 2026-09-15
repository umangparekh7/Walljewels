# Wallpaper Rolls — Admin Guide

How to add, update and publish a wallpaper roll collection on walljewels.in.
Written for someone comfortable with folders, files and copying text — no
programming needed. Everything below is done from the site folder:

```
walljewels-site\
```

Open a terminal in that folder (in File Explorer: right-click the folder →
"Open in Terminal"). All commands in this guide are typed there.

---

## 1. How a collection is put together

Each collection is one folder of source files plus two entries in two JSON
text files. Everything else on the website is generated from those.

```
assets\rolls\
  collections.json                     ← one entry per collection (you edit this)
  designs.json                         ← one entry per design (you edit this)
  <collection-slug>\
    catalogue.pdf                      ← the supplier catalogue (you add this)
    cover.jpg                          ← card image, optional (made for you if missing)
    pages\                             ← catalogue page images (generated, do not edit)
    designs\
      <design-slug>\
        full.jpg                       ← the design image (you add this)
        swatch.jpg                     ← optional pattern swatch (you add this)
        detail.jpg                     ← optional close-up (you add this)
        web.jpg  thumb.jpg  …          ← generated, do not edit
```

You provide: the PDF, the design images and the two JSON entries.
Two commands then produce every page image, thumbnail, web page and sitemap
entry. Nothing about a collection is typed into the web pages by hand.

---

## 2. Naming rules

**Collection slug** — the folder name and the web address
(`walljewels.in/wallpaper-rolls/<slug>/`).

* Lower-case letters, digits and hyphens only: `athenic-india`, `plain`,
  `royal-textures-2`.
* Choose it once. Changing a slug later changes every address on Google.

**Design slug** — the folder name for one design, derived from the design
number printed in the catalogue:

* Lower-case; every run of characters other than `a–z` `0–9` becomes one
  hyphen; no hyphen at the start or end.
* `12` → `12`, `6877/2` → `6877-2`, `KP 108` → `kp-108`.
* Must be unique inside its collection.

The customer always sees the real design number (`6877/2`) — the slug is only
used for folders and addresses.

---

## 3. Add the catalogue PDF

1. Create the folder `assets\rolls\<collection-slug>\`.
2. Copy the supplier PDF into it and rename it to exactly `catalogue.pdf`.
3. Note two facts you will need for the JSON entry: the **number of pages**
   and the **file size in MB** (right-click → Properties). The tools will warn
   you if either is wrong.

Tips

* Keep the PDF as small as the supplier can give it — it is offered as a
  download on the collection page. Anything under ~30 MB is fine.
* Pages can be any shape. Very tall strip pages (as in Athenic India) are
  handled; the viewer simply scrolls them.

---

## 4. Cover image (optional)

`assets\rolls\<collection-slug>\cover.jpg` is the picture on the collection
card. If you do not supply one, it is created from page 1 of the PDF (the top
part of the page when page 1 is a tall strip). To use your own image, save a
JPEG about 1200 px wide there before running the tools. To regenerate it from
the PDF later, delete `cover.jpg` and run the image tool again.

---

## 5. Add the design images

For every design you want on the site:

1. Create `assets\rolls\<collection-slug>\designs\<design-slug>\`.
2. Save the design image there as `full.jpg`.
   * JPEG, the best quality you have — ideally 1400 px or more on the long
     edge. It is the zoom image on the design page; smaller sizes are made
     from it automatically and it is never altered.
   * A crop of the catalogue page, a supplier photograph or a room shot are
     all fine. One image per design.
3. Optional extras in the same folder: `swatch.jpg` (a flat pattern swatch)
   and `detail.jpg` (a close-up). They appear under the main image labelled
   "Swatch" and "Close-up".

For the two current collections the design images were cut from the
catalogue PDFs with the extractors in this folder (`extract-athenic.py`,
`extract-plain.py`). Those are specific to the layout of those two books;
for a new catalogue, cut the images by hand (any image editor) or ask the
supplier for design images.

---

## 6. Add the collection entry — `assets\rolls\collections.json`

Open the file in Notepad (or any text editor), find the `"collections": [`
list and add a new block. Copy an existing one and change the values.

```json
{
  "id": "royal-textures",
  "slug": "royal-textures",
  "name": "Royal Textures",
  "tagline": "Woven textures and metallic plains for formal rooms",
  "description": "One or two sentences shown at the top of the collection page. Say what the book is about and the roll size.",
  "catalogueName": "ROYAL TEXTURES.pdf",
  "catalogueFile": "assets/rolls/royal-textures/catalogue.pdf",
  "catalogueSizeMB": 18.6,
  "pageCount": 24,
  "coverImage": "assets/rolls/royal-textures/cover.jpg",
  "rollSize": 57,
  "coverage": 50,
  "pricePerSqFt": 30,
  "rollPrice": 1710,
  "unit": "sq.ft",
  "currency": "INR",
  "sort": 3,
  "published": true
}
```

| Field | What to put |
|---|---|
| `id`, `slug` | The collection slug (both the same). |
| `name` | Display name, as the customer should read it. |
| `tagline` | One line under the name. |
| `description` | One or two sentences for the collection page. |
| `catalogueName` | The PDF's original name, shown next to "Download PDF" and in the viewer title. |
| `catalogueFile` | Always `assets/rolls/<slug>/catalogue.pdf` (forward slashes). |
| `catalogueSizeMB` | File size in MB, one decimal. Shown on the download button. |
| `pageCount` | Number of pages in the PDF. |
| `coverImage` | Always `assets/rolls/<slug>/cover.jpg`. |
| `rollSize` | Printed roll size in sq.ft (e.g. 54 or 57). Shown to the customer. |
| `coverage` | Usable wall coverage per roll in sq.ft after trimming and matching (e.g. 45 or 50). **This is the number the calculator divides by.** |
| `pricePerSqFt` | Book price per sq.ft, shown as "Book price ₹30 / sq.ft". |
| `rollPrice` | Price per roll in rupees, no decimals. Normally `rollSize × pricePerSqFt` (57 × 30 = 1710). **This is the number the calculator multiplies by.** |
| `unit`, `currency` | Leave as `"sq.ft"` and `"INR"`. |
| `sort` | Order on the landing page, lowest first. |
| `published` | `true` to show the collection; `false` hides it everywhere without deleting anything. |

Watch the commas: every block except the last one in the list ends with `},`.
If the file has a mistake, the tools stop and tell you the line.

---

## 7. Add the design entries — `assets\rolls\designs.json`

One block per design, inside the `"designs": [` list. Copy an existing block
and change the values.

```json
{
  "id": "royal-textures:rt-204",
  "collectionId": "royal-textures",
  "designNumber": "RT 204",
  "slug": "rt-204",
  "image": "assets/rolls/royal-textures/designs/rt-204/full.jpg",
  "web": "assets/rolls/royal-textures/designs/rt-204/web.jpg",
  "thumbnail": "assets/rolls/royal-textures/designs/rt-204/thumb.jpg",
  "swatch": null,
  "detail": null,
  "cataloguePage": 7,
  "patternRepeat": "64 cm",
  "colourway": "Ivory",
  "group": null,
  "needsReview": false,
  "reviewNote": ""
}
```

| Field | What to put |
|---|---|
| `id` | `<collection-slug>:<designNumber>` exactly as printed, e.g. `plain:6877/2`. |
| `collectionId` | The collection slug. |
| `designNumber` | The number exactly as printed in the catalogue. This is what customers see and search for. |
| `slug` | The design slug (section 2). Must match the folder name. |
| `image` | `assets/rolls/<slug>/designs/<design-slug>/full.jpg`. |
| `web`, `thumbnail` | Same folder, `web.jpg` and `thumb.jpg` (generated for you, but the paths are listed here). |
| `swatch`, `detail` | Path to `swatch.jpg` / `detail.jpg` if you added them, otherwise `null`. |
| `width`, `height` | Leave out — filled in automatically from `full.jpg`. |
| `cataloguePage` | Page of the PDF where the design appears (1 = first page), or `null` if unknown. Powers "View in catalogue". |
| `patternRepeat` | e.g. `"53 cm"`, or `null`. |
| `colourway` | Colour name, or `null`. |
| `group` | Optional label linking colourways of one pattern (e.g. `"8-10-12-13"`), or `null`. |
| `needsReview` | `false` normally. `true` when you are not yet sure the design number is right (see section 12). |
| `reviewNote` | A note to yourself about why it is flagged; `""` otherwise. |

Required: `id`, `collectionId`, `designNumber`, `slug`, `image`, `thumbnail`.
Everything else may be left out or set to `null`.

Designs are shown in natural numeric order of their design number (2 before
10; 5314/9 before 5314/10) whatever order they are in the file.

---

## 8. Make the images — `prepare-images.py`

```
python tools\rolls\prepare-images.py
```

This:

* renders every page of every published catalogue into three sizes
  (`pages\p001.jpg` 1400 px for desktop, `m001.jpg` 800 px for phones,
  `t001.jpg` 200 px thumbnails for the viewer's film-strip);
* creates `cover.jpg` when missing;
* makes `web.jpg` and `thumb.jpg` (and `swatch-web.jpg` / `detail-web.jpg`)
  from every `full.jpg`;
* writes the measured `width` and `height` into `designs.json`;
* prints a summary table and a list of warnings.

It only redoes work whose source changed, so it is quick to run again after
adding one design. Useful variants:

```
python tools\rolls\prepare-images.py --collection royal-textures   only this collection
python tools\rolls\prepare-images.py --force                       redo everything
python tools\rolls\prepare-images.py --pdf-only                    catalogue pages and cover only
python tools\rolls\prepare-images.py --designs-only                design images and designs.json only
```

Read the warnings. The common ones:

| Warning | Meaning |
|---|---|
| `catalogue not found` | `catalogue.pdf` is missing or misnamed in that folder. |
| `pageCount … PDF has …` | Fix `pageCount` in collections.json. |
| `catalogueSizeMB … file is …` | Fix `catalogueSizeMB` in collections.json. |
| `designs/<x>/ has no full.jpg` | A design folder without its image. |
| `designs.json <id>: … full.jpg is missing` | An entry points to a folder or file that is not there. |
| `… exists but no designs.json entry references it` | A design folder you have not added to designs.json yet. |

The whole run for both current collections takes about 15 seconds.

---

## 9. Build the pages — `build.mjs`

```
node tools\rolls\build.mjs
```

This reads the two JSON files and writes:

* `assets\js\rolls-data.js` — the data the pages use for search, filtering
  and the calculator;
* `wallpaper-rolls\index.html`, `wallpaper-rolls\calculator\index.html`,
  `wallpaper-rolls\<slug>\index.html` and one
  `wallpaper-rolls\<slug>\<design-slug>\index.html` per design;
* the Wallpaper Rolls block inside `sitemap.xml`.

It checks the data first (unique slugs, required fields, images that exist)
and stops with a clear message if something is wrong. To check without
writing anything:

```
node tools\rolls\build.mjs --check
```

Design pages for designs you removed from `designs.json` are deleted on the
next build, so the site never keeps orphaned pages.

Run the two commands in this order whenever you change anything:
**images first, then build.**

---

## 10. Preview on your computer

```
python tools\serve.py 5178
```

Then open <http://localhost:5178/wallpaper-rolls/> in a browser. Leave the
terminal window open while you look; press `Ctrl+C` to stop it.

Check:

* the new collection card, its cover and its three buttons;
* "View catalogue" opens the viewer and pages through the whole book;
* the design cards, quick view, and each design page;
* the calculator with the new collection selected (try 120 × 108 inches);
* the WhatsApp enquiry text from "Request a quote";
* both the dark and the light theme (toggle in the header), and a phone-width
  window.

The roll maths has its own automatic test; if you ever suspect it, run:

```
node --test tools\rolls\test-calc.mjs
```

---

## 11. Publish

The site is published from the `main` branch of its Git repository. Every push
to `main` runs the deploy workflow, which copies the web pages, `assets\`,
`showrooms\` and `wallpaper-rolls\` to the live server and stamps every asset
link with a fresh version so browsers pick up the change.

```
git add -A
git commit -m "Add Royal Textures wallpaper roll collection"
git push origin main
```

Allow a few minutes, then check <https://www.walljewels.in/wallpaper-rolls/>.
Catalogue PDFs are served inline (they open in the browser tab rather than
downloading) and cached for a week.

Commit everything the tools produced — page images, covers, `web.jpg` /
`thumb.jpg`, `rolls-data.js`, the `wallpaper-rolls\` pages and `sitemap.xml`
— along with your source files. The live site is a plain copy of the
repository; nothing is generated on the server.

---

## 12. Flagged designs (`needsReview`)

Set `"needsReview": true` on a design whose number you could not confirm
(for example a crop where the printed number was cut off). The design is
still published — it has a page, appears in the gallery and the calculator
works — but the design page shows a small honest note:

> Design number to be confirmed by the Wall Jewels team

Once you have confirmed the number, correct `designNumber` (and `id`, `slug`
and the folder name if they change), set `needsReview` back to `false`,
clear `reviewNote`, then run the two commands and publish. Flagged designs
are never hidden and never silently renamed.

---

## 13. How the calculator works

Every calculator on the site uses one rule, driven only by the collection's
`coverage` and `rollPrice`:

```
wall area (sq.ft) = width in inches × height in inches ÷ 144
rolls needed      = wall area ÷ coverage, rounded UP to a whole roll
estimated cost    = rolls needed × rollPrice
```

Example, Athenic India (coverage 45, roll price ₹2,970):
a 120″ × 108″ wall is 90 sq.ft → 90 ÷ 45 = 2 rolls → ₹5,940.
A 100 sq.ft wall → 2.22 → 3 rolls → ₹8,910.

Notes

* `rollSize` (54 sq.ft printed on the roll) is shown for information; the
  division always uses `coverage`, which already allows for trimming and
  pattern matching.
* The result is always rounded up; there are no half rolls.
* No GST, delivery or installation is included — wallpaper cost only. The
  disclaimer under every calculator says so, and every enquiry ends with a
  request for the team to confirm the final count.
* Inputs must be between 1 and 2400 inches; anything else shows a quiet
  message instead of a result.
* Nothing is hard-coded per collection. Change `coverage` or `rollPrice` in
  `collections.json`, rebuild, publish — every page, card and estimate
  follows.

---

## 14. Everyday changes

| Task | Do this |
|---|---|
| Change a price | Edit `rollPrice` (and `pricePerSqFt`) in collections.json → `node tools\rolls\build.mjs` → publish. |
| Add one design | Add the folder with `full.jpg`, add its designs.json entry → both commands → publish. |
| Remove a design | Delete its entry from designs.json (and the folder if you like) → both commands → publish. |
| Replace a catalogue PDF | Overwrite `catalogue.pdf`, update `pageCount` / `catalogueSizeMB` → both commands → publish. Pages are re-rendered automatically because the PDF is newer. Delete `cover.jpg` first if you want a new cover from the new page 1. |
| Hide a collection temporarily | Set `"published": false` → both commands → publish. Its files stay in place. |
| Re-order collections | Change `sort` values → build → publish. |

---

## 15. Requirements

* **Python 3** with the `pymupdf` and `pillow` packages
  (`pip install pymupdf pillow` once).
* **Node.js** 20 or newer (no packages to install).
* **Git** with access to the site repository.

If `python` or `node` is "not recognised", install them from python.org and
nodejs.org and reopen the terminal.
