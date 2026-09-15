"""Wallpaper Rolls image pipeline (SPEC section 10).

Renders every catalogue PDF page to the three sizes the catalogue viewer uses,
creates a collection cover when one is missing, and produces the web / thumb
derivatives for every design folder that holds a full.jpg. Sizes measured from
full.jpg are written back into designs.json when they are missing or wrong.

Usage (from anywhere):
    python tools/rolls/prepare-images.py
    python tools/rolls/prepare-images.py --collection athenic-india
    python tools/rolls/prepare-images.py --force            # re-render everything
    python tools/rolls/prepare-images.py --pdf-only         # catalogue pages + cover only
    python tools/rolls/prepare-images.py --designs-only     # design derivatives + JSON only

Outputs are skipped when they are already newer than their source, so the
script is safe to run as often as you like. full.jpg and catalogue.pdf are
never modified.

Requires Python 3.10+ with PyMuPDF (import pymupdf) and Pillow.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

try:
    import pymupdf
except ImportError:  # pragma: no cover - environment guard
    sys.exit("PyMuPDF is required:  pip install pymupdf")

try:
    from PIL import Image, ImageOps
except ImportError:  # pragma: no cover - environment guard
    sys.exit("Pillow is required:  pip install pillow")

# Catalogue strips can be ~11,000px tall at 1400px wide; that is expected.
Image.MAX_IMAGE_PIXELS = None

# ---------------------------------------------------------------------------
# Output specification (matches SPEC section 1 and section 10)
# ---------------------------------------------------------------------------

PAGE_SIZES = (
    # prefix, target width px, JPEG quality
    ("p", 1400, 80),
    ("m", 800, 76),
    ("t", 200, 70),
)
COVER_WIDTH = 1200
COVER_QUALITY = 82
COVER_TALL_RATIO = 2.2      # height / width above which page 1 is a strip
COVER_CROP_RATIO = 0.75     # crop height = width * 0.75 for strips

WEB_LONG_EDGE = 1200
WEB_QUALITY = 82
THUMB_WIDTH = 480
THUMB_QUALITY = 78
EXTRA_LONG_EDGE = 900       # swatch-web.jpg / detail-web.jpg
EXTRA_QUALITY = 82
EXTRA_SOURCES = (("swatch.jpg", "swatch-web.jpg"), ("detail.jpg", "detail-web.jpg"))

PDF_POINTS_PER_INCH = 72
SIZE_MB_TOLERANCE = 0.15

SITE_ROOT = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------


@dataclass
class Report:
    """Per-collection tally printed in the summary table."""

    slug: str
    pages_total: int = 0
    pages_rendered: int = 0
    pages_skipped: int = 0
    cover: str = "-"
    designs_total: int = 0
    designs_rendered: int = 0
    designs_skipped: int = 0
    json_updated: int = 0
    warnings: list[str] = field(default_factory=list)

    def warn(self, message: str) -> None:
        self.warnings.append(message)
        print(f"  WARNING  {message}")


def is_up_to_date(output: Path, *sources: Path) -> bool:
    """True when output exists and is at least as new as every source."""
    if not output.exists():
        return False
    out_mtime = output.stat().st_mtime
    return all(out_mtime >= src.stat().st_mtime for src in sources)


def save_jpeg(image: Image.Image, target: Path, quality: int) -> int:
    """Write a progressive RGB JPEG atomically; returns the byte size."""
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_name(target.name + ".tmp")
    if image.mode != "RGB":
        image = image.convert("RGB")
    image.save(tmp, "JPEG", quality=quality, progressive=True, optimize=True)
    os.replace(tmp, target)
    return target.stat().st_size


def resize_to_width(image: Image.Image, width: int) -> Image.Image:
    """Scale to an exact width (never upscales)."""
    if image.width <= width:
        return image
    height = max(1, round(image.height * width / image.width))
    return image.resize((width, height), Image.Resampling.LANCZOS)


def resize_long_edge(image: Image.Image, long_edge: int) -> Image.Image:
    """Scale so the longest edge fits inside long_edge (never upscales)."""
    longest = max(image.width, image.height)
    if longest <= long_edge:
        return image
    scale = long_edge / longest
    size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    return image.resize(size, Image.Resampling.LANCZOS)


def human_size(num_bytes: int) -> str:
    if num_bytes >= 1024 * 1024:
        return f"{num_bytes / (1024 * 1024):.1f} MB"
    return f"{num_bytes / 1024:.0f} KB"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path: Path, data: dict) -> None:
    """Write JSON with the house formatting (2-space, UTF-8, key order kept)."""
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    os.replace(tmp, path)


# ---------------------------------------------------------------------------
# Catalogue pages
# ---------------------------------------------------------------------------


def render_page(page: "pymupdf.Page", width: int) -> Image.Image:
    """Render one PDF page to a Pillow RGB image of the requested width."""
    dpi = width / page.rect.width * PDF_POINTS_PER_INCH
    zoom = dpi / PDF_POINTS_PER_INCH
    pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False, colorspace=pymupdf.csRGB)
    image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    if image.width != width:  # rounding in the pixmap grid
        image = image.resize((width, max(1, round(image.height * width / image.width))), Image.Resampling.LANCZOS)
    return image


def page_outputs(pages_dir: Path, number: int) -> list[tuple[Path, int, int]]:
    """(target path, width, quality) for the three renders of a page."""
    return [(pages_dir / f"{prefix}{number:03d}.jpg", width, quality) for prefix, width, quality in PAGE_SIZES]


def remove_stale_pages(pages_dir: Path, page_count: int, report: Report) -> None:
    """Delete renders left over from a previous, longer PDF."""
    if not pages_dir.is_dir():
        return
    pattern = re.compile(r"^([pmt])(\d{3})\.jpg$")
    for entry in sorted(pages_dir.iterdir()):
        match = pattern.match(entry.name)
        if match and int(match.group(2)) > page_count:
            entry.unlink()
            print(f"  removed stale render {entry.name}")


def render_catalogue(collection: dict, root: Path, force: bool, report: Report) -> "pymupdf.Document | None":
    """Render p/m/t images for every page. Returns the open document (or None)."""
    slug = collection["slug"]
    pdf_path = root / collection.get("catalogueFile", f"assets/rolls/{slug}/catalogue.pdf")
    pages_dir = root / "assets" / "rolls" / slug / "pages"

    if not pdf_path.is_file():
        report.warn(f"catalogue not found: {pdf_path.relative_to(root).as_posix()} - pages skipped")
        return None

    try:
        doc = pymupdf.open(pdf_path)
    except Exception as exc:  # corrupt or encrypted file
        report.warn(f"could not open {pdf_path.name}: {exc}")
        return None

    if doc.needs_pass:
        report.warn(f"{pdf_path.name} is password protected - pages skipped")
        doc.close()
        return None

    page_count = doc.page_count
    report.pages_total = page_count
    if page_count == 0:
        report.warn(f"{pdf_path.name} has no pages")
        doc.close()
        return None

    declared = collection.get("pageCount")
    if declared is not None and declared != page_count:
        report.warn(f"collections.json says pageCount {declared}, PDF has {page_count} - update collections.json")
    declared_mb = collection.get("catalogueSizeMB")
    actual_mb = round(pdf_path.stat().st_size / (1024 * 1024), 1)
    if declared_mb is not None and abs(float(declared_mb) - actual_mb) > SIZE_MB_TOLERANCE:
        report.warn(f"collections.json says catalogueSizeMB {declared_mb}, file is {actual_mb} MB - update collections.json")

    pages_dir.mkdir(parents=True, exist_ok=True)
    remove_stale_pages(pages_dir, page_count, report)

    for index in range(page_count):
        number = index + 1
        outputs = page_outputs(pages_dir, number)
        if not force and all(is_up_to_date(path, pdf_path) for path, _, _ in outputs):
            report.pages_skipped += 1
            continue

        page = doc[index]
        started = time.perf_counter()
        master = render_page(page, PAGE_SIZES[0][1])
        sizes = []
        for path, width, quality in outputs:
            image = master if width == master.width else resize_to_width(master, width)
            sizes.append(f"{path.name} {image.width}x{image.height} {human_size(save_jpeg(image, path, quality))}")
        master.close()
        report.pages_rendered += 1
        elapsed = time.perf_counter() - started
        print(f"  page {number:>3}/{page_count}  " + "  |  ".join(sizes) + f"  ({elapsed:.1f}s)")

    return doc


def ensure_cover(collection: dict, doc: "pymupdf.Document | None", root: Path, report: Report) -> None:
    """Create cover.jpg from page 1 when the collection has no cover yet."""
    slug = collection["slug"]
    cover_path = root / collection.get("coverImage", f"assets/rolls/{slug}/cover.jpg")
    if cover_path.is_file():
        report.cover = "kept"
        return
    if doc is None or doc.page_count == 0:
        report.warn(f"no cover.jpg and no catalogue to make one from: {cover_path.relative_to(root).as_posix()}")
        report.cover = "missing"
        return

    page = doc[0]
    image = render_page(page, COVER_WIDTH)
    if image.height > image.width * COVER_TALL_RATIO:
        # Tall strip: keep the top, roughly square region so the card reads as artwork.
        image = image.crop((0, 0, image.width, round(image.width * COVER_CROP_RATIO)))
        note = "top crop of page 1"
    else:
        note = "full page 1"

    width, height = image.width, image.height
    size = save_jpeg(image, cover_path, COVER_QUALITY)
    image.close()
    report.cover = f"created ({note})"
    print(f"  cover.jpg created from {note}: {width}x{height}, {human_size(size)}")


# ---------------------------------------------------------------------------
# Design derivatives
# ---------------------------------------------------------------------------


def open_source_image(path: Path) -> Image.Image:
    """Open an image honouring EXIF orientation and normalising to RGB."""
    image = Image.open(path)
    image = ImageOps.exif_transpose(image) or image
    if image.mode != "RGB":
        image = image.convert("RGB")
    return image


def build_design_derivatives(design_dir: Path, force: bool, report: Report) -> bool:
    """Produce web.jpg / thumb.jpg (+ swatch-web / detail-web). Returns True if any file was written."""
    full_path = design_dir / "full.jpg"
    written = False

    web_path = design_dir / "web.jpg"
    thumb_path = design_dir / "thumb.jpg"
    if force or not (is_up_to_date(web_path, full_path) and is_up_to_date(thumb_path, full_path)):
        try:
            with open_source_image(full_path) as source:
                web = resize_long_edge(source, WEB_LONG_EDGE)
                web_size = save_jpeg(web, web_path, WEB_QUALITY)
                thumb = resize_to_width(source, THUMB_WIDTH)
                thumb_size = save_jpeg(thumb, thumb_path, THUMB_QUALITY)
                print(
                    f"  {design_dir.name:<12} full {source.width}x{source.height}"
                    f"  ->  web {web.width}x{web.height} {human_size(web_size)}"
                    f"  |  thumb {thumb.width}x{thumb.height} {human_size(thumb_size)}"
                )
            written = True
        except Exception as exc:
            report.warn(f"{design_dir.name}/full.jpg could not be processed: {exc}")
            return False

    for source_name, target_name in EXTRA_SOURCES:
        source_path = design_dir / source_name
        if not source_path.is_file():
            continue
        target_path = design_dir / target_name
        if not force and is_up_to_date(target_path, source_path):
            continue
        try:
            with open_source_image(source_path) as source:
                small = resize_long_edge(source, EXTRA_LONG_EDGE)
                size = save_jpeg(small, target_path, EXTRA_QUALITY)
                print(f"  {design_dir.name:<12} {source_name} -> {target_name} {small.width}x{small.height} {human_size(size)}")
            written = True
        except Exception as exc:
            report.warn(f"{design_dir.name}/{source_name} could not be processed: {exc}")

    return written


def image_dimensions(path: Path) -> tuple[int, int] | None:
    try:
        with Image.open(path) as image:
            image = ImageOps.exif_transpose(image) or image
            return image.width, image.height
    except Exception:
        return None


def with_dimensions(entry: dict, width: int, height: int) -> dict:
    """Return a copy of the design entry with width/height set, keeping key order.

    Missing keys are inserted after "detail" (the SPEC position) so the file
    keeps reading the same way it was written by hand.
    """
    if "width" in entry and "height" in entry:
        return {**entry, "width": width, "height": height}

    updated: dict = {}
    inserted = False
    anchor_keys = ("detail", "swatch", "thumbnail", "web", "image")
    anchor = next((key for key in anchor_keys if key in entry), None)
    for key, value in entry.items():
        if key in ("width", "height"):
            continue
        updated[key] = value
        if key == anchor:
            updated["width"] = width
            updated["height"] = height
            inserted = True
    if not inserted:
        updated["width"] = width
        updated["height"] = height
    return updated


def process_designs(collection: dict, root: Path, force: bool, report: Report, designs: list[dict]) -> list[dict]:
    """Derivatives for every design folder; returns the (possibly updated) designs list."""
    slug = collection["slug"]
    designs_dir = root / "assets" / "rolls" / slug / "designs"

    folders = sorted((p for p in designs_dir.iterdir() if p.is_dir()), key=lambda p: p.name) if designs_dir.is_dir() else []
    with_full = [p for p in folders if (p / "full.jpg").is_file()]
    report.designs_total = len(with_full)

    for folder in folders:
        if folder not in with_full:
            report.warn(f"designs/{folder.name}/ has no full.jpg - skipped")

    if not with_full:
        print(f"  no design folders with full.jpg under assets/rolls/{slug}/designs/ (nothing to do)")
    for folder in with_full:
        if build_design_derivatives(folder, force, report):
            report.designs_rendered += 1
        else:
            report.designs_skipped += 1

    # Write measured sizes back into designs.json (missing or wrong only).
    known_slugs = {p.name for p in with_full}
    referenced: set[str] = set()
    updated_designs: list[dict] = []
    for entry in designs:
        if entry.get("collectionId") != collection.get("id", slug):
            updated_designs.append(entry)
            continue
        image_rel = entry.get("image") or f"assets/rolls/{slug}/designs/{entry.get('slug', '')}/full.jpg"
        full_path = root / image_rel
        referenced.add(full_path.parent.name)
        if not full_path.is_file():
            report.warn(f"designs.json {entry.get('id', '?')}: {image_rel} is missing")
            updated_designs.append(entry)
            continue
        dims = image_dimensions(full_path)
        if dims is None:
            report.warn(f"designs.json {entry.get('id', '?')}: could not read {image_rel}")
            updated_designs.append(entry)
            continue
        width, height = dims
        if entry.get("width") == width and entry.get("height") == height:
            updated_designs.append(entry)
            continue
        updated_designs.append(with_dimensions(entry, width, height))
        report.json_updated += 1
        print(f"  designs.json {entry.get('id', '?')}: width/height -> {width}x{height}")

    for orphan in sorted(known_slugs - referenced):
        report.warn(f"designs/{orphan}/full.jpg exists but no designs.json entry references it")

    return updated_designs


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------


def print_summary(reports: list[Report], json_written: bool) -> None:
    headers = ("collection", "pages", "rendered", "skipped", "cover", "designs", "made", "skipped", "json")
    rows = [
        (
            r.slug,
            str(r.pages_total),
            str(r.pages_rendered),
            str(r.pages_skipped),
            r.cover,
            str(r.designs_total),
            str(r.designs_rendered),
            str(r.designs_skipped),
            str(r.json_updated),
        )
        for r in reports
    ]
    widths = [max(len(h), *(len(row[i]) for row in rows)) if rows else len(h) for i, h in enumerate(headers)]
    line = "  ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    print()
    print(line)
    print("-" * len(line))
    for row in rows:
        print("  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)))
    print()
    print("designs.json " + ("updated" if json_written else "unchanged"))
    warnings = [f"{r.slug}: {w}" for r in reports for w in r.warnings]
    if warnings:
        print(f"{len(warnings)} warning(s):")
        for w in warnings:
            print(f"  - {w}")
    else:
        print("no warnings")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render catalogue pages and design derivatives for the Wallpaper Rolls pages.")
    parser.add_argument("--collection", action="append", metavar="SLUG", help="only this collection slug (repeatable)")
    parser.add_argument("--force", action="store_true", help="re-create outputs even when they are up to date")
    parser.add_argument("--pdf-only", action="store_true", help="catalogue pages and cover only")
    parser.add_argument("--designs-only", action="store_true", help="design derivatives and designs.json only")
    parser.add_argument("--root", metavar="DIR", help="site root (default: derived from this script's location)")
    args = parser.parse_args(argv)
    if args.pdf_only and args.designs_only:
        parser.error("--pdf-only and --designs-only cannot be combined")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(args.root).resolve() if args.root else SITE_ROOT
    collections_path = root / "assets" / "rolls" / "collections.json"
    designs_path = root / "assets" / "rolls" / "designs.json"

    if not collections_path.is_file():
        print(f"ERROR  {collections_path} not found")
        return 2
    try:
        collections_data = load_json(collections_path)
    except (OSError, ValueError) as exc:
        print(f"ERROR  could not read collections.json: {exc}")
        return 2

    collections = [c for c in collections_data.get("collections", []) if isinstance(c, dict) and c.get("slug")]
    if args.collection:
        wanted = set(args.collection)
        known = {c["slug"] for c in collections}
        unknown = sorted(wanted - known)
        if unknown:
            print(f"ERROR  unknown collection slug(s): {', '.join(unknown)}  (known: {', '.join(sorted(known))})")
            return 2
        selected = [c for c in collections if c["slug"] in wanted]
    else:
        selected = []
        for c in collections:
            if c.get("published", True):
                selected.append(c)
            else:
                print(f"skipping {c['slug']} (published: false)")

    if not selected:
        print("no collections to process")
        return 0

    designs_data: dict = {"designs": []}
    designs_loaded = False
    if not args.pdf_only:
        if designs_path.is_file():
            try:
                designs_data = load_json(designs_path)
                designs_loaded = True
            except (OSError, ValueError) as exc:
                print(f"WARNING  could not read designs.json ({exc}); sizes will not be written back")
        else:
            print("WARNING  designs.json not found; sizes will not be written back")
    designs = list(designs_data.get("designs", []))
    original_designs = list(designs)

    reports: list[Report] = []
    for collection in selected:
        slug = collection["slug"]
        report = Report(slug=slug)
        reports.append(report)
        print(f"\n== {collection.get('name', slug)} ({slug}) ==")

        if not args.designs_only:
            doc = render_catalogue(collection, root, args.force, report)
            try:
                ensure_cover(collection, doc, root, report)
            finally:
                if doc is not None:
                    doc.close()

        if not args.pdf_only:
            designs = process_designs(collection, root, args.force, report, designs)

    json_written = False
    if designs_loaded and any(a is not b for a, b in zip(designs, original_designs)):
        write_json(designs_path, {**designs_data, "designs": designs})
        json_written = True

    print_summary(reports, json_written)
    return 0


if __name__ == "__main__":
    sys.exit(main())
