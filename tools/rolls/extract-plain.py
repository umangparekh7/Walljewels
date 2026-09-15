"""Extract the individual designs of the Plain catalogue.

The Plain catalogue is a 22-page dealer edition: a cover, then one page per
scene with the room photograph on top and, on the black lower band, one or two
swatch rectangles with the printed design number(s). The layout and wording
vary page by page, so the mapping of swatch → design number is curated by hand
in tools/rolls/source/plain-map.json (transcribed from the printed captions and
cross-checked by OCR). This script only does the mechanical part:

  * detects the swatch rectangles on the black band (in reading order),
  * detects the room photograph (top of the page),
  * crops full.jpg (the swatch — the design itself) and detail.jpg (the room view)
    for each design into assets/rolls/plain/designs/<slug>/,
  * writes the collection cover, a QA sheet per page and the audit trail,
  * merges the entries into assets/rolls/designs.json.

Usage (from the site root):  python tools/rolls/extract-plain.py [--pages 4,14] [--no-merge]
"""
import argparse
import json
import os
import re

import cv2
import numpy as np
import pymupdf
from PIL import Image, ImageDraw, ImageFont

SITE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "plain"
PDF = os.path.join(SITE, "assets", "rolls", SLUG, "catalogue.pdf")
OUT_DESIGNS = os.path.join(SITE, "assets", "rolls", SLUG, "designs")
SOURCE_DIR = os.path.join(SITE, "tools", "rolls", "source")
QA_DIR = os.path.join(SOURCE_DIR, "qa")
MAP = os.path.join(SOURCE_DIR, "plain-map.json")
DPI = 144

os.makedirs(OUT_DESIGNS, exist_ok=True)
os.makedirs(QA_DIR, exist_ok=True)


def render(doc, page_no, dpi=DPI):
    pix = doc[page_no - 1].get_pixmap(dpi=dpi)
    return np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3].copy()


def slugify(no):
    s = re.sub(r"[^a-z0-9]+", "-", no.lower()).strip("-")
    return s


def find_swatches(img, expected):
    """Bright rectangles sitting on the black lower band, in reading order.
    First pass keeps adjacent swatches apart; a second, more forgiving pass (closing
    the fine weave lines of textured swatches) runs only when too few were found."""
    H, W = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    for closing, min_fill in ((0, 0.85), (13, 0.7)):
        bright = (gray > 45).astype(np.uint8) * 255
        if closing:
            bright = cv2.morphologyEx(bright, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (closing, closing)))
        bright = cv2.morphologyEx(bright, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9)))
        n, lab, stats, _ = cv2.connectedComponentsWithStats(bright, 8)
        boxes = []
        for i in range(1, n):
            x, y, w, h, a = stats[i]
            fill = a / (w * h)
            if 0.08 * W < w < 0.6 * W and 0.06 * H < h < 0.5 * H and fill > min_fill and y > 0.45 * H:
                boxes.append([int(x), int(y), int(x + w), int(y + h)])
        boxes.sort(key=lambda b: (round(b[1] / 60), b[0]))
        if len(boxes) >= expected:
            return boxes
    return boxes


def find_room(img, swatches):
    """The photograph at the top: from the first non-white row down to the black gap
    that separates it from the swatch band (found by walking up from the first swatch
    through rows that are at least 90% near-black)."""
    H, W = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    rowmean = img.mean(axis=(1, 2))
    dark_frac = (gray < 28).mean(axis=1)
    if swatches:
        y = min(b[1] for b in swatches) - 2
        while y > 0 and dark_frac[y] >= 0.9:
            y -= 1
        y_black = y + 1
        if y_black > int(H * 0.8) or y_black < int(H * 0.2):
            y_black = min(b[1] for b in swatches) - 30
    else:
        y_black = int(H * 0.6)
    nonwhite = rowmean < 238
    y_top = int(np.argmax(nonwhite)) if nonwhite.any() else 0
    region = img[y_top:y_black]
    colmean = region.mean(axis=(0, 2))
    cols = np.where(colmean < 238)[0]
    x0, x1 = (int(cols[0]), int(cols[-1]) + 1) if len(cols) else (0, W)
    return [x0, y_top, x1, y_black]


def label_font(size):
    for cand in ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"]:
        if os.path.exists(cand):
            return ImageFont.truetype(cand, size)
    return ImageFont.load_default()


def save_jpg(arr, path, q=92):
    Image.fromarray(arr).save(path, "JPEG", quality=q, optimize=True, progressive=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages")
    ap.add_argument("--no-merge", action="store_true")
    args = ap.parse_args()
    wanted = {int(p) for p in args.pages.split(",")} if args.pages else None

    with open(MAP, encoding="utf-8") as f:
        pmap = json.load(f)["pages"]
    doc = pymupdf.open(PDF)
    print(f"catalogue: {PDF} ({len(doc)} pages); mapped pages: {len(pmap)}")

    cover = render(doc, 1)
    cov = Image.fromarray(cover)
    cov = cov.resize((1200, int(cov.height * 1200 / cov.width)), Image.LANCZOS)
    cov.save(os.path.join(SITE, "assets", "rolls", SLUG, "cover.jpg"), "JPEG", quality=86, optimize=True, progressive=True)

    font, small = label_font(46), label_font(26)
    audit = {"pages": {}}
    designs = []
    seen = {}
    for page_s, entries in sorted(pmap.items(), key=lambda kv: int(kv[0])):
        page = int(page_s)
        if wanted and page not in wanted:
            continue
        img = render(doc, page)
        H, W = img.shape[:2]
        need = max(e["swatch"] for e in entries) + 1
        boxes = find_swatches(img, need)
        room = find_room(img, boxes)
        rec = {"page": page, "size": [W, H], "swatches": boxes, "room": room, "flags": []}
        if len(boxes) < need:
            rec["flags"].append(f"{len(boxes)} swatch rectangles found, map expects {need}")
        qa = []
        for e in entries:
            no = e["designNumber"]
            slug = slugify(no)
            if slug in seen:
                rec["flags"].append(f"duplicate slug {slug} (page {seen[slug]})")
            seen[slug] = page
            flags = []
            if e.get("needsReview"):
                flags.append(e.get("reviewNote", "needs review"))
            ddir = os.path.join(OUT_DESIGNS, slug)
            os.makedirs(ddir, exist_ok=True)
            crop = None
            if e["swatch"] < len(boxes):
                x0, y0, x1, y1 = boxes[e["swatch"]]
                inset = 12  # drop the frame line around the swatch (a few px of gold or white)
                x0, y0, x1, y1 = x0 + inset, y0 + inset, x1 - inset, y1 - inset
                if e.get("half") == "left":
                    x1 = x0 + (x1 - x0) // 2 - 3
                elif e.get("half") == "right":
                    x0 = x0 + (x1 - x0) // 2 + 3
                crop = img[y0:y1, x0:x1]
                save_jpg(crop, os.path.join(ddir, "full.jpg"), 92)
            else:
                flags.append("swatch rectangle not detected on the page — image missing")
            rx0, ry0, rx1, ry1 = room
            save_jpg(img[ry0:ry1, rx0:rx1], os.path.join(ddir, "detail.jpg"), 90)
            entry = {
                "id": f"{SLUG}:{no}", "collectionId": SLUG, "designNumber": no, "slug": slug,
                "image": f"assets/rolls/{SLUG}/designs/{slug}/full.jpg",
                "web": f"assets/rolls/{SLUG}/designs/{slug}/web.jpg",
                "thumbnail": f"assets/rolls/{SLUG}/designs/{slug}/thumb.jpg",
                "swatch": None,
                "detail": f"assets/rolls/{SLUG}/designs/{slug}/detail.jpg", "detailLabel": "In the room",
                "width": int(crop.shape[1]) if crop is not None else None,
                "height": int(crop.shape[0]) if crop is not None else None,
                "cataloguePage": page, "patternRepeat": None,
                "colourway": e.get("colourway"), "group": None,
                "caption": e.get("caption"),
                "needsReview": bool(flags), "reviewNote": "; ".join(flags),
            }
            designs.append(entry)
            qa.append((no, crop, e.get("colourway")))
        audit["pages"][page] = rec

        # QA sheet: page thumbnail + each swatch crop with its assigned number
        thumb = Image.fromarray(img).resize((420, int(H * 420 / W)))
        band_img = Image.fromarray(img[room[3]:H])
        band_w = 440 + 320 * max(len(qa), 1) - 20
        band_img = band_img.resize((band_w, int(band_img.height * band_w / band_img.width)))
        sheet = Image.new("RGB", (band_w + 20, max(thumb.height, 420) + 70 + band_img.height + 20), (250, 247, 240))
        sheet.paste(thumb, (10, 10))
        drw = ImageDraw.Draw(sheet)
        drw.text((10, max(thumb.height, 420) + 24), "printed captions on the catalogue page:", fill=(40, 40, 40), font=small)
        sheet.paste(band_img, (10, max(thumb.height, 420) + 60))
        for i, (no, crop, colour) in enumerate(qa):
            x = 440 + i * 320
            if crop is not None:
                im = Image.fromarray(crop)
                im.thumbnail((300, 300))
                sheet.paste(im, (x, 70))
            drw.rectangle([x, 10, x + 300, 62], fill=(180, 20, 20))
            drw.text((x + 8, 14), f"= {no}", fill="white", font=font)
            drw.text((x, 380), (colour or "")[:26], fill=(40, 40, 40), font=small)
        sheet.save(os.path.join(QA_DIR, f"plain-p{page:02d}.jpg"), quality=85)
        print(f"page {page:2d}: swatches={len(boxes)} room={room} designs={[e['designNumber'] for e in entries]} {'| ' + ' | '.join(rec['flags']) if rec['flags'] else ''}")

    with open(os.path.join(SOURCE_DIR, "plain-extraction.json"), "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=1, ensure_ascii=False, default=int)
    with open(os.path.join(SOURCE_DIR, f"{SLUG}-designs.json"), "w", encoding="utf-8") as f:
        json.dump({"designs": designs}, f, indent=2, ensure_ascii=False)
    print(f"{len(designs)} designs; flagged: {[d['designNumber'] for d in designs if d['needsReview']]}")
    if not args.no_merge and not wanted:
        path = os.path.join(SITE, "assets", "rolls", "designs.json")
        data = {"designs": []}
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        keep = [d for d in data.get("designs", []) if d.get("collectionId") != SLUG]
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"designs": keep + designs}, f, indent=2, ensure_ascii=False)
        print(f"merged into designs.json: {len(keep) + len(designs)} designs total")


if __name__ == "__main__":
    main()
