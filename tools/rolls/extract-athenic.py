"""Extract the individual designs of the Athenic India catalogue.

Catalogue structure (read from the PDF itself):
  page 1      cover
  page 2      index: one header per colourway family ("1-3-4-6  Rep:53cm") with
              small swatches; families are laid out in two columns, row by row,
              and appear on the following pages in exactly that order
  pages 3-18  one family per page: a room shot per design (design number printed
              in the bottom-right corner, ascending order), one or two roll
              photos labelled with all numbers of the family, sometimes a
              close-up, a "standing rolls" photo, and finally a swatch row with
              the number printed under each swatch.

What this script does, deterministically:
  1. OCR the index page to get the families, their order and pattern repeat.
  2. Segment every family page into photo panels (uniform separator strips),
     find the swatch tiles in the bottom band, and read the number labels.
  3. Assign design numbers from the family order, cross-checked against the
     OCR of the printed labels. Any disagreement is flagged needsReview.
  4. Write full.jpg (room shot) and swatch.jpg per design under
     assets/rolls/athenic-india/designs/<no>/, the collection cover, a QA sheet
     per page (tools/rolls/source/qa/) and the audit trail (athenic-extraction.json),
     then merge the entries into assets/rolls/designs.json.

Usage (from the site root):  python tools/rolls/extract-athenic.py [--pages 3,4] [--no-merge]
"""
import argparse
import json
import os
import re
import sys
from collections import Counter

import cv2
import numpy as np
import pymupdf
from PIL import Image, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None

SITE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "athenic-india"
PDF = os.path.join(SITE, "assets", "rolls", SLUG, "catalogue.pdf")
OUT_DESIGNS = os.path.join(SITE, "assets", "rolls", SLUG, "designs")
SOURCE_DIR = os.path.join(SITE, "tools", "rolls", "source")
QA_DIR = os.path.join(SOURCE_DIR, "qa")
DPI = 144  # the embedded images are exactly 2 px per point → 144 dpi is native resolution
INDEX_PAGE = 2
FIRST_FAMILY_PAGE = 3

os.makedirs(OUT_DESIGNS, exist_ok=True)
os.makedirs(QA_DIR, exist_ok=True)


# ----------------------------------------------------------------------------- helpers
def render(doc, page_no, dpi=DPI):
    pix = doc[page_no - 1].get_pixmap(dpi=dpi)
    return np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3].copy()


def runs(mask, minlen, gap=0):
    idx = np.where(mask)[0]
    if len(idx) == 0:
        return []
    out, s, prev = [], idx[0], idx[0]
    for i in idx[1:]:
        if i - prev > gap + 1:
            if prev - s + 1 >= minlen:
                out.append((int(s), int(prev) + 1))
            s = i
        prev = i
    if prev - s + 1 >= minlen:
        out.append((int(s), int(prev) + 1))
    return out


def nonuniform_rows(img, thr=28):
    med = np.median(img, axis=1, keepdims=True)
    d = np.abs(img.astype(int) - med.astype(int)).sum(axis=2)
    return np.percentile(d, 97, axis=1) >= thr


def col_profile(band):
    med = np.median(band, axis=0, keepdims=True)
    d = np.abs(band.astype(int) - med.astype(int)).sum(axis=2)
    return np.percentile(d, 97, axis=0), med[0]


def photo_panels(img):
    """Photos separated by uniform strips. Columns split only on strips that share the
    colour of the separator rows around the band (so a dark door frame inside a photo
    never splits it)."""
    H, W = img.shape[:2]
    nonuni = nonuniform_rows(img)
    out = []
    for y0, y1 in runs(nonuni, 30, gap=2):
        above = img[max(0, y0 - 8):y0]
        below = img[y1:min(H, y1 + 8)]
        sep_src = above if above.shape[0] >= 4 else below
        sep_colour = np.median(sep_src.reshape(-1, 3), axis=0) if sep_src.size else np.array([0, 0, 0])
        band = img[y0:y1]
        p97, colmed = col_profile(band)
        uniform = p97 < 28
        matches = np.abs(colmed.astype(int) - sep_colour.astype(int)).sum(axis=1) < 40
        content = ~(uniform & matches)
        for x0, x1 in runs(content, 30, gap=2):
            if (x1 - x0) > 0.5 * W and (y1 - y0) > 300:
                out.append([int(x0), int(y0), int(x1), int(y1)])
    return out


def find_tiles(img, y_start):
    """Swatch tiles in the bottom band: the band is a flat fill, tiles are anything that
    differs from it. Returns tiles sorted left→right and the band colour."""
    region = img[y_start:]
    if region.shape[0] < 120:
        return [], None
    flat = region.reshape(-1, 3)
    # mode colour of the band (flat synthetic fill)
    keys = flat[:, 0].astype(np.int32) * 65536 + flat[:, 1].astype(np.int32) * 256 + flat[:, 2]
    vals, counts = np.unique(keys, return_counts=True)
    k = int(vals[np.argmax(counts)])
    bg = np.array([k // 65536, (k // 256) % 256, k % 256])
    diff = np.abs(region.astype(int) - bg).sum(axis=2)
    mask = (diff > 5).astype(np.uint8) * 255
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7)))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    tiles = []
    for i in range(1, n):
        x, y, w, h, a = stats[i]
        if w >= 150 and h >= 150 and 0.55 <= w / h <= 1.8 and a / (w * h) > 0.8:
            tiles.append([int(x), int(y_start + y), int(x + w), int(y_start + y + h)])
    tiles.sort(key=lambda b: b[0])
    return tiles, bg


class OCR:
    def __init__(self):
        from rapidocr_onnxruntime import RapidOCR
        self.eng = RapidOCR()

    def read(self, crop, scale=2.0):
        if crop.size == 0:
            return []
        big = cv2.resize(crop, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        res, _ = self.eng(big)
        out = []
        for box, txt, conf in (res or []):
            xs = [p[0] / scale for p in box]
            ys = [p[1] / scale for p in box]
            out.append({"text": txt, "conf": round(float(conf), 2),
                        "box": [int(min(xs)), int(min(ys)), int(max(xs)), int(max(ys))]})
        return out

    def digits(self, crop, scale=2.0):
        toks = []
        for r in self.read(crop, scale):
            for t in re.findall(r"\d+", r["text"]):
                toks.append((t, r["conf"], r["box"]))
        return toks

    def white_digits(self, crop):
        """White printed digits on a photo: isolate near-white pixels, invert, OCR."""
        g = cv2.cvtColor(crop, cv2.COLOR_RGB2GRAY)
        m = (g >= 244).astype(np.uint8) * 255
        m = cv2.dilate(m, np.ones((2, 2), np.uint8))
        inv = cv2.cvtColor(255 - m, cv2.COLOR_GRAY2RGB)
        toks = self.digits(inv, 2.5)
        if not toks:
            toks = self.digits(crop, 2.5)
        return toks


def parse_index(ocr, img):
    """Families from the index page: header text like '1-3-4-6' with 'Rep:53cm' nearby."""
    reads = ocr.read(img, 1.5)
    heads, reps = [], []
    for r in reads:
        t = r["text"].replace(" ", "")
        m = re.search(r"(\d+(?:-\d+)+)", t)
        if m and "Rep" not in t.split(m.group(1))[0]:
            heads.append((m.group(1), r["box"], t))
        m2 = re.search(r"Rep:?(\d+)\s*cm", t, re.I)
        if m2:
            reps.append((int(m2.group(1)), r["box"]))
    fam = []
    for name, box, text in heads:
        cy = (box[1] + box[3]) / 2
        rep = None
        m_in = re.search(r"Rep:?(\d+)\s*cm", text, re.I)
        if m_in:
            rep = int(m_in.group(1))          # printed in the same run of text
        else:
            best = 1e9
            for val, rb in reps:
                rcy = (rb[1] + rb[3]) / 2
                dist = rb[0] - box[2]          # the repeat sits immediately right of the header
                if abs(rcy - cy) < 40 and -10 <= dist < 160 and dist < best:
                    best, rep = dist, val
        fam.append({"name": name, "numbers": [int(n) for n in name.split("-")], "repeat_cm": rep, "box": box})
    # reading order: rows (y) then columns (x)
    fam.sort(key=lambda f: (round(f["box"][1] / 120), f["box"][0]))
    return fam


def label_font(size):
    for cand in ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"]:
        if os.path.exists(cand):
            return ImageFont.truetype(cand, size)
    return ImageFont.load_default()


def save_jpg(arr, path, q=92):
    Image.fromarray(arr).save(path, "JPEG", quality=q, optimize=True, progressive=True)


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", help="comma list of family pages to process (default all)")
    ap.add_argument("--no-merge", action="store_true", help="do not write designs.json")
    args = ap.parse_args()

    doc = pymupdf.open(PDF)
    ocr = OCR()
    print(f"catalogue: {PDF} ({len(doc)} pages)")

    # 1. families from the index page
    index_img = render(doc, INDEX_PAGE)
    families = parse_index(ocr, index_img)
    print(f"index: {len(families)} families")
    for i, f in enumerate(families):
        f["page"] = FIRST_FAMILY_PAGE + i
        print(f"  page {f['page']}: {f['name']}  repeat {f['repeat_cm']} cm")
    all_numbers = [n for f in families for n in f["numbers"]]
    dup = [n for n, c in Counter(all_numbers).items() if c > 1]
    missing = sorted(set(range(1, max(all_numbers) + 1)) - set(all_numbers))
    if dup or missing:
        print(f"  WARNING index numbers duplicated={dup} missing={missing}")
    if FIRST_FAMILY_PAGE + len(families) - 1 != len(doc):
        print(f"  WARNING {len(families)} families but {len(doc) - FIRST_FAMILY_PAGE + 1} family pages")

    # cover: the boxed catalogue mock-up at the top of page 1
    cover_path = os.path.join(SITE, "assets", "rolls", SLUG, "cover.jpg")
    p1 = render(doc, 1)
    cov = p1[0:1750]
    cov = np.array(Image.fromarray(cov).resize((1200, int(1750 * 1200 / cov.shape[1])), Image.LANCZOS))
    save_jpg(cov, cover_path, 86)

    wanted = None
    if args.pages:
        wanted = {int(p) for p in args.pages.split(",")}

    audit = {"families": families, "pages": {}}
    designs = []
    font = label_font(54)
    small = label_font(30)

    for fam in families:
        page = fam["page"]
        if wanted and page not in wanted:
            continue
        numbers = fam["numbers"]
        G = len(numbers)
        img = render(doc, page)
        H, W = img.shape[:2]
        photos = photo_panels(img)
        rec = {"page": page, "family": fam["name"], "size": [W, H], "photos": photos, "flags": []}
        if len(photos) < G + 1:
            rec["flags"].append(f"only {len(photos)} photo panels for a family of {G}")
        rooms = photos[:G]
        extras = photos[G:]

        # swatch tiles + labels in the band under the last photo
        band_top = photos[-1][3] + 4 if photos else int(H * 0.85)
        tiles, band_bg = find_tiles(img, band_top)
        if len(tiles) < G:
            # band is not a flat fill on this page: split the swatch row on uniform columns instead
            row = img[band_top:min(H, band_top + 470)]
            p97, colmed = col_profile(row)
            alt = [[x0, band_top, x1, band_top + 470] for x0, x1 in runs(p97 >= 28, 150, gap=2) if 150 <= x1 - x0 <= 480]
            if len(alt) >= len(tiles):
                # trim each tile vertically to its non-uniform rows
                fixed = []
                for x0, y0, x1, y1 in alt:
                    sub = img[y0:y1, x0:x1]
                    rr = runs(nonuniform_rows(sub, 20), 100, gap=3)
                    if rr:
                        fixed.append([x0, y0 + rr[0][0], x1, y0 + rr[0][1]])
                tiles = fixed
                rec_note = "swatch tiles found by column split (band not a flat colour)"
            else:
                rec_note = None
        else:
            rec_note = None
        rec["tiles"] = tiles
        if rec_note:
            rec["flags"].append(rec_note)
        tile_labels = []
        tile_num = {}
        if tiles:
            strip_y0 = max(t[3] for t in tiles) + 2
            strip_y1 = min(H, strip_y0 + 110)
            for ti, t in enumerate(tiles):
                # the number is printed centred under its own swatch: read each label alone
                pad = 30
                cell = img[strip_y0:strip_y1, max(0, t[0] - pad):min(W, t[2] + pad)]
                toks = [(int(n), c) for n, c, b in ocr.digits(cell, 3.0)]
                toks = [tk for tk in toks if tk[0] in numbers] or toks
                if toks:
                    best = max(toks, key=lambda tk: tk[1])
                    tile_labels.append({"tile": ti, "num": best[0], "conf": best[1]})
                    tile_num[ti] = best[0]
        rec["tile_labels"] = tile_labels
        tiles_ok = len(tiles) == G
        if not tiles_ok:
            rec["flags"].append(f"{len(tiles)} swatch tiles for a family of {G}")
        ordered_nums = sorted(numbers)
        if tiles_ok and len(tile_num) < G:
            # printed order under the swatches is ascending left→right in this catalogue
            for ti in range(G):
                tile_num.setdefault(ti, ordered_nums[ti])
            rec["flags"].append("swatch labels partly unreadable; left-to-right ascending order used")
        rec["tile_num"] = tile_num
        if tiles_ok and sorted(tile_num.values()) != ordered_nums:
            rec["flags"].append(f"swatch labels {sorted(tile_num.values())} != family {ordered_nums}")

        # extras: roll photos (several numbers) / close-up (one number)
        extra_info = []
        for ei, box in enumerate(extras):
            x0, y0, x1, y1 = box
            w, h = x1 - x0, y1 - y0
            corner = img[y1 - int(h * 0.13):y1, x1 - int(w * 0.34):x1]
            toks = [int(t) for t, c, b in ocr.white_digits(corner) if int(t) in numbers]
            top = img[y0:y0 + int(h * 0.16), x0:x1]
            top_toks = [int(t) for t, c, b in ocr.digits(top, 1.5) if int(t) in numbers]
            kind = "standing" if ei == len(extras) - 1 else ("closeup" if len(set(toks)) == 1 else "rolls")
            extra_info.append({"box": box, "kind": kind, "corner": sorted(set(toks)), "top": sorted(set(top_toks))})
        rec["extras"] = extra_info

        # room shots → designs
        qa_tiles = []
        for i, box in enumerate(rooms):
            no = ordered_nums[i]
            x0, y0, x1, y1 = box
            w, h = x1 - x0, y1 - y0
            corner = img[y1 - int(h * 0.13):y1, x1 - int(w * 0.30):x1]
            read = [int(t) for t, c, b in ocr.white_digits(corner)]
            flags = []
            if read and no not in read:
                flags.append(f"printed label read as {read}, expected {no}")
            slug = str(no)
            ddir = os.path.join(OUT_DESIGNS, slug)
            os.makedirs(ddir, exist_ok=True)
            crop = img[y0:y1, x0:x1]
            save_jpg(crop, os.path.join(ddir, "full.jpg"), 92)
            sw_path = None
            ti = next((k for k, v in tile_num.items() if v == no), None)
            if ti is not None and ti < len(tiles):
                t = tiles[ti]
                save_jpg(img[t[1]:t[3], t[0]:t[2]], os.path.join(ddir, "swatch.jpg"), 92)
                sw_path = f"assets/rolls/{SLUG}/designs/{slug}/swatch.jpg"
            det_path = None
            for e in extra_info:
                if e["kind"] == "closeup" and e["corner"] == [no]:
                    b = e["box"]
                    save_jpg(img[b[1]:b[3], b[0]:b[2]], os.path.join(ddir, "detail.jpg"), 90)
                    det_path = f"assets/rolls/{SLUG}/designs/{slug}/detail.jpg"
            entry = {
                "id": f"{SLUG}:{no}", "collectionId": SLUG, "designNumber": str(no), "slug": slug,
                "image": f"assets/rolls/{SLUG}/designs/{slug}/full.jpg",
                "web": f"assets/rolls/{SLUG}/designs/{slug}/web.jpg",
                "thumbnail": f"assets/rolls/{SLUG}/designs/{slug}/thumb.jpg",
                "swatch": sw_path, "detail": det_path, "detailLabel": "Close-up" if det_path else None,
                "width": int(w), "height": int(h), "cataloguePage": page,
                "patternRepeat": f"{fam['repeat_cm']} cm" if fam.get("repeat_cm") else None,
                "colourway": None, "group": fam["name"],
                "needsReview": bool(flags), "reviewNote": "; ".join(flags),
            }
            designs.append(entry)
            qa_tiles.append((no, crop, read, ti))
        rec["designs"] = [d["designNumber"] for d in designs if d["cataloguePage"] == page]
        audit["pages"][page] = rec

        # QA sheet: room crops with assigned number + OCR reading, swatch row underneath
        cell = 300
        sheet_w = cell * max(G, 1) + 20
        band_img = Image.fromarray(img[band_top:H]) if H - band_top > 40 else None
        band_h = int(band_img.height * (sheet_w - 20) / band_img.width) if band_img else 0
        sheet = Image.new("RGB", (sheet_w, cell + 340 + 20 + band_h + 60), (250, 247, 240))
        drw = ImageDraw.Draw(sheet)
        if band_img:
            drw.text((10, cell + 350), "printed swatch row from the catalogue page:", fill=(40, 40, 40), font=small)
            sheet.paste(band_img.resize((sheet_w - 20, band_h)), (10, cell + 390))
        for i, (no, crop, read, ti) in enumerate(qa_tiles):
            im = Image.fromarray(crop).resize((cell - 10, int((cell - 10) * crop.shape[0] / crop.shape[1])))
            sheet.paste(im, (10 + i * cell, 10))
            drw.rectangle([10 + i * cell, 10, 10 + i * cell + 150, 74], fill=(180, 20, 20))
            drw.text((18 + i * cell, 12), f"= {no}", fill="white", font=font)
            drw.text((12 + i * cell, cell + 4), f"label OCR: {read or '?'}", fill=(40, 40, 40), font=small)
            if ti is not None and ti < len(tiles):
                t = tiles[ti]
                sw = Image.fromarray(img[t[1]:t[3], t[0]:t[2]]).resize((220, 220))
                sheet.paste(sw, (10 + i * cell, cell + 50))
                drw.text((12 + i * cell, cell + 280), f"swatch → {tile_num.get(ti)}", fill=(40, 40, 40), font=small)
        sheet.save(os.path.join(QA_DIR, f"athenic-p{page:02d}.jpg"), quality=85)
        flag_txt = " | ".join(rec["flags"]) if rec["flags"] else "ok"
        print(f"page {page:2d} family {fam['name']:<12} photos={len(photos)} tiles={len(tiles)} labels={[l['num'] for l in tile_labels]} -> {flag_txt}")

    designs.sort(key=lambda d: int(d["designNumber"]))
    with open(os.path.join(SOURCE_DIR, "athenic-extraction.json"), "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=1, ensure_ascii=False, default=int)
    with open(os.path.join(SOURCE_DIR, f"{SLUG}-designs.json"), "w", encoding="utf-8") as f:
        json.dump({"designs": designs}, f, indent=2, ensure_ascii=False)
    print(f"{len(designs)} designs extracted; flagged: {[d['designNumber'] for d in designs if d['needsReview']]}")

    if not args.no_merge and not wanted:
        merge(designs)


def merge(designs):
    path = os.path.join(SITE, "assets", "rolls", "designs.json")
    data = {"designs": []}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    keep = [d for d in data.get("designs", []) if d.get("collectionId") != SLUG]
    data = {"designs": keep + designs}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"merged into {path}: {len(data['designs'])} designs total")


if __name__ == "__main__":
    main()
